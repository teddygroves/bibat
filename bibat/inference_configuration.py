"""Definition of the InferenceConfiguration class."""

import os
from pathlib import Path
from typing import Callable, Dict, List, Optional

import toml
from pydantic import BaseModel, Field, field_validator, model_validator

DEFAULT_DIMS = {"llik": ["observation"], "yrep": ["observation"]}
DEFAULT_SAMPLE_KWARGS = {"show_progress": False}


class InferenceConfiguration(BaseModel):
    """Container for a path to a Stan model and some configuration.

    For example, you may want to compare how well two stan programs fit the
    same data, or how well the same model fits the data with different
    covariates.

    :param name: string name identifying the model configuration

    :param stan_file: Path to a Stan program, with "/" even on windows

    :param prepared_data_dir: Path to a directory containing prepared data

    :param stan_input_function: name of a function from src.stan_input_functions
    used to get a Stan input dictionary from a PreparedData object.

    :param sample_kwargs: dictionary of keyword arguments to
    cmdstanpy.CmdStanModel.sample.

    :param modes: which modes to run the model in. Choose one or more of the
    AVAILABLE_MODES.

    :param dims: map from parameter names to lists of coordinate names. See the
    field names of the file "coords.json" in the prepared_data_dir for possible
    coordinate names.

    :param cpp_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    :param stanc_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    """

    name: str
    stan_file: str
    prepared_data_dir: str
    stan_input_function: str
    fitting_modes: List[str] = Field(alias="modes")
    sample_kwargs: dict = Field(default_factory=lambda: DEFAULT_SAMPLE_KWARGS)
    dims: Dict[str, List[str]] = Field(default_factory=lambda: DEFAULT_DIMS)
    mode_options: Optional[Dict[str, dict]] = None
    cpp_options: Optional[dict] = None
    stanc_options: Optional[dict] = None

    @model_validator(mode="after")
    def check_folds(cls, m: "InferenceConfiguration"):
        """Check that there is a number of folds if required."""
        if any(m == "kfold" for m in m.fitting_modes):
            if m.mode_options is None:
                raise ValueError(
                    "Mode 'kfold' requires a mode_options.kfold table."
                )
            if "kfold" not in m.mode_options.keys():
                raise ValueError(
                    "Mode 'kfold' requires a mode_options.kfold table."
                )
            elif "n_folds" not in m.mode_options["kfold"].keys():
                raise ValueError("Set 'n_folds' field in kfold mode options.")
            else:
                assert int(m.mode_options["kfold"]["n_folds"]), (
                    f"Could not coerce n_folds choice "
                    f"{m.mode_options['kfold']['n_folds']} to int."
                )
        return m

    @field_validator("stan_file")
    def check_stan_file_exists(cls, v):
        """Check that the stan file exists."""
        here = Path(".")
        stan_dir = here / "src" / "stan"
        if not os.path.exists(stan_dir / v):
            raise ValueError(f"{v} is not a file in {stan_dir}.")
        return v


def load_inference_configuration(path: Path):
    """Load an inference configuration object from a toml file.

    :param path: Path to directory containing a suitable config.toml file

    """
    kwargs = toml.load(path / "config.toml")
    for k, default in zip(
        ["dims", "sample_kwargs"], [DEFAULT_DIMS, DEFAULT_SAMPLE_KWARGS]
    ):
        if k in kwargs.keys():
            kwargs[k] = default | kwargs[k]
    return InferenceConfiguration(**kwargs)
