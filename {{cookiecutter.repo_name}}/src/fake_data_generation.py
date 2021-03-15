"""Function for generating fake data."""


from cmdstanpy import CmdStanModel
import numpy as np
import pandas as pd

from .model_configurations_to_try import INTERACTION_CONFIG as TRUE_MODEL_CONFIG


# True values for each variable in your program's `parameters` block. Make sure
# that the dimensions agree with `TRUE_MODEL_FILE`!
TRUE_PARAM_VALUES = {"a": 0.1, "b": [0.1, 2.5], "sigma": 0.5}

# How many fake measurements should be generated?
N_FAKE_MEASUREMENTS = 100

# Distributions of covariates in simulated data. First value is mean, second is
# stanard deviation.
FAKE_DATA_X_STATS = {
    "x1": [-1, 0.2],
    "x2": [0.2, 1],
}


def generate_fake_measurements() -> pd.DataFrame:
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
            colname: np.random.normal(
                stat_list[0], stat_list[1], N_FAKE_MEASUREMENTS
            )
            for colname, stat_list in FAKE_DATA_X_STATS.items()
        }
    )
    fake["x1:x2"] = fake["x1"] * fake["x2"]
    fake["y"] = 0
    model = CmdStanModel(stan_file=TRUE_MODEL_CONFIG.stan_file)
    stan_input = TRUE_MODEL_CONFIG.stan_input_function(fake)
    mcmc = model.sample(
        stan_input, inits=TRUE_PARAM_VALUES, fixed_param=True, iter_sampling=1
    )
    return fake.assign(y=mcmc.stan_variable("yrep")[0])
