import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.sparse import issparse, csr_matrix
from sklearn.decomposition import PCA, TruncatedSVD

import warnings
import anndata
from typing import Union
from ..dynamo_logger import LoggerManager, main_info, main_warning
from ..utils import areinstance


# ---------------------------------------------------------------------------------------------------
# symbol conversion related
def convert2gene_symbol(input_names, scopes="ensembl.gene"):
    """Convert ensemble gene id to official gene names using mygene package.

    Parameters
    ----------
        input_names: list-like
            The ensemble gene id names that you want to convert to official gene names. All names should come from the
            same species.
        scopes: `list-like` or `None` (default: `None`)
            Scopes are needed when you use non-official gene name as your gene indices (or adata.var_name). This
            arugument corresponds to type of types of identifiers, either a list or a comma-separated fields to specify
            type of input qterms, e.g. “entrezgene”, “entrezgene,symbol”, [“ensemblgene”, “symbol”]. Refer to official
            MyGene.info docs (https://docs.mygene.info/en/latest/doc/query_service.html#available_fields) for full list
            of fields.

    Returns
    -------
        var_pd: `pd.Dataframe`
            A pandas dataframe that includes the following columns:
            query: the input ensmble ids
            _id: identified id from mygene
            _score: confidence of the retrieved official gene name.
            symbol: retrieved official gene name
    """

    try:
        import mygene
    except ImportError:
        raise ImportError(
            "You need to install the package `mygene` (pip install mygene --user) "
            "See https://pypi.org/project/mygene/ for more details."
        )

    mg = mygene.MyGeneInfo()

    ensemble_names = [i.split(".")[0] for i in input_names]
    var_pd = mg.querymany(
        ensemble_names,
        scopes=scopes,
        fields="symbol",
        as_dataframe=True,
        df_index=True,
    )
    # var_pd.drop_duplicates(subset='query', inplace=True) # use when df_index is not True
    var_pd = var_pd.loc[~var_pd.index.duplicated(keep="first")]

    return var_pd


def convert2symbol(adata, scopes=None, subset=True):
    if np.all(adata.var_names.str.startswith("ENS")) or scopes is not None:
        logger = LoggerManager.gen_logger("dynamo-utils")
        logger.info("convert ensemble name to official gene name", indent_level=1)

        prefix = adata.var_names[0]
        if scopes is None:
            if prefix[:4] == "ENSG" or prefix[:7] == "ENSMUSG":
                scopes = "ensembl.gene"
            elif prefix[:4] == "ENST" or prefix[:7] == "ENSMUST":
                scopes = "ensembl.transcript"
            else:
                raise Exception(
                    "Your adata object uses non-official gene names as gene index. \n"
                    "Dynamo finds those IDs are neither from ensembl.gene or ensembl.transcript and thus cannot "
                    "convert them automatically. \n"
                    "Please pass the correct scopes or first convert the ensemble ID to gene short name "
                    "(for example, using mygene package). \n"
                    "See also dyn.pp.convert2gene_symbol"
                )

        adata.var["query"] = [i.split(".")[0] for i in adata.var.index]
        if scopes is str:
            adata.var[scopes] = adata.var.index
        else:
            adata.var["scopes"] = adata.var.index

        logger.warning(
            "Your adata object uses non-official gene names as gene index. \n"
            "Dynamo is converting those names to official gene names."
        )
        official_gene_df = convert2gene_symbol(adata.var_names, scopes)
        merge_df = adata.var.merge(official_gene_df, left_on="query", right_on="query", how="left").set_index(
            adata.var.index
        )
        adata.var = merge_df
        valid_ind = np.where(merge_df["notfound"] != True)[0]  # noqa: E712

        if subset is True:
            adata._inplace_subset_var(valid_ind)
            adata.var.index = adata.var["symbol"].values.copy()
        else:
            indices = np.array(adata.var.index)
            indices[valid_ind] = adata.var.loc[valid_ind, "symbol"].values.copy()
            adata.var.index = indices

    return adata


def gene_exp_fraction(X, threshold=0.001):
    """Calculate fraction of each gene's coun to total counts across cells and identify high fraction genes."""

    frac = X.sum(0) / X.sum()
    if issparse(X):
        frac = frac.A.reshape(-1, 1)

    valid_ids = np.where(frac > threshold)[0]

    return frac, valid_ids


# ---------------------------------------------------------------------------------------------------
# implmentation of Cooks' distance (but this is for Poisson distribution fitting)

# https://stackoverflow.com/questions/47686227/poisson-regression-in-statsmodels-and-r

