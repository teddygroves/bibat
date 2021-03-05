"""Functions and global variables for fitting."""

import arviz as az
from cmdstanpy import CmdStanModel
from cmdstanpy.utils import jsondump
import os
import pandas as pd


# Where to save files
LOO_DIR = os.path.join("results", "loo")
SAMPLES_DIR = os.path.join("results", "samples")
INFD_DIR = os.path.join("results", "infd")
JSON_DIR = os.path.join("results", "input_data_json")


def generate_samples(
    study_name,
    measurements,
    model_configurations,
    logger,
    sample_kwargs,
):
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
        get_stan_input = model_config["stan_input_function"]
        get_infd_kwargs = model_config["infd_kwargs_function"]
        likelihood = model_config["likelihood"]
        stan_input = get_stan_input(measurements, model_config)
        print(f"Writing input data to {json_file}")
        jsondump(json_file, stan_input)
        model = CmdStanModel(
            model_name=fit_name, stan_file=stan_file, logger=logger
        )
        mcmc = model.sample(data=stan_input, **sample_kwargs)
        print(mcmc.diagnose().replace("\n\n", "\n"))
        infd_kwargs = get_infd_kwargs(measurements, x_cols, sample_kwargs)
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

