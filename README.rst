====================================================
Bibat: Batteries-Included Bayesian Analysis Template
====================================================

.. image:: https://zenodo.org/badge/344553551.svg
   :target: https://zenodo.org/badge/latestdoi/344553551

.. image:: https://readthedocs.org/projects/bibat/badge/?version=latest
    :target: https://bibat.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/teddygroves/bibat/actions/workflows/run_tox.yml/badge.svg
    :target: https://github.com/teddygroves/bibat/actions/workflows/run_tox.yml
    :alt: Test

.. image:: https://github.com/teddygroves/bibat/actions/workflows/test_end_to_end.yml/badge.svg
    :target: https://github.com/teddygroves/bibat/actions/workflows/test_end_to_end.yml
    :alt: Test

.. image:: https://www.repostatus.org/badges/latest/active.svg
   :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.
   :target: https://www.repostatus.org/#active

.. image:: https://img.shields.io/badge/python->=3.9-blue.svg
   :alt: Supported Python versions: 3.9 and newer
   :target: https://www.python.org/

.. image:: https://badge.fury.io/py/bibat.svg
    :target: https://badge.fury.io/py/bibat

.. image:: https://codecov.io/github/teddygroves/bibat/branch/main/graph/badge.svg?token=ck0IKyzP7J
    :target: https://codecov.io/github/teddygroves/bibat

.. image:: https://tinyurl.com/y22nb8up
   :alt: pyOpenSci
   :target: https://github.com/pyOpenSci/software-review/issues/83

Bibat is a Python package providing a flexible interactive template for Bayesian
statistical analysis projects.

It aims to make it easier to create software projects that implement a Bayesian
workflow that scales to arbitrarily many inter-related statistical models, data
transformations, inferences and computations. Bibat also aims to promote
software quality by providing a modular, automated and reproducible project that
takes advantage of and integrates together the most up to date statistical
software.

Bibat comes with "batteries included" in the sense that it creates a working
example project, which the user can adapt so that it implements their desired
analysis. We believe this style of template makes for better usability and
easier testing of Bayesian workflow projects compared with the alternative
approach of providing an incomplete skeleton project.

Documentation
=============

Check out bibat's documentation at `https://bibat.readthedocs.io
<https://bibat.readthedocs.io>`_.

In particular, you may find it useful to have a look at `this vignette
<https://bibat.readthedocs.io/en/latest/_static/report.html>`_ that
demonstrates, step by step, how to use bibat to implement a complex statistical
analysis.

Installation
============

You can install bibat like this (make sure you are in a Python environment where
you would like to install bibat):

.. code:: sh

    $ pip install bibat

To install the latest version of bibat from github:

.. code:: sh

    $ pip install git+https://github.com/teddygroves/bibat.git@main


To install bibat with development dependencies:

.. code:: sh

    $ pip install bibat'[development]'

Usage
=====

Bibat is intended to be used from the command line like this:

.. code:: sh

    $ bibat

Running this command will trigger a command line wizard. After following the
wizard's instructions, a new directory will be created that implements a simple
statistical analysis. To try out the example analysis, run the following
command from the root of the new directory:

.. code:: sh

    $ make analysis

If you already know how you are going to answer the wizard's questions, you can
put your answers in a json file with relative path `my_json_file.json` and run
bibat like this:

.. code:: sh

    $ bibat --config_file=my_json_file.json

See `bibat's cookiecutter schema
<https://github.com/teddygroves/bibat/blob/main/bibat/cookiecutter.json>`_ for
the information you need to create a suitable json file.

Dependencies
============

Bibat's dependencies fall into two categories: a few that are required by bibat
itself, and some more that are required in order to run the analyses that bibat
generates.

Dependencies required by bibat
------------------------------

Bibat requires Python version 3.9 or greater.

Bibat's other dependencies are all Python packages. These can be found in
bibat's `pyproject.toml file
<https://github.com/teddygroves/bibat/blob/main/pyproject.toml>`_.

The following packages are required in order to run bibat and are installed
automatically when you run :code:`pip install bibat`:

- cookiecutter
- click
- pydantic


Bibat also has the following development dependencies, which can be installed
by running :code:`pip install bibat'[development]'`:

- black
- isort
- pre-commit
- pytest
- tox
- codecov
- pytest-cov
- sphinx
- sphinx-click
- pydata_sphinx_theme


Target project dependencies: Python
-----------------------------------

Projects generated by bibat have their Python dependencies listed in the file
:code:`pyproject.toml`.  The cookiecutter template that generates this file can
be found `here
<https://github.com/teddygroves/bibat/blob/main/bibat/%7B%7Bcookiecutter.repo_name%7D%7D/pyproject.toml>`_.
These packages will be installed when you run :code:`make env` or :code:`make analysis`
and are as follows:

- arviz
- cmdstanpy
- jupyter
- numpy
- pandas
- pandera
- pydantic
- scipy
- scikit-learn
- toml

In addition, the following Python packages may be installed, depending on how
the user answers bibat's wizard:

- pytest
- black
- sphinx

Target project dependencies: Cmdstan
------------------------------------

Bibat will attempt to install `cmdstan
<https://mc-stan.org/docs/cmdstan-guide/index.html>`__, the command line
interface to Stan, when you run the commands :code:`make env` or :code:`make analysis` 
from the root of the target project.

If bibat fails to install cmdstan, please raise an issue! The relevant
parts of the `cmdstan
<https://mc-stan.org/docs/cmdstan-guide/cmdstan-installation.html>`__ and
`cmdstanpy
<https://cmdstanpy.readthedocs.io/en/v1.1.0/installation.html#cmdstan-installation>`_
documentation might also be useful.

Target project dependencies: Quarto
-----------------------------------

Bibat supports automatic generation of documentation using either Sphinx or
`Quarto <https://quarto.org/>`_. Whereas bibat will install Sphinx
automatically, Quarto must be installed manually: see the `quarto
documentation <https://quarto.org/docs/get-started/>`_ for instructions.

Citation information
====================

If you would like to cite bibat using bibtex please use the following format:

.. code:: sh

  @software{bibat,
    doi = {10.5281/zenodo.7775328},
    url = {https://github.com/teddygroves/bibat},
    year = {2023},
    author = {Teddy Groves},
    title = {Bibat: batteries-included Bayesian analysis template},
  }
