import json
import os

import pandas as pd
import toml
from cmdstanpy import write_stan_json

from src.data_configuration import DataConfiguration
from src.data_preparation import PREPARE_DATA_FUNCTIONS
from src.prepared_data import PrepareDataFunction

PREPARE_DATA_FUNCTIONS_BY_NAME = {f.__name__: f for f in PREPARE_DATA_FUNCTIONS}

# Where to find raw data and where to save prepared data: probably don't edit!
RAW_DATA_DIR = os.path.join("data", "raw")
PREPARED_DATA_DIR = os.path.join("data", "prepared")
DATA_CONFIGURATION_DIR = "data_configurations"

# Filenames of the input and output: edit these unless they are already what
# you want
RAW_DATA_CSV = "raw_measurements.csv"
PREPARED_DATA_CSV = "data_prepared.csv"


def main():
    config_files = sorted(
        [
            os.path.join(DATA_CONFIGURATION_DIR, f)
            for f in os.listdir(DATA_CONFIGURATION_DIR)
            if f.endswith(".toml")
        ]
    )
    for config_file in config_files:
        dc = DataConfiguration(**toml.load(config_file))
        print(f"Preparing data for data configuration {dc.name}...")
        assert (
            dc.prepare_data_function in PREPARE_DATA_FUNCTIONS_BY_NAME.keys()
        ), f"Unknown function {dc.prepare_data_function}"
        prepare_data_function: PrepareDataFunction = (
            PREPARE_DATA_FUNCTIONS_BY_NAME[dc.prepare_data_function]
        )
        raw_df = pd.read_csv(dc.raw_df)
        prepped = prepare_data_function(dc.name, raw_df, dc.xcols, dc.n_folds)
        output_dir = os.path.join(PREPARED_DATA_DIR, prepped.name)
        cv_dir = os.path.join(output_dir, "stan_inputs_cv")
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
            os.mkdir(cv_dir)
        output_dir_files = {
            "coords": "coords.json",
            "dims": "dims.json",
            "measurements": "measurements.csv",
            "stan_input_prior": "stan_input_prior.json",
            "stan_input_posterior": "stan_input_posterior.json",
        }
        output_dir_files = {
            k: os.path.join(output_dir, v) for k, v in output_dir_files.items()
        }
        with open(output_dir_files["coords"], "w") as f:
            json.dump(prepped.coords, f)
        with open(output_dir_files["dims"], "w") as f:
            json.dump(prepped.dims, f)
        prepped.df.to_csv(output_dir_files["measurements"])
        write_stan_json(
            output_dir_files["stan_input_prior"], prepped.stan_input_prior
        )
        write_stan_json(
            output_dir_files["stan_input_posterior"],
            prepped.stan_input_posterior,
        )
        for i, si in enumerate(prepped.stan_inputs_cv):
            f = os.path.join(cv_dir, f"split_{str(i)}.json")
            write_stan_json(f, si)
    print("Data prepared!")


if __name__ == "__main__":
    main()
