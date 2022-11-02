"""How to run models in modes.

There should be a ModelMode in AVAILABLE_MODEL_MODES for every model/mode
combination that this analysis considers.

"""

from typing import Callable, Dict, List, Union
from src import stan_input_functions, models
from src.prepared_data import PreparedData
from dataclasses import dataclass


@dataclass
class ModelMode:
    """Information about how to run a model in a mode.

    :param model: an MbagModel object

    :param mode_name: name of the mode, e.g. "prior"

    :param stan_input_function: a function taking in a PreparedData and
    returning a stan input dictionary or a list of these.

    :param multiple_runs: Whether or not the mode involves multiple sampling
    runs.

    """

    model: models.MbagModel
    mode_name: str
    stan_input_function: Callable[[PreparedData], Union[Dict, List[Dict]]]
    multiple_runs: bool


AVAILABLE_MODEL_MODES = [
    ModelMode(
        model=models.MULTILEVEL_LINEAR_REGRESSION,
        mode_name="prior",
        stan_input_function=stan_input_functions.get_stan_input_prior,
        multiple_runs=False,
    ),
    ModelMode(
        model=models.MULTILEVEL_LINEAR_REGRESSION,
        mode_name="posterior",
        stan_input_function=stan_input_functions.get_stan_input_posterior,
        multiple_runs=False,
    ),
    ModelMode(
        model=models.MULTILEVEL_LINEAR_REGRESSION,
        mode_name="kfold",
        stan_input_function=stan_input_functions.get_stan_inputs_10fold,
        multiple_runs=True,
    ),
]
