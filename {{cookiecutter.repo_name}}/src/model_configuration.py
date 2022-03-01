"""Definition of the ModelConfiguration class."""

import os
from dataclasses import dataclass
from typing import List, Optional


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
    "prior", "posterior" and "cross_validation"

    :param cpp_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    :param stanc_options: valid choices for the `cpp_options` argument to
    CmdStanModel

    """

    name: str
    stan_file: str
    data_dir: str
    sample_kwargs: dict
    modes: List[str]
    cpp_options: Optional[dict] = None
    stanc_options: Optional[dict] = None

    def __post_init__(self) -> None:
        """Handle windows paths correctly"""
        self.stan_file = os.path.join(*self.stan_file.split("/"))
        self.data_dir = os.path.join(*self.data_dir.split("/"))
