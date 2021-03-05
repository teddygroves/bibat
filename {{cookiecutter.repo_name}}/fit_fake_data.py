"""A script for running a fake data simulation study.

Run this script as part of your process for checking that the Stan programs in
`STAN_FILES` behave as expected.

 """

from datetime import datetime
import numpy as np
import os
import pandas as pd
from cmdstanpy import CmdStanModel
from cmdstanpy.utils import jsondump
from typing import Dict, List

from fitting import MODEL_CONFIGURATIONS, generate_samples

# only display messages with at least this severity
LOGGER_LEVEL = 40

# Where to save fake data
FAKE_DATA_DIR = os.path.join("data", "fake")

# True values for each variable in your program's `parameters` block. Make sure
# that the dimensions agree with `TRUE_MODEL_FILE`!
TRUE_PARAM_VALUES = {
    "a": 0.1,
    "b": [0.1, 2.5],
    "sigma": 0.5
}

# Distributions of covariates in simulated data. First value is mean, second is
# stanard deviation.
FAKE_DATA_X_STATS = {
    "A": [-1, 0.2],
    "B": [0.2, 1],
}

# How many fake measurements should be generated?
N = 100

# One of the `STAN_FILES` which will be used to generate fake data
TRUE_MODEL_CONFIG = MODEL_CONFIGURATIONS["interaction"]


def fake_measurements(
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


def main():
    logger = get_logger()
    logger.setLevel(LOGGER_LEVEL)
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    study_name = f"sim_study-{now}"
    print("Generating fake data...")
    measurements = fake_measurements(
        TRUE_PARAM_VALUES, TRUE_MODEL_CONFIG, N, FAKE_DATA_X_STATS
    )
    fake_data_file = os.path.join(FAKE_DATA_DIR, f"fake_data-{study_name}.csv")
    print(f"Writing fake data to {fake_data_file}")
    measurements.to_csv(fake_data_file)
    generate_samples(study_name, measurements, MODEL_CONFIGURATIONS, logger)
         
if __name__ == "__main__":
    main()
