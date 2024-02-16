"""Tests for the fitting module."""

import json
import os
from pathlib import Path

import pandas as pd
import pytest
import toml

from bibat.fitting import IdataSaveFormat, run_all_inferences, run_inference
from bibat.fitting_mode import (
    kfold_mode,
    posterior_mode,
)
from bibat.inference_configuration import (
    InferenceConfiguration,
    load_inference_configuration,
)
from bibat.prepared_data import PreparedData
from bibat.util import (
    CoordDict,
    DfInPydanticModel,
    StanInputDict,
    returns_stan_input,
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


@pytest.fixture(scope="session")
def stan_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a Stan file."""
    stan_dir = tmp_path_factory.getbasetemp() / "src" / "stan"
    stan_dir.mkdir(parents=True, exist_ok=True)
    file = stan_dir / "multilevel-linear-regression.stan"
    file.write_text(TEST_MODEL)
    return file


class ExamplePreparedData(PreparedData):
    """An example prepared data dataclass."""

    name: str
    coords: CoordDict
    measurements: DfInPydanticModel


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
        mode_options={"kfold": {"n_folds": 2}},
    )
    path = inf_dir / "config.toml"
    with path.open("w") as f:
        toml.dump(ic.model_dump(by_alias=True), f)
    return path


@returns_stan_input
def get_stan_input_interaction(
    prepared_data: ExamplePreparedData,
) -> StanInputDict:
    """General function for creating a Stan input."""
    measurements = prepared_data.measurements
    x_cols = ["x1", "x2", "x1:x2"]
    return {
        "N": len(measurements),
        "N_train": len(measurements),
        "N_test": len(measurements),
        "K": len(x_cols),
        "x": measurements[x_cols].to_numpy().tolist(),
        "y": measurements["y"].tolist(),
        "ix_train": [i + 1 for i in range(len(measurements))],
        "ix_test": [i + 1 for i in range(len(measurements))],
    }


def load_prepared_data(path: Path) -> ExamplePreparedData:
    """Load a prepared data object from a path."""
    with path.open("r") as f:
        return ExamplePreparedData(**json.load(f))


def test_run_inference(
    stan_file: Path,  # noqa: ARG001
    prepared_data_json: Path,
    inference_config: Path,
) -> None:
    """Test a good case of run_inference."""
    ic = load_inference_configuration(inference_config.parent)
    prepared_data = load_prepared_data(prepared_data_json)
    _ = run_inference(
        ic=ic,
        prepared_data=prepared_data,
        fitting_mode_options={"posterior": posterior_mode, "kfold": kfold_mode},
        local_functions={
            "get_stan_input_interaction": get_stan_input_interaction,
        },
    )


def test_run_all_inferences(
    stan_file: Path,  # noqa: ARG001
    prepared_data_json: Path,
    inference_config: Path,
) -> None:
    """Test a good case of run_inference."""
    _ = run_all_inferences(
        inferences_dir=inference_config.parent.parent,
        data_dir=prepared_data_json.parent,
        fitting_mode_options={"posterior": posterior_mode, "kfold": kfold_mode},
        loader=load_prepared_data,
        local_functions={
            "get_stan_input_interaction": get_stan_input_interaction,
        },
        idata_save_format=IdataSaveFormat.zarr,
    )


def test_run_all_inferences_json(
    stan_file: Path,  # noqa: ARG001
    prepared_data_json: Path,
    inference_config: Path,
) -> None:
    """Test a good case of run_inference."""
    _ = run_all_inferences(
        inferences_dir=inference_config.parent.parent,
        data_dir=prepared_data_json.parent,
        fitting_mode_options={"posterior": posterior_mode, "kfold": kfold_mode},
        loader=load_prepared_data,
        local_functions={
            "get_stan_input_interaction": get_stan_input_interaction,
        },
        idata_save_format=IdataSaveFormat.json,
    )
