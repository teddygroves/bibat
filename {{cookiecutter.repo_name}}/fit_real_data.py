from munging import prepare_data
from cmdstanpy.utils import get_logger
from datetime import datetime
import os

from fitting import generate_samples
from model_configuration import SAMPLE_KWARGS

# File where a csv of measurements can be found. Edit unless your measurements
# file is called `raw_measurements.csv`!
CSV_INPUT = os.path.join("data", "raw", "raw_measurements.csv")

# Directories where output should be saved. You shouldn't need to edit these.
LOO_DIR = os.path.join("results", "loo")
SAMPLES_DIR = os.path.join("results", "samples")
INFD_DIR = os.path.join("results", "infd")
JSON_DIR = os.path.join("results", "input_data_json")

# only display messages with at least this severity
LOGGER_LEVEL = 40

# Specify whether to use the measurement model. Set to false for priors-only
# mode.
LIKELIHOOD = True

def main():
    logger = get_logger()
    logger.setLevel(LOGGER_LEVEL)
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    analysis_name = f"real_study-{now}"
    measurements = prepare_data(pd.read_csv(CSV_FILE))
    generate_samples(study_name, measurements, MODEL_CONFIGURATIONS, logger, SAMPLE_KWARGS)


if __name__ == "__main__":
    main()
