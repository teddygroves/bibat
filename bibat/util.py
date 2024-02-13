"""A module that provides some Bayesian analysis oriented utility code."""

from __future__ import annotations

from collections.abc import Mapping
from functools import wraps
from typing import TYPE_CHECKING, Any, NewType, ParamSpec

import pandas as pd
from stanio.json import process_dictionary

if TYPE_CHECKING:
    from collections.abc import Callable

CoordDict = NewType("CoordDict", dict[str, list[str]])
StanInputDict = Mapping[str, Any]

P = ParamSpec("P")


def returns_stan_input(
    func: Callable[P, Mapping[str, Any]],
) -> Callable[P, Mapping[str, Any]]:
    """Decorate a function so it returns a json-serialisable dictionary."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Mapping[str, Any]:
        return process_dictionary(func(*args, **kwargs))

    return wrapper


def one_encode(s: pd.Series) -> pd.Series:
    """Replace a series's values with 1-indexed integer factors.

    :param s: a pandas Series that you want to factorise.

    """
    return pd.Series(pd.factorize(s)[0] + 1, index=s.index)


def make_columns_lower_case(df: pd.DataFrame) -> pd.DataFrame:
    """Make a DataFrame's columns lower case.

    :param df: a pandas DataFrame
    """
    new = df.copy()
    if isinstance(new.columns, pd.MultiIndex):
        new.columns = pd.MultiIndex.from_arrays(
            [
                [c.lower() for c in new.columns.get_level_values(i)]
                for i in range(len(new.columns.levels))
            ],
        )
    else:
        new.columns = pd.Index([c.lower() for c in new.columns])
    return new


def check_is_df(maybe_df: Any) -> pd.DataFrame:  # noqa: ANN401
    """Check that an object is a DataFrame."""
    if not isinstance(maybe_df, pd.DataFrame):
        msg = "Want dataframe."
        raise TypeError(msg)
    return maybe_df
