"""Run all the configs in the model_configurations folder."""

import json
import os

import toml
import xarray

from src.model_configuration import ModelConfiguration
from src.sampling import sample

MODEL_CONFIGURATION_DIR = "model_configurations"
RESULTS_DIR = os.path.join("results", "runs")


def main():
    config_files = [
        os.path.join(MODEL_CONFIGURATION_DIR, f)
        for f in os.listdir(MODEL_CONFIGURATION_DIR)
        if f.endswith(".toml")
    ]
    for config_file in sorted(config_files):
        mc = ModelConfiguration(**toml.load(config_file))
        with open(os.path.join(mc.data_dir, "coords.json"), "r") as f:
            coords = json.load(f)
        with open(os.path.join(mc.data_dir, "dims.json"), "r") as f:
            dims = json.load(f)
        run_dir = os.path.join(RESULTS_DIR, mc.name)
        if not os.path.exists(run_dir):
            os.mkdir(run_dir)
        for mode in mc.modes:
            sample_kwargs = {
                k: v for k, v in mc.sample_kwargs.items() if k not in mc.modes
            }
            if mode in mc.sample_kwargs.keys():
                sample_kwargs = {**sample_kwargs, **mc.sample_kwargs[mode]}
            if mode == "cross_validation":
                llik_file = os.path.join(run_dir, "llik_cv.nc")
                lliks = []
                cv_input_dir = os.path.join(mc.data_dir, "stan_inputs_cv")
                for f in sorted(os.listdir(cv_input_dir)):
                    input_json_file = os.path.join(cv_input_dir, f)
                    llik = sample(
                        stan_file=mc.stan_file,
                        stanc_options=mc.stanc_options,
                        cpp_options=mc.cpp_options,
                        input_json=input_json_file,
                        coords={
                            k: v
                            for k, v in coords.items()
                            if k != "observation"
                        },
                        dims=dims,
                        sample_kwargs=sample_kwargs,
                    ).get("log_likelihood")
                    lliks.append(llik)
                full_llik = xarray.concat(lliks, dim="ix_test")
                print(
                    f"\n***Writing out-of-sample log likelihoods to {llik_file}***\n"
                )
                full_llik.to_netcdf(llik_file)
            else:
                idata_file = os.path.join(run_dir, f"{mode}.nc")
                input_json = os.path.join(
                    mc.data_dir, f"stan_input_{mode}.json"
                )
                print(f"\n***Fitting model {mc.name} in {mode} mode...***\n")
                idata = sample(
                    stan_file=mc.stan_file,
                    stanc_options=mc.stanc_options,
                    cpp_options=mc.cpp_options,
                    input_json=input_json,
                    coords=coords,
                    dims=dims,
                    sample_kwargs=sample_kwargs,
                )
                print(f"\n***Writing inference data to {idata_file}***\n")
                idata.to_netcdf(idata_file)


if __name__ == "__main__":
    main()