# from __future__ import division, print_function

# https://stats.stackexchange.com/questions/356053/the-identity-link-function-does-not-respect-the-domain-of-the-gamma-
# family
def _weight_matrix(fitted_model):
    """Calculates weight matrix in Poisson regression

    Parameters
    ----------
    fitted_model : statsmodel object
        Fitted Poisson model

    Returns
    -------
    W : 2d array-like
        Diagonal weight matrix in Poisson regression
    """
    return np.diag(fitted_model.fittedvalues)


def _hessian(X, W):
    """Hessian matrix calculated as -X'*W*X

    Parameters
    ----------
    X : 2d array-like
        Matrix of covariates

    W : 2d array-like
        Weight matrix

    Returns
    -------
    hessian : 2d array-like
        Hessian matrix
    """
    return -np.dot(X.T, np.dot(W, X))


def _hat_matrix(X, W):
    """Calculate hat matrix = W^(1/2) * X * (X'*W*X)^(-1) * X'*W^(1/2)

    Parameters
    ----------
    X : 2d array-like
        Matrix of covariates

    W : 2d array-like
        Diagonal weight matrix

    Returns
    -------
    hat : 2d array-like
        Hat matrix
    """
    # W^(1/2)
    Wsqrt = W ** (0.5)

    # (X'*W*X)^(-1)
    XtWX = -_hessian(X=X, W=W)
    XtWX_inv = np.linalg.inv(XtWX)

    # W^(1/2)*X
    WsqrtX = np.dot(Wsqrt, X)

    # X'*W^(1/2)
    XtWsqrt = np.dot(X.T, Wsqrt)

    return np.dot(WsqrtX, np.dot(XtWX_inv, XtWsqrt))


def cook_dist(model, X, good):
    # Weight matrix
    W = _weight_matrix(model)

    # Hat matrix
    H = _hat_matrix(X, W)
    hii = np.diag(H)  # Diagonal values of hat matrix # fit.get_influence().hat_matrix_diag

    # Pearson residuals
    r = model.resid_pearson

    # Cook's distance (formula used by R = (res/(1 - hat))^2 * hat/(dispersion * p))
    # Note: dispersion is 1 since we aren't modeling overdispersion

    resid = good.disp - model.predict(good)
    rss = np.sum(resid ** 2)
    MSE = rss / (good.shape[0] - 2)
    # use the formula from: https://www.mathworks.com/help/stats/cooks-distance.html
    cooks_d = r ** 2 / (2 * MSE) * hii / (1 - hii) ** 2  # (r / (1 - hii)) ** 2 *  / (1 * 2)

    return cooks_d


# ---------------------------------------------------------------------------------------------------
# preprocess utilities
def filter_genes_by_pattern(
    adata: anndata.AnnData,
    patterns: tuple = ("MT-", "RPS", "RPL", "MRPS", "MRPL", "ERCC-"),
    drop_genes: bool = False,
) -> Union[list, None]:
    """Utility function to filter mitochondria, ribsome protein and ERCC spike-in genes, etc."""
    logger = LoggerManager.gen_logger("dynamo-utils")

    matched_genes = pd.Series(adata.var_names).str.startswith(patterns).to_list()
    logger.info(
        "total matched genes is " + str(sum(matched_genes)),
        indent_level=1,
    )
    if sum(matched_genes) > 0:
        if drop_genes:
            gene_bools = np.ones(adata.n_vars, dtype=bool)
            gene_bools[matched_genes] = False
            logger.info(
                "inplace subset matched genes ... ",
                indent_level=1,
            )
            # let us ignore the `inplace` parameter in pandas.Categorical.remove_unused_categories  warning.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                adata._inplace_subset_var(gene_bools)

            logger.finish_progress(progress_name="filter_genes_by_pattern")
            return None
        else:
            logger.finish_progress(progress_name="filter_genes_by_pattern")
            return matched_genes


def basic_stats(adata):
    adata.obs["nGenes"], adata.obs["nCounts"] = (adata.X > 0).sum(1), (adata.X).sum(1)
    adata.var["nCells"], adata.var["nCounts"] = (adata.X > 0).sum(0).T, (adata.X).sum(0).T
    mito_genes = adata.var_names.str.upper().str.startswith("MT-")
    try:
        adata.obs["pMito"] = (
            (adata.X[:, mito_genes]).sum(1).A1 / adata.obs["nCounts"]
            if issparse(adata.X)
            else (adata.X[:, mito_genes]).sum(1) / adata.obs["nCounts"]
        )
    except:  # noqa E722
        raise ValueError("looks like your var_names may be corrupted (i.e. include nan values)")


