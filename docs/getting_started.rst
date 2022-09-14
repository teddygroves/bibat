===============
Getting started
===============

The steps for using cookiecutter-cmdstanpy-analysis are:

1. Install cookiecutter
2. Load the cookiecutter-cmdstanpy-analysis template
3. Run the example analysis
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
- Whether to create a :literal:`tests` directory
- Whether to create a :literal:`.github` directory

A folder with the repo name you chose should now appear in your current working
directory, with a lot of the boilerplate work of setting up a cmdstanpy project already done. 

Run the example analysis
========================

The example analysis can be run using the command :literal:`make analysis`. The
first time you run this command, it will set up an appropriate environment
first, creating a new Python virtual environment and installing Python
dependencies and `cmdstan <https://mc-stan.org/users/interfaces/cmdstan>`_.

The python dependencies are as follows:

- arviz
- cmdstanpy
- jupyter
- LovelyPlots
- numpy
- sklearn
- pandas
- pytest (only installed if you choose the option :literal:`y` at the prompt :literal:`create_tests_directory`)
- sphinx (only installed if you choose the option :literal:`sphinx` at the prompt :literal:`docs_format`)
- toml

After the environment has been set up, the python scripts
:literal:`prepare_data.py` and :literal:`sample.py` will run, populating the
directories :literal:`data/prepared` and :literal:`results/runs`. Finally the
jupyter notebook :literal:`investigate.ipynb` will be executed, which will save
some :literal:`.png` files to the directory :literal:`results/plots`.


