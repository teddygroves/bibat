# cookiecutter-cmdstanpy: a template for one-off cmdstanpy projects

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
can start with the template and edit it to match your case, which should
hopefully take less time and effort.

## How to get started

First you need to install the python package
[cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/). This can be done
as follows:

```sh
pip install cookiecutter

```

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
2. Choose some model configurations - i.e. a Stan program plus some choices
   like what priors or covariates to use - that you want to run and
   analyse. Hardcode these in the python dictionary `MODEL_CONFIGURATIONS` in
   the file `model_configuration.py`.
3. Decide how to run your models, i.e. write

   - A function `model_configuration.get_stan_input` for generating a data
     dictionary that can be passed to `cmdstanpy.CmdStanModel.sample`.
   - A function `model_configuration.get_infd_kwargs` for generating arguments to
     `arviz.from_cmdstanpy`.
   - A dictionary `model_configuration.SAMPLE_KWARGS` with arguments to
     `cmdstanpy.CmdStanModel.sample` (how many iterations, HMC control
     parameters, etc.)
   - A function `model_configuration.generate_fake_measurements` for making
     fake data to test your model on.
   - Some hardcoded variables for generating fake data, also in
     `model_configuration.py`.
4. Fit every model configuration using fake data and analyse the
   results. Possibly go back to step 1.
5. Fit every model configuration using real data and
   analyse the results
6. Write up the results of the investigation in `report.md` and generate
   a nicely formatted `report.pdf`.
   
## Dependencies
- arviz
- numpy
- scipy
- pandas
- cmdstanpy
- pandoc


