"""Provides a function prepare_data."""

import pandas as pd

from .util import make_columns_lower_case

RENAMING_DICT = {"yButIThoughtIdAddSomeLetters": "y"}
COLS_THAT_MUST_BE_NON_NULL = ["y"]


def prepare_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Takes in raw data, returns prepared data.

    :param raw_data: pd.DataFrame of raw data
    ::
    """
    out = (
        raw_data.copy()
        .rename(columns=RENAMING_DICT)
        .pipe(make_columns_lower_case)
        .dropna(subset=COLS_THAT_MUST_BE_NON_NULL)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    out["x1:x2"] = out["x1"] * out["x2"]
    return out
