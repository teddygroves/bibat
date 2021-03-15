"""Prepare the data at RAW_DATA_CSV and save it to PREPARED_DATA_CSV."""

import os
import pandas as pd
from src.data_preparation import prepare_data

# Where to find raw data and where to save prepared data: probably don't edit!
RAW_DATA_DIR = os.path.join("data", "raw")
PREPARED_DATA_DIR = os.path.join("data", "prepared")

# Filenames of the input and output: edit these unless they are already what
# you want
RAW_DATA_CSV = "raw_measurements.csv"
PREPARED_DATA_CSV = "data_prepared.csv"


def main():
    """Run the script."""
    raw_data_csv = os.path.join(RAW_DATA_DIR, RAW_DATA_CSV)
    prepared_data_csv = os.path.join(PREPARED_DATA_DIR, PREPARED_DATA_CSV)
    print(f"Reading raw data from {raw_data_csv}")
    raw = pd.read_csv(raw_data_csv)
    out = prepare_data(raw)
    print(f"Writing prepared data to {prepared_data_csv}")
    out.to_csv(prepared_data_csv)


if __name__ == "__main__":
    main()
