====================================================
Bibat: Batteries-Included Bayesian Analysis Template
====================================================

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

Quick Start
===========

You can try out bibat like this (make sure you are in a Python environment where
you would like to install bibat and `its dependencies
<https://github.com/teddygroves/bibat/blob/main/setup.cfg#L28>`_):

.. code:: sh

    $ pip install bibat
    $ bibat

After following the wizard's instructions, you should now have a new directory
implementing a simple statistical analysis. To try it out, run the following
command from the root of the new directory:

.. code:: sh

    $ make analysis

To install the latest version from github:

.. code:: sh

    $ pip install git+https://github.com/teddygroves/bibat.git@main
