"""Run all the inferences in the inferences folder."""

from pathlib import Path

from src.data_preparation import load_prepared_data
from src.stan_input_functions import (
    get_stan_input_interaction,
    get_stan_input_no_interaction,
)

from bibat import kfold_mode, posterior_mode, prior_mode
from bibat.fitting import run_all_inferences

HERE = Path(__file__).parent
INFERENCES_DIR = HERE / ".." / "inferences"
PREPARED_DATA_DIR = HERE / ".." / "data" / "prepared"
STAN_DIR = HERE / "stan"
FITTING_MODE_OPTIONS = {
    "prior": prior_mode,
    "posterior": posterior_mode,
    "kfold": kfold_mode,
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
        load_prepared_data,
        LOCAL_FUNCTIONS,
    )
