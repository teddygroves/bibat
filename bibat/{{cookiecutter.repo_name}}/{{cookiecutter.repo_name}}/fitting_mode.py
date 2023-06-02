"""A general definition of a fitting mode, plus some mode instances."""

import textwrap
from enum import Enum
from typing import Callable, Dict, Union

import numpy as np
import xarray as xr
from cmdstanpy import CmdStanMCMC, CmdStanModel
from pydantic import BaseModel
from sklearn.model_selection import KFold


class IdataTarget(str, Enum):
    """An enum for choosing the group that a fitting mode writes to."""

    prior = "prior"
    posterior = "posterior"
    log_likelihood = "log_likelihood"

class FittingMode(BaseModel):
    """A way of fitting a statistical model.

    Each fitting mode has a name, an 'idata_target', i.e. the group that this
    mode will create in the output InferenceData, and a function that performs
    the fitting.

    Inferences can be configured to use any of the fitting modes defined here
    by including them by name in the top-level list 'modes'. For example:

      ...
      modes = ['prior', 'posterior', 'kfold']
      ...

    The idata_target must be one out of 'prior', 'posterior' and
    'log_likelihood', and specifies which out of these InferenceData groups the
    output will be written to.

    Each fitting mode's fit function must match the signature specified in the
    FittingMode class. This can also be changed, but must agree with the
    'sample' module.


    """
    name: str
    idata_target: IdataTarget
    fit: Callable[[CmdStanModel, Dict, Dict[str, str]], Union[CmdStanMCMC, xr.Dataset]]


def fit_prior(model: CmdStanModel, input_dict: dict, kwargs) -> CmdStanMCMC:
    """Create a CmdStanMCMC from a model, data and config, in prior mode.

    :param model: a CmdStanModel. It must have a data variable called
    'likelihood': setting this variable to 0 should trigger prior mode,
    typically by causing the code that performs likelihood evaluations not to
    run.

    :param input_dict: a Stan input dictionary. It doesn't need to have a
    'likelihood' entry: if it does, it will be overwritten.

    :param kwargs: keyword arguments for CmdStanModel.sample

    """
    input_dict_final = input_dict | {"likelihood": 0}
    return model.sample(input_dict_final, **kwargs)


def fit_posterior(model: CmdStanModel, input_dict: dict, kwargs) -> CmdStanMCMC:
    """Create a CmdStanMCMC from a model, data and config, in posterior mode.

    :param model: a CmdStanModel. It must have a data variable called
    'likelihood': setting this variable to 1 should trigger posterior mode,
    typically by causing the code that performs likelihood evaluations to run.

    :param input_dict: a Stan input dictionary. It doesn't need to have a
    'likelihood' entry: if it does, it will be overwritten.

    :param kwargs: keyword arguments for CmdStanModel.sample
    """
    input_dict_final = input_dict | {"likelihood": 1}
    return model.sample(input_dict_final, **kwargs)


def fit_kfold(model: CmdStanModel, input_dict :dict, kwargs) -> xr.DataArray:
    """Do k-fold cross validation, given a CmdStanModel, some data and config.

    :param model: a CmdStanModel. It must have a data variables called
    'likelihood', 'N_train', 'N_test', 'ix_train' and 'ix_test'.

    :param input_dict: a Stan input dictionary. It doesn't need to have any of
    the required variables set (they will be overwritten if they are set).

    :param kwargs: dictionary with an entry for 'n_folds' that specifies the
    value of k for k-fold cross-validation, plus keyword arguments for
    CmdStanModel.sample

    """
    if "n_folds" not in kwargs.keys():
        msg = textwrap.dedent(
            """
            kfold mode requires a set number of folds. Ensure that the
            inference configuration file contains a table called
            'mode_options.kfold' and that this table has an integer-valued
            field called 'n_folds'.
            """
        )
        raise ValueError(msg)
    else:
        n_folds = int(kwargs["n_folds"])
    sample_kwargs = {k: v for k, v in kwargs.items() if k != "n_folds"}
    kf = KFold(n_folds, shuffle=True, random_state=1234)
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
            {"new_chain": ("chain", [0])}
        ).set_index(chain="new_chain")
        lliks_by_fold.append(llik_fold["llik"])
    return xr.concat(lliks_by_fold, dim="llik_dim_0").sortby("llik_dim_0")

prior_mode = FittingMode(name="prior", idata_target="prior", fit=fit_prior)
posterior_mode = FittingMode(
    name="posterior", idata_target="posterior", fit=fit_posterior
)
kfold_mode = FittingMode(name="kfold", idata_target="log_likelihood", fit=fit_kfold)
