"""A script for running a fake data simulation study.

Run this script as part of your process for checking that the Stan programs in
`STAN_FILES` behave as expected.

 """

from datetime import datetime
import numpy as np
import os
import pandas as pd
from cmdstanpy import CmdStanModel
from cmdstanpy.utils import get_logger
from typing import Dict, List

from model_configuration import (
    generate_fake_measurements,
    MODEL_CONFIGURATIONS,
    TRUE_MODEL_CONFIG,
    TRUE_PARAM_VALUES,
    N_FAKE_MEASUREMENTS,
    FAKE_DATA_X_STATS,
    SAMPLE_KWARGS
)
from fitting import generate_samples

# only display messages with at least this severity
LOGGER_LEVEL = 40

# Where to save fake data
FAKE_DATA_DIR = os.path.join("data", "fake")


def main():
    logger = get_logger()
    logger.setLevel(LOGGER_LEVEL)
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    study_name = f"sim_study-{now}"
    print("Generating fake data...")
    measurements = generate_fake_measurements(
        TRUE_PARAM_VALUES,
        MODEL_CONFIGURATIONS[TRUE_MODEL_CONFIG],
        N_FAKE_MEASUREMENTS,
        FAKE_DATA_X_STATS
    )
    fake_data_file = os.path.join(FAKE_DATA_DIR, f"fake_data-{study_name}.csv")
    print(f"Writing fake data to {fake_data_file}")
    measurements.to_csv(fake_data_file)
    generate_samples(
        study_name, measurements, MODEL_CONFIGURATIONS, logger, SAMPLE_KWARGS
    )
         
if __name__ == "__main__":
    main()
