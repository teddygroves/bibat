"""Definition of the ModelConfiguration class."""

from dataclasses import dataclass
from typing import Callable, Dict
import pandas as pd


@dataclass
class ModelConfiguration:
    """Container for a path to a Stan model and some configuration.

    For example, you may want to compare how well two stan programs fit the
    same data, or how well the same model fits the data with different
    covariates.

    :param name: string name identifying the model configuration

    :param stan_file: Path to a Stan program

    :param stan_input_function: Function taking in a pd.DataFrame of
    measurements and returning a dictionary that can be used as input to
    cmdstanpy.CmdStanModel.sample.

    :param infd_kwargs_function: Function taking in a pd.DataFrame of
    measurements and returning a dictionary of keyword arguments to
    arviz.from_cmdstanpy.

    :param sample_kwargs: dictionary of keyword arguments to
    cmdstanpy.CmdStanModel.sample.

    """

    name: str
    stan_file: str
    stan_input_function: Callable[[pd.DataFrame], Dict]
    infd_kwargs_function: Callable[[pd.DataFrame], Dict]
    sample_kwargs: Dict