def unique_var_obs_adata(adata):
    """Function to make the obs and var attribute's index unique"""
    adata.obs_names_make_unique()
    adata.var_names_make_unique()

    return adata


def layers2csr(adata):
    """Function to make the obs and var attribute's index unique"""
    for i in adata.layers.keys():
        adata.layers[i] = csr_matrix(adata.layers[i]) if not issparse(adata.layers[i]) else adata.layers[i]

    return adata


def merge_adata_attrs(adata_ori, adata, attr):
    if attr == "var":
        _columns = set(adata.var.columns).difference(adata_ori.var.columns)
        var_df = adata_ori.var.merge(adata.var[_columns], how="left", left_index=True, right_index=True)
        adata_ori.var = var_df.loc[adata_ori.var.index, :]
    elif attr == "obs":
        _columns = set(adata.obs.columns).difference(adata_ori.obs.columns)
        obs_df = adata_ori.obs.merge(adata.obs[_columns], how="left", left_index=True, right_index=True)
        adata_ori.obs = obs_df.loc[adata_ori.obs.index, :]

    return adata_ori


def allowed_layer_raw_names():
    only_splicing = ["spliced", "unspliced"]
    only_labeling = ["new", "total"]
    splicing_and_labeling = ["uu", "ul", "su", "sl"]

    return only_splicing, only_labeling, splicing_and_labeling


def allowed_X_layer_names():
    only_splicing = ["X_spliced", "X_unspliced"]
    only_labeling = ["X_new", "X_total"]
    splicing_and_labeling = ["X_uu", "X_ul", "X_su", "X_sl"]

    return only_splicing, only_labeling, splicing_and_labeling


def get_layer_keys(adata, layers="all", remove_normalized=True, include_protein=True):
    """Get the list of available layers' keys."""
    layer_keys = list(adata.layers.keys())
    if remove_normalized:
        layer_keys = [i for i in layer_keys if not i.startswith("X_")]

    if "protein" in adata.obsm.keys() and include_protein:
        layer_keys.extend(["X", "protein"])
    else:
        layer_keys.extend(["X"])
    layers = layer_keys if layers == "all" else list(set(layer_keys).intersection(list(layers)))

    layers = list(set(layers).difference(["matrix", "ambiguous", "spanning"]))
    return layers


def get_shared_counts(adata, layers, min_shared_count, type="gene"):
    layers = list(set(layers).difference(["X", "matrix", "ambiguous", "spanning"]))
    layers = np.array(layers)[~pd.DataFrame(layers)[0].str.startswith("X_").values]

    _nonzeros, _sum = None, None
    for layer in layers:
        if issparse(adata.layers[layers[0]]):
            _nonzeros = adata.layers[layer] > 0 if _nonzeros is None else _nonzeros.multiply(adata.layers[layer] > 0)
        else:
            _nonzeros = adata.layers[layer] > 0 if _nonzeros is None else _nonzeros * (adata.layers[layer] > 0)

    for layer in layers:
        if issparse(adata.layers[layers[0]]):
            _sum = (
                _nonzeros.multiply(adata.layers[layer])
                if _sum is None
                else _sum + _nonzeros.multiply(adata.layers[layer])
            )
        else:
            _sum = (
                np.multiply(_nonzeros, adata.layers[layer])
                if _sum is None
                else _sum + np.multiply(_nonzeros, adata.layers[layer])
            )

    if type == "gene":
        return (
            np.array(_sum.sum(0).A1 >= min_shared_count)
            if issparse(adata.layers[layers[0]])
            else np.array(_sum.sum(0) >= min_shared_count)
        )
    if type == "cells":
        return (
            np.array(_sum.sum(1).A1 >= min_shared_count)
            if issparse(adata.layers[layers[0]])
            else np.array(_sum.sum(1) >= min_shared_count)
        )


def clusters_stats(U, S, clusters_uid, cluster_ix, size_limit=40):
    """Calculate the averages per cluster

    If the cluster is too small (size<size_limit) the average of the total is reported instead
    This function is modified from velocyto in order to reproduce velocyto's DentateGyrus notebook.
    """
    U_avgs = np.zeros((S.shape[1], len(clusters_uid)))
    S_avgs = np.zeros((S.shape[1], len(clusters_uid)))
    # avgU_div_avgS = np.zeros((S.shape[1], len(clusters_uid)))
    # slopes_by_clust = np.zeros((S.shape[1], len(clusters_uid)))

    for i, uid in enumerate(clusters_uid):
        cluster_filter = cluster_ix == i
        n_cells = np.sum(cluster_filter)
        if n_cells > size_limit:
            U_avgs[:, i], S_avgs[:, i] = (
                U[cluster_filter, :].mean(0),
                S[cluster_filter, :].mean(0),
            )
        else:
            U_avgs[:, i], S_avgs[:, i] = U.mean(0), S.mean(0)

    return U_avgs, S_avgs


