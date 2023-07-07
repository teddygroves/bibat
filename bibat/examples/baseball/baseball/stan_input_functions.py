"""Functions for generating input to Stan from prepared data."""

from typing import Dict

import numpy as np
from scipy.special import expit, logit

from baseball.data_preparation import PreparedData


def get_stan_input_normal(ppd: PreparedData) -> Dict:
    """General function for creating a Stan input."""
    return {
        "N": len(ppd.measurements),
        "K": ppd.measurements["n_attempt"].values,
        "y": ppd.measurements["n_success"].values,
        "prior_mu": [logit(0.25), 0.2],
        "prior_tau": [0.2, 0.1],
        "prior_b_K": [0, 0.03],
    }


def get_stan_input_gpareto(ppd: PreparedData) -> Dict:
    """General function for creating a Stan input."""
    return {
        "N": len(ppd.measurements),
        "K": ppd.measurements["n_attempt"].values,
        "y": ppd.measurements["n_success"].values,
        "min_alpha": logit(0.07),
        "max_alpha": logit(0.5),
        "prior_sigma": [1.5, 0.4],
        "prior_k": [-0.5, 1],
    }


def get_stan_input_normal_fake(ppd: PreparedData) -> Dict:
    """Generate fake Stan input consistent with the normal model."""
    N = len(ppd.measurements)
    rng = np.random.default_rng(seed=1234)
    true_param_values = {
        "mu": logit(0.25),
        "tau": 0.18,  # 2sds is 0.19 to 0.32 batting average
        "b_K": 0.04,  # slight effect of more attempts
        "alpha_std": rng.random.normal(loc=0, scale=1, size=N),
    }
    K = ppd.measurements["n_attempt"].values
    log_K_std = (np.log(K) - np.log(K).mean()) / np.log(K).std()
    alpha = (
        true_param_values["mu"]
        + true_param_values["b_K"] * log_K_std
        + true_param_values["tau"] * true_param_values["alpha_std"]
    )
    y = rng.random.binomial(K, expit(alpha))
    return {"N": N, "K": K, "y": y} | true_param_values


def get_stan_input_gpareto_fake(ppd: PreparedData) -> Dict:
    """Generate fake Stan input consistent with the gpareto model."""
    N = len(ppd.measurements)
    K = ppd.measurements["n_attempt"].values
    min_alpha = 0.1
    rng = np.random.default_rng(seed=1234)
    true_param_values = {"sigma": -1.098, "k": 0.18}
    true_param_values["alpha"] = gpareto_rvs(
        rng,
        N,
        min_alpha,
        true_param_values["k"],
        true_param_values["sigma"],
    )
    y = rng.binomial(K, expit(true_param_values["alpha"]))
    return {"N": N, "K": K, "y": y, "min_alpha": min_alpha} | true_param_values


def gpareto_rvs(
    rng: np.random.Generator, size: int, mu: float, k: float, sigma: float
):
    """Generate random numbers from a generalised pareto distribution.

    See https://en.wikipedia.org/wiki/Generalized_Pareto_distribution for
    source.

    """
    U = rng.uniform(size)
    if k == 0:
        return mu - sigma * np.log(U)
    else:
        return mu + (sigma * (U**-k) - 1) / sigma
