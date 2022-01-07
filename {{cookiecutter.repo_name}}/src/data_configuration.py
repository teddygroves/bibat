from dataclasses import dataclass, field
from typing import Callable, List

import pandas as pd


@dataclass
class DataConfiguration:
    name: str
    raw_df: str
    xcols: List[str]
    prepare_data_function: str
    n_folds: int = 5
