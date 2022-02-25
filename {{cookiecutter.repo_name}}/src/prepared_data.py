""""Class defining what prepared data looks like.

It bundles some logic for creating stan inputs for all 

"""


from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

import pandas as pd
from sklearn.model_selection import KFold

from src.util import CoordDict, StanInput


@dataclass
class PreparedData:
    name: str
    coords: CoordDict
    dims: Dict[str, Any]
    measurements: pd.DataFrame
    number_of_cv_folds: int
    stan_input_function: Callable
    stan_input_prior: StanInput = field(init=False)
    stan_input_posterior: StanInput = field(init=False)
    stan_inputs_cv: List[StanInput] = field(init=False)

    def __post_init__(self):
        ix_all = list(range(len(self.measurements)))
        self.stan_input_prior, self.stan_input_posterior = (
            self.stan_input_function(
                measurements=self.measurements,
                train_ix=ix_all,
                test_ix=ix_all,
                likelihood=likelihood,
            )
            for likelihood in (False, True)
        )
        stan_inputs_cv = []
        kf = KFold(self.number_of_cv_folds, shuffle=True)
        for train, test in kf.split(self.measurements):
            stan_inputs_cv.append(
                self.stan_input_function(
                    measurements=self.measurements,
                    likelihood=True,
                    train_ix=list(train),
                    test_ix=list(test),
                )
            )
        self.stan_inputs_cv = stan_inputs_cv
