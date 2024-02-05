import json
import os
from pathlib import Path
from typing import Callable, Mapping

import arviz as az

from bibat.fitting_mode import FittingMode
from bibat.inference_configuration import load_inference_configuration
from bibat.prepared_data import PreparedData


def run_all_inferences(
    inferences_dir: Path,
    data_dir: Path,
    fitting_mode_options: dict[str, FittingMode],
    preprared_data_options: Mapping[str, type[PreparedData]],
    local_functions: dict[str, Callable],
):
    """Fit all inferences in all modes."""
    inference_dirs = inferences_dir.iterdir()
    for dir in sorted(inference_dirs):
        run_inference(
            dir,
            data_dir,
            fitting_mode_options,
            preprared_data_options,
            local_functions,
        )


def run_inference(
    dir: Path,
    data_dir: Path,
    fitting_mode_options: dict[str, FittingMode],
    preprared_data_options: Mapping[str, type[PreparedData]],
    local_functions: dict[str, Callable],
):
    ic = load_inference_configuration(dir)
    prepdef = preprared_data_options[ic.prepared_data_dir]
    with open(os.path.join(data_dir, ic.prepared_data_dir + ".json"), "r") as f:
        prepared_data = prepdef(**json.load(f))
    idata_kwargs = {
        "log_likelihood": "llik",
        "coords": prepared_data.coords,
        "dims": ic.dims,
    }
    llik_outputs = dict()
    for mode_name in ic.fitting_modes:
        mode = fitting_mode_options[mode_name]
        output = mode.fit(ic, prepared_data, local_functions)
        if mode.idata_target in ["prior", "posterior"]:
            idata_kwargs[mode.idata_target] = output
            idata_kwargs[f"{mode.idata_target.value}_predictive"] = "yrep"
        elif mode.idata_target == "log_likelihood":
            llik_outputs[f"llik_{mode.name}"] = output
        else:
            raise ValueError(
                f"idata_target {mode.idata_target} is not yet supported"
            )
    idata = az.from_cmdstanpy(**idata_kwargs)
    for varname, output in llik_outputs.items():
        idata.log_likelihood[varname] = output
    idata_dir = os.path.join(dir, "idata")
    print(f"Saving idata to {idata_dir}")
    idata.to_zarr(idata_dir)
