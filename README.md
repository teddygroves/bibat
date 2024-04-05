# Bibat: Batteries-Included Bayesian Analysis Template

[![](https://zenodo.org/badge/344553551.svg)](https://zenodo.org/badge/latestdoi/344553551)
[![Documentation Status](https://readthedocs.org/projects/bibat/badge/?version=latest)](https://bibat.readthedocs.io/en/latest/?badge=latest)
[![Tox](https://github.com/teddygroves/bibat/actions/workflows/run_tox.yml/badge.svg)](https://github.com/teddygroves/bibat/actions/workflows/run_tox.yml)
[![Test end-to-end](https://github.com/teddygroves/bibat/actions/workflows/test_end_to_end.yml/badge.svg)](https://github.com/teddygroves/bibat/actions/workflows/test_end_to_end.yml)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Supported Python versions: 3.11 and newer](https://img.shields.io/badge/python->=3.11-blue.svg)](https://www.python.org/)
[![](https://badge.fury.io/py/bibat.svg)](https://badge.fury.io/py/bibat)
[![](https://codecov.io/github/teddygroves/bibat/branch/main/graph/badge.svg?token=ck0IKyzP7J)](https://codecov.io/github/teddygroves/bibat)
[![pyOpenSci](https://tinyurl.com/y22nb8up)](https://github.com/pyOpenSci/software-review/issues/83)

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

## Documentation

Check out bibat's documentation at <https://bibat.readthedocs.io>.

In particular, you may find it useful to have a look at [this vignette](https:// bibat.readthedocs.io/en/latest/_static/report.html) that demonstrates, step by
step, how to use bibat to implement a complex statistical analysis.

## How to use bibat

To start a Bayesian statistical analysis project using bibat, first install [copier](https://copier.readthedocs.io), for example like this:

```sh
$ pipx install copier
```

Now choose a directory name for your analysis, for example `my_cool_project`,
and copy bibat's example project there:

```sh
$ copier copy gh:teddygroves/bibat my_cool_project
```

This will trigger an interactive questionnaire and then create a brand
new, custom, batteries-included, Bayesian analysis project in the directory
`my_cool_project`. See [bibat's documentation](https://bibat.readthedocs.io) for
what to do next.

If you want to use bibat's Python code separately from the template, you can
install it to your python environment as follows:

```sh
$ pip install bibat
```

To install bibat with development dependencies:

```sh
$ pip install bibat'[development]'
```

## Dependencies

Bibat requires Python version 3.11 or greater.

Bibat's Python dependencies can be found in its [pyproject.toml file](https://github.com/teddygroves/bibat/blob/main/pyproject.toml).

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

Bibat's development dependencies (install these by running `pip install
bibat'[development]'`):

- black
- pre-commit
- codecov
- mkdocs
- mkdocs-material
- mkdocstrings
- mkdocstrings-python
- pymdown-extensions
- pytest
- pytest-cov
- tox
- ruff

Projects created by bibat have Python dependencies listed in their [pyproject.toml file](https://github.com/teddygroves/bibat/blob/main/template/pyproject.toml.jinja). The additional ones are as follows:

- bibat
- jupyter

In addition, the following Python packages may be installed, depending on how
the user answers bibat's questionnaire:

- sphinx

Bibat projects also depend on [cmdstan](https://mc-stan.org/docs/cmdstan-guide/index.html), the command line
interface to Stan. Bibat projects include code that installs cmdstan when you
run the command `make analysis` from the root of the target project. To only install dependencies, you can also run the command `make env`.

If bibat fails to install cmdstan, please raise an issue! The relevant
parts of the [cmdstan](https://mc-stan.org/docs/cmdstan-guide/cmdstan-installation.html) and
[cmdstanpy](https://cmdstanpy.readthedocs.io/en/v1.1.0/installation.html#cmdstan-installation)
documentation might also be useful.

### Target project dependencies: Quarto

Bibat supports automatic generation of documentation using either Sphinx or
[Quarto](https://quarto.org/). Whereas bibat will install Sphinx
automatically, Quarto must be installed manually: see the [quarto
documentation](https://quarto.org/docs/get-started/) for instructions.

## Citation information

If you would like to cite bibat using bibtex please use the following format:


```sh
  @software{bibat,
    doi = {10.5281/zenodo.7775328},
    url = {https://github.com/teddygroves/bibat},
    year = {2023},
    author = {Teddy Groves},
    title = {Bibat: batteries-included Bayesian analysis template},
  }
```
