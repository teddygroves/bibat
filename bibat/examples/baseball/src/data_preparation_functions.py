"""Provides functions prepare_data_x.

These functions should take in a dataframe of measurements and return a
PreparedData object.

"""

import pandas as pd
from src.prepared_data import PreparedData


def prepare_data_2006(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare the 2006 data."""
    measurements = (
        measurements_raw
        .rename(columns={"K": "n_attempt", "y": "n_success"})
        .assign(
            season="2006",
            player=lambda df: [f"2006-player-{i+1}" for i in range(len(df))]
        )
    )
    return PreparedData(
        name="2006",
        coords={
            "player": measurements["player"].tolist(),
            "season": measurements["season"].tolist()
        },
        measurements=measurements,
    )


def prepare_data_recent(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare the recent data.

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
    def filter_batters(df: pd.DataFrame):
        return (
            (df["AB"] >= 20)
            & ~df["Pos.Summary"].astype(str).str.contains("1")
        )
    measurements = (
        measurements_raw
        .assign(
            season=lambda df: df["year"].astype(str),
            player=lambda df: df["Name.additional"].str.cat(df["Tm"]).str.cat(df["Lg"]).str.cat(df["season"]),
            n_attempt=lambda df: df[["AB", "BB", "HBP", "SF"]].fillna(0).sum(
                axis=1).astype(int),
            n_success=lambda df: (
                df[["H", "BB", "HBP"]].fillna(0).sum(axis=1).astype(int)
            )
        )
        .loc[filter_batters, ["player", "season", "n_attempt", "n_success"]]
        .copy()
    )
    return PreparedData(
        name="recent",
        coords={
            "player": measurements["player"].tolist(),
            "season": measurements["season"].tolist()
        },
        measurements=measurements,
    )
