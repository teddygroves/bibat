"""Provides the function prepare_data_main.

You can also define alternative data prep functions here.


"""

from functools import partial
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

from .prepared_data import PreparedData
from .util import CoordDict, StanInput, make_columns_lower_case

RENAMING_DICT = {"yButIThoughtIdAddSomeLetters": "y"}
COLS_THAT_MUST_BE_NON_NULL = ["y"]


def prepare_data_main(
    name: str, df: pd.DataFrame, xcols: List[str], n_folds: int
) -> PreparedData:
    df = (
        df.copy()
        .rename(columns=RENAMING_DICT)
        .pipe(make_columns_lower_case)
        .dropna(subset=COLS_THAT_MUST_BE_NON_NULL)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    df["x1:x2"] = df["x1"] * df["x2"]
    coords = {
        "covariate": xcols,
        "ix_test": df.index.values.tolist(),
    }
    dims = {
        "b": ["covariate"],
        "yrep": ["ix_test"],
        "llik": ["ix_test"],
    }
    ix_all = list(range(len(df)))
    splits = get_splits(df, n_folds)
    get_stan_input_cv = partial(
        get_stan_input, df=df, coords=coords, likelihood=True
    )
    get_stan_input_non_cv = partial(
        get_stan_input,
        df=df,
        coords=coords,
        train_ix=ix_all,
        test_ix=ix_all,
    )
    stan_input_prior, stan_input_posterior = (
        get_stan_input_non_cv(likelihood=likelihood)
        for likelihood in (False, True)
    )
    stan_inputs_cv = [
        get_stan_input_cv(train_ix=train_ix, test_ix=test_ix)
        for train_ix, test_ix in splits
    ]
    return PreparedData(
        name=name,
        df=df,
        coords=coords,
        dims=dims,
        stan_input_prior=stan_input_prior,
        stan_input_posterior=stan_input_posterior,
        stan_inputs_cv=stan_inputs_cv,
    )


def get_splits(df: pd.DataFrame, k: int) -> List[List[List[int]]]:
    """Get results of sklearn KFold split as list of list of lists.

    Each element of the return value is a list whose first value is a list of
    train indices, and whose second value is a list of test indices.

    :param df: Dataframe that you want the splits for

    :param k: number of Kfold splits

    """
    splits = []
    for train, test in KFold(k, shuffle=True).split(df):
        assert isinstance(train, np.ndarray)
        assert isinstance(test, np.ndarray)
        splits.append([list(train), list(test)])
    return splits


def get_stan_input(
    df: pd.DataFrame,
    coords: CoordDict,
    likelihood: bool,
    train_ix: List[int],
    test_ix: List[int],
) -> StanInput:
    """Get a Stan input

    :param lits: Dataframe of lits
    :param coords: Dictionary of coordinates
    :param likelihood: Whether or not to run in likelihood mode
    :param: train_ix: List of indexes of training lits
    :param: test_ix: List of indexes of test lits
    """
    xcols = coords["covariate"]
    return listify_dict(
        {
            "N": len(df),
            "N_train": len(train_ix),
            "N_test": len(test_ix),
            "K": len(xcols),
            "x": df[xcols].values,
            "y": df["y"].values,
            "likelihood": int(likelihood),
            "ix_train": [i + 1 for i in train_ix],
            "ix_test": [i + 1 for i in test_ix],
            "y": df["y"],
            "likelihood": int(likelihood),
        }
    )


def listify_dict(d: Dict) -> StanInput:
    """Make sure a dictionary is a valid Stan input.

    :param d: input dictionary, possibly with wrong types
    """
    out = {}
    for k, v in d.items():
        if not isinstance(k, str):
            raise ValueError(f"key {str(k)} is not a string!")
        elif isinstance(v, pd.Series):
            out[k] = v.to_list()
        elif isinstance(v, np.ndarray):
            out[k] = v.tolist()
        elif isinstance(v, (list, int, float)):
            out[k] = v
        else:
            raise ValueError(f"value {str(v)} has wrong type!")
    return out


PREPARE_DATA_FUNCTIONS = [prepare_data_main]
