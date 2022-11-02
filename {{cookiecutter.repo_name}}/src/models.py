"""Information about models.

All models that are used in this analysis should appear in the list
AVAILABLE_MODELS.

There should not be more than one model in AVAILABLE_MODELS with the same
stan_file attribute.

"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MbagModel:
    """Information about an mbag model.

    :param stan_file: file name of the stan file defining the model. This file
    should be in the folder src/stan.

    :param dims: Dictionary mapping model parameters to lists of coordinate
    names.

    """

    stan_file: str
    dims: Dict[str, List[str]]


MULTILEVEL_LINEAR_REGRESSION = MbagModel(
    stan_file="multilevel-linear-regression.stan",
    dims={
        "b": ["covariate"],
        "y": ["observation"],
    },
)

AVAILABLE_MODELS = [MULTILEVEL_LINEAR_REGRESSION]
