"""Prepare the data at RAW_DATA_CSV and save it to PREPARED_DATA_CSV."""

import os
from typing import List, Dict
import pandas as pd

from util import make_columns_lower_case

# Where to find raw data and where to save prepared data: probably don't edit!
RAW_DATA_DIR = os.path.join("data", "raw")
PREPARED_DATA_DIR = os.path.join("data", "prepared")

# Filenames of the input and output: edit these unless they are already what
# you want
RAW_DATA_CSV = "raw_measurements.csv"
PREPARED_DATA_CSV = "data_prepared.csv"

RENAMING_DICT = {"yButIThoughtIdAddSomeLetters": "y"}
COLS_THAT_MUST_BE_NON_NULL = ["y"]


def prepare_data(
    raw_data: pd.DataFrame,
    renaming_dict: Dict[str, str],
    cols_that_must_be_non_null: List[str],
) -> pd.DataFrame:
    """Takes in raw data, returns prepared data.

    :param raw_data: pd.DataFrame of raw data
    ::
    """
    out = (
        raw_data.copy()
        .rename(columns=renaming_dict)
        .pipe(make_columns_lower_case)
        .dropna(subset=cols_that_must_be_non_null)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    out["x1:x2"] = out["x1"] * out["x2"]
    return out


def main():
    """Run the script."""
    raw_data_csv = os.path.join(RAW_DATA_DIR, RAW_DATA_CSV)
    prepared_data_csv = os.path.join(PREPARED_DATA_DIR, PREPARED_DATA_CSV)
    print(f"Reading raw data from {raw_data_csv}")
    raw = pd.read_csv(raw_data_csv)
    out = prepare_data(raw, RENAMING_DICT, COLS_THAT_MUST_BE_NON_NULL)
    print(f"Writing prepared data to {prepared_data_csv}")
    out.to_csv(prepared_data_csv)


if __name__ == "__main__":
    main()