def get_svr_filter(adata, layer="spliced", n_top_genes=3000, return_adata=False):
    score_name = "score" if layer in ["X", "all"] else layer + "_score"
    valid_idx = np.where(np.isfinite(adata.var.loc[:, score_name]))[0]

    valid_table = adata.var.iloc[valid_idx, :]
    nth_score = np.sort(valid_table.loc[:, score_name])[::-1][np.min((n_top_genes - 1, valid_table.shape[0] - 1))]

    feature_gene_idx = np.where(valid_table.loc[:, score_name] >= nth_score)[0][:n_top_genes]
    feature_gene_idx = valid_idx[feature_gene_idx]

    if return_adata:
        adata.var.loc[:, "use_for_pca"] = False
        adata.var.loc[adata.var.index[feature_gene_idx], "use_for_pca"] = True
        res = adata
    else:
        filter_bool = np.zeros(adata.n_vars, dtype=bool)
        filter_bool[feature_gene_idx] = True
        res = filter_bool

    return res


def sz_util(
    adata,
    layer,
    round_exprs,
    method,
    locfunc,
    total_layers=None,
    CM=None,
    scale_to=None,
):
    adata = adata.copy()

    if layer == "_total_" and "_total_" not in adata.layers.keys():
        if total_layers is not None:
            if not isinstance(total_layers, list):
                total_layers = [total_layers]
            if len(set(total_layers).difference(adata.layers.keys())) == 0:
                total = None
                for t_key in total_layers:
                    total = adata.layers[t_key] if total is None else total + adata.layers[t_key]
                adata.layers["_total_"] = total

    if layer == "raw":
        CM = adata.raw.X if CM is None else CM
    elif layer == "X":
        CM = adata.X if CM is None else CM
    elif layer == "protein":
        if "protein" in adata.obsm_keys():
            CM = adata.obsm["protein"] if CM is None else CM
        else:
            return None, None
    else:
        CM = adata.layers[layer] if CM is None else CM

    if round_exprs:
        if issparse(CM):
            CM.data = np.round(CM.data, 0)
        else:
            CM = CM.round().astype("int")

    cell_total = CM.sum(axis=1).A1 if issparse(CM) else CM.sum(axis=1)
    cell_total += cell_total == 0  # avoid infinity value after log (0)

    if method in ["mean-geometric-mean-total", "geometric"]:
        sfs = cell_total / (np.exp(locfunc(np.log(cell_total))) if scale_to is None else scale_to)
    elif method == "median":
        sfs = cell_total / (np.nanmedian(cell_total) if scale_to is None else scale_to)
    elif method == "mean":
        sfs = cell_total / (np.nanmean(cell_total) if scale_to is None else scale_to)
    else:
        raise NotImplementedError(f"This method {method} is not supported!")

    return sfs, cell_total


def get_sz_exprs(adata, layer, total_szfactor=None):
    if layer == "raw":
        CM = adata.raw.X
        szfactors = adata.obs[layer + "Size_Factor"].values[:, None]
    elif layer == "X":
        CM = adata.X
        szfactors = adata.obs["Size_Factor"].values[:, None]
    elif layer == "protein":
        if "protein" in adata.obsm_keys():
            CM = adata.obsm[layer]
            szfactors = adata.obs["protein_Size_Factor"].values[:, None]
        else:
            CM, szfactors = None, None
    else:
        CM = adata.layers[layer]
        szfactors = adata.obs[layer + "_Size_Factor"].values[:, None]

    if total_szfactor is not None and total_szfactor in adata.obs.keys():
        szfactors = adata.obs[total_szfactor][:, None]
    else:
        if total_szfactor is not None:
            main_warning("`total_szfactor` is not `None` and it is not in adata object.")

    return szfactors, CM


