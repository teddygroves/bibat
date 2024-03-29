"""Unit tests for the InferenceConfiguration class."""

import os
from pathlib import Path

import pytest
import toml

from bibat.inference_configuration import (
    InferenceConfiguration,
    load_inference_configuration,
)

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


@pytest.fixture(scope="session")
def stan_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a Stan file."""
    stan_dir = tmp_path_factory.getbasetemp() / "src" / "stan"
    stan_dir.mkdir(parents=True, exist_ok=True)
    file = stan_dir / "multilevel-linear-regression.stan"
    file.write_text("data {int N;}")
    return file


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


def test_model_configuration_good_modes(stan_file: Path) -> None:
    """Check that an inference configuration with good modes initialises."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        mode_options={"kfold": {"n_folds": 10}},
        modes=MODES_GOOD,
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_bad_modes(stan_file: Path) -> None:
    """Check that an inference configuration with bad modes fails."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_BAD,
        mode_options={"kfold": {"n_folds": 10}},
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_no_mode_options_kfold(stan_file: Path) -> None:
    """Check that an inference configuration with no kfold options fails."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        mode_options={},  # This is the bad bit!
        modes=MODES_GOOD,  # it would be ok if 'kfold' weren't in here.
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_kfold_not_in_mode_options(stan_file: Path) -> None:
    """Check that an inference configuration with no kfold options fails."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        mode_options={"bla": {"something": "?"}},  # This is the bad bit!
        modes=MODES_GOOD,  # it would be ok if 'kfold' weren't in here.
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_no_k(stan_file: Path) -> None:
    """Check that an inference configuration with no kfold options fails."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        mode_options={"kfold": {}},  # This is the bad bit!
        modes=MODES_GOOD,  # it would be ok if 'kfold' weren't in here.
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_bad_k(stan_file: Path) -> None:
    """Check that an inference configuration with no kfold options fails."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        mode_options={"kfold": {"n_folds": "!"}},  # This is the bad bit!
        modes=MODES_GOOD,  # it would be ok if 'kfold' weren't in here.
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_no_stan_file(stan_file: Path) -> None:
    """Check that an inference configuration with absent Stan file fails."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="XXXXXXXXXXXXXXXXXXXX",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="get_stan_input_interaction",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        mode_options={"kfold": {"n_folds": 10}},
        cpp_options=None,
        stanc_options=None,
    )


@pytest.mark.xfail()
def test_model_configuration_no_stan_input_function(stan_file: Path) -> None:
    """Check that absent Stan input function causes failure."""
    os.chdir(stan_file.parent.parent.parent)
    _ = InferenceConfiguration(
        name="my_mc",
        stan_file="multilevel-linear-regression.stan",
        prepared_data=str(Path("hi") / "hello" / "hey"),
        stan_input_function="XXXXXXXXXXXXXXXXXX",
        sample_kwargs=SAMPLE_KWARGS,
        modes=MODES_GOOD,
        mode_options={"kfold": {"n_folds": 10}},
        cpp_options=None,
        stanc_options=None,
    )


def test_load_inference_configuration(inference_config: Path) -> None:
    """Test the function load_inference_configuration."""
    _ = load_inference_configuration(inference_config.parent)
