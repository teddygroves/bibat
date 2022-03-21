=======================================
Intended workflow and project structure
=======================================

This page describes the file structure that cookiecutter-cmdstanpy-analysis creates and how it is intended to be used.

Intended workflow
=================

As cookiecutter-cmdstanpy-analysis sees it, a statistical analysis consists of the following ingredients:

- Some raw data
- Some ways of processing the raw data
- Some statistical models
- Some `model configurations`, i.e. combinations of a statistical model, a processed dataset and some specification: what MCMC settings to use, whether to run in priors-only mode, etc
- Some maths, words and graphs that investigate the results of running each model configuration

cookiecutter-cmdstanpy-analysis tries to represent these ingredients as explicitly as possible:

- Raw data are files that live in their own directory :literal:`data/raw`
- Ways of processing raw data are functions in the file :literal:`src/data_preparation.py`
- Statistical models are Stan programs in the directory :literal:`src/stan`
- Model configurations are special :literal:`toml` files in the directory `model_configurations`
- Post-run investigations are files in the directory :literal:`docs` (or the investigation notebook :literal:`investigate.ipynb`)
  
To actually perform the analysis, you have to run every data preparation function, then run every model configuration, then make some graphs and do some writing. To make this process as convenient as possible, cookiecutter-cmdstanpy-analysis represents these actions with runnable Python scripts (and a Jupyter notebook) corresponding to each step, and a phony Makefile target :literal:`analysis` that runs them all in sequence.

After going through this process once, a statistical analysis typically begins again - the results will suggest a new model, data processing procedure or algorithm setting to investigate next. cookiecutter-cmdstanpy-analysis makes expanding an analysis in this way pretty natural. You just leave everything as it is, write a new Stan program, data processing function or algorithm setting in their appropriate place, then add a new model configuration file. Now when you run :literal:`make analysis` everything will work as before, but the new model configuration will run as well!

Structuring the code and data that implements a statistical analysis in this way is meant to lead to a workflow where deciding where to make a code change is intuitive, and where changes in the analysis leave behind traceable clues that make sense to collaborators and future selves.

Directory structure
===================

cookiecutter-cmdstanpy-analysis creates a directory with the following structure (assuming the user chose :literal:`Markdown` at the :literal:`docs_format` prompt and :literal:`y` at all the :literal:`create` prompts):

.. code:: sh

    .
    ├── .github
    │   └── workflows
    │       └── run_pytest.yml
    ├── .gitignore
    ├── CODE_OF_CONDUCT.md
    ├── LICENSE
    ├── Makefile
    ├── README.md
    ├── investigate.ipynb
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
    │   ├── test_integration
    │   │   └── test_data_preparation.py
    │   └── test_unit
    │       └── test_util.py
    └── docs
        ├── bibliography.bib
        ├── img
        │   ├── example.png
        │   └── readme.md
        ├── Makefile
        └── report.md

Top level files
...............

The project root directory contains project-level configuration files, a Makefile, a readme, license and code of conduct, Python scripts like :literal:`prepare_data.py` and :literal:`sample.py`, and a Jupyter notebook :literal:`investigate.ipynb`.

The script `prepare_data.py` imports data preparation functions from :literal:`src/data_preparation.py` and uses them to convert raw data from the directory :literal:`data/raw` into subdirectories of `data/prepared`.

The script `sample.py` runs each model configuration file in the `model_configurations` in all specified modes, converts the results to arviz :literal:`InferenceData` objects and save them in netcdf format in the directory :literal:`results/runs/<name-of-model-configuration>/`.

The example Jupyter notebook `investigate.py` looks at all completed model runs and compares their approximate leave-one-out cross-validation and exact k-fold cross-validation performance. It also plots the runs' marginal posterior predictive distributions.

The file `Makefile` contains phony targets for conveniently running the whole analysis (`make analysis`) and deleting files (`clean-stan`, `clean-report`, `clean-prepared-data`, `clean-results` and `clean-all`).

Finally, the file `pyproject.toml` contains some default configuration for the common python developer tools `black`, `isort`, `pylint` and `pyright`.

Library code
............

The directory :literal:`src` contains library code that is intended to be imported and used in the top-level scripts. Most of the logic that implements your analysis should live here.

To illustrate, the file :literal:`src/data_preparation.py` contains a function for each data-preparation variation that the example project takes into consideration. These functions are imported by the script :literal:`prepare_data.py` and used to write prepared data to subdirectories of :literal:`data/prepared`.

Model Configurations
....................

The folder :literal:`model_configurations` contains :literal:`toml` files, each of which specifies a data/statistical model combination that the analysis will investigate. In the example project, the fields :literal:`name`, :literal:`stan_file` and :literal:`data_dir` must be entered, and a list of :literal:`modes` as well as tables :literal:`stanc_options`, :literal:`cpp_options`, :literal:`sample_kwargs` and :literal:`sample_kwargs.<mode>` can also be included. These can be customised by editing the class :literal:`ModelConfiguration` in the file :literal:`src/model_configuration.py`

To see how a model configuration file works in practice, here are the contents of the file :literal:`model_configurations/interaction.toml`:

.. code:: toml

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

This model configuration is called :literal:`interaction`, and uses the model at `src/stan/model.stan` and the data at `data/prepared/interaction`. It will run in `prior`, `posterior` and `cross_validation` modes, with pedantic warnings being raised when the model's Stan code is compiled. Some keyword arguments for cmdstanpy's `sample` method are set for all modes, and the `chains` argument is set to one for the mode `cross_validation`.

Tests
.....

Tests live in the the optional :literal:`tests` directory, with separate directories for unit tests and integration tests.

The example tests can be triggered by running the command :literal:`python -m pytest` from the project root directory.

Documentation
.............

The directory docs contains stub documentation, either in `pandoc Markdown <https://pandoc.org/MANUAL.html#pandocs-markdown>`_ or `sphinx <https://www.sphinx-doc.org/en/master/index.html>`_ format.

Continuous integration with github actions
..........................................

The optional directory :literal:`.github` contains an example `github actions <https://docs.github.com/en/actions>`_ workflow that installs the example project's dependencies and then runs its tests, using the latest ubuntu and windows operating systems, whenever a push is made to a branch in the repository.

