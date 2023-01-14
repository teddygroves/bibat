"""Read the data in RAW_DIR and save prepared data to PREPARED_DIR."""

import os

import pandas as pd
from src import data_preparation_functions

DATA_PREPARATION_FUNCTIONS_TO_RUN = [
    data_preparation_functions.prepare_data_fake_interaction,
    data_preparation_functions.prepare_data_interaction,
    data_preparation_functions.prepare_data_no_interaction,
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PREPARED_DIR = os.path.join(DATA_DIR, "prepared")
RAW_DATA_FILES = {
    "raw_measurements": os.path.join(RAW_DIR, "raw_measurements.csv"),
}


def main():
    """Save prepared data in the PREPARED_DIR."""
    print("Reading raw data...")
    raw_data = {
        k: pd.read_csv(v, index_col=None) for k, v in RAW_DATA_FILES.items()
    }
    print("Preparing data...")
    for dpf in DATA_PREPARATION_FUNCTIONS_TO_RUN:
        print(f"Running data preparation function {dpf.__name__}...")
        prepared_data = dpf(raw_data["raw_measurements"])
        output_dir = os.path.join(PREPARED_DIR, prepared_data.name)
        print(f"\twriting files to {output_dir}")
        prepared_data.write_files(output_dir)


if __name__ == "__main__":
    main()
