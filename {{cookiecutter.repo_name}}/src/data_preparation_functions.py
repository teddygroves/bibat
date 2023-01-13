"""Provides functions prepare_data_x.

These functions should take in a dataframe of measurements and return a
PreparedData object.

"""

import numpy as np
import pandas as pd
from src.prepared_data import PreparedData
from src.util import CoordDict, make_columns_lower_case

NEW_COLNAMES = {"yButIThoughtIdAddSomeLetters": "y"}
DROPNA_COLS = ["y"]
N_CV_FOLDS = 10
DIMS = {
    "b": ["covariate"],
    "y": ["observation"],
    "yrep": ["observation"],
    "llik": ["observation"],
}


def prepare_data_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with an interaction column."""
    measurements = process_measurements(measurements_raw)
    return PreparedData(
        name="interaction",
        coords=CoordDict(
            {
                "covariate": ["x1", "x2", "x1:x2"],
                "observation": measurements.index.tolist(),
            }
        ),
        measurements=measurements,
    )


def prepare_data_no_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with no interaction column."""
    measurements = process_measurements(measurements_raw)
    return PreparedData(
        name="no_interaction",
        coords=CoordDict(
            {
                "covariate": ["x1", "x2"],
                "observation": measurements.index.tolist(),
            }
        ),
        measurements=measurements,
    )


def prepare_data_fake_interaction(
    measurements_raw: pd.DataFrame,
) -> PreparedData:
    """Prepare fake data with an interaction column."""
    TRUE_PARAMS = {"a": 1, "b": [0.6, -0.3, 0.2], "sigma": 0.3}
    x_cols = ["x1", "x2", "x1:x2"]
    measurements = process_measurements(measurements_raw)
    yhat = TRUE_PARAMS["a"] + measurements[x_cols] @ np.array(TRUE_PARAMS["b"])
    measurements["y"] = np.random.normal(
        yhat, TRUE_PARAMS["sigma"]
    )  # type: ignore
    return PreparedData(
        name="fake_interaction",
        coords=CoordDict(
            {
                "covariate": x_cols,
                "observation": measurements.index.tolist(),
            }
        ),
        measurements=measurements,
    )


def process_measurements(measurements: pd.DataFrame) -> pd.DataFrame:
    """Process the measurements.

    This is to illustrate how you might want to do common table manipulation
    tasks like filtering, changing column names and adding new columns.

    Note that if you want, you can use different measurement processing
    functions for different prepare_data functions

    """
    out = (
        measurements.rename(columns=NEW_COLNAMES)
        .pipe(make_columns_lower_case)
        .dropna(subset=DROPNA_COLS, axis=0)
    ).copy()
    for col in ["x1", "x2", "y"]:
        out[col] = out[col].astype(float)
    out["x1:x2"] = out["x1"] * out["x2"]
    return out
