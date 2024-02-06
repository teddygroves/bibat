"""Unit tests for the InferenceConfiguration class."""

from pathlib import Path

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


def test_model_configuration_good_modes() -> None:
    """Check that an inference configuration with good modes initialises."""
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=Path("hi") / "hello" / "hey",
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        mode_options={"kfold": {"n_folds": 10}},
        modes=MODES_GOOD,
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_bad_modes() -> None:
    """Check that an inference configuration with bad modes fails."""
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=Path("hi") / "hello" / "hey",
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_BAD,
        mode_options={"kfold": {"n_folds": 10}},
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_no_k() -> None:
    """Check that an inference configuration with no kfold options fails."""
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=Path("hi") / "hello" / "hey",
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        mode_options={"kfold": None},  # This is the bad mode!
        modes=MODES_GOOD,  # it would be ok if 'kfold' weren't in here.
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_no_stan_file() -> None:
    """Check that an inference configuration with absent Stan file fails."""
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="XXXXXXXXXXXXXXXXXXXX",
        prepared_data_dir=Path("hi") / "hello" / "hey",
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        mode_options={"kfold": {"n_folds": 10}},
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_no_stan_input_function() -> None:
    """Check that absent Stan input function causes failure."""
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data_dir=Path("hi") / "hello" / "hey",
        stan_input_function="XXXXXXXXXXXXXXXXXX",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        mode_options={"kfold": {"n_folds": 10}},
        cpp_options=None,
        stanc_options=None,
    )
