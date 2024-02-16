"""The inference_configuration module.

This module provides the class InferenceConfiguration and the function
`load_inference_configuration`.

"""

from __future__ import annotations

from pathlib import Path

import toml
from pydantic import BaseModel, Field, field_validator, model_validator

DEFAULT_DIMS = {"llik": ["observation"], "yrep": ["observation"]}
DEFAULT_SAMPLE_KWARGS = {"show_progress": False}


class InferenceConfiguration(BaseModel):
    """Configuration for a statistical inference.

    :param name: A name identifying the model configuration

    :param stan_file: Path to a Stan program, with "/" even on windows

    :param prepared_data: Name of the prepared data for this inference

    :param stan_input_function: name of a function from src.stan_input_functions
    used to get a Stan input dictionary from a PreparedData object.

    :param sample_kwargs: dictionary of keyword arguments to
    cmdstanpy.CmdStanModel.sample.

    :param modes: which modes to run the model in. Choose one or more of the
    AVAILABLE_MODES.

    :param dims: map from parameter names to lists of coordinate names.

    :param cpp_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    :param stanc_options: valid choices for the `cpp_options` argument to
    CmdStanModel
    """

    name: str
    stan_file: str
    prepared_data: str
    stan_input_function: str
    fitting_modes: list[str] = Field(alias="modes")
    sample_kwargs: dict = Field(default_factory=lambda: DEFAULT_SAMPLE_KWARGS)
    dims: dict[str, list[str]] = Field(default_factory=lambda: DEFAULT_DIMS)
    mode_options: dict[str, dict] = Field(default_factory=dict)
    cpp_options: dict | None = None
    stanc_options: dict | None = None

    @model_validator(mode="after")
    def check_folds(self: InferenceConfiguration) -> InferenceConfiguration:
        """Check that there is a number of folds if required."""
        if any(m == "kfold" for m in self.fitting_modes):
            if self.mode_options == {}:
                msg = "Mode 'kfold' requires a mode_options.kfold table."
                raise ValueError(
                    msg,
                )
            if "kfold" not in self.mode_options:
                msg = "Mode 'kfold' requires a mode_options.kfold table."
                raise ValueError(
                    msg,
                )
            if "n_folds" not in self.mode_options["kfold"]:
                msg = "Set 'n_folds' field in kfold mode options."
                raise ValueError(msg)
            mo = self.mode_options["kfold"]["n_folds"]
            if isinstance(mo, str) and not mo.isdigit():
                msg = (
                    f"Could not coerce n_folds choice "
                    f"{self.mode_options['kfold']['n_folds']} to int."
                )
                raise ValueError(msg)
        return self

    @field_validator("stan_file")
    @classmethod
    def check_stan_file_exists(
        cls: type[InferenceConfiguration],
        v: str,
    ) -> str:
        """Check that the stan file exists."""
        stan_dir = Path("src") / "stan"
        file = stan_dir / v
        if not file.exists():
            msg = f"{v} is not a file in {stan_dir}."
            raise ValueError(msg)
        return v


def load_inference_configuration(path: Path) -> InferenceConfiguration:
    """Load an inference configuration object from a toml file.

    :param path: Path to directory containing a suitable config.toml file

    """
    kwargs = toml.load(path / "config.toml")
    for k, default in zip(
        ["dims", "sample_kwargs"],
        [DEFAULT_DIMS, DEFAULT_SAMPLE_KWARGS],
        strict=True,
    ):
        if k in kwargs:
            kwargs[k] = default | kwargs[k]
    return InferenceConfiguration(**kwargs)
