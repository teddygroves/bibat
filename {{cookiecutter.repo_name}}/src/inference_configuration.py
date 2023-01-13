"""Definition of the ModelConfiguration class."""

import os
from typing import Callable, Dict, List, Optional

import toml
from pydantic import BaseModel, Field, root_validator, validator
from src import stan_input_functions

AVAILABLE_MODES = ["prior", "posterior", "kfold"]
HERE = os.path.dirname(os.path.abspath(__file__))
STAN_DIR = os.path.join(HERE, "stan")
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

    :param stan_input_function: function from src.stan_input_functions used to
    get a Stan input dictionary from a PreparedData object.

    :param sample_kwargs: dictionary of keyword arguments to
    cmdstanpy.CmdStanModel.sample.

    :param modes: which modes to run the model in. Choose one or more of the
    AVAILABLE_MODES.

    :param dims: map from parameter names to lists of coordinate names. See the
    field names of the file "coords.json" in the prepared_data_dir for possible
    coordinate names.

    :param kfold_folds: How many kfold folds to run

    :param cpp_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    :param stanc_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    """

    name: str
    stan_file: str
    prepared_data_dir: str
    modes: List[str]
    stan_input_function: Callable
    sample_kwargs: dict = Field(default_factory=lambda: DEFAULT_SAMPLE_KWARGS)
    dims: Dict[str, List[str]] = Field(default_factory=lambda: DEFAULT_DIMS)
    kfold_folds: Optional[int] = None
    cpp_options: Optional[dict] = None
    stanc_options: Optional[dict] = None

    def __init__(self, **data):
        """Initialise an InferenceConfiguration."""
        data["stan_input_function"] = getattr(
            stan_input_functions, data["stan_input_function"]
        )
        super().__init__(**data)

    @root_validator
    def check_folds(cls, values):
        """Check that there is a number of folds if required."""
        if "kfold" in values["modes"] and values["kfold_folds"] is None:
            raise ValueError("Set kfold_folds in order to run in kfold mode.")
        return values

    @validator("stan_file")
    def check_stan_file_exists(cls, v):
        """Check that the stan file exists."""
        if not os.path.exists(os.path.join("src", "stan", v)):
            raise ValueError(f"{v} is not a file in src/stan.")
        return v

    @validator("modes")
    def check_modes(cls, v):
        """Check that the provided modes exist."""
        for mode in v:
            if mode not in AVAILABLE_MODES:
                raise ValueError(
                    f"{mode} not in available modes: {AVAILABLE_MODES}."
                )
        return v


def load_inference_configuration(path: str):
    """Load an inference configuration object from a toml file."""
    kwargs = toml.load(path)
    for k, default in zip(
        ["dims", "sample_kwargs"], [DEFAULT_DIMS, DEFAULT_SAMPLE_KWARGS]
    ):
        if k in kwargs.keys():
            kwargs[k] = default | kwargs[k]
    return InferenceConfiguration(**kwargs)
