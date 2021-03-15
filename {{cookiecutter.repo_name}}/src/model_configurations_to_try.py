"""Define a list of ModelConfiguration objects called MODEL_CONFIGURATIONS."""

import os
from .util import get_99_pct_params_ln, get_99_pct_params_n
from .model_configuration import ModelConfiguration
from .pandas_to_cmdstanpy import get_stan_input
from .cmdstanpy_to_arviz import get_infd_kwargs


# Location of this file
HERE = os.path.dirname(os.path.abspath(__file__))

# Configure cmdstanpy.CmdStanModel.sample
SAMPLE_KWARGS = dict(
    show_progress=True,
    save_warmup=False,
    iter_warmup=2000,
    iter_sampling=2000,
)

# Configuration of model.stan with an interaction between covariates A and B.
INTERACTION_CONFIG = ModelConfiguration(
    name="interaction",
    stan_file=os.path.join(HERE, "stan", "model.stan"),
    stan_input_function=lambda df: get_stan_input(
        df,
        x_cols=["x1", "x2", "x1:x2"],
        priors={
            "prior_a": get_99_pct_params_n(-1, 1),
            "prior_b": [
                get_99_pct_params_n(-2, 2),
                get_99_pct_params_n(-2, 2),
                get_99_pct_params_n(-1, 1),
            ],
            "prior_sigma": get_99_pct_params_ln(0.4, 5.2),
        },
        likelihood=True,
    ),
    infd_kwargs_function=lambda df: get_infd_kwargs(
        df, ["x1", "x2", "x1:x2"], SAMPLE_KWARGS
    ),
    sample_kwargs=SAMPLE_KWARGS,
)

# Configuration of model.stan with no A:B interaction
NON_INTERACTION_CONFIG = ModelConfiguration(
    name="no interaction",
    stan_file=os.path.join(HERE, "stan", "model.stan"),
    stan_input_function=lambda df: get_stan_input(
        df,
        x_cols=["x1", "x2"],
        priors={
            "prior_a": get_99_pct_params_n(0, 1),
            "prior_b": [
                get_99_pct_params_n(-2, 2),
                get_99_pct_params_n(-2, 2),
            ],
            "prior_sigma": get_99_pct_params_ln(0.4, 5.2),
        },
        likelihood=True,
    ),
    infd_kwargs_function=lambda df: get_infd_kwargs(
        df, ["x1", "x2"], SAMPLE_KWARGS
    ),
    sample_kwargs=SAMPLE_KWARGS,
)

# A list of model configurations to test
MODEL_CONFIGURATIONS = [
    INTERACTION_CONFIG,
    NON_INTERACTION_CONFIG,
]