def normalize_util(CM, szfactors, relative_expr, pseudo_expr, norm_method=np.log1p):
    if norm_method == np.log1p:
        pseudo_expr = 0
    if relative_expr:
        CM = CM.multiply(csr_matrix(1 / szfactors)) if issparse(CM) else CM / szfactors

    if pseudo_expr is None:
        pseudo_expr = 1
    if issparse(CM):
        CM.data = norm_method(CM.data + pseudo_expr) if norm_method is not None else CM.data
        if norm_method is not None and norm_method.__name__ == "Freeman_Tukey":
            CM.data -= 1
    else:
        CM = norm_method(CM + pseudo_expr) if norm_method is not None else CM

    return CM


def Freeman_Tukey(X, inverse=False):
    if inverse:
        res = np.sqrt(X) + np.sqrt((X + 1))
    else:
        res = (X ** 2 - 1) ** 2 / (4 * X ** 2)

    return res


def anndata_bytestring_decode(adata_item):
    for key in adata_item.keys():
        df = adata_item[key]
        if df.dtype.name == "category" and areinstance(df.cat.categories, bytes):
            cat = [c.decode() for c in df.cat.categories]
            df.cat.rename_categories(cat, inplace=True)


def decode_index(adata_item):
    if areinstance(adata_item.index, bytes):
        index = {i: i.decode() for i in adata_item.index}
        adata_item.rename(index, inplace=True)


def decode(adata):
    decode_index(adata.obs)
    decode_index(adata.var)
    anndata_bytestring_decode(adata.obs)
    anndata_bytestring_decode(adata.var)


# ---------------------------------------------------------------------------------------------------
# pca


def pca(
    adata,
    X_data=None,
    n_pca_components=30,
    pca_key="X",
    pcs_key="PCs",
    genes_to_append=None,
    layer=None,
    return_all=False,
):
    # only use genes pass filter (based on use_for_pca) to perform dimension reduction.
    if X_data is None:
        if "use_for_pca" not in adata.var.keys():
            adata.var["use_for_pca"] = True

        if layer is None:
            X_data = adata.X[:, adata.var.use_for_pca.values]
        else:
            if "X" in layer:
                X_data = adata.X[:, adata.var.use_for_pca.values]
            elif "total" in layer:
                X_data = adata.layers["X_total"][:, adata.var.use_for_pca.values]
            elif "spliced" in layer:
                X_data = adata.layers["X_spliced"][:, adata.var.use_for_pca.values]
            elif "protein" in layer:
                X_data = adata.obsm["X_protein"]
            elif type(layer) is str:
                X_data = adata.layers["X_" + layer][:, adata.var.use_for_pca.values]
            else:
                raise ValueError(
                    f"your input layer argument should be either a `str` or a list that includes one of `X`, "
                    f"`total`, `protein` element. `Layer` currently is {layer}."
                )

        cm_genesums = X_data.sum(axis=0)
        valid_ind = np.logical_and(np.isfinite(cm_genesums), cm_genesums != 0)
        valid_ind = np.array(valid_ind).flatten()

        bad_genes = np.where(adata.var.use_for_pca)[0][~valid_ind]
        if genes_to_append is not None and len(adata.var.index[bad_genes].intersection(genes_to_append)) > 0:
            raise ValueError(
                f"The gene list passed to argument genes_to_append contains genes with no expression "
                f"across cells or non finite values. Please check those genes:"
                f"{set(bad_genes).intersection(genes_to_append)}!"
            )

        adata.var.iloc[bad_genes, adata.var.columns.tolist().index("use_for_pca")] = False
        X_data = X_data[:, valid_ind]

    if adata.n_obs < 100000:
        pca = PCA(
            n_components=min(n_pca_components, X_data.shape[1] - 1),
            svd_solver="arpack",
            random_state=0,
        )
        fit = pca.fit(X_data.toarray()) if issparse(X_data) else pca.fit(X_data)
        X_pca = fit.transform(X_data.toarray()) if issparse(X_data) else fit.transform(X_data)
        adata.obsm[pca_key] = X_pca
        adata.uns[pcs_key] = fit.components_.T

        adata.uns["explained_variance_ratio_"] = fit.explained_variance_ratio_
    else:
        # unscaled PCA
        fit = TruncatedSVD(
            n_components=min(n_pca_components + 1, X_data.shape[1] - 1),
            random_state=0,
        )
        # first columns is related to the total UMI (or library size)
        X_pca = fit.fit_transform(X_data)[:, 1:]
        adata.obsm[pca_key] = X_pca
        adata.uns[pcs_key] = fit.components_.T

        adata.uns["explained_variance_ratio_"] = fit.explained_variance_ratio_[1:]

    adata.uns["explained_variance_ratio_"] = fit.explained_variance_ratio_[1:]
    adata.uns["pca_mean"] = fit.mean_ if hasattr(fit, "mean_") else None

    if return_all:
        return adata, fit, X_pca
    else:
        return adata


