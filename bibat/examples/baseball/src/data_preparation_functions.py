"""Provides functions prepare_data_x.

These functions should take in a dataframe of measurements and return a
PreparedData object.

"""

import pandas as pd
from src.prepared_data import PreparedData


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
            "season": measurements["season"].tolist(),
        },
        measurements=measurements,
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
            "season": measurements["season"].tolist(),
        },
        measurements=measurements,
    )
