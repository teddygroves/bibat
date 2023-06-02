"""Run all the inferences in the inferences folder."""

import os

import arviz as az
import cmdstanpy

from baseball.data_preparation import load_prepared_data
from baseball.inference_configuration import load_inference_configuration

HERE = os.path.dirname(__file__)
RUNS_DIR = os.path.join(HERE, "..", "inferences")
STAN_DIR = os.path.join(HERE, "stan")


def main():
    """Fit all inferences in all modes."""
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
        llik_outputs = {}
        for mode in ic.fitting_modes:
            fit_kwargs = ic.sample_kwargs
            if (
                ic.mode_options is not None
                and mode.name in ic.mode_options.keys()
            ):
                fit_kwargs |= ic.mode_options[mode.name]
            output = mode.fit(model, stan_input_base, fit_kwargs)
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
        idata_file = os.path.join(run_dir, "idata.json")
        print(f"Saving idata to {idata_file}")
        idata.to_json(idata_file)


if __name__ == "__main__":
    main()
