"""Fit the models in MODEL_CONFIGURATIONS to real data."""

from datetime import datetime
import os
import pandas as pd

from fitting import generate_samples
from model_configurations_to_try import MODEL_CONFIGURATIONS

# File where a prepared csv of measurements can be found
CSV_INPUT = os.path.join("data", "prepared", "data_prepared.csv")

# only display messages with at least this severity
LOGGER_LEVEL = 40

# Specify whether to use the measurement model. Set to false for priors-only
# mode.
LIKELIHOOD = True


def main():
    """Run the script."""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    study_name = f"real_study-{now}"
    measurements = pd.read_csv(CSV_INPUT)
    generate_samples(study_name, measurements, MODEL_CONFIGURATIONS)


if __name__ == "__main__":
    main()
