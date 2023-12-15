"""Provides function `prepare_data` and runs it.

This function should run some other functions with names `prepare_data_x`, which
each take in a dataframe of measurements and return a PreparedData object.

"""
import json
import os
from io import StringIO
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series
from pandera.typing.common import DataFrameBase
from pydantic import BaseModel, field_serializer, field_validator
from {{cookiecutter.repo_name}} import util

HERE = Path(__file__).parent
RAW_DIR = HERE /  ".." / "data" / "raw"
PREPARED_DIR = HERE / ".." / "data" / "prepared"
RAW_DATA_FILES = {"measurements": RAW_DIR / "raw_measurements.csv"}


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
    measurements: Any

    @field_validator("measurements")
    def validate_measurements(
        cls, v: Any
    ) -> DataFrameBase[MeasurementsDF]:
        if isinstance(v, str):
            v = pd.read_json(StringIO(v))
        return MeasurementsDF.validate(v)

    @field_serializer("measurements")
    def serialize_measurements(
        self, measurements: DataFrame[MeasurementsDF], _info
    ):
        return measurements.to_json()


def load_prepared_data(path_to_data: str) -> PreparedData:
    """Load a dataset."""
    with open(path_to_data) as f:
        raw = json.load(f)
    return PreparedData(**raw)


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
    dropna_cols = ["y"]
    new_colnames = {"yButIThoughtIdAddSomeLetters": "y"}
    out = (
        measurements.rename(columns=new_colnames)
        .pipe(util.make_columns_lower_case)
        .dropna(subset=dropna_cols, axis=0)
    ).copy()
    for col in ["x1", "x2", "y"]:
        out[col] = out[col].astype(float)
    out["x1:x2"] = out["x1"] * out["x2"]
    return out


def prepare_data():
    """Run main function."""
    print("Reading raw data...")
    raw_data = {
        k: pd.read_csv(v, index_col=None) for k, v in RAW_DATA_FILES.items()
    }
    print("Preparing data...")
    for prepare_data_func in  [
        prepare_data_interaction,
        prepare_data_no_interaction,
        prepare_data_fake_interaction
    ]:
        print(f"Running data preparation function {prepare_data_func.__name__}...")
        prepared_data = prepare_data_func(raw_data["measurements"])
        output_file = os.path.join(PREPARED_DIR, prepared_data.name + ".json")
        print(f"\twriting prepared_data to {output_file}")
        if not os.path.exists(PREPARED_DIR):
            os.mkdir(PREPARED_DIR)
        with open(output_file, "w") as f:
            f.write(prepared_data.model_dump_json())


if __name__ == "__main__":
    prepare_data()
