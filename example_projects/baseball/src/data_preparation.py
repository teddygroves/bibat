"""Provides data preparation definitions and functions.

This function should run some other functions with names `prepare_data_x`, which
each take in a dataframe of measurements and return a PreparedData object.

"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series
from pydantic import field_validator

from bibat.prepared_data import PreparedData
from bibat.util import CoordDict, DfInPydanticModel

if TYPE_CHECKING:
    from pandera.typing.common import DataFrameBase

HERE = Path(__file__).parent
RAW_DIR = HERE / ".." / "data" / "raw"
PREPARED_DIR = HERE / ".." / "data" / "prepared"
RAW_DATA_FILES = {
    "2006": [RAW_DIR / "2006.csv"],
    "bdb": [
        RAW_DIR / "bdb-main.csv",
        RAW_DIR / "bdb-post.csv",
        RAW_DIR / "bdb-apps.csv",
    ],
}


class BaseballMeasurementsDF(pa.SchemaModel):
    """A BaseballPreparedData should have a measurements table like this."""

    player_season: Series[str]
    season: Series[str] = pa.Field(coerce=True)
    n_attempt: Series[int] = pa.Field(ge=1)
    n_success: Series[int] = pa.Field(ge=0)


class BaseballPreparedData(PreparedData):
    """What prepared data looks like in this analysis."""

    name: str
    coords: CoordDict
    measurements: DfInPydanticModel

    @field_validator("measurements")
    def validate_measurements(
        cls,  # noqa: N805, ANN101
        v: DfInPydanticModel,
    ) -> DataFrameBase[BaseballMeasurementsDF]:
        """Validate the measurements table."""
        return BaseballMeasurementsDF.validate(v)


def prepare_data_2006(measurements_raw: pd.DataFrame) -> BaseballPreparedData:
    """Prepare the 2006 data."""
    measurements = measurements_raw.rename(
        columns={
            "K": "n_attempt",
            "y": "n_success",
        },
    ).assign(
        season="2006",
        player_season=lambda df: [f"2006-player-{i+1}" for i in range(len(df))],
    )
    return BaseballPreparedData(
        name="2006",
        coords=CoordDict(
            {
                "player_season": measurements["player_season"].tolist(),
                "season": measurements["season"].astype(str).tolist(),
            },
        ),
        measurements=DataFrame[BaseballMeasurementsDF](measurements),
    )


def prepare_data_bdb(
    measurements_main: pd.DataFrame,
    measurements_post: pd.DataFrame,
    appearances: pd.DataFrame,
) -> BaseballPreparedData:
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
        lambda df: df["G_p"] == df["G_all"],
        "playerID",
    ].unique()

    def filter_batters(df: pd.DataFrame) -> pd.Series:
        return (
            (df["AB"] >= 20)  # noqa: PLR2004
            & (df["season"].ge(2017))
            & (~df["player"].isin(pitchers))
        )

    measurements_main, measurements_post = (
        m.rename(columns={"yearID": "season", "playerID": "player"})
        .assign(
            player_season=lambda df: df["player"].str.cat(
                df["season"].astype(str),
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
    return BaseballPreparedData(
        name="bdb",
        coords=CoordDict(
            {
                "player_season": measurements["player_season"].tolist(),
                "season": measurements["season"].astype(str).tolist(),
            },
        ),
        measurements=DataFrame[BaseballMeasurementsDF](measurements),
    )


def prepare_data() -> None:
    """Run main function."""
    raw_data = {
        k: [pd.read_csv(file, index_col=None) for file in v]
        for k, v in RAW_DATA_FILES.items()
    }
    data_preparation_functions_to_run = {
        "2006": prepare_data_2006,
        "bdb": prepare_data_bdb,
    }
    for name, prepare_data_func in data_preparation_functions_to_run.items():
        logging.info("Preparing %s data", name)
        prepared_data = prepare_data_func(*raw_data[name])
        output_file = prepared_data.name + ".json"
        output_path = PREPARED_DIR / output_file
        if not PREPARED_DIR.exists():
            PREPARED_DIR.mkdir()
        with output_path.open("w") as f:
            f.write(prepared_data.model_dump_json())


def load_prepared_data(path: Path | str) -> BaseballPreparedData:
    """Load a prepared data object from a path."""
    if isinstance(path, str):
        path = Path(path)
    with path.open("r") as f:
        return BaseballPreparedData(**json.load(f))


if __name__ == "__main__":
    prepare_data()
