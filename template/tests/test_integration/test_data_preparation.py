"""Integration tests for functions in src/data_preparation.py."""

from collections.abc import Callable

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from bibat.util import CoordDict
from src.data_preparation import (
    prepare_data_interaction,
    prepare_data_no_interaction,
)

EXAMPLE_RAW_MEASUREMENTS = pd.DataFrame(
    {
        "X1": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
        "X2": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
        "yButIThoughtIdAddSomeLetters": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
    },
)


@pytest.mark.parametrize(
    (
        "prepare_data_function",
        "name",
        "raw_measurements",
        "expected_measurements",
        "expected_coords",
    ),
    [
        (
            prepare_data_interaction,
            "interaction",
            EXAMPLE_RAW_MEASUREMENTS,
            pd.DataFrame(
                {
                    "x1": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
                    "x2": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
                    "y": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
                    "x1:x2": [1, 4, 9, 1, 4, 9, 1, 4, 9, 1, 4],
                },
            ).apply(lambda s: s.astype(float)),
            {
                "covariate": ["x1", "x2", "x1:x2"],
                "observation": [str(i) for i in range(11)],
            },
        ),
        (
            prepare_data_no_interaction,
            "no_interaction",
            EXAMPLE_RAW_MEASUREMENTS,
            pd.DataFrame(
                {
                    "x1": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
                    "x2": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
                    "y": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
                    "x1:x2": [1, 4, 9, 1, 4, 9, 1, 4, 9, 1, 4],
                },
            ).apply(lambda s: s.astype(float)),
            {
                "covariate": ["x1", "x2"],
                "observation": [str(i) for i in range(11)],
            },
        ),
    ],
)
def test_prepare_data_function(
    prepare_data_function: Callable,
    name: str,
    raw_measurements: pd.DataFrame,
    expected_measurements: pd.DataFrame,
    expected_coords: CoordDict,
) -> None:
    """Check that a prepare data function behaves as expected."""
    prepped = prepare_data_function(raw_measurements)
    if prepped.name != name:
        raise ValueError
    if prepped.coords != expected_coords:
        raise ValueError
    assert_frame_equal(prepped.measurements, expected_measurements)
