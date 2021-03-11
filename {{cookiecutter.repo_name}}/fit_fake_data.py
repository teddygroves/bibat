"""A script for running a fake data simulation study."""

from datetime import datetime
import os

from model_configurations_to_try import MODEL_CONFIGURATIONS
from model_configurations_to_try import INTERACTION_CONFIG as TRUE_MODEL_CONFIG
from fake_data_generation import generate_fake_measurements
from fitting import generate_samples

# Distributions of covariates in simulated data. First value is mean, second is
# stanard deviation.
FAKE_DATA_X_STATS = {
    "x1": [-1, 0.2],
    "x2": [0.2, 1],
}

# True values for each variable in your program's `parameters` block. Make sure
# that the dimensions agree with `TRUE_MODEL_FILE`!
TRUE_PARAM_VALUES = {"a": 0.1, "b": [0.1, 2.5], "sigma": 0.5}

# How many fake measurements should be generated?
N_FAKE_MEASUREMENTS = 100


# Where to save fake data
FAKE_DATA_DIR = os.path.join("data", "fake")


def main():
    """Run a simulation study."""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    study_name = f"sim_study-{now}"
    print("Generating fake data...")
    measurements = generate_fake_measurements(
        TRUE_PARAM_VALUES,
        TRUE_MODEL_CONFIG,
        N_FAKE_MEASUREMENTS,
        FAKE_DATA_X_STATS,
    )
    fake_data_file = os.path.join(FAKE_DATA_DIR, f"fake_data-{study_name}.csv")
    print(f"Writing fake data to {fake_data_file}")
    measurements.to_csv(fake_data_file)
    generate_samples(study_name, measurements, MODEL_CONFIGURATIONS)


if __name__ == "__main__":
    main()
