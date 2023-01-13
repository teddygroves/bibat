"""Run all the configs in the model_configurations folder."""

import os
from typing import Dict

import arviz as az
import cmdstanpy
import numpy as np
import xarray as xr
from sklearn.model_selection import KFold
from src.inference_configuration import (
    AVAILABLE_MODES,
    InferenceConfiguration,
    load_inference_configuration,
)
from src.prepared_data import load_prepared_data
from src.util import CoordDict

RUNS_DIR = "inferences"
STAN_DIR = os.path.join("src", "stan")


def get_sample_kwargs(raw: Dict, mode: str) -> Dict:
    """Get the sampel kwargs for a mode from raw toml."""
    out = {k: v for k, v in raw.items() if k not in AVAILABLE_MODES}
    if mode in raw.keys():
        out |= raw[mode]
    return out


def get_kfold_llik(
    ic: InferenceConfiguration,
    stan_input_base: Dict,
    model: cmdstanpy.CmdStanModel,
    coords: CoordDict,
) -> xr.DataArray:
    """Run k-fold cross-validation and return out-of-sample log likelihood.

    :param ic: InferenceConfiguration, must have non-null field kfold_folds

    :param stan_input_base: stan input dictionary

    :param model: CmdStanModel
    """
    n_folds = ic.kfold_folds
    sample_kwargs = get_sample_kwargs(ic.sample_kwargs, "kfold")
    kf = KFold(n_folds, shuffle=True, random_state=1234)
    lliks_by_fold = []
    full_ix = np.array(stan_input_base["ix_train"])
    for fold, (ix_train, ix_test) in enumerate(kf.split(full_ix)):
        input_dict = stan_input_base | {
            "likelihood": 1,
            "N_train": len(ix_train),
            "N_test": len(ix_test),
            "ix_train": full_ix[ix_train].tolist(),
            "ix_test": full_ix[ix_test].tolist(),
        }
        mcmc = model.sample(data=input_dict, **sample_kwargs)
        llik_fold = mcmc.draws_xr(vars=["llik"])
        # remember the fold
        llik_fold["fold"] = fold
        llik_fold = llik_fold.set_coords("fold")
        # set value of index "chain" to zero to match arviz convention
        llik_fold = llik_fold.assign_coords(
            {"new_chain": ("chain", [0])}
        ).set_index(chain="new_chain")
        # get observation correct
        llik_fold["llik_dim_0"] = np.array(coords["observation"])[ix_test]
        # rename coord "llik_dim_0" to "observation"
        llik_fold = llik_fold.rename({"llik_dim_0": "observation"})
        lliks_by_fold.append(llik_fold["llik"])
    return xr.concat(lliks_by_fold, dim="observation").sortby("observation")


def main():
    """Run the main script."""
    run_dirs = [
        os.path.join(RUNS_DIR, d)
        for d in os.listdir(RUNS_DIR)
        if os.path.isdir(os.path.join(RUNS_DIR, d))
    ]
    for run_dir in sorted(run_dirs):
        ic = load_inference_configuration(os.path.join(run_dir, "config.toml"))
        stan_file = os.path.join(STAN_DIR, ic.stan_file)
        prepared_data_dir = os.path.join(
            "data", "prepared", ic.prepared_data_dir
        )
        model = cmdstanpy.CmdStanModel(
            stan_file=stan_file,
            cpp_options=ic.cpp_options,
            stanc_options=ic.stanc_options,
        )
        prepared_data = load_prepared_data(prepared_data_dir)
        stan_input_base = ic.stan_input_function(prepared_data)
        idata_kwargs = {
            "observed_data": stan_input_base,
            "log_likelihood": "llik",
            "coords": prepared_data.coords,
            "dims": ic.dims,
        }
        for mode, likelihood in [("prior", 0), ("posterior", 1)]:
            if mode in ic.modes:
                sample_kwargs = get_sample_kwargs(ic.sample_kwargs, mode)
                input_dict = stan_input_base | {"likelihood": likelihood}
                idata_kwargs[mode] = model.sample(
                    data=input_dict, **sample_kwargs
                )
                idata_kwargs[f"{mode}_predictive"] = "yrep"
        idata = az.from_cmdstanpy(**idata_kwargs)
        if "kfold" in ic.modes:
            llik_kfold = get_kfold_llik(
                ic, stan_input_base, model, prepared_data.coords
            )
            idata.log_likelihood["llik_kfold"] = llik_kfold
        idata_file = os.path.join(run_dir, "idata.json")
        print(f"Saving idata to {idata_file}")
        idata.to_json(idata_file)


if __name__ == "__main__":
    main()
