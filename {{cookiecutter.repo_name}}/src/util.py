"""Some handy python functions."""

from typing import Dict, List, Union

import pandas as pd

# handy types
CoordDict = Dict[str, List[str]]
StanInput = Dict[str, Union[float, int, List[float], List[int]]]


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
    new.columns = [c.lower() for c in new.columns]
    return new
