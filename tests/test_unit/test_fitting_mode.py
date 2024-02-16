"""Tests for the fitting mode module."""

import os
from collections.abc import Callable
from pathlib import Path

import pandas as pd
import pytest
import toml
from cmdstanpy import CmdStanMCMC, CmdStanModel

from bibat.fitting_mode import (
    FittingMode,
    IdataTarget,
    sample_hmc_kfold,
    sample_hmc_posterior,
    sample_hmc_prior,
)
from bibat.inference_configuration import (
    InferenceConfiguration,
    load_inference_configuration,
)
from bibat.prepared_data import PreparedData
from bibat.util import CoordDict, DfInPydanticModel
from tests.test_unit.test_fitting import (
    get_stan_input_interaction,
    load_prepared_data,
)

TEST_MODEL = """
    data {
        int N;
        vector[N] y;
    }
    generated quantities {
        vector[N] llik;
        vector[N] yrep;
        for (n in 1:N){
          llik[n] = normal_lpdf(y[n] | 0, 1);
          yrep[n] = normal_rng(0, 1);
        }
    }
"""


class ExamplePreparedData(PreparedData):
    """An example prepared data dataclass."""

    name: str
    coords: CoordDict
    measurements: DfInPydanticModel


@pytest.fixture(scope="session")
def stan_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a Stan file."""
    stan_dir = tmp_path_factory.getbasetemp() / "src" / "stan"
    stan_dir.mkdir(parents=True, exist_ok=True)
    file = stan_dir / "multilevel-linear-regression.stan"
    file.write_text(TEST_MODEL)
    return file


@pytest.fixture(scope="session")
def prepared_data_json(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a prepared data json file."""
    data_dir = tmp_path_factory.getbasetemp() / "data" / "prepared"
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "interaction.json"
    test_prepared_data = ExamplePreparedData(
        name="example_prepared_data",
        coords=CoordDict({"observation": ["a", "b"]}),
        measurements=pd.DataFrame(
            {"x1": [1, 2], "x2": [3, 4], "x1:x2": [3, 8], "y": [0.0, 1.0]},
        ),
    )
    path.write_text(test_prepared_data.model_dump_json())
    return path


@pytest.fixture(scope="session")
def inference_config(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create an inference directory containing a toml file."""
    inf_dir = tmp_path_factory.getbasetemp() / "inferences" / "example"
    inf_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(inf_dir.parent.parent)
    ic = InferenceConfiguration(
        name="example",
        prepared_data="interaction",
        stan_file="multilevel-linear-regression.stan",
        stan_input_function="get_stan_input_interaction",
        modes=["posterior", "kfold"],
        sample_kwargs={"chains": 1, "iter_warmup": 2, "iter_sampling": 2},
        mode_options={
            "kfold": {"n_folds": 2},
            "prior": {"max_treedepth": 2},
            "posterior": {"iter_warmup": 3},
        },
    )
    path = inf_dir / "config.toml"
    with path.open("w") as f:
        toml.dump(ic.model_dump(by_alias=True), f)
    return path


@pytest.fixture(scope="session")
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


def test_sample_hmc_prior(
    stan_file: Path,  # noqa: ARG001
    prepared_data_json: Path,
    inference_config: Path,
) -> None:
    """Test the function sample_hmc_prior."""
    ic = load_inference_configuration(inference_config.parent)
    data = load_prepared_data(prepared_data_json)
    local_functions = {
        "get_stan_input_interaction": get_stan_input_interaction,
    }
    _ = sample_hmc_prior(ic=ic, data=data, local_functions=local_functions)


def test_sample_hmc_posterior(
    stan_file: Path,  # noqa: ARG001
    prepared_data_json: Path,
    inference_config: Path,
) -> None:
    """Test the function sample_hmc_prior."""
    ic = load_inference_configuration(inference_config.parent)
    data = load_prepared_data(prepared_data_json)
    local_functions = {
        "get_stan_input_interaction": get_stan_input_interaction,
    }
    _ = sample_hmc_posterior(ic=ic, data=data, local_functions=local_functions)


@pytest.mark.xfail()
def test_sample_hmc_kfold_bad(
    stan_file: Path,  # noqa: ARG001
    prepared_data_json: Path,
    inference_config_bad_mode_options: Path,
) -> None:
    """Test the function sample_hmc_prior."""
    ic = load_inference_configuration(inference_config_bad_mode_options.parent)
    data = load_prepared_data(prepared_data_json)
    local_functions = {
        "get_stan_input_interaction": get_stan_input_interaction,
    }
    _ = sample_hmc_kfold(ic=ic, data=data, local_functions=local_functions)
