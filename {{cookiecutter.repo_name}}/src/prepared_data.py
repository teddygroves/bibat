from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import pandas as pd

from .util import CoordDict, StanInput


@dataclass
class PreparedData:
    name: str
    df: pd.DataFrame
    coords: CoordDict
    dims: Dict[str, Any]
    stan_input_prior: StanInput
    stan_input_posterior: StanInput
    stan_inputs_cv: List[StanInput]


PrepareDataFunction = Callable[
    [str, pd.DataFrame, List[str], int], PreparedData
]
