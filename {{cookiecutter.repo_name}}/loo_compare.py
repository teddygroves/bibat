"""Simple tweak to the arviz compare function so that it works with a
dictionary of arviz ELPDData objects rather than of InferenceData objects. The
reason for doing this is so that the arviz reloo function returns an ELPDData.

"""


from scipy.optimize import minimize
import numpy as np
from arviz.stats.stats import _ic_matrix
import pandas as pd


def compare(elpd_data_dict):
    r"""Compare models based on PSIS-LOO `loo`, i.e.
    LOO is leave-one-out (PSIS-LOO `loo`) cross-validation and

    Read more theory here - in a paper by some of the leading authorities
    on model selection dx.doi.org/10.1111/1467-9868.00353

    Parameters
    ----------
    elpd_data_dict: dict[str] -> InferenceData
        A dictionary of model names and ELPDData objects
    Returns
    -------
    A DataFrame, ordered from best to worst model (measured by information criteria).
    The index reflects the key with which the models are passed to this function. The columns are:
    rank: The rank-order of the models. 0 is the best.
    IC: Information Criteria (PSIS-LOO `loo` or WAIC `waic`).
        Higher IC indicates higher out-of-sample predictive fit ("better" model). Default LOO.
        If `scale` is `deviance` or `negative_log` smaller IC indicates
        higher out-of-sample predictive fit ("better" model).
    pIC: Estimated effective number of parameters.
    dIC: Relative difference between each IC (PSIS-LOO `loo` or WAIC `waic`)
          and the lowest IC (PSIS-LOO `loo` or WAIC `waic`).
          The top-ranked model is always 0.
    weight: Relative weight for each model.
        This can be loosely interpreted as the probability of each model (among the compared model)
        given the data. By default the uncertainty in the weights estimation is considered using
        Bayesian bootstrap.
    SE: Standard error of the IC estimate.
        If method = BB-pseudo-BMA these values are estimated using Bayesian bootstrap.
    dSE: Standard error of the difference in IC between each model and the top-ranked model.
        It's always 0 for the top-ranked model.
    warning: A value of 1 indicates that the computation of the IC may not be reliable.
        This could be indication of WAIC/LOO starting to fail see
        http://arxiv.org/abs/1507.04544 for details.
    scale: Scale used for the IC.
    Examples
    --------
    Compare the centered and non centered models of the eight school problem:
    .. ipython::
        In [1]: import arviz as az
           ...: data1 = az.load_arviz_data("non_centered_eight")
           ...: data2 = az.load_arviz_data("centered_eight")
           ...: compare_dict = {"non centered": data1, "centered": data2}
           ...: az.compare(compare_dict)
    Compare the models using LOO-CV, returning the IC in log scale and calculating the
    weights using the stacking method.
    .. ipython::
        In [1]: az.compare(compare_dict, ic="loo", method="stacking", scale="log")
    See Also
    --------
    loo : Compute the Pareto Smoothed importance sampling Leave One Out cross-validation.
    waic : Compute the widely applicable information criterion.
    """
    def w_fuller(weights):
        return np.concatenate((weights, [max(1.0 - np.sum(weights), 0.0)]))

    def log_score(weights):
        w_full = w_fuller(weights)
        score = 0.0
        for i in range(rows):
            score += np.log(np.dot(exp_ic_i[i], w_full))
        return -score

    def gradient(weights):
        w_full = w_fuller(weights)
        grad = np.zeros(km1)
        for k in range(km1):
            for i in range(rows):
                grad[k] += (exp_ic_i[i, k] - exp_ic_i[i, km1]) / np.dot(exp_ic_i[i], w_full)
        return -grad

    ic = "loo"
    names = list(elpd_data_dict.keys())
    scale = "log"
    scale_value = 1
    ascending = False
    df_comp = pd.DataFrame(
        index=names,
        columns=[
            "rank",
            "loo",
            "p_loo",
            "d_loo",
            "weight",
            "se",
            "dse",
            "warning",
            "loo_scale",
        ],
        dtype=np.float,
    )
    ics = (
        pd.DataFrame(elpd_data_dict.values(), index=names)
        .sort_values("loo", ascending=False)
        .assign(loo_i=lambda df: df["loo_i"].apply(lambda x: x.values.flatten()))
    )
    rows, cols, ic_i_val = _ic_matrix(ics, "loo_i")
    exp_ic_i = np.exp(ic_i_val / scale_value)
    km1 = cols - 1
    theta = np.full(km1, 1.0 / cols)
    bounds = [(0.0, 1.0) for _ in range(km1)]
    constraints = [
        {"type": "ineq", "fun": lambda x: -np.sum(x) + 1.0},
        {"type": "ineq", "fun": np.sum},
    ]
    weights = minimize(
        fun=log_score, x0=theta, jac=gradient, bounds=bounds, constraints=constraints
    )
    weights = w_fuller(weights["x"])
    ses = ics["loo_se"]
    if np.any(weights):
        min_ic_i_val = ics["loo_i"].iloc[0]
        for idx, val in enumerate(ics.index):
            res = ics.loc[val]
            if scale_value < 0:
                diff = res["loo_i"] - min_ic_i_val
            else:
                diff = min_ic_i_val - res["loo_i"]
            d_ic = np.sum(diff)
            d_std_err = np.sqrt(len(diff) * np.var(diff))
            std_err = ses.loc[val]
            weight = weights[idx]
            df_comp.at[val] = (
                idx,
                res["loo"],
                res["p_loo"],
                d_ic,
                weight,
                std_err,
                d_std_err,
                res["warning"],
                res["loo_scale"],
            )
    df_comp["rank"] = df_comp["rank"].astype(int)
    df_comp["warning"] = df_comp["warning"].astype(bool)
    return df_comp.sort_values(by=ic, ascending=ascending)
