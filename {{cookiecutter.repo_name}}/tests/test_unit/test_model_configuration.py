"""Unit tests for the ModelConfiguration class."""
import os

import pytest

from src.model_configuration import ModelConfiguration

SAMPLE_KWARGS = {
    "iter_warmup": 50,
    "iter_sampling": 50,
    "chains": 2,
    "step_size": 0.01,
    "adapt_delta": 0.7,
    "show_progress": False,
}
MODES_GOOD = ["prior", "posterior", "cross_validation"]
MODES_BAD = ["prio", "prserior", "cross-validation"]


def test_model_configuration_good_modes():
    mc = ModelConfiguration(
        name="my_mc",
        stan_file=os.path.join("bla", "bla", "bla"),
        data_dir=os.path.join("hi", "hello", "hey"),
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail
def test_model_configuration_bad_modes():
    mc = ModelConfiguration(
        name="my_mc",
        stan_file=os.path.join("bla", "bla", "bla"),
        data_dir=os.path.join("hi", "hello", "hey"),
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_BAD,
        cpp_options=None,
        stanc_options=None,
    )
