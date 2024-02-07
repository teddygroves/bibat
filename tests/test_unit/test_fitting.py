"""Tests for the fitting module."""

import json
import os
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import pytest
import toml
from pydantic import ConfigDict, field_serializer, field_validator

from bibat.fitting import run_inference
from bibat.fitting_mode import prior_mode
from bibat.inference_configuration import InferenceConfiguration
from bibat.prepared_data import PreparedData
from bibat.util import CoordDict, StanInputDict, returns_stan_input


@pytest.fixture(scope="session")
def stan_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a Stan file."""
    stan_dir = tmp_path_factory.getbasetemp() / "src" / "stan"
    stan_dir.mkdir(parents=True, exist_ok=True)
    file = stan_dir / "multilevel-linear-regression.stan"
    file.write_text(
        "data {int N; vector[N] y;}"
        "generated quantities {vector[N] yrep;"
        "for (n in 1:N) yrep[n] = normal_rng(0, 1);}",
    )
    return file


class ExamplePreparedData(PreparedData):
    """An example prepared data dataclass."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    coords: CoordDict
    measurements: Any

    @field_validator("measurements")
    def validate_measurements(
        cls,  # noqa: N805, ANN101
        v: Any,  # noqa: ANN401
    ) -> pd.DataFrame:
        """Validate the measurements table."""
        if isinstance(v, str):
            v = pd.read_json(StringIO(v))
        return v

    @field_serializer("measurements")
    def serialize_measurements(
        self,  # noqa: ANN101
        measurements: pd.DataFrame,
        _info,  # noqa: ANN001
    ) -> str | None:
        """Convert the measurements table to json."""
        return measurements.to_json()


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
        prepared_data_dir="interaction",
        stan_file="multilevel-linear-regression.stan",
        stan_input_function="get_stan_input_interaction",
        modes=["prior"],
        sample_kwargs={"chains": 1, "iter_warmup": 2, "iter_sampling": 2},
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
    _ = run_inference(
        inference_dir=inference_config.parent,
        data_dir=prepared_data_json.parent,
        fitting_mode_options={"prior": prior_mode},
        loader=load_prepared_data,
        local_functions={
            "get_stan_input_interaction": get_stan_input_interaction,
        },
    )
