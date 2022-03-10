"""Integration tests for functions in src/data_preparation.py"""

from typing import Callable

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.data_preparation import (
    N_CV_FOLDS,
    get_stan_inputs,
    prepare_data_interaction,
    prepare_data_no_interaction,
)
from src.util import CoordDict

EXAMPLE_RAW_MEASUREMENTS = pd.DataFrame(
    {
        "X1": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
        "X2": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
        "yButIThoughtIdAddSomeLetters": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],
    }
)


@pytest.mark.parametrize(
    "prepare_data_function,name,raw_measurements,expected_measurements,expected_coords",
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
                }
            ),
            {
                "covariate": ["x1", "x2", "x1:x2"],
                "observation": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
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
                }
            ),
            {
                "covariate": ["x1", "x2"],
                "observation": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
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
):
    prepped = prepare_data_function(raw_measurements)
    si_prior, si_posterior, sis_cv = get_stan_inputs(prepped)
    assert prepped.name == name
    assert prepped.coords == expected_coords
    assert_frame_equal(prepped.measurements, expected_measurements)
    assert prepped.number_of_cv_folds == N_CV_FOLDS
    assert (
        prepped.stan_input_function(
            measurements=prepped.measurements,
            likelihood=True,
            train_ix=list(range(len(prepped.measurements))),
            test_ix=list(range(len(prepped.measurements))),
        )
        == si_posterior
    )
    assert si_prior["likelihood"] == 0
    assert si_posterior["likelihood"] == 1
    for i, si in enumerate(sis_cv):
        # check that each measurement is in at most one cv test index
        for i_other, si_other in enumerate(sis_cv):
            if i != i_other:
                ixs_i = si["ix_test"]
                ixs_other = si_other["ix_test"]
                assert isinstance(ixs_i, list)
                assert isinstance(ixs_other, list)
                assert not any([ix in ixs_other for ix in ixs_i])
