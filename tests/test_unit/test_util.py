"""Unit tests for functions in src/util.py."""

import json

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from bibat.util import (
    make_columns_lower_case,
    one_encode,
    returns_stan_input,
    validate_df_or_string,
)


@pytest.mark.parametrize(
    ("s_in", "expected"),
    [
        (
            pd.Series(["8", 1, "????"], index=["a", "b", "c"]),
            pd.Series([1, 2, 3], index=["a", "b", "c"]),
        ),
        (
            pd.Series([1, "????", "????"], index=["a", "b", "c"]),
            pd.Series([1, 2, 2], index=["a", "b", "c"]),
        ),
    ],
)
def test_one_encode(s_in: pd.Series, expected: pd.Series) -> None:
    """Check that the function one_encode works as expected."""
    assert_series_equal(one_encode(s_in), expected)


@pytest.mark.parametrize(
    ("df_in", "expected"),
    [
        (
            pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]}),
            pd.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"]}),
        ),
        (
            pd.DataFrame(
                [[1, 1]],
                columns=pd.MultiIndex.from_product([["A"], ["B", "C"]]),
            ),
            pd.DataFrame(
                [[1, 1]],
                columns=pd.MultiIndex.from_product([["a"], ["b", "c"]]),
            ),
        ),
    ],
)
def test_make_columns_lower_case(
    df_in: pd.DataFrame,
    expected: pd.DataFrame,
) -> None:
    """Check that the function make_columns_lower_case works as expected."""
    assert_frame_equal(make_columns_lower_case(df_in), expected)


def test_validate_df_or_string() -> None:
    """Test the function validate_df_or_string."""
    example_df = pd.DataFrame({"a": [1, 2]})
    _ = validate_df_or_string(example_df)
    _ = validate_df_or_string(str(example_df.to_json()))


def test_returns_stan_input() -> None:
    """Test the function returns_stan_input."""

    @returns_stan_input
    def does_return_stan_input() -> dict:
        return {"a": pd.Series([1, 2, 3])}

    stan_input = does_return_stan_input()
    _ = json.dumps(stan_input)
