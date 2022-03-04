# cookiecutter-cmdstanpy

A small statistical statistical analysis can often be done by a single script or notebook file. This is really nice because the file is easy to keep track of and work with. Unfortunately it usually happens that the single file starts to get a bit big: a few models have to be compared, there are a few data input options to consider, several plots need drawing, it would be nice to test the models against some fake data, and so on.

Luckily [Stan](https://mc-stan.org/) and python libraries like
[cmdstanpy](https://cmdstanpy.readthedocs.io/) and
[arviz](https://arviz-devs.github.io/arviz/) support splitting your analysis up
into multiple files when it starts getting unwieldy. Still, lots of decisions need to be made about how exactly to do this and it can be tricky and tedious to choose and implement a good layout and then remember it at the start of every new project.

cookiecutter-cmdstanpy attempts to address this problem by implementing a
flexible but still effort-saving template for medium to largish statistical
analyis projects. Instead of writing everything from scratch, you can start with
this template and edit it to match your specific use case.

The structure is meant to be general enough to support a range of typical
statistical workflows, from fitting a single model once to a single dataset to
fitting arbitrary combinations of models and datasets in prior, posterior and kfold-cross-validation modes. 

## How to use cookiecutter-cmdstanpy

The steps are:

1. Install cookiecutter
2. Load the cookiecutter-cmdstanpy template
3. Install other dependencies (e.g. cmdstanpy, cmdstan)
4. Customise the template so that it implements your analysis

### Get cookiecutter

First ensure you are using a recent python version (3.7 or above should work)
and install the package
[cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) as follows:

```sh
pip install cookiecutter

```

### Load cookiecutter-cmdstanpy
To load cookiecutter-cmdstanpy, go to the directory where you want to put your project and run the following command:

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
- Whether to create a writing directory

A folder with the repo name you chose should now appear in your current working
directory, with a lot of the boilerplate work of setting up a cmdstanpy project already done. 

### Install dependencies

The template project uses the following python libraries:

- arviz
- cmdstanpy
- numpy
- sklearn
- pandas
- pytest (only required if you choose the option `y` at the prompt `create_tests_directory`)
- toml

These can be installed after creating your project by going to its root
directory and running this command:

```sh
pip install -r requirements.txt
```

Cmdstanpy depends on [cmdstan](https://mc-stan.org/users/interfaces/cmdstan) and provides helpful utilities for installing it: see [here](https://cmdstanpy.readthedocs.io/en/v0.9.68/installation.html#install-cmdstan) for details.

Finally, if you chose the option `y` at the prompt `create_writing_directory`, there will be a report file `writing/report.md` and a makefile recipe for building the target `writing/report.pdf` with [pandoc](https://pandoc.org/). Running this recipe with the command `make report` will only work if pandoc is installed.

## Intended workflow

Now you can get started with tweaking the defaults so that they implement your analysis.

The idea behind the template is to take advantage of cmdstanpy's file-based
workflow to ensure reproducibility and persistence while using a standard
directory structure to keep things organised.

The template is set up already filled in with an analysis of a linear regression problem, comparing the results of fitting a model with and without an interaction effect, and also seeing what happens when the model with the interaction effect is fit to fake data generated using its assumptions.

The template creates the following file structure:

```sh
.
├── CODE_OF_CONDUCT.md
├── LICENSE
├── Makefile
├── README.md
├── analyse.py
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
├── requirements.txt
├── results
│   └── runs
│       └── readme.md
├── sample.py
├── src
│   ├── data_preparation.py
│   ├── model_configuration.py
│   ├── prepared_data.py
│   ├── readme.md
│   ├── sampling.py
│   ├── stan
│   │   ├── custom_functions.stan
│   │   ├── model.stan
│   │   └── readme.md
│   └── util.py
├── tests
│   ├── __init__.py
│   ├── test_integration
│   │   ├── __init__.py
│   │   └── test_data_preparation.py
│   └── test_unit
│       ├── __init__.py
│       └── test_util.py
└── writing
    ├── bibliography.bib
    ├── img
    │   ├── example.png
    │   └── readme.md
    └── report.md
```

Entry-points to your analysis should live in `.py` files in the project root, such as `prepare_data.py`, `sample.py` and `analyse.py`. Most logic should go in python files in the `src` directory. Stan code should go in the directory `src/stan`. 

Tests should go in the the optional `tests` directory. Some example tests are provided and can be triggered by running the command `pytest` from the project root.

In particular, the file `data_preparation.py` should contain a function for each data-preparation variation you would like to investigate. These functions can be imported by the script `prepare_data.py` and used to write prepared data to subdirectories of `data/prepared`. The example logic in these files aims to cover a wide range of data preparation workflows and carry out boilerplate tasks like reading and writing files, splitting data for cross-validation and handling boolean `likelihood` variables, so that adapting the code for your use case should hopefully be mostly a matter of changing substantive details in the file `src/data_preparation.py`.

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

## Customising the template

You will almost definitely want to customise the template so that it implements your analysis, rather than the packaged example analysis. This section explains how to do this.

### Adding a script for fetching data
Perhaps your analysis involves fetching some data from the internet, and you would like to include the code that does the fetching alongside the code that implements the rest of your analysis. A way to do this that fits in nicely with the rest of the template would be to write a new script `fetch_data.py` that writes to `data/raw` and possibly a library file `fetching.py` with code for the script to import.

### Preparing two tables
Perhaps your data doesn't naturally fit into a single table, and you would like
your analysis to assume that prepared data may include two extra tables: `cats`
and `hats`. This can be done by first adding optional attributes to the
`PreparedData` class in the file `src/prepared_data.py`:

```python
...
from typing import Any, Callable, Dict, List, Optional
...
@dataclass
class PreparedData:
    ...
    cats: Optional[pd.DataFrame] = None
    hats: Optional[pd.DataFrame] = None
    ...
```

Next go to `src/data_preparation.py` and add a new function for processing a new `cats` dataframe:

```python
def prepare_data_cats_hats(
    measurements_raw: pd.DataFrame,
    cats_raw: pd.DataFrame,
    hats_raw: pd.DataFrame
) -> PreparedData:
    """Prepare data involving cats, hats and measurements."""
    
    ... 
    
    return PreparedData(
        name="cats_hats",
        measurements=measurements,
        cats=cats,
        hats=hats,
        ...
    )

```

At this point you might want to delete the packaged data preparation functions and their corresponding model configurations, or perhaps keep them around as a handy comparison.

Finally go to `prepare_data.py` and add logic for reading and writing the `cats` and `hats`:

```python
...
RAW_DATA_FILES = {
    "raw_measurements": os.path.join(RAW_DIR, "raw_measurements.csv"),
    "raw_cats": os.path.join(RAW_DIR, "raw_cats.csv"),
    "raw_hats": os.path.join(RAW_DIR, "raw_hats.csv"),
}
...
def main():
    ...
    for data_prep_function in [
        ...
        prepare_data_cats_hats,
    ]:
        prepared_data = data_prep_function(
            raw_data["raw_measurements"], 
            raw_data["raw_cats"],
            raw_data["raw_hats"]
        )
        ...
        measurements_file = os.path.join(output_dir, "measurements.csv")
        cats_file = os.path.join(output_dir, "cats.csv")
        hats_file = os.path.join(output_dir, "hats.csv")
        ...
        prepared_data.measurements.to_csv(measurements_file)
        prepared_data.cats.to_csv(cats_file)
        prepared_data.hats.to_csv(hats_file)
        ...
```

Now when you run the script `prepare_data.py`, a new folder should be created at `data/prepared/cats_hats` containing the new data in the correct shape.

### Adding a partially pooled intercept effect for a categorical variable

You might like to write a new statistical model including a term capturing the effect of a cat's hat type on its measurement. There are five types - "bowler", "trucker", "beanie", "stetson" and "wizard" - and you don't think they naturally fit on a cardinal or even ordinal scale.

The first step is to write a Stan program `src/stan/model_cats_hats.stan` including the effect. This can be done by adding the following lines to the packaged program `model.stan`.

```stan
data {
  ...
  int<lower=1> H;  // types of hat
  int<lower=1> C;  // cats
  ...
  array[N] int<lower=1,upper=C> cat;
  array[C] int<lower=1,upper=H> hat_type;
  ...
}
...
parameters {
  ...
  real<lower=0> tau_hat_type;
  vector<multiplier=tau_hat_type>[H] a_hat_type;
  ...
}
...
model {
  ...
  a_hat_type ~ normal(0, tau_hat_type);
  tau_hat_type ~ lognormal(0, 0.3);
  ...
    y[ix_train] ~ normal_id_glm(x_std[ix_train], a + a_hat_type[hat[cat]], b, sigma);
}
...
generated quantities {
...
    yrep[n] = normal_rng(a + a_hat_type[hat[cat[n]]] + x_std[ix_test[n]] * b, sigma);
    llik[n] = normal_lpdf(y[ix_test[n]] | a + a_hat_type[hat[cat[n]]] x_std[ix_test[n]] * b, sigma);
}

```

Next the python code needs to be edited so as to match the new input and output format. First we create functions `prepare_data_cats_hats` and `get_stan_input_cats_hats` in `src/data_preparation.py`. Again these can mostly be copy/pasted from packaged functions with similar names:

```python
from src.util import one_encode
...
def prepare_data_cats_hats(
    measurements_raw: pd.DataFrame,
    cats_raw: pd.DataFrame,
    hats_raw: pd.DataFrame
) -> PreparedData:
    """Prepare data involving cats, hats and measurements."""
    
    ...
    measurements["cat_fct"] = one_encode(measurements["cat"])
    hats["hat_type_fct"] = one_encode(hats["hat_type"])
    cats = cats.join(hats.set_index("id")["hat_type_fct"], on="hat_id")

    ...
    coords = CoordDict({
        "covariate": x_cols,
        "hat_type": pd.factorize(hats["hat_type"])[1],
    })
    dims = {"b": ["covariate"], "a_hat_type": ["hat_type"]}
    ...
    return PreparedData(
        name="cats_hats",
        measurements=measurements,
        cats=cats,
        hats=hats,
        coords=coords,
        dims=dims,
        stan_input_function=get_stan_input_cats_hats
    )

...

def get_stan_input_cats_hats(
    measurements: pd.DataFrame,
    cats: pd.DataFrame,
    hats: pd.DataFrame,
) -> StanInput:
...
    return stanify_dict(
        {
            ...
            "H": hats["hat_type"].nunique(),
            "C": cats["id"].nunique(),
            ...
            "cat": measurements["cat_fct"],
            "hat_type": cats["hat_type_fct"],
            ...
        }
    )
```

The last step is to write a new model configuration:

```toml
name = "cats_hats"
stan_file = "src/stan/model_cats_hats.stan"
data_dir = "data/prepared/cats_hats"
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

Now when you run the python script `sample.py`, results for the new model configuration should be created and written alongside the other surviving model configurations to `results/runs/cats_hats`!

## Contributing

All contributions are very welcome!

If you have a specific suggestion for how cookiecutter-cmdstanpy could be
improved, or if you find a bug then please file an issue or submit a pull
request.

Alternatively, if you have any more general thoughts or questions, please post
them in the [discussions
page](https://github.com/teddygroves/cookiecutter-cmdstanpy/discussions).

If you'd like to contribute code changes, just follow the normal github workflow.

To test changes to the template locally, I recommend avoiding having to complete the wizard every time by making a [yaml](https://yaml.org/) config file like this (copied from the file tests/data/example_config.yml):

```yaml
default_context:
  project_name: "My Cool Project"
  repo_name: "my_cool_project"
  author_name: "Dr Statistics"
  description: "I used cookiecutter, cmdstanpy and arviz to do an analysis."
  open_source_license: "MIT"
  create_writing_directory: "y"

```

You should now be able to create a `my_cool_project` cmdstanpy project like this:

```
cookiecutter --no-input --config-file path/to/config.yml path/to/cookiecutter-cmdstanpy
```
