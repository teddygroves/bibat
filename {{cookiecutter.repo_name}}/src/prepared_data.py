""""Class defining what prepared data looks like."""


from dataclasses import dataclass
from typing import Any, Callable, Dict

import pandas as pd

from src.util import CoordDict, StanInput


@dataclass
class PreparedData:
    name: str
    coords: CoordDict
    dims: Dict[str, Any]
    measurements: pd.DataFrame
    number_of_cv_folds: int
    stan_input_function: Callable[..., StanInput]
