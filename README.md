# cookiecutter-cmdstanpy

## A template for one-off cmdstanpy projects.

So you have a nice idea about how to model some data, but your intended model
can't easily be implemented with a generic solution like
[brms](https://paul-buerkner.github.io/brms/) or
[bambi](https://bambinos.github.io/bambi/).

Luckily almost any statistical model can be implemented as a
[Stan](https://mc-stan.org/) program, and python libraries like
[cmdstanpy](https://cmdstanpy.readthedocs.io/) and
[arviz](https://arviz-devs.github.io/arviz/) make it pretty straightforward to
run these programs and analyse their results. Still, a lot of typing seems to
lie in your future. 

Unless...

## Overview

This template aims to reduce the amount of work you repeat every time you
embark on a cmdstanpy project. Instead of writing everything from scratch, you
can start with the template and edit it to match your specific use case, which
should hopefully take less time and effort.

## Dependencies
The only requirement in order to create a new project with
cookiecutter-cmdstanpy is the python package
[cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/), which can be
installed as follows:

```sh
pip install cookiecutter

```

However, the code in the template assumes that the following python libraries
are available:

- arviz
- cmdstanpy
- numpy
- scipy
- pandas

These can be installed after creating your project by going to its root
directory and running this terminal command:

```sh
pip install -r requirements.txt
```

Cmdstanpy depends on [cmdstan](https://mc-stan.org/users/interfaces/cmdstan)
and provides helpful utilities for installing it: see
[here](https://cmdstanpy.readthedocs.io/en/v0.9.68/installation.html#install-cmdstan)
for details.

Finally, generating `report.pdf` with `make report.pdf` requires
[pandoc](https://pandoc.org/) and [make](https://www.gnu.org/software/make/).

## How to get started

To download the template and customise it for your project, go to the directory
where you want to put your project and enter the following command:

```sh
cookiecutter https://github.com/teddygroves/cookiecutter-cmdstanpy

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

Now you can get started with tweaking the defaults so that they implement and
analyse your model.

## Intended workflow

The template is made with the following workflow in mind:

1. Write one or more Stan programs implementing statistical models and store
   them in the `stan` folder.
2. Write one or more functions for generating cmdstanpy input dictionaries that
   are compatible with your models and put these in the file
   `pandas_to_cmdstanpy.py`.
3. Write functions for generating keyword arguments to the arviz function
   `from_cmdstanpy` and put these in the file `cmdstanpy_to_arviz.py`.
4. Choose some model configurations - i.e. a Stan program plus functions for
   generating cmdstanpy inputs and arviz keyword arguments - that you want to
   run and analyse. Put these in the list `MODEL_CONFIGURATIONS` in the file
   `model_configurations_to_try.py`. See `model_configuration.py` for the
   specification of a model configuration.
5. Write functions for generating fake data given known parameter values. Put
   them in `fake_data_generation.py`.
6. Write a function for preparing raw data and put it in `data_preparation.py`.
7. Fit every model configuration using fake data and analyse the
   results. Possibly go back to step 1.
8. Prepare real data, fit every model configuration to it and analyse the
   results. Possibly go back to step 1.
9. Write up the results of the investigation in `report.md` and generate
   a nicely formatted pdf file.

Steps 1 to 6 are already completed for the simple example model at
`stan/model.stan`. Hopefully there should be some common ground between this
model and at least the first iteration of the custom model you would like to
build, so that the template only need to be tweaked rather than completely
re-written.

Steps 7 to 9 should not require any custom writing, except for analysing the
models' output. They can be completed with the following terminal commands:

```sh
python fit_fake_data.py  # step 7

# Analyse the results...

python prepare_data.py   # step 8
python fit_real_data.py

# Analyse the results...

make report.pdf          # step 9
```

## Contributing

If you have a suggestion or comment, or find a bug then please file an issue or
submit a pull request.
