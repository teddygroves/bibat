"""Definition of the ModelConfiguration class."""

import os
from dataclasses import dataclass
from typing import List, Optional

from src.model_modes import AVAILABLE_MODEL_MODES
from src.models import AVAILABLE_MODELS


@dataclass
class ModelConfiguration:
    """Container for a path to a Stan model and some configuration.

    For example, you may want to compare how well two stan programs fit the
    same data, or how well the same model fits the data with different
    covariates.

    :param name: string name identifying the model configuration

    :param stan_file: Path to a Stan program, with "/" even on windows

    :param data_dir: Path to a directory containing prepared data

    :param sample_kwargs: dictionary of keyword arguments to
    cmdstanpy.CmdStanModel.sample.

    :param modes: which modes to run the model in. Choose one or more of
    "prior", "posterior" and "kfold"

    :param cpp_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    :param stanc_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    """

    name: str
    model_file: str
    prepared_data_dir: str
    sample_kwargs: dict
    modes: List[str]
    cpp_options: Optional[dict] = None
    stanc_options: Optional[dict] = None

    def __post_init__(self) -> None:
        """Validate provided modes"""
        available_model_files = [m.stan_file for m in AVAILABLE_MODELS]
        available_mode_names = [
            mm.mode_name
            for mm in AVAILABLE_MODEL_MODES
            if mm.model.stan_file == self.model_file
        ]
        if self.model_file not in available_model_files:
            raise ValueError(
                f"{self.model_file} not in available model files:"
                f" {available_model_files}"
            )
        for mode in self.modes:
            if mode not in available_mode_names:
                raise ValueError(
                    f"{mode} not in available mode names"
                    f" for model {self.model_file}:"
                    f" {available_mode_names}"
                )
