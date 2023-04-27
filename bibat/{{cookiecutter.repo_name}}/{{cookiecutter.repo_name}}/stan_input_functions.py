"""Functions for generating input to Stan from prepared data."""


from typing import Dict, List

import pandas as pd
from {{cookiecutter.repo_name}}.data_preparation import PreparedData


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


def get_stan_input_interaction(prepared_data: PreparedData) -> Dict:
    """Get a Stan input with an interaction predictor."""
    return get_stan_input(prepared_data.measurements, ["x1", "x2", "x1:x2"])


def get_stan_input_no_interaction(prepared_data: PreparedData) -> Dict:
    """Get a Stan input without an interaction predictor."""
    return get_stan_input(prepared_data.measurements, ["x1", "x2"])
