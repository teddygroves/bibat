"""Functions and global variables for fitting.

This file should include all non-Stan configuration for your models.

"""

import arviz as az
from cmdstanpy import CmdStanModel
from cmdstanpy.utils import jsondump
import os
import pandas as pd
from typing import Dict, List

from util import get_99_pct_params_ln, get_99_pct_params_n

# Where to save files
LOO_DIR = os.path.join("results", "loo")
SAMPLES_DIR = os.path.join("results", "samples")
INFD_DIR = os.path.join("results", "infd")
JSON_DIR = os.path.join("results", "input_data_json")

# Configure cmdstanpy.CmdStanModel.sample
SAMPLE_KWARGS = dict(  
    show_progress=True,
    save_warmup=False,
    iter_warmup=2000,
    iter_sampling=2000,
)

# Put different configurations of covariates and priors here.
MODEL_CONFIGURATIONS = {
    "interaction": {
        "likelihood": True,
        "stan_file": os.path.join("stan", "model.stan"),
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
):
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


def generate_samples(study_name, measurements, model_configurations, logger):
    infds = {}
    for model_config_name, model_config in model_configurations.items():
        fit_name = f"{study_name}-{model_config_name}"
        print(f"Fitting model {fit_name}...")
        loo_file = os.path.join(LOO_DIR, f"loo_{fit_name}.pkl")
        infd_file = os.path.join(INFD_DIR, f"infd_{fit_name}.ncdf")
        json_file = os.path.join(JSON_DIR, f"input_data_{fit_name}.json")
        stan_file = model_config["stan_file"]
        x_cols = model_config["x_cols"]
        priors = model_config["priors"]
        likelihood = model_config["likelihood"]
        stan_input = get_stan_input(measurements, model_config)
        print(f"Writing input data to {json_file}")
        jsondump(json_file, stan_input)
        model = CmdStanModel(
            model_name=fit_name, stan_file=stan_file, logger=logger
        )
        mcmc = model.sample(data=stan_input, **SAMPLE_KWARGS)
        print(mcmc.diagnose().replace("\n\n", "\n"))
        infd_kwargs = get_infd_kwargs(measurements, x_cols, SAMPLE_KWARGS)
        infd = az.from_cmdstanpy(mcmc, **infd_kwargs)
        print(az.summary(infd))
        infds[fit_name] = infd
        loo = az.loo(infd, pointwise=True)
        print(f"Writing csv files to {SAMPLES_DIR}")
        mcmc.save_csvfiles(SAMPLES_DIR)
        print(f"Writing inference data to {infd_file}")
        infd.to_netcdf(infd_file)
        print(f"Writing psis-loo results to {loo_file}\n")
        loo.to_pickle(loo_file)
    if len(infds) > 1:
        comparison = az.compare(infds)
        print(f"Loo comparison:")
        print(comparison)
        comparison.to_csv(os.path.join(LOO_DIR, f"loo_comparison.csv"))
    else:
        print(f"Loo results:")
        print(loo)

