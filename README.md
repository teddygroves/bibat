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
one-off cmdstanpy projects. It aims to reduce the amount of work you repeat
every time you want to use cmdstanpy to analyse some data. Instead of writing
everything from scratch, you can start with this template and edit it to match
your specific use case.

The strucutre is meant to be general enough to support a range of typical
statistical workflows, from fitting a single model once to a single dataset to
fitting arbitrary combinations of models and datasets in prior, posterior and kfold-cross-validation modes. 

Unfortunately, covering all these possibilities meant introducing some
abstraction in the form of two concepts that are specific to the template:
**data configuration** and **model configuration**. A data configuration points
to and configures a function that turns some raw data into a Stan input. A model
configuration points to some prepared data in the form of a Stan input and a
model in the form of a Stan program, configures Stan's sampler and specifies which modes to run the model in (currently the options are prior, posterior and cross validation).

## Dependencies
The only requirement in order to create a new project with
cookiecutter-cmdstanpy is the python package
[cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/), which can be
installed as follows:

```sh
pip install cookiecutter

```

However, the code in the template will only work for python versions at least
3.7, and assumes the following python libraries are available:

- arviz
- cmdstanpy
- numpy
- sklearn
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
   them in the folder
   [`src/stan`]({{cookiecutter.repo_name}}/src/stan).
2. Write one or more functions for generating cmdstanpy input dictionaries that
   are compatible with your models. Put these in the file
   [`src/data_preparation.py`]({{cookiecutter.repo_name}}/src/data_preparation.py)
   and configure them with toml files in the folder
   [`data_configurations`]({{cookiecutter.repo_name}}/data_configurations).
3. Write some model configurations - i.e. toml files referring to a data
   configuration and a Stan program and providing keyword arguments to
   cmdstanpy's `sample` method. Put these in the folder
   [`model_configurations`]({{cookiecutter.repo_name}}/model_configurations).
4. Run the script
   [`prepare_data.py`]({{cookiecutter.repo_name}}/prepare_data.py). This will
   create a subfolder of
   [`data/prepared`]({{cookiecutter.repo_name}}/data/prepared) containing all
   the prepared data for each data configuration.
5. Run the script
   [`sample.py`]({{cookiecutter.repo_name}}/prepare_data.py). This will create a
   subfolder of [`results/runs`]({{cookiecutter.repo_name}}/results/runs) for
   each model configuration and populate it with the results of running the
   specified model and data in each of three modes: prior, posterior and
   cross-validation. The results are stored as netcdf files from which you can
   easily load arviz `InferenceData` objects.
6. Check out the results, then write up the results of your investigation in
   [`report.md`]({{cookiecutter.repo_name}}/report.md) and generate a nicely
   formatted pdf file by running `make report`.

To illustrate how this is intended to work, these steps have are already
completed for the simple example model at
[`src/stan/model.stan`]({{cookiecutter.repo_name}}/src/stan/model.stan) and the
example data configurations `interaction` and `no_interaction`. Hopefully there
should be some common ground between this model and at least the first iteration
of the custom model you would like to build, so that the template only needs to
be tweaked rather than completely re-written.


## Contributing

All contributions are very welcome!

If you have a specific suggestion for how cookiecutter-cmdstanpy could be
improved, or if you find a bug then please file an issue or submit a pull
request.

Alternatively, if you have any more general thoughts or questions, please post
them in the [discussions
page](https://github.com/teddygroves/cookiecutter-cmdstanpy/discussions).
