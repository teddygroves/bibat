"""Functions for generating input to Stan from prepared data."""

import pandas as pd
from src.data_preparation import ExamplePreparedData

from bibat.util import StanInputDict, returns_stan_input


@returns_stan_input
def get_stan_input(
    measurements: pd.DataFrame,
    x_cols: list[str],
) -> StanInputDict:
    """General function for creating a Stan input."""
    return {
        "N": len(measurements),
        "N_train": len(measurements),
        "N_test": len(measurements),
        "K": len(x_cols),
        "x": measurements[x_cols].to_numpy().tolist(),
        "y": measurements["y"].tolist(),
        "ix_train": [i + 1 for i in range(len(measurements))],
        "ix_test": [i + 1 for i in range(len(measurements))],
    }


@returns_stan_input
def get_stan_input_interaction(
    prepared_data: ExamplePreparedData,
) -> StanInputDict:
    """Get a Stan input with an interaction predictor."""
    return get_stan_input(prepared_data.measurements, ["x1", "x2", "x1:x2"])


@returns_stan_input
def get_stan_input_no_interaction(
    prepared_data: ExamplePreparedData,
) -> StanInputDict:
    """Get a Stan input without an interaction predictor."""
    return get_stan_input(prepared_data.measurements, ["x1", "x2"])