def pca_genes(PCs: list, n_top_genes: int = 100):
    """[summary]
    For each gene, if the gene is n_top in some principle component
    then it is valid. Return all such valid genes.
    Parameters
    ----------
    PCs :
        principle components(PC) of PCA
    n_top_genes :
        number of gene candidates in EACH PC

    Returns
    -------
        ret
    """
    valid_genes = np.zeros(PCs.shape[0], dtype=bool)
    for q in PCs.T:
        sorted_q = np.sort(np.abs(q))[::-1]
        is_pc_top_n = np.abs(q) > sorted_q[n_top_genes]
        valid_genes = np.logical_or(is_pc_top_n, valid_genes)
    return valid_genes


def top_pca_genes(adata, pc_key="PCs", n_top_genes=100, pc_components=None, adata_store_key="top_pca_genes"):
    if pc_key in adata.uns.keys():
        Q = adata.uns[pc_key]
    elif pc_key in adata.varm.keys():
        Q = adata.varm[pc_key]
    else:
        raise Exception(f"No PC matrix {pc_key} found in neither .uns nor .varm.")
    if pc_components is not None:
        if type(pc_components) == int:
            Q = Q[:, :pc_components]
        elif type(pc_components) == list:
            Q = Q[:, pc_components]

    pcg = pca_genes(Q, n_top_genes=n_top_genes)
    genes = np.zeros(adata.n_vars, dtype=bool)
    if "use_for_pca" in adata.var.keys():
        genes[adata.var["use_for_pca"]] = pcg
    else:
        genes = pcg
    print("%d top PCA genes found for %d PCs." % (np.sum(pcg), Q.shape[1]))
    adata.var[adata_store_key] = genes
    return adata


def add_noise_to_duplicates(adata, basis="pca"):
    X_data = adata.obsm["X_" + basis]
    min_val = abs(X_data).min()

    n_obs, n_var = X_data.shape
    while True:
        _, index = np.unique(X_data, axis=0, return_index=True)
        duplicated_idx = np.setdiff1d(np.arange(n_obs), index)

        if len(duplicated_idx) == 0:
            adata.obsm["X_" + basis] = X_data
            break
        else:
            X_data[duplicated_idx, :] += np.random.normal(0, min_val / 1000, (len(duplicated_idx), n_var))


# ---------------------------------------------------------------------------------------------------
# labeling related


def collapse_adata(adata):
    """Function to collapse the four species data, will be generalized to handle dual-datasets"""
    (
        only_splicing,
        only_labeling,
        splicing_and_labeling,
    ) = allowed_layer_raw_names()

    if np.all([i in adata.layers.keys() for i in splicing_and_labeling]):
        if only_splicing[0] not in adata.layers.keys():
            adata.layers[only_splicing[0]] = adata.layers["su"] + adata.layers["sl"]
        if only_splicing[1] not in adata.layers.keys():
            adata.layers[only_splicing[1]] = adata.layers["uu"] + adata.layers["ul"]
        if only_labeling[0] not in adata.layers.keys():
            adata.layers[only_labeling[0]] = adata.layers["ul"] + adata.layers["sl"]
        if only_labeling[1] not in adata.layers.keys():
            adata.layers[only_labeling[1]] = adata.layers[only_labeling[0]] + adata.layers["uu"] + adata.layers["su"]

    return adata


def detect_datatype(adata):
    has_splicing, has_labeling, splicing_labeling, has_protein = (
        False,
        False,
        False,
        False,
    )

    layers = adata.layers.keys()
    if (
        len({"ul", "sl", "uu", "su"}.difference(layers)) == 0
        or len({"X_ul", "X_sl", "X_uu", "X_su"}.difference(layers)) == 0
    ):
        has_splicing, has_labeling, splicing_labeling = True, True, True
    elif (
        len({"unspliced", "spliced", "new", "total"}.difference(layers)) == 0
        or len({"X_unspliced", "X_spliced", "X_new", "X_total"}.difference(layers)) == 0
    ):
        has_splicing, has_labeling = True, True
    elif (
        len({"unspliced", "spliced"}.difference(layers)) == 0
        or len({"X_unspliced", "X_spliced"}.difference(layers)) == 0
    ):
        has_splicing = True
    elif len({"new", "total"}.difference(layers)) == 0 or len({"X_new", "X_total"}.difference(layers)) == 0:
        has_labeling = True

    if "protein" in adata.obsm.keys():
        has_protein = True

    return has_splicing, has_labeling, splicing_labeling, has_protein


