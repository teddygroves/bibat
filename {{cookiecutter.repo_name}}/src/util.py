"""Some handy python functions."""

from typing import Dict, List, NewType, Union

import numpy as np
import pandas as pd

StanInput = NewType(
    "StanInput", Dict[str, Union[float, int, List[float], List[int]]]
)
CoordDict = NewType("CoordDict", Dict[str, List[str]])


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
    if isinstance(new.columns, pd.Index):
        new.columns = pd.Index([c.lower() for c in new.columns])
    elif isinstance(new.columns, pd.MultiIndex):
        new.columns = pd.MultiIndex.from_arrays(
            [
                [c.lower() for c in new.columns.get_level_values(l)]
                for l in new.columns.levels
            ]
        )
    return new


def check_is_df(maybe_df) -> pd.DataFrame:
    """Shut up the type checker!"""
    assert isinstance(maybe_df, pd.DataFrame)
    return maybe_df


def stanify_dict(d: Dict) -> StanInput:
    """Make sure a dictionary is a valid Stan input.

    :param d: input dictionary, possibly with wrong types
    """
    out = {}
    for k, v in d.items():
        if not isinstance(k, str):
            raise ValueError(f"key {str(k)} is not a string!")
        elif isinstance(v, pd.Series):
            out[k] = v.to_list()
        elif isinstance(v, pd.DataFrame):
            out[k] = v.values.tolist()
        elif isinstance(v, np.ndarray):
            out[k] = v.tolist()
        elif isinstance(v, (list, int, float)):
            out[k] = v
    return StanInput(out)


from itertools import islice
from pathlib import Path


def tree(
    dir_path_str: str,
    level: int = -1,
    limit_to_directories: bool = False,
    length_limit: int = 1000,
):
    """Given a directory Path object print a visual tree structure

    Copied from https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python

    """
    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "
    dir_path = Path(dir_path_str)  # accept string coerceable to Path
    files = 0
    directories = 0

    def inner(dir_path: Path, prefix: str = "", level=-1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else:
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(
                    path, prefix=prefix + extension, level=level - 1
                )
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1

    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f"... length_limit, {length_limit}, reached, counted:")
    print(
        f"\n{directories} directories" + (f", {files} files" if files else "")
    )
