"""Run all the inferences in the inferences folder."""

from pathlib import Path

from bibat.fitting import run_all_inferences
from bibat.fitting_mode import posterior_mode, prior_mode
from src.data_preparation import load_prepared_data
from src.stan_input_functions import (
    get_stan_input_gpareto,
    get_stan_input_gpareto_fake,
    get_stan_input_normal,
    get_stan_input_normal_fake,
)

HERE = Path(__file__).parent
INFERENCES_DIR = HERE / ".." / "inferences"
PREPARED_DATA_DIR = HERE / ".." / "data" / "prepared"
STAN_DIR = HERE / "stan"
FITTING_MODE_OPTIONS = {"prior": prior_mode, "posterior": posterior_mode}
LOCAL_FUNCTIONS = {
    "get_stan_input_gpareto": get_stan_input_gpareto,
    "get_stan_input_gpareto_fake": get_stan_input_gpareto_fake,
    "get_stan_input_normal": get_stan_input_normal,
    "get_stan_input_normal_fake": get_stan_input_normal_fake,
}

if __name__ == "__main__":
    run_all_inferences(
        INFERENCES_DIR,
        PREPARED_DATA_DIR,
        FITTING_MODE_OPTIONS,
        load_prepared_data,
        LOCAL_FUNCTIONS,
    )
