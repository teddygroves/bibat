""""Class defining what prepared data looks like."""


import json
import os

import pandas as pd

from src.util import CoordDict

COORDS_FILENAME = "coords.json"
MEASUREMENTS_FILENAME = "measurements.csv"
PREPARED_DATA_DIR = os.path.join("data", "prepared")


class PreparedData:
    """What prepared data looks like in this analysis."""

    def __init__(
        self, name: str, coords: CoordDict, measurements: pd.DataFrame
    ):
        self.name = name
        self.coords = coords
        self.measurements = measurements

    def write_files(self, directory: str):
        """Write prepared data files to a directory."""
        measurements_file = os.path.join(directory, MEASUREMENTS_FILENAME)
        coords_file = os.path.join(directory, COORDS_FILENAME)
        self.measurements.to_csv(measurements_file)
        with open(coords_file, "w") as f:
            json.dump(self.coords, f)


def load_prepared_data(name) -> PreparedData:
    """Load prepared data from files in directory"""
    coords_file = os.path.join(PREPARED_DATA_DIR, name, COORDS_FILENAME)
    measurements_file = os.path.join(PREPARED_DATA_DIR, name, MEASUREMENTS_FILENAME)
    with open(coords_file, "r") as f:
        coords = json.load(f)
    measurements = pd.read_csv(measurements_file)
    return PreparedData(name=name, coords=coords, measurements=measurements)
