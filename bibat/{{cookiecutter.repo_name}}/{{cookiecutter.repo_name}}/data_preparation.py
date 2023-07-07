"""Provides functions prepare_data_x.

These functions should take in a dataframe of measurements and return a
PreparedData object.

"""
import json
import os

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series
from pydantic import BaseModel
from {{cookiecutter.repo_name}} import util

NAME_FILE = "name.txt"
COORDS_FILE = "coords.json"
MEASUREMENTS_FILE = "measurements.csv"
NEW_COLNAMES = {"yButIThoughtIdAddSomeLetters": "y"}
DROPNA_COLS = ["y"]
N_CV_FOLDS = 10
DIMS = {
    "b": ["covariate"],
    "y": ["observation"],
    "yrep": ["observation"],
    "llik": ["observation"],
}

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PREPARED_DIR = os.path.join(DATA_DIR, "prepared")
RAW_DATA_FILES = {
    "raw_measurements": os.path.join(RAW_DIR, "raw_measurements.csv"),
}


def prepare_data():
    """Run main function."""
    print("Reading raw data...")
    raw_data = {
        k: pd.read_csv(v, index_col=None) for k, v in RAW_DATA_FILES.items()
    }
    data_preparation_functions_to_run = [
        prepare_data_interaction,
        prepare_data_no_interaction,
        prepare_data_fake_interaction
    ]
    print("Preparing data...")
    for dpf in data_preparation_functions_to_run:
        print(f"Running data preparation function {dpf.__name__}...")
        prepared_data = dpf(raw_data["raw_measurements"])
        output_dir = os.path.join(PREPARED_DIR, prepared_data.name)
        print(f"\twriting files to {output_dir}")
        if not os.path.exists(PREPARED_DIR):
            os.mkdir(PREPARED_DIR)
        write_prepared_data(prepared_data, output_dir)


class MeasurementsDF(pa.SchemaModel):
    """A PreparedData should have a measurements dataframe like this.

    Other columns are also allowed!
    """

    x1: Series[float]
    x2: Series[float]
    x1colonx2: Series[float] = pa.Field(alias="x1:x2")
    y: Series[float]


class PreparedData(BaseModel, arbitrary_types_allowed=True):
    """What prepared data looks like in this analysis."""

    name: str
    coords: util.CoordDict
    measurements: DataFrame[MeasurementsDF]


def load_prepared_data(directory: str) -> PreparedData:
    """Load prepared data from files in directory."""
    with open(os.path.join(directory, COORDS_FILE), "r") as f:
        coords = json.load(f)
    with open(os.path.join(directory, NAME_FILE), "r") as f:
        name = f.read()
    measurements = pd.read_csv(os.path.join(directory, MEASUREMENTS_FILE))
    return PreparedData(
        name=name,
        coords=coords,
        measurements=DataFrame[MeasurementsDF](measurements),
    )


def write_prepared_data(prepped: PreparedData, directory):
    """Write prepared data files to a directory."""
    if not os.path.exists(directory):
        os.mkdir(directory)
        prepped.measurements.to_csv(os.path.join(directory, MEASUREMENTS_FILE))
    with open(os.path.join(directory, COORDS_FILE), "w") as f:
        json.dump(prepped.coords, f)
    with open(os.path.join(directory, NAME_FILE), "w") as f:
        f.write(prepped.name)

def prepare_data_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with an interaction column."""
    measurements = process_measurements(measurements_raw)
    return PreparedData(
        name="interaction",
        coords=util.CoordDict(
            {
                "covariate": ["x1", "x2", "x1:x2"],
                "observation": measurements.index.map(str).tolist(),
            }
        ),
        measurements=DataFrame[MeasurementsDF](measurements),
    )


def prepare_data_no_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with no interaction column."""
    measurements = process_measurements(measurements_raw)
    return PreparedData(
        name="no_interaction",
        coords=util.CoordDict(
            {
                "covariate": ["x1", "x2"],
                "observation": measurements.index.map(str).tolist(),
            }
        ),
        measurements=DataFrame[MeasurementsDF](measurements),
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
        coords=util.CoordDict(
            {
                "covariate": x_cols,
                "observation": measurements.index.map(str).tolist(),
            }
        ),
        measurements=DataFrame[MeasurementsDF](measurements),
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
        .pipe(util.make_columns_lower_case)
        .dropna(subset=DROPNA_COLS, axis=0)
    ).copy()
    for col in ["x1", "x2", "y"]:
        out[col] = out[col].astype(float)
    out["x1:x2"] = out["x1"] * out["x2"]
    return out
