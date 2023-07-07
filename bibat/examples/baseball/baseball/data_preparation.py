"""Provides functions prepare_data_x.

These functions should take in a dataframe of measurements and return a
PreparedData object.

"""
import json
import os

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series
from pydantic import BaseModel

from baseball import util

NAME_FILE = "name.txt"
COORDS_FILE = "coords.json"
MEASUREMENTS_FILE = "measurements.csv"
N_CV_FOLDS = 10

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PREPARED_DIR = os.path.join(DATA_DIR, "prepared")
RAW_DATA_FILES = {
    "2006": [os.path.join(RAW_DIR, "2006.csv")],
    "bdb": [
        os.path.join(RAW_DIR, "bdb-main.csv"),
        os.path.join(RAW_DIR, "bdb-post.csv"),
        os.path.join(RAW_DIR, "bdb-apps.csv"),
    ],
}


def prepare_data():
    """Run main function."""
    print("Reading raw data...")
    raw_data = {
        k: [pd.read_csv(file, index_col=None) for file in v]
        for k, v in RAW_DATA_FILES.items()
    }
    data_preparation_functions_to_run = {
        "2006": prepare_data_2006,
        "bdb": prepare_data_bdb,
    }
    print("Preparing data...")
    for name, dpf in data_preparation_functions_to_run.items():
        print(f"Running data preparation function {dpf.__name__}...")
        prepared_data = dpf(*raw_data[name])
        output_dir = os.path.join(PREPARED_DIR, prepared_data.name)
        print(f"\twriting files to {output_dir}")
        if not os.path.exists(PREPARED_DIR):
            os.mkdir(PREPARED_DIR)
        write_prepared_data(prepared_data, output_dir)


class MeasurementsDF(pa.SchemaModel):
    """A PreparedData should have a measurements dataframe like this.

    Other columns are also allowed!
    """

    player_season: Series[str]
    season: Series[str] = pa.Field(coerce=True)
    n_attempt: Series[int] = pa.Field(ge=1)
    n_success: Series[int] = pa.Field(ge=0)


class PreparedData(BaseModel, arbitrary_types_allowed=True):
    """What prepared data looks like in this analysis."""

    name: str
    coords: util.CoordDict
    measurements: DataFrame[MeasurementsDF]


def prepare_data_2006(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare the 2006 data."""
    measurements = measurements_raw.rename(
        columns={"K": "n_attempt", "y": "n_success"}
    ).assign(
        season="2006",
        player_season=lambda df: [f"2006-player-{i+1}" for i in range(len(df))],
    )
    return PreparedData(
        name="2006",
        coords={
            "player_season": measurements["player_season"].tolist(),
            "season": measurements["season"].astype(str).tolist(),
        },
        measurements=DataFrame[MeasurementsDF](measurements),
    )


def prepare_data_bdb(
    measurements_main: pd.DataFrame,
    measurements_post: pd.DataFrame,
    appearances: pd.DataFrame,
) -> PreparedData:
    """Prepare the baseballdatabank data.

    There are a few substantive data choices here.

    First, the function excludes players who have a '1' in their position as
    these are likely pitchers, as well as players with fewer than 20 at bats.

    Second, the function defines a successes and attempts according to the
    'on-base percentage' metric, so a success is a time when a player got a hit,
    a base on ball/walk or a hit-by-pitch and an attempt is an at-bat or a
    base-on-ball/walk or a hit-by-pitch or a sacrifice fly. This could have
    alternatively been calculated as just hits divided by at-bats, but my
    understanding is that this method underrates players who are good at getting
    walks.

    """
    pitchers = appearances.loc[
        lambda df: df["G_p"] == df["G_all"], "playerID"
    ].unique()

    def filter_batters(df: pd.DataFrame):
        return (
            (df["AB"] >= 20)
            & (df["season"].ge(2017))
            & (~df["player"].isin(pitchers))
        )

    measurements_main, measurements_post = (
        m.rename(columns={"yearID": "season", "playerID": "player"})
        .assign(
            player_season=lambda df: df["player"].str.cat(
                df["season"].astype(str)
            ),
            n_attempt=lambda df: df[["AB", "BB", "HBP", "SF"]]
            .fillna(0)
            .sum(axis=1)
            .astype(int),
            n_success=lambda df: (
                df[["H", "BB", "HBP"]].fillna(0).sum(axis=1).astype(int)
            ),
        )
        .loc[
            filter_batters,
            ["player_season", "season", "n_attempt", "n_success"],
        ]
        .copy()
        for m in [measurements_main, measurements_post]
    )
    measurements = (
        pd.concat([measurements_main, measurements_post])
        .groupby(["player_season", "season"])
        .sum()
        .reset_index()
    )
    return PreparedData(
        name="bdb",
        coords={
            "player_season": measurements["player_season"].tolist(),
            "season": measurements["season"].astype(str).tolist(),
        },
        measurements=DataFrame[MeasurementsDF](measurements),
    )


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
