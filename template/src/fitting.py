"""Run all the inferences in the inferences folder."""

import os
from pathlib import Path

import arviz as az
import cmdstanpy
from src.data_preparation import ExamplePreparedData
from src.stan_input_functions import (
    get_stan_input_interaction,
    get_stan_input_no_interaction,
)

from bibat.fitting import run_all_inferences
from bibat.fitting_mode import posterior_mode, prior_mode
from bibat.inference_configuration import load_inference_configuration

HERE = Path(__file__).parent
INFERENCES_DIR = HERE / ".." / "inferences"
PREPARED_DATA_DIR = HERE / ".." / "data" / "prepared"
STAN_DIR = HERE / "stan"
FITTING_MODE_OPTIONS = {
    "prior": prior_mode,
    "posterior": posterior_mode,
    # "kfold": kfold_mode,
}
PREPARED_DATA_OPTIONS = {
    "interaction": ExamplePreparedData,
    "no_interaction": ExamplePreparedData,
    "fake_interaction": ExamplePreparedData,
}
LOCAL_FUNCTIONS = {
    "get_stan_input_interaction": get_stan_input_interaction,
    "get_stan_input_no_interaction": get_stan_input_no_interaction,
}

if __name__ == "__main__":
    run_all_inferences(
        INFERENCES_DIR,
        PREPARED_DATA_DIR,
        FITTING_MODE_OPTIONS,
        PREPARED_DATA_OPTIONS,  # type: ignore
        LOCAL_FUNCTIONS,
    )
