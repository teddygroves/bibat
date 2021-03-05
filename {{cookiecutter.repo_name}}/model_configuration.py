"""This file should include all non-Stan configuration for your models."""

import numpy as np
import os
import pandas as pd
from cmdstanpy import CmdStanModel
from util import get_99_pct_params_ln, get_99_pct_params_n
from typing import Dict, List


# Configure cmdstanpy.CmdStanModel.sample
SAMPLE_KWARGS = dict(  
    show_progress=True,
    save_warmup=False,
    iter_warmup=2000,
    iter_sampling=2000,
)


# Simulation study configuration...
# Model configuration that will be assumed true for generating fake data
TRUE_MODEL_CONFIG = "interaction"
# Distributions of covariates in simulated data. First value is mean, second is
# stanard deviation.
FAKE_DATA_X_STATS = {
    "A": [-1, 0.2],
    "B": [0.2, 1],
}
# True values for each variable in your program's `parameters` block. Make sure
# that the dimensions agree with `TRUE_MODEL_FILE`!
TRUE_PARAM_VALUES = {
    "a": 0.1,
    "b": [0.1, 2.5],
    "sigma": 0.5
}
# How many fake measurements should be generated?
N_FAKE_MEASUREMENTS = 100


def get_stan_input(
    measurements: pd.DataFrame,
    model_config: Dict,
) -> Dict:
    """Get an input to cmdstanpy.CmdStanModel.sample.

    :param measurements: a pandas DataFrame whose rows represent measurements

    :param model_config: a dictionary with keys "priors", "likelihood" and
    "x_cols".

    """
    return {**model_config["priors"], **{
        "N": len(measurements),
        "K": len(model_config["x_cols"]),
        "x": measurements[model_config["x_cols"]].values,
        "y": measurements["y"].values,
        "N_test": len(measurements),
        "x_test": measurements[model_config["x_cols"]].values,
        "y_test": measurements["y"].values,
        "likelihood": int(model_config["likelihood"]),
    }}


def get_infd_kwargs(
    measurements: pd.DataFrame, x_cols: List[str], sample_kwargs: Dict
) -> Dict:
    """Get a dictionary of keyword arguments to arviz.from_cmdstanpy.
    
    :param measurements: pandas dataframe whose rows represent
    measurements. Must be the same as was used for `get_stan_input`.
    
    :param x_cols: list of columns of `measurements` representing real-valued
    covariates. Must be the same as was used for `get_stan_input`.
    
    :param sample_kwargs: dictionary of keyword arguments that were passed to
    cmdstanpy.CmdStanModel.sample.

    """
    return dict(
        log_likelihood="llik",
        observed_data={"y": measurements["y"].values},
        posterior_predictive="yrep",
        coords={
            "covariate": x_cols,
            "measurement": measurements.index.values,
        },
        dims={
            "b": ["covariate"],
            "yrep": ["measurement"],
            "llik": ["measurement"],
        },
        save_warmup=sample_kwargs["save_warmup"]
    )

def generate_fake_measurements(
    true_param_values: Dict,
    true_model_config: Dict,
    n: int,
    x_stats: Dict[str, List[float]]
) -> pd.DataFrame:
    """Fake a table of measurements by simulating from the true model.
    
    You will need to customise this function to make sure it matches the data
    generating process you want to simulate from.
    
    :param true_param_values: a dictionary of true parameter values.

    :param true_model_config: configuration for the true model. Must have keys
    "stan_file" and "priors".
    
    :param n: number of fake measurements to be generated.

    :param x_stats: dictionary mapping names of covariate columns to lists
    indicating the desired mean and standard deviation of the covariate column.

    """
    x = pd.DataFrame({
        colname: np.random.normal(stat_list[0], stat_list[1], n)
        for colname, stat_list in x_stats.items()
    })
    x["A:B"] = x["A"] * x["B"]
    model = CmdStanModel(stan_file=true_model_config["stan_file"])
    stan_input = {**{
        "N": n,
        "K": len(x.columns),
        "x": x.values,
        "y": np.zeros(n),
        "N_test": n,
        "x_test": x.values,
        "y_test": np.zeros(n),
        "likelihood": 1,
    }, **true_model_config["priors"]}
    mcmc = model.sample(
        stan_input, inits=true_param_values, fixed_param=True, iter_sampling=1
    )
    return x.assign(y=mcmc.stan_variable("yrep")[0])


# Put different configurations of covariates and priors here.
MODEL_CONFIGURATIONS = {
    "interaction": {
        "likelihood": True,
        "stan_file": os.path.join("stan", "model.stan"),
        "stan_input_function": get_stan_input,
        "infd_kwargs_function": get_infd_kwargs,
        "x_cols": ["A", "B", "A:B"],
        "priors": {
            "prior_a": get_99_pct_params_n(0, 1),
            "prior_b": [
                get_99_pct_params_n(0, 2),
                get_99_pct_params_n(0, 2),
                get_99_pct_params_n(0, 2)
            ],
            "prior_sigma": get_99_pct_params_ln(0.4, 5.2),
        },
    },
    "no_interaction": {
        "likelihood": True,
        "stan_file": os.path.join("stan", "model.stan"),
        "stan_input_function": get_stan_input,
        "infd_kwargs_function": get_infd_kwargs,
        "x_cols": ["A", "B"],
        "priors": {
            "prior_a": get_99_pct_params_n(0, 1),
            "prior_b": [
                get_99_pct_params_n(0, 2),
                get_99_pct_params_n(0, 2),
            ],
            "prior_sigma": get_99_pct_params_ln(0.4, 5.2),
        }
    }
}
