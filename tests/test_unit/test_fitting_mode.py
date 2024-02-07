"""Tests for the fitting mode module."""

from collections.abc import Callable
from pathlib import Path

import pytest
from cmdstanpy import CmdStanMCMC, CmdStanModel

from bibat.fitting_mode import FittingMode, IdataTarget
from bibat.inference_configuration import InferenceConfiguration
from bibat.prepared_data import PreparedData


def example_good_fit_func(
    ic: InferenceConfiguration,
    data: PreparedData,
    local_functions: dict[str, Callable],
) -> CmdStanMCMC:
    """Perform a fitting mode."""
    sif = local_functions[ic.stan_input_function]
    input_dict = sif(data) | {"likelihood": 0}
    stan_file = Path("src") / "stan" / ic.stan_file
    model = CmdStanModel(stan_file=stan_file)
    sample_kwargs = ic.sample_kwargs
    if ic.mode_options is not None and "prior" in ic.mode_options:
        sample_kwargs |= ic.mode_options["prior"]
    return model.sample(input_dict, **sample_kwargs)


@pytest.mark.parametrize("target", ["prior", "posterior", "log_likelihood"])
def test_idata_target_good(target: str) -> None:
    """Good cases for InferenceDataTarget."""
    _ = IdataTarget(target)


@pytest.mark.xfail()
@pytest.mark.parametrize("target", ("ptior"))
def test_idata_target_bad(target: str) -> None:
    """Bad cases for InferenceDataTarget."""
    _ = IdataTarget(target)


def test_fitting_mode_good() -> None:
    """Test a good case of making a fitting mode."""
    _ = FittingMode(
        name="prior",
        idata_target=IdataTarget.prior,
        fit=example_good_fit_func,
    )
