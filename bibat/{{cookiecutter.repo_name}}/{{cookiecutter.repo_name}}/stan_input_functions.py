"""Functions for generating input to Stan from prepared data."""


from typing import Any, Callable, Dict, List

import pandas as pd
from stanio.json import process_dictionary
from {{cookiecutter.repo_name}}.data_preparation import PreparedData


def returns_stan_input(func: Callable[[Any], Dict]) -> Callable[[Any], Dict]:
    """Decorate a function so it returns a json-serialisable dictionary."""

    def wrapper(*args, **kwargs):
        return process_dictionary(func(*args, **kwargs))

    return wrapper


@returns_stan_input
def get_stan_input(measurements: pd.DataFrame, x_cols: List[str]) -> Dict:
    """General function for creating a Stan input."""
    return {
        "N": len(measurements),
        "N_train": len(measurements),
        "N_test": len(measurements),
        "K": len(x_cols),
        "x": measurements[x_cols].values.tolist(),
        "y": measurements["y"].tolist(),
        "ix_train": [i + 1 for i in range(len(measurements))],
        "ix_test": [i + 1 for i in range(len(measurements))],
    }


@returns_stan_input
def get_stan_input_interaction(prepared_data: PreparedData) -> Dict:
    """Get a Stan input with an interaction predictor."""
    return get_stan_input(prepared_data.measurements, ["x1", "x2", "x1:x2"])


@returns_stan_input
def get_stan_input_no_interaction(prepared_data: PreparedData) -> Dict:
    """Get a Stan input without an interaction predictor."""
    return get_stan_input(prepared_data.measurements, ["x1", "x2"])
