# cookiecutter-cmdstanpy

So you have a nice idea about how to model some data, but your intended model
can't easily be implemented with a generic solution like
[brms](https://paul-buerkner.github.io/brms/) or
[bambi](https://bambinos.github.io/bambi/).

Luckily almost any statistical model can be implemented as a
[Stan](https://mc-stan.org/) program, and python libraries like
[cmdstanpy](https://cmdstanpy.readthedocs.io/) and
[arviz](https://arviz-devs.github.io/arviz/) make it pretty straightforward to
run these programs and analyse their results. Still, a lot of typing seems to
lie in your future. Unless...

## Overview

This repository is a
[cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) template for
cmdstanpy projects. It aims to reduce the amount of work you repeat every time
you want to use cmdstanpy to analyse some data. Instead of writing everything
from scratch, you can start with this template and edit it to match your
specific use case.

The strucutre is meant to be general enough to support a range of typical
statistical workflows, from fitting a single model once to a single dataset to
fitting arbitrary combinations of models and datasets in prior, posterior and kfold-cross-validation modes. 

## How to use cookiecutter-cmdstanpy

### Get cookiecutter

First ensure you are using a recent python version (3.7 or above should work)
and install the package
[cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) as follows:

```sh
pip install cookiecutter

```

Now download the template and customise it for your project by going to the
directory where you want to put your project and entering the following command:

### Use the template

```sh
cookiecutter gh:teddygroves/cookiecutter-cmdstanpy

```

A wizard will now ask you to enter the following bits of configuration
information:

- Project name
- Repo name
- Author name (the name of your organisation/company/team will also work)
- Project description
- Open source license (can be one of MIT, BSD-3 or none)

A folder with the repo name you chose should now appear in your current working
directory, containing a lot of the writing you would otherwise have had to do
yourself. 

### Install dependencies

The template project requires the following python libraries:

- arviz
- cmdstanpy
- numpy
- sklearn
- pandas
- toml

These can be installed after creating your project by going to its root
directory and running this command:

```sh
pip install -r requirements.txt
```

Cmdstanpy depends on [cmdstan](https://mc-stan.org/users/interfaces/cmdstan) and
provides helpful utilities for installing it: see
[here](https://cmdstanpy.readthedocs.io/en/v0.9.68/installation.html#install-cmdstan)
for details.

Finally, the project also comes with a recipe for generating a pdf report file `report.pdf` from the markdown file `report.md` using the command `make report.pdf`. This recipe requires [pandoc](https://pandoc.org/).

Now you can get started with tweaking the defaults so that they implement your analysis.

## Intended workflow

The idea behind the template is to take advantage of cmdstanpy's file-based
workflow to ensure reproducibility and persistence while using a standard
directory structure to keep things organised.

The template creates the following file structure:

```sh
.
├── LICENSE
├── Makefile
├── README.md
├── analyse.py
├── bibliography.bib
├── data
│   ├── prepared
│   │   └── readme.md
│   └── raw
│       ├── raw_measurements.csv
│       └── readme.md
├── model_configurations
│   ├── interaction.toml
│   ├── interaction_fake_data.toml
│   └── no_interaction.toml
├── prepare_data.py
├── pyproject.toml
├── report.md
├── requirements.txt
├── results
│   └── runs
│       └── readme.md
├── sample.py
└── src
    ├── data_preparation.py
    ├── model_configuration.py
    ├── prepared_data.py
    ├── readme.md
    ├── sampling.py
    ├── stan
    │   ├── custom_functions.stan
    │   ├── model.stan
    │   └── readme.md
    └── util.py
```

Entry-points to your analysis should live in `.py` files in the project root, such as `prepare_data.py`, `sample.py` and `analyse.py`. Most logic should go in python files in the `src` directory. In particular, Stan code should go in the directory `src/stan`.

In particular, the file `data_preparation.py` should contain a function for each data-preparation variation you would like to investigate. These functions can be imported by the script `prepare_data.py` and used to write prepared data to subdirectories of `data/prepared`. The provided `PreparedData` class and the example logic in the files `prepare_data.py` aim to cover a wide range of data preparation workflows and carry out boilerplate tasks like reading and writing files, splitting data for cross-validation and handling boolean `likelihood` variables, so that adapting the code for your use case should hopefully be mostly a matter of changing substantive details in the file `src/data_preparation.py`.

The folder `model_configurations` should contain `toml` files, each of which specifies a data/statistical model combination that you would like to investigate. The fields `name`, `stan_file` and `data_dir` must be entered, and a list of `modes` as well as tables `stanc_options`, `cpp_options`, `sample_kwargs` and `sample_kwargs.<mode>` can also be included. For example, here are the contents of the file `model_configurations/interaction.toml`:

```toml
name = "interaction"
stan_file = "src/stan/model.stan"
data_dir = "data/prepared/interaction"
modes = ["prior", "posterior", "cross_validation"]

[stanc_options]
warn-pedantic = true

[sample_kwargs]
show_progress = true
save_warmup = false
iter_warmup = 2000
iter_sampling = 2000

[sample_kwargs.cross_validation]
chains = 1
```

This model configuration is called "interaction", and uses the model at `src/stan/model.stan` and the data at `data/prepared/interaction`. It will run in `prior`, `posterior` and `cross_validation` modes, with pedantic warnings being raised when the model's Stan code is compiled. Some keyword arguments for cmdstanpy's `sample` method are set for all modes, and the `chains` argument is set to one for the mode `cross_validation`.

The script `sample.py` will run each model configurations in all specified modes, convert the results to arviz InferenceData objects and save them in netcdf format in the directory `results/runs/<name-of-model-configuration>/`.

The example script `analyse.py` looks at all completed model runs and compares their approximate leave-one-out cross-validation and exact k-fold cross-validation performance. This script could also contain code for drawing plots based on the results.

The file `Makefile` has instructions for building the target `report.pdf` with pandoc, as well as phony targets for conveniently running the whole analysis (`make analysis`) and deleting files (`clean-stan`, `clean-report`, `clean-prepared-data`, `clean-results` and `clean-all`)

Finally, the file `pyproject.toml` contains some default configuration for the common python developer tools `black`, `isort`, `pylint` and `pyright`.

To get a better idea of how everything works, why not try running the example yourself, checking out the output and then tweaking something? You can do this by running `make analysis`: this will run `prepare_data.py`, then `sample.py` and then `analyse.py`.

## Extending the template

Perhaps your analysis involves fetching some data from the internet, and you would like to include the code that does the fetching alongside the code that implements the rest of your analysis. A way to do this that fits in nicely with the rest of the template would be to write a new script `fetch_data.py` that writes to `data/raw` and possibly a library file `fetching.py` with code for the script to import.

Perhaps your data doesn't naturally fit into a single table, and you would like your analysis to assume that prepared data has two tables: `measurements` and `cats`. This can be done by first editing the `PreparedData` class:

```python
@dataclass
class PreparedData:
    name: str
    coords: CoordDict
    dims: Dict[str, Any]
    measurements: pd.DataFrame
    cats: pd.DataFrame
    ...
```

Next go to `src/data_preparation.py` and add logic for processing a new `cats` dataframe:

```python
def prepare_data_cats_hats(measurements_raw: pd.DataFrame, cats_raw) -> PreparedData:
    """Prepare data about cats with hats."""
    
    ... 
    
    return PreparedData(
        name="cats_hats",
        measurements=measurements,
        cats=cats,
        ...
    )

```

Finally go to `prepare_data.py` and add logic for reading and writing the `cats`:

```python
...
RAW_DATA_FILES = {
    "raw_measurements": os.path.join(RAW_DIR, "raw_measurements.csv"),
    "raw_cats": os.path.join(RAW_DIR, "raw_cats.csv"),
}
...
def main():
    ...
        prepared_data = data_prep_function(
            raw_data["raw_measurements"], raw_data["raw_cats"]
        )
        ...
        measurements_file = os.path.join(output_dir, "measurements.csv")
        cats_file = os.path.join(output_dir, "cats.csv")
        ...
        prepared_data.measurements.to_csv(measurements_file)
        prepared_data.cats.to_csv(cats_file)
        ...
```

## Contributing

All contributions are very welcome!

If you have a specific suggestion for how cookiecutter-cmdstanpy could be
improved, or if you find a bug then please file an issue or submit a pull
request.

Alternatively, if you have any more general thoughts or questions, please post
them in the [discussions
page](https://github.com/teddygroves/cookiecutter-cmdstanpy/discussions).
