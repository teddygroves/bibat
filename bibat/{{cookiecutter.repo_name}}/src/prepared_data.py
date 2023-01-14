"""Class defining what prepared data looks like."""

import json
import os

import pandas as pd
import pandera as pa
from pydantic.dataclasses import dataclass
from src.util import CoordDict

NAME_FILE = "name.txt"
COORDS_FILE = "coords.json"
MEASUREMENTS_FILE = "measurements.csv"


class MeasurementsDF(pa.SchemaModel):
    """A PreparedData should have a measurements dataframe like this.

    Other columns are also allowed!
    """

    x1: pa.typing.Series[float]
    x2: pa.typing.Series[float]
    x1colonx2: pa.typing.Series[float] = pa.Field(alias="x1:x2")
    y: pa.typing.Series[float]


@dataclass
class PreparedData:
    """What prepared data looks like in this analysis."""

    name: str
    coords: CoordDict
    measurements: pa.typing.DataFrame[MeasurementsDF]


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
        measurements=measurements,
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
