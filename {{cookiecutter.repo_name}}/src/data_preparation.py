"""Provides functions prepare_data_x.

These functions should take in a dataframe of measurements and return a
PreparedData object.

Note that you can change the input arbitrarily - for example if you want to take
in two dataframes, a dictionary etc. However in this case you will need to edit
the corresponding code in the file prepare_data.py accordingly.

"""

from functools import partial
from typing import List

import numpy as np
import pandas as pd

from src.prepared_data import PreparedData
from src.util import (
    CoordDict,
    StanInput,
    check_is_df,
    make_columns_lower_case,
    stanify_dict,
)

NEW_COLNAMES = {"yButIThoughtIdAddSomeLetters": "y"}
DROPNA_COLS = ["y"]
N_CV_FOLDS = 10


def prepare_data_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with an interaction column."""
    x_cols = ["x1", "x2", "x1:x2"]
    measurements = process_measurements(measurements_raw)
    return PreparedData(
        name="interaction",
        coords=CoordDict({"covariate": x_cols}),
        dims={"b": ["covariate"]},
        measurements=measurements,
        number_of_cv_folds=N_CV_FOLDS,
        stan_input_function=partial(get_stan_input, x_cols=x_cols),
    )


def prepare_data_no_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with no interaction column."""
    x_cols = ["x1", "x2"]
    measurements = process_measurements(measurements_raw)
    return PreparedData(
        name="no_interaction",
        coords=CoordDict({"covariate": x_cols}),
        dims={"b": ["covariate"]},
        measurements=measurements,
        number_of_cv_folds=N_CV_FOLDS,
        stan_input_function=partial(get_stan_input, x_cols=x_cols),
    )


def prepare_data_fake_interaction(
    measurements_raw: pd.DataFrame,
) -> PreparedData:
    """Prepare fake data with an interaction column."""
    TRUE_PARAMS = {"a": 1, "b": [0.6, -0.3, 0.2], "sigma": 0.3}
    x_cols = ["x1", "x2", "x1:x2"]
    measurements = process_measurements(measurements_raw)
    yhat = TRUE_PARAMS["a"] + measurements[x_cols] @ np.array(TRUE_PARAMS["b"])
    measurements["y"] = np.random.normal(yhat, TRUE_PARAMS["sigma"])
    return PreparedData(
        name="fake_interaction",
        coords=CoordDict({"covariate": x_cols}),
        dims={"b": ["covariate"]},
        measurements=measurements,
        number_of_cv_folds=N_CV_FOLDS,
        stan_input_function=partial(get_stan_input, x_cols=x_cols),
    )


def process_measurements(measurements: pd.DataFrame) -> pd.DataFrame:
    """Process the measurements.

    This is to illustrate how you might want to do common table manipulation
    tasks like filtering, changing column names and adding new columns.

    Note that if you want, you can use different measurement processing
    functions for different prepare_data functions

    Contains check_is_df a lot because many pandas methods have return signatures
    including None, but we want to raise an error unless a DataFrame is returned.

    """
    out = check_is_df(
        check_is_df(
            check_is_df(measurements.rename(columns=NEW_COLNAMES))
            .pipe(make_columns_lower_case)
            .dropna(subset=DROPNA_COLS, axis=0)
        ).drop_duplicates()
    ).copy()
    out["x1:x2"] = out["x1"] * out["x2"]
    return out


def get_stan_input(
    measurements: pd.DataFrame,
    x_cols: List[str],
    likelihood: bool,
    train_ix: List[int],
    test_ix: List[int],
) -> StanInput:
    """Turn a processed dataframe into a Stan input.

    You can change the inputs to this function, but remember to also edit the
    PreparedData class accordingly. In particular, for analyses involving exact
    cross-validation you will probably want to keep the `train_ix` and `test_ix`
    arguments, and for analyses involving both prior and posterior modes you
    should keep the argument `likelihood`.

    """
    return stanify_dict(
        {
            "N": len(measurements),
            "N_train": len(train_ix),
            "N_test": len(test_ix),
            "K": len(x_cols),
            "x": measurements[x_cols],
            "y": measurements["y"],
            "likelihood": int(likelihood),
            "ix_train": [i + 1 for i in train_ix],
            "ix_test": [i + 1 for i in test_ix],
            "y": measurements["y"],
            "likelihood": int(likelihood),
        }
    )
