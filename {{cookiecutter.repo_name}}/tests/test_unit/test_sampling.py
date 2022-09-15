"""Unit tests for functions in src/sampling.py"""

import os

import pytest

from src.sampling import sample

# Locations
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(HERE, "..", "..")
STAN_FILE = os.path.join(PROJECT_ROOT, "src", "stan", "model.stan")
INPUT_FILE = os.path.join(HERE, "..", "data", "example_input_data_good.json")
COORDS = {
    "covariate": ["x1", "x2"],
    "observation": [0, 1, 2, 3],
}
DIMS = {
    "b": ["covariate"],
    "y": ["observation"],
    "yrep": ["observation"],
    "llik": ["observation"],
}
SAMPLE_KWARGS = {
    "iter_warmup": 50,
    "iter_sampling": 50,
    "chains": 2,
    "step_size": 0.01,
    "adapt_delta": 0.7,
    "show_progress": False,
}
ARGS_GOOD = {  # this input to sample should work
    "stan_file": STAN_FILE,
    "input_json": INPUT_FILE,
    "coords": COORDS,
    "dims": DIMS,
    "sample_kwargs": SAMPLE_KWARGS,
    "cpp_options": None,
    "stanc_options": None,
}


@pytest.mark.parametrize("argdict", [ARGS_GOOD])
def test_sample(argdict):
    """Test that the sample function works as expected."""
    idata = sample(**argdict)
    assert hasattr(idata, "posterior_predictive")
    assert idata.posterior_predictive["yrep"].shape == (
        SAMPLE_KWARGS["chains"],
        SAMPLE_KWARGS["iter_sampling"],
        len(COORDS["observation"])
    )
