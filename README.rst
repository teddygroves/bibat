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

See `here
<https://github.com/teddygroves/bibat/blob/main/bibat/cookiecutter.json>`_ for
the information you need to create a suitable json file.


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
