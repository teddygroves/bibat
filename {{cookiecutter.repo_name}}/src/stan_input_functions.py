"""Functions for generating input to Stan from prepared data."""


import pandas as pd
from sklearn.model_selection import KFold

from typing import List, Dict, Optional

from src.prepared_data import PreparedData


def get_stan_input(
    measurements: pd.DataFrame,
    x_cols: List[str],
    likelihood: bool,
    train_ix: List[int],
    test_ix: List[int],
) -> Dict:
    """General function for creating a Stan input."""
    return {
        "N": len(measurements),
        "N_train": len(train_ix),
        "N_test": len(test_ix),
        "K": len(x_cols),
        "x": measurements[x_cols].values.tolist(),
        "y": measurements["y"].tolist(),
        "likelihood": int(likelihood),
        "ix_train": [i + 1 for i in train_ix],
        "ix_test": [i + 1 for i in test_ix],
    }


def get_stan_input_prior(prepared_data: PreparedData) -> Dict:
    """Get a Stan input from a PreparedData, for prior mode."""
    ix = list(range(len(prepared_data.measurements)))
    return get_stan_input(
        measurements=prepared_data.measurements,
        x_cols=prepared_data.coords["covariate"],
        likelihood=False,
        train_ix=ix,
        test_ix=ix,
    )


def get_stan_input_posterior(prepared_data: PreparedData) -> Dict:
    """Get a Stan input from a PreparedData, for posterior mode."""
    ix = list(range(len(prepared_data.measurements)))
    return get_stan_input(
        measurements=prepared_data.measurements,
        x_cols=prepared_data.coords["covariate"],
        likelihood=True,
        train_ix=ix,
        test_ix=ix,
    )


def get_stan_inputs_10fold(prepared_data: PreparedData) -> List[Dict]:
    """Get a list of Stan inputs from a PreparedData, for kfold mode."""

    kf = KFold(10, shuffle=True, random_state=1234)
    return [
        get_stan_input(
            measurements=prepared_data.measurements,
            x_cols=prepared_data.coords["covariate"],
            likelihood=True,
            train_ix=list(map(int, ix_train)),
            test_ix=list(map(int, ix_test)),
        )
        for ix_train, ix_test in kf.split(prepared_data.measurements)
    ]