def default_layer(adata):
    has_splicing, has_labeling, splicing_labeling, _ = detect_datatype(adata)

    if has_splicing:
        if has_labeling:
            if len(set(adata.layers.keys()).intersection(["new", "total", "spliced", "unspliced"])) == 4:
                adata = collapse_adata(adata)
            default_layer = (
                "M_t" if "M_t" in adata.layers.keys() else "X_total" if "X_total" in adata.layers.keys() else "total"
            )
        else:
            default_layer = (
                "M_s"
                if "M_s" in adata.layers.keys()
                else "X_spliced"
                if "X_spliced" in adata.layers.keys()
                else "spliced"
            )
    else:
        default_layer = (
            "M_t" if "M_t" in adata.layers.keys() else "X_total" if "X_total" in adata.layers.keys() else "total"
        )

    return default_layer


def NTR(adata):
    """calculate the new to total ratio across cells. Note that
    NTR for the first time point in degradation approximates gamma/beta."""

    if len({"new", "total"}.intersection(adata.layers.keys())) == 2:
        ntr = adata.layers["new"].sum(1) / adata.layers["total"].sum(1)
        ntr = ntr.A1 if issparse(adata.layers["new"]) else ntr

        var_ntr = adata.layers["new"].sum(0) / adata.layers["total"].sum(0)
        var_ntr = var_ntr.A1 if issparse(adata.layers["new"]) else var_ntr
    elif len({"uu", "ul", "su", "sl"}.intersection(adata.layers.keys())) == 4:
        new = adata.layers["ul"].sum(1) + adata.layers["sl"].sum(1)
        total = new + adata.layers["uu"].sum(1) + adata.layers["su"].sum(1)
        ntr = new / total

        ntr = ntr.A1 if issparse(adata.layers["uu"]) else ntr

        new = adata.layers["ul"].sum(0) + adata.layers["sl"].sum(0)
        total = new + adata.layers["uu"].sum(0) + adata.layers["su"].sum(0)
        var_ntr = new / total

        var_ntr = var_ntr.A1 if issparse(adata.layers["uu"]) else var_ntr
    elif len({"unspliced", "spliced"}.intersection(adata.layers.keys())) == 2:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            ntr = adata.layers["unspliced"].sum(1) / (adata.layers["unspliced"] + adata.layers["spliced"]).sum(1)
            var_ntr = adata.layers["unspliced"].sum(0) / (adata.layers["unspliced"] + adata.layers["spliced"]).sum(0)

        ntr = ntr.A1 if issparse(adata.layers["unspliced"]) else ntr
        var_ntr = var_ntr.A1 if issparse(adata.layers["unspliced"]) else var_ntr
    else:
        ntr, var_ntr = None, None

    return ntr, var_ntr


def scale(adata, layers=None, scale_to_layer=None, scale_to=1e6):
    """scale layers to a particular total expression value, similar to `normalize_expr_data` function."""
    layers = get_layer_keys(adata, layers)
    has_splicing, has_labeling, _ = detect_datatype(adata)

    if scale_to_layer is None:
        scale_to_layer = "total" if has_labeling else None
        scale = scale_to / adata.layers[scale_to_layer].sum(1)
    else:
        scale = None

    for layer in layers:
        if scale is None:
            scale = scale_to / adata.layers[layer].sum(1)

        adata.layers[layer] = csr_matrix(adata.layers[layer].multiply(scale))

    return adata


# ---------------------------------------------------------------------------------------------------
# ERCC related


