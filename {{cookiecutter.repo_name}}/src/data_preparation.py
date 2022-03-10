"""Provides functions prepare_data_x.

These functions should take in a dataframe of measurements and return a
PreparedData object.

Note that you can change the input arbitrarily - for example if you want to take
in two dataframes, a dictionary etc. However in this case you will need to edit
the corresponding code in the file prepare_data.py accordingly.

"""

from functools import partial
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

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
DIMS = {
    "b": ["covariate"],
    "y": ["observation"],
    "yrep": ["observation"],
    "llik": ["observation"],
}


def prepare_data_interaction(measurements_raw: pd.DataFrame) -> PreparedData:
    """Prepare data with an interaction column."""
    x_cols = ["x1", "x2", "x1:x2"]
    measurements = process_measurements(measurements_raw)
    return PreparedData(
        name="interaction",
        coords=CoordDict(
            {"covariate": x_cols, "observation": measurements.index.tolist()}
        ),
        dims=DIMS,
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
        coords=CoordDict(
            {"covariate": x_cols, "observation": measurements.index.tolist()}
        ),
        dims=DIMS,
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
        coords=CoordDict(
            {"covariate": x_cols, "observation": measurements.index.tolist()}
        ),
        dims=DIMS,
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
        )
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
    """Turn a processed dataframe into a Stan input."""
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


def get_stan_inputs(
    prepared_data: PreparedData,
) -> Tuple[StanInput, StanInput, List[StanInput]]:
    """Get Stan input dictionaries for all modes from a PreparedData object."""
    ix_all = list(range(len(prepared_data.measurements)))
    stan_input_prior, stan_input_posterior = (
        prepared_data.stan_input_function(
            measurements=prepared_data.measurements,
            train_ix=ix_all,
            test_ix=ix_all,
            likelihood=likelihood,
        )
        for likelihood in (False, True)
    )
    stan_inputs_cv = []
    kf = KFold(prepared_data.number_of_cv_folds, shuffle=True)
    for train, test in kf.split(prepared_data.measurements):
        stan_inputs_cv.append(
            prepared_data.stan_input_function(
                measurements=prepared_data.measurements,
                likelihood=True,
                train_ix=list(train),
                test_ix=list(test),
            )
        )
    return stan_input_prior, stan_input_posterior, stan_inputs_cv
