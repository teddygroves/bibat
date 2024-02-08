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

How to use bibat
================

To start a Bayesian statistical analysis project using bibat, first install `copier <https://copier.readthedocs.io>`_, for example like this:

.. code:: sh

    $ pipx install bibat

Now choose a directory name for your analysis, for example `my_cool_project`,
and copy bibat's example project there:

.. code:: sh

    $ copier copy gh:teddygroves/bibat my_cool_project

If you want to use bibat's Python api but not the example project, you can
install it to your python enviornment as follows:

.. code:: sh

    $ pip install bibat

Finally, to install bibat with development dependencies:

.. code:: sh

    $ pip install bibat'[development]'

Dependencies
============

Bibat requires Python version 3.11 or greater.

Bibat's Python dependencies can be found in its `pyproject.toml file <https://github.com/teddygroves/bibat/blob/main/pyproject.toml>`_.

Bibat's Python dependencies:

- arviz
- cmdstanpy
- copier
- numpy
- pandas
- pandera
- pydantic
- scikit-learn
- stanio
- toml
- xarray
- zarr

Bibat's development dependencies (install these by running :code:`pip install
bibat'[development]'`):

- black
- pre-commit
- codecov
- pytest
- pytest-cov
- tox
- sphinx
- sphinx-click
- ruff
- furo

Projects created by bibat have Python dependencies listed in their `pyproject.toml file <https://github.com/teddygroves/bibat/blob/main/bibat/template/pyproject.toml.jinja>`. The additional ones are as follows:

- bibat
- jupyter

In addition, the following Python packages may be installed, depending on how
the user answers bibat's questionnaire:

- sphinx

Bibat projects also depend on `cmdstan
<https://mc-stan.org/docs/cmdstan-guide/index.html>`__, the command line
interface to Stan. Bibat projects include code that installs cmdstan when you
run the command :code:`make analysis` from the root of the target project. To only install dependencies, you can also run the command :code:`make env`.

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
