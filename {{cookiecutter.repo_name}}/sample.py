"""Run all the configs in the model_configurations folder."""

import json
import os

import toml
import xarray

from src.model_configuration import ModelConfiguration
from src.sampling import sample
from src.models import AVAILABLE_MODELS
from src.model_modes import AVAILABLE_MODEL_MODES
from src.prepared_data import load_prepared_data

RUNS_DIR = "runs"
STAN_DIR = os.path.join("src", "stan")

def main():
    run_dirs = [
        os.path.join(RUNS_DIR, d)
        for d in os.listdir(RUNS_DIR)
        if os.path.isdir(os.path.join(RUNS_DIR, d))
    ]
    for run_dir in sorted(run_dirs):
        config_file = os.path.join(run_dir, "config.toml")
        mc = ModelConfiguration(**toml.load(config_file))
        model = next(
            m for m in AVAILABLE_MODELS if m.stan_file == mc.model_file
        )
        prepared_data = load_prepared_data(mc.prepared_data_dir)
        for mode in mc.modes:
            model_mode = next(
                mm
                for mm in AVAILABLE_MODEL_MODES
                if mm.model == model and mm.mode_name == mode
            )
            stan_inputs = model_mode.stan_input_function(prepared_data)
            if not model_mode.multiple_runs:
                stan_inputs = [stan_inputs]
            sample_kwargs = {
                k: v for k, v in mc.sample_kwargs.items() if k not in mc.modes
            }
            if mode in mc.sample_kwargs.keys():
                sample_kwargs = {**sample_kwargs, **mc.sample_kwargs[mode]}
            for i, stan_input in enumerate(stan_inputs):
                print(f"\n***Fitting model {mc.name} in {mode} mode...***\n")
                suff = f"{mode}-{i}" if model_mode.multiple_runs else f"{mode}"
                idata_file = os.path.join(run_dir, f"idata-{suff}.json")
                input_file = os.path.join(run_dir, f"input-{suff}.json")
                with open(input_file, "w") as f:
                    json.dump(stan_input, f)
                idata = sample(
                    stan_file=os.path.join(STAN_DIR, mc.model_file),
                    stanc_options=mc.stanc_options,
                    cpp_options=mc.cpp_options,
                    input_json=input_file,
                    coords=prepared_data.coords,
                    dims=model.dims,
                    sample_kwargs=sample_kwargs,
                )
                print(f"\n***Writing inference data to {idata_file}***\n")
                idata.to_json(idata_file)


if __name__ == "__main__":
    main()
