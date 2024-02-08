"""Provides data preparation definitions and functions.

This function should run some other functions with names `prepare_data_x`, which
each take in a dataframe of measurements and return a PreparedData object.

"""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series
from pydantic import field_serializer, field_validator

from bibat.prepared_data import PreparedData
from bibat.util import CoordDict, make_columns_lower_case

if TYPE_CHECKING:
    from pandera.typing.common import DataFrameBase

HERE = Path(__file__).parent
RAW_DIR = HERE / ".." / "data" / "raw"
PREPARED_DIR = HERE / ".." / "data" / "prepared"
RAW_DATA_FILES = {"measurements": RAW_DIR / "raw_measurements.csv"}


class ExampleMeasurementsDF(pa.SchemaModel):
    """An ExamplePreparedData should have a measurements dataframe like this.

    Other columns are also allowed!
    """

    x1: Series[float]
    x2: Series[float]
    x1colonx2: Series[float] = pa.Field(alias="x1:x2")
    y: Series[float]


class ExamplePreparedData(PreparedData):
    """What prepared data looks like in bibat's example analysis."""

    name: str
    coords: CoordDict
    measurements: Any

    @field_validator("measurements")
    def validate_measurements(
        cls,  # noqa: N805, ANN101
        v: Any,  # noqa: ANN401
    ) -> DataFrameBase[ExampleMeasurementsDF]:
        """Validate the measurements table."""
        if isinstance(v, str):
            v = pd.read_json(StringIO(v))
        return ExampleMeasurementsDF.validate(v)

    @field_serializer("measurements")
    def serialize_measurements(
        self,  # noqa: ANN101
        measurements: DataFrame[ExampleMeasurementsDF],
        _info,  # noqa: ANN001
    ) -> str | None:
        """Convert the measurements table to json."""
        return measurements.to_json()


def prepare_data_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with an interaction column."""
    measurements = process_measurements(measurements_raw)
    return ExamplePreparedData(
        name="interaction",
        coords=CoordDict(
            {
                "covariate": ["x1", "x2", "x1:x2"],
                "observation": measurements.index.map(str).tolist(),
            },
        ),
        measurements=DataFrame[ExampleMeasurementsDF](measurements),
    )


def prepare_data_no_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with no interaction column."""
    measurements = process_measurements(measurements_raw)
    return ExamplePreparedData(
        name="no_interaction",
        coords=CoordDict(
            {
                "covariate": ["x1", "x2"],
                "observation": measurements.index.map(str).tolist(),
            },
        ),
        measurements=DataFrame[ExampleMeasurementsDF](measurements),
    )


def prepare_data_fake_interaction(
    measurements_raw: pd.DataFrame,
) -> PreparedData:
    """Prepare fake data with an interaction column."""
    true_params = {"a": 1, "b": [0.6, -0.3, 0.2], "sigma": 0.3}
    x_cols = ["x1", "x2", "x1:x2"]
    measurements = process_measurements(measurements_raw)
    yhat = true_params["a"] + measurements[x_cols] @ np.array(true_params["b"])
    measurements["y"] = np.random.default_rng().normal(
        yhat,
        true_params["sigma"],
    )
    return ExamplePreparedData(
        name="fake_interaction",
        coords=CoordDict(
            {
                "covariate": x_cols,
                "observation": measurements.index.map(str).tolist(),
            },
        ),
        measurements=DataFrame[ExampleMeasurementsDF](measurements),
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
        .pipe(make_columns_lower_case)
        .dropna(subset=dropna_cols, axis=0)
    ).copy()
    for col in ["x1", "x2", "y"]:
        out[col] = out[col].astype(float)
    out["x1:x2"] = out["x1"] * out["x2"]
    return out


def prepare_data() -> None:
    """Run main function."""
    raw_data = {
        k: pd.read_csv(v, index_col=None) for k, v in RAW_DATA_FILES.items()
    }
    for prepare_data_func in [
        prepare_data_interaction,
        prepare_data_no_interaction,
        prepare_data_fake_interaction,
    ]:
        prepared_data = prepare_data_func(raw_data["measurements"])
        output_file = prepared_data.name + ".json"
        output_path = PREPARED_DIR / output_file
        if not PREPARED_DIR.exists():
            PREPARED_DIR.mkdir()
        with output_path.open("w") as f:
            f.write(prepared_data.model_dump_json())


def load_prepared_data(path: Path | str) -> ExamplePreparedData:
    """Load a prepared data object from a path."""
    if isinstance(path, str):
        path = Path(path)
    with path.open("r") as f:
        return ExamplePreparedData(**json.load(f))


if __name__ == "__main__":
    prepare_data()
