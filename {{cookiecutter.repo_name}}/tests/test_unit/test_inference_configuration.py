"""Unit tests for the ModelConfiguration class."""
import os

import pytest

from src.inference_configuration import InferenceConfiguration

SAMPLE_KWARGS = {
    "iter_warmup": 50,
    "iter_sampling": 50,
    "chains": 2,
    "step_size": 0.01,
    "adapt_delta": 0.7,
    "show_progress": False,
}
MODES_GOOD = ["prior", "posterior", "kfold"]
MODES_BAD = ["prio", "prserior", "cross-validation"]


def test_model_configuration_good_modes():
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=os.path.join("hi", "hello", "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        kfold_folds=10,
        modes=MODES_GOOD,
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail
def test_model_configuration_bad_modes():
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=os.path.join("hi", "hello", "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_BAD,
        kfold_options=10,
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail
def test_model_configuration_no_k():
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=os.path.join("hi", "hello", "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        kfold_options=None,  # this is the bad field!
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail
def test_model_configuration_no_stan_file():
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="XXXXXXXXXXXXXXXXXXXX",
        prepared_data_dir=os.path.join("hi", "hello", "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        kfold_options=10,
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail
def test_model_configuration_no_stan_input_function():
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=os.path.join("hi", "hello", "hey"),
        stan_input_function="XXXXXXXXXXXXXXXXXX",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        kfold_options=10,
        cpp_options=None,
        stanc_options=None,
    )