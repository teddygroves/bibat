"""Functions for generating input to Stan from prepared data."""

import numpy as np
from scipy.special import expit, logit

from bibat.util import returns_stan_input
from src.data_preparation import BaseballPreparedData


@returns_stan_input
def get_stan_input_normal(ppd: BaseballPreparedData) -> dict:
    """General function for creating a Stan input."""
    return {
        "N": len(ppd.measurements),
        "K": ppd.measurements["n_attempt"],
        "y": ppd.measurements["n_success"],
        "prior_mu": [logit(0.25), 0.2],
        "prior_tau": [0.2, 0.1],
        "prior_b_K": [0, 0.03],
    }


@returns_stan_input
def get_stan_input_gpareto(ppd: BaseballPreparedData) -> dict:
    """General function for creating a Stan input."""
    return {
        "N": len(ppd.measurements),
        "K": ppd.measurements["n_attempt"],
        "y": ppd.measurements["n_success"],
        "min_alpha": logit(0.07),
        "max_alpha": logit(0.5),
        "prior_sigma": [1.5, 0.4],
        "prior_k": [-0.5, 1],
    }


@returns_stan_input
def get_stan_input_normal_fake(ppd: BaseballPreparedData) -> dict:
    """Generate fake Stan input consistent with the normal model."""
    n = len(ppd.measurements)
    rng = np.random.default_rng(seed=1234)
    true_param_values = {
        "mu": logit(0.25),
        "tau": 0.18,  # 2sds is 0.19 to 0.32 batting average
        "b_K": 0.04,  # slight effect of more attempts
        "alpha_std": rng.random.normal(loc=0, scale=1, size=n),
    }
    n_attempt = ppd.measurements["n_attempt"]
    log_k_std = (np.log(n_attempt) - np.log(n_attempt).mean()) / np.log(
        n_attempt,
    ).std()
    alpha = (
        true_param_values["mu"]
        + true_param_values["b_K"] * log_k_std
        + true_param_values["tau"] * true_param_values["alpha_std"]
    )
    y = rng.random.binomial(n_attempt, expit(alpha))
    return {"N": n, "K": n_attempt, "y": y} | true_param_values


@returns_stan_input
def get_stan_input_gpareto_fake(ppd: BaseballPreparedData) -> dict:
    """Generate fake Stan input consistent with the gpareto model."""
    n = len(ppd.measurements)
    n_attempt = ppd.measurements["n_attempt"]
    min_alpha = 0.1
    rng = np.random.default_rng(seed=1234)
    true_sigma = -1.098
    true_k = 0.18
    true_param_values = {
        "sigma": true_sigma,
        "k": true_k,
        "alpha": gpareto_rvs(rng, n, min_alpha, true_sigma, true_k),
    }
    y = rng.binomial(n_attempt, expit(true_param_values["alpha"]))
    return {
        "N": n,
        "K": n_attempt,
        "y": y,
        "min_alpha": min_alpha,
    } | true_param_values


def gpareto_rvs(
    rng: np.random.Generator,
    size: int,
    mu: float,
    k: float,
    sigma: float,
) -> np.ndarray:
    """Generate random numbers from a generalised pareto distribution.

    See https://en.wikipedia.org/wiki/Generalized_Pareto_distribution for
    source.

    """
    u = rng.uniform(size)
    if k == 0:
        return mu - sigma * np.log(u)
    return mu + (sigma * (u**-k) - 1) / sigma
