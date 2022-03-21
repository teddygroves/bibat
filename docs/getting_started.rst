===============
Getting started
===============

The steps for using cookiecutter-cmdstanpy-analysis are:

1. Install cookiecutter
2. Load the cookiecutter-cmdstanpy-analysis template
3. Install project dependencies (e.g. cmdstanpy, cmdstan)
4. Customise the template so that it implements your analysis

This page covers steps 1 to 3. For the final step see :doc:`design` and :doc:`customisation`.

Install cookiecutter
====================

First ensure you are using a recent python version (3.7 or above should work) and install the package `cookiecutter <https://cookiecutter.readthedocs.io/en/1.7.2/>`_ as follows:

.. code:: sh

   $ pip install cookiecutter


Load cookiecutter-cmdstanpy-analysis
====================================

To load cookiecutter-cmdstanpy-analysis, go to the directory where you want to put your project and run the following command:

.. code:: sh

   $ cookiecutter gh:teddygroves/cookiecutter-cmdstanpy-analysis


A wizard will now ask you to enter the following bits of configuration
information:

- Project name
- Repo name
- Author name (the name of your organisation/company/team will also work)
- Project description
- Open source license (can be one of MIT, BSD-3 or none)
- Whether to create a docs directory, and if so in what format

A folder with the repo name you chose should now appear in your current working
directory, with a lot of the boilerplate work of setting up a cmdstanpy project already done. 

Install project dependencies
============================

The template project uses the following python libraries:

- arviz
- cmdstanpy
- jupyter
- numpy
- sklearn
- pandas
- pytest (only required if you choose the option :literal:`y` at the prompt :literal:`create_tests_directory`)
- sphinx (only required if you choose the option :literal:`sphinx` at the prompt :literal:`docs_format`)
- toml

These can be installed after creating your project by going to its root
directory and running this command:

.. code:: sh

    $ pip install -r requirements.txt

Cmdstanpy depends on `cmdstan <https://mc-stan.org/users/interfaces/cmdstan>`_ and provides helpful utilities for installing it: see `here <https://cmdstanpy.readthedocs.io/en/v0.9.68/installation.html#install-cmdstan>`_ for details.

Finally, if you chose the option :literal:`Markdown` at the prompt :literal:`docs_format`, there will be a directory called :literal:`docs` containing a report file :literal:`report.md` and a makefile with a recipe for building the target :literal:`report.pdf` with `pandoc <https://pandoc.org/>`_. You should only choose this option if pandoc is installed.
