"""Some handy python functions."""

from __future__ import annotations

from collections.abc import Mapping
from functools import wraps
from typing import TYPE_CHECKING, Any, NewType, ParamSpec

import numpy as np
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
    """Shut up the type checker."""
    if not isinstance(maybe_df, pd.DataFrame):
        msg = "Want dataframe."
        raise TypeError(msg)
    return maybe_df


def stanify_dict(d: dict) -> StanInputDict:
    """Make sure a dictionary is a valid Stan input.

    :param d: input dictionary, possibly with wrong types
    """
    out: StanInputDict = {}
    for k, v in d.items():
        if not isinstance(k, str):
            msg = f"key {k!r} is not a string!"
            raise TypeError(msg)
        if isinstance(v, pd.Series):
            out[k] = v.to_list()
        elif isinstance(v, pd.DataFrame):
            out[k] = v.to_numpy().tolist()
        elif isinstance(v, np.ndarray):
            out[k] = v.tolist()
        else:
            out[k] = v
    return out


def standardise(
    s: pd.Series,
    mu: float | None = None,
    std: float | None = None,
) -> pd.Series:
    """Standardise a series by subtracting mu and dividing by sd."""
    if mu is None:
        mu = s.mean()
    if std is None:
        std = s.std()
    return s.subtract(mu).divide(std)


def center(
    s: pd.Series,
    mu: float | None = None,
) -> pd.Series:
    """Center a series by subtracting mu."""
    if mu is None:
        mu = s.mean()
    return s.subtract(mu)
