"""Function for generating fake data."""

from typing import Dict, List

from cmdstanpy import CmdStanModel
import numpy as np
import pandas as pd

from model_configuration import ModelConfiguration


def generate_fake_measurements(
    param_values: Dict,
    model_config: ModelConfiguration,
    n: int,
    x_stats: Dict[str, List[float]],
) -> pd.DataFrame:
    """Fake a table of measurements by simulating from the true model.

    You will need to customise this function to make sure it matches the data
    generating process you want to simulate from.

    :param param_values: a dictionary of true parameter values.

    :param model_config: configuration for the true model. Must have keys
    "stan_file" and "priors".

    :param n: number of fake measurements to be generated.

    :param x_stats: dictionary mapping names of covariate columns to lists
    indicating the desired mean and standard deviation of the covariate column.

    """
    fake = pd.DataFrame(
        {
            colname: np.random.normal(stat_list[0], stat_list[1], n)
            for colname, stat_list in x_stats.items()
        }
    )
    fake["x1:x2"] = fake["x1"] * fake["x2"]
    fake["y"] = 0
    model = CmdStanModel(stan_file=model_config.stan_file)
    stan_input = model_config.stan_input_function(fake)
    mcmc = model.sample(
        stan_input, inits=param_values, fixed_param=True, iter_sampling=1
    )
    return fake.assign(y=mcmc.stan_variable("yrep")[0])
