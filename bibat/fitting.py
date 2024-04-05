"""Functions for running inferences."""

import logging
from collections.abc import Callable
from enum import Enum
from pathlib import Path

import arviz as az

from bibat.fitting_mode import FittingMode
from bibat.inference_configuration import (
    InferenceConfiguration,
    load_inference_configuration,
)
from bibat.prepared_data import PreparedData


class IdataSaveFormat(str, Enum):
    """An enum for choosing the format in which inferences are saved."""

    zarr = "prior"
    json = "json"


def run_all_inferences(  # noqa: PLR0913
    inferences_dir: Path,
    data_dir: Path,
    fitting_mode_options: dict[str, FittingMode],
    loader: Callable[[Path], PreparedData],
    local_functions: dict[str, Callable],
    idata_save_format: IdataSaveFormat = IdataSaveFormat.zarr,
) -> None:
    """Fit all inferences in all modes."""
    inference_dirs = inferences_dir.iterdir()
    for inference_dir in sorted(inference_dirs):
        ic = load_inference_configuration(inference_dir)
        prepared_data_json = (data_dir / ic.prepared_data).with_suffix(".json")
        prepared_data = loader(prepared_data_json)
        idata = run_inference(
            ic,
            prepared_data,
            fitting_mode_options,
            local_functions,
        )
        if idata_save_format == IdataSaveFormat.zarr:
            idata_dir = inference_dir / "idata"
            idata.to_zarr(str(idata_dir))
        else:
            idata_file = inference_dir / "idata.json"
            logging.info("Saving idata to %s", idata_file)
            az.to_json(idata, idata_file)


def run_inference(
    ic: InferenceConfiguration,
    prepared_data: PreparedData,
    fitting_mode_options: dict[str, FittingMode],
    local_functions: dict[str, Callable],
) -> az.InferenceData:
    """Run an inference."""
    idata_kwargs = {
        "log_likelihood": "llik",
        "coords": prepared_data.coords,
        "dims": ic.dims,
    }
    if ic.stan_input_function is not None:
        idata_kwargs["observed_data"] = local_functions[ic.stan_input_function](
            prepared_data,
        )
    llik_outputs: dict = {}
    for mode_name in ic.fitting_modes:
        mode = fitting_mode_options[mode_name]
        output = mode.fit(ic, prepared_data, local_functions)
        if mode.idata_target in ["prior", "posterior"]:
            idata_kwargs[mode.idata_target] = output
            idata_kwargs[f"{mode.idata_target.value}_predictive"] = "yrep"
        elif mode.idata_target == "log_likelihood":
            llik_outputs[f"llik_{mode.name}"] = output
    idata = az.from_cmdstanpy(**idata_kwargs)
    for varname, output in llik_outputs.items():
        idata.log_likelihood[varname] = output
    return idata
