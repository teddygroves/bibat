"""Functions for fitting models using cmdstanpy."""

import json
import os
from typing import Optional

import arviz as az
from arviz.data.inference_data import InferenceData
from cmdstanpy import CmdStanModel

# Location of this file
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")


def sample(
    stan_file: str,
    input_json: str,
    coords: dict,
    dims: dict,
    sample_kwargs: dict,
    cpp_options: Optional[dict],
    stanc_options: Optional[dict],
) -> InferenceData:
    """Run cmdstanpy.CmdStanModel.sample and return an InferenceData."""
    model = CmdStanModel(
        stan_file=stan_file,
        cpp_options=cpp_options,
        stanc_options=stanc_options,
    )
    with open(input_json, "r") as f:
        stan_input = json.load(f)
    coords["ix_train"] = [i - 1 for i in stan_input["ix_train"]]
    coords["ix_test"] = [i - 1 for i in stan_input["ix_test"]]
    mcmc = model.sample(data=stan_input, **sample_kwargs)
    return az.from_cmdstanpy(
        posterior=mcmc,
        log_likelihood="llik",
        posterior_predictive="yrep",
        observed_data=stan_input,
        coords=coords,
        dims=dims,
    )
