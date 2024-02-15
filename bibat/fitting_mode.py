"""A general definition of a fitting mode, plus some mode instances."""

from __future__ import annotations

from collections.abc import Callable  # noqa: TCH003
from enum import Enum
from pathlib import Path

import numpy as np
import xarray as xr
from cmdstanpy import CmdStanMCMC, CmdStanModel
from pydantic import BaseModel
from sklearn.model_selection import KFold

from bibat.inference_configuration import InferenceConfiguration  # noqa: TCH001
from bibat.prepared_data import PreparedData  # noqa: TCH001


class IdataTarget(str, Enum):
    """An enum for choosing the group that a fitting mode writes to."""

    prior = "prior"
    posterior = "posterior"
    log_likelihood = "log_likelihood"


class FittingMode(BaseModel):
    """A way of fitting a statistical model.

    Inferences can be configured to use any of the fitting modes defined here
    by including them by name in the top-level list 'modes'. For example:

    ```toml
      ...
      modes = ['prior', 'posterior', 'kfold']
      ...
    ```

    :param name: A string identifying the fitting mode

    :param idata_target: A string identifying the
    [`InferenceData`](https://python.arviz.org/en/stable/api/inference_data.html)
    group that the mode writes to. Must be one of "prior", "posterior" or
    "log_likelihood".

    :param fit: A function that takes in an `InferenceConfiguration` object, a
    `PreparedData` object and a dictionary of local functions, and returns
    either a CmdStanMCMC object (if the `idata_target` is "prior" or
    "posterior") or an xarray DataArray object (if the `idata_target` is
    "log_likelihood")
    """

    name: str
    idata_target: IdataTarget
    fit: Callable[
        [InferenceConfiguration, PreparedData, dict[str, Callable]],
        CmdStanMCMC | xr.DataArray,
    ]


def sample_hmc_prior(
    ic: InferenceConfiguration,
    data: PreparedData,
    local_functions: dict[str, Callable],
) -> CmdStanMCMC:
    """Run hmc in prior mode."""
    sif = local_functions[ic.stan_input_function]
    input_dict = sif(data) | {"likelihood": 0}
    stan_file = Path("src") / "stan" / ic.stan_file
    model = CmdStanModel(stan_file=stan_file)
    sample_kwargs = ic.sample_kwargs
    if ic.mode_options is not None and "prior" in ic.mode_options:
        sample_kwargs |= ic.mode_options["prior"]
    return model.sample(input_dict, **sample_kwargs)


def sample_hmc_posterior(
    ic: InferenceConfiguration,
    data: PreparedData,
    local_functions: dict[str, Callable],
) -> CmdStanMCMC:
    """Run hmc in posterior mode."""
    sif = local_functions[ic.stan_input_function]
    input_dict = sif(data) | {"likelihood": 1}
    stan_file = Path("src") / "stan" / ic.stan_file
    model = CmdStanModel(stan_file=stan_file)
    sample_kwargs = ic.sample_kwargs
    if ic.mode_options is not None and "posterior" in ic.mode_options:
        sample_kwargs |= ic.mode_options["posterior"]
    return model.sample(input_dict, **sample_kwargs)


def sample_hmc_kfold(
    ic: InferenceConfiguration,
    data: PreparedData,
    local_functions: dict[str, Callable],
) -> xr.DataArray:
    """Do k-fold cross validation, given a CmdStanModel, some data and config.

    :param model: a CmdStanModel. It must have a data variables called
    'likelihood', 'N_train', 'N_test', 'ix_train' and 'ix_test'.

    :param input_dict: a Stan input dictionary. It doesn't need to have any of
    the required variables set (they will be overwritten if they are set).

    :param kwargs: dictionary with an entry for 'n_folds' that specifies the
    value of k for k-fold cross-validation, plus keyword arguments for
    CmdStanModel.sample

    """
    k = ic.mode_options["kfold"]["n_folds"]
    kf = KFold(k, shuffle=True, random_state=1234)
    sif = local_functions[ic.stan_input_function]
    input_dict = sif(data) | {"likelihood": 1}
    stan_file = Path("src") / "stan" / ic.stan_file
    model = CmdStanModel(stan_file=stan_file)
    sample_kwargs = ic.sample_kwargs | {
        k: v for k, v in ic.mode_options["kfold"].items() if k != "n_folds"
    }
    lliks_by_fold = []
    full_ix = np.array(input_dict["ix_train"])
    for fold, (ix_train, ix_test) in enumerate(kf.split(full_ix)):
        input_dict_fold = input_dict | {
            "likelihood": 1,
            "N_train": len(ix_train),
            "N_test": len(ix_test),
            "ix_train": full_ix[ix_train].tolist(),
            "ix_test": full_ix[ix_test].tolist(),
        }
        mcmc = model.sample(data=input_dict_fold, **sample_kwargs)
        llik_fold = mcmc.draws_xr(vars=["llik"])
        # remember the fold
        llik_fold["fold"] = fold
        llik_fold = llik_fold.set_coords("fold")
        # set value of index "chain" to zero to match arviz convention
        llik_fold = llik_fold.assign_coords(
            {"new_chain": ("chain", [0])},
        ).set_index(
            chain="new_chain",
        )
        lliks_by_fold.append(llik_fold["llik"])
    return xr.concat(lliks_by_fold, dim="llik_dim_0").sortby("llik_dim_0")


prior_mode = FittingMode(
    name="prior",
    idata_target=IdataTarget.prior,
    fit=sample_hmc_prior,
)
posterior_mode = FittingMode(
    name="posterior",
    idata_target=IdataTarget.posterior,
    fit=sample_hmc_posterior,
)
kfold_mode = FittingMode(
    name="kfold",
    idata_target=IdataTarget.log_likelihood,
    fit=sample_hmc_kfold,
)