def relative2abs(
    adata,
    dilution,
    volume,
    from_layer=None,
    to_layers=None,
    mixture_type=1,
    ERCC_controls=None,
    ERCC_annotation=None,
):
    """Converts FPKM/TPM data to transcript counts using ERCC spike-in. This is based on the relative2abs function from
    monocle 2 (Qiu, et. al, Nature Methods, 2017).

    Parameters
    ----------
        adata: :class:`~anndata.AnnData`
            an Annodata object
        dilution: `float`
            the dilution of the spikein transcript in the lysis reaction mix. Default is 40, 000. The number of spike-in
            transcripts per single-cell lysis reaction was calculated from.
        volume: `float`
            the approximate volume of the lysis chamber (nanoliters). Default is 10
        from_layer: `str` or `None`
            The layer in which the ERCC TPM values will be used as the covariate for the ERCC based linear regression.
        to_layers: `str`, `None` or `list-like`
            The layers that our ERCC based transformation will be applied to.
        mixture_type:
            the type of spikein transcripts from the spikein mixture added in the experiments. By default, it is mixture
            1. Note that m/c we inferred are also based on mixture 1.
        ERCC_controls:
            the FPKM/TPM matrix for each ERCC spike-in transcript in the cells if user wants to perform the
            transformation based on their spike-in data. Note that the row and column names should match up with the
            ERCC_annotation and relative_exprs_matrix respectively.
        ERCC_annotation:
            the ERCC_annotation matrix from illumina USE GUIDE which will be ued for calculating the ERCC transcript
            copy number for performing the transformation.

    Returns
    -------
        An adata object with the data specified in the to_layers transformed into absolute counts.
    """

    if ERCC_annotation is None:
        ERCC_annotation = pd.read_csv(
            "https://www.dropbox.com/s/cmiuthdw5tt76o5/ERCC_specification.txt?dl=1",
            sep="\t",
        )

    ERCC_id = ERCC_annotation["ERCC ID"]

    ERCC_id = adata.var_names.intersection(ERCC_id)
    if len(ERCC_id) < 10 and ERCC_controls is None:
        raise Exception("The adata object you provided has less than 10 ERCC genes.")

    if to_layers is not None:
        to_layers = [to_layers] if to_layers is str else to_layers
        to_layers = list(set(adata.layers.keys()).intersection(to_layers))
        if len(to_layers) == 0:
            raise Exception(
                f"The layers {to_layers} that will be converted to absolute counts doesn't match any layers"
                f"from the adata object."
            )

    mixture_name = (
        "concentration in Mix 1 (attomoles/ul)" if mixture_type == 1 else "concentration in Mix 2 (attomoles/ul)"
    )
    ERCC_annotation["numMolecules"] = ERCC_annotation.loc[:, mixture_name] * (
        volume * 10 ** (-3) * 1 / dilution * 10 ** (-18) * 6.02214129 * 10 ** (23)
    )

    ERCC_annotation["rounded_numMolecules"] = ERCC_annotation["numMolecules"].astype(int)

    if from_layer in [None, "X"]:
        X, X_ercc = (
            adata.X,
            adata[:, ERCC_id].X if ERCC_controls is None else ERCC_controls,
        )
    else:
        X, X_ercc = (
            adata.layers[from_layer],
            adata[:, ERCC_id] if ERCC_controls is None else ERCC_controls,
        )

    logged = False if X.max() > 100 else True

    if not logged:
        X, X_ercc = (
            np.log1p(X.A) if issparse(X_ercc) else np.log1p(X),
            np.log1p(X_ercc.A) if issparse(X_ercc) else np.log1p(X_ercc),
        )
    else:
        X, X_ercc = (
            X.A if issparse(X_ercc) else X,
            X_ercc.A if issparse(X_ercc) else X_ercc,
        )

    y = np.log1p(ERCC_annotation["numMolecules"])

    for i in range(adata.n_obs):
        X_i, X_ercc_i = X[i, :], X_ercc[i, :]

        X_i, X_ercc_i = sm.add_constant(X_i), sm.add_constant(X_ercc_i)
        res = sm.RLM(y, X_ercc_i).fit()
        k, b = res.params[::-1]

        if to_layers is None:
            X = adata.X
            logged = False if X.max() > 100 else True

            if not logged:
                X_i = np.log1p(X[i, :].A) if issparse(X) else np.log1p(X[i, :])
            else:
                X_i = X[i, :].A if issparse(X) else X[i, :]

            res = k * X_i + b
            res = res if logged else np.expm1(res)
            adata.X[i, :] = csr_matrix(res) if issparse(X) else res
        else:
            for cur_layer in to_layers:
                X = adata.layers[cur_layer]

                logged = False if X.max() > 100 else True
                if not logged:
                    X_i = np.log1p(X[i, :].A) if issparse(X) else np.log1p(X[i, :])
                else:
                    X_i = X[i, :].A if issparse(X) else X[i, :]

                res = k * X_i + b if logged else np.expm1(k * X_i + b)
                adata.layers[cur_layer][i, :] = csr_matrix(res) if issparse(X) else res


# ---------------------------------------------------------------------------------------------------
# coordinate/vector space operations


def affine_transform(X, A, b):
    X = np.array(X)
    A = np.array(A)
    b = np.array(b)
    return (A @ X.T).T + b


def gen_rotation_2d(degree: float):
    from math import cos, sin, radians

    rad = radians(degree)
    R = [
        [cos(rad), -sin(rad)],
        [sin(rad), cos(rad)],
    ]
    return np.array(R)
