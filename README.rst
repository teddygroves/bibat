===============================
cookiecutter-cmdstanpy-analysis
===============================

cookiecutter-cmdstanpy analysis is a `cookiecutter <https://cookiecutter.readthedocs.io/>`_ template for statistical analysis templates that use `Stan <https://mc-stan.org/>`_, `cmdstanpy <https://cmdstanpy.readthedocs.io/en/v1.0.1/>`_ and `arviz <https://arviz-devs.github.io/>`_.

Documentation
=============
Check out cookiecutter-cmdstanpy-analysis's documentation at `https://cookiecutter-cmdstanpy-analysis.readthedocs.io <https://cookiecutter-cmdstanpy-analysis.readthedocs.io>`_.

Quick Start
===========

You can try out cookiecutter-cmdstanpy-analysis like this:

.. code:: sh

    $ pip install cookiecutter
    $ cookiecutter gh:teddygroves/cookiecutter-cmdstanpy-analysis

After following the wizard's instructions, you should now have a new directory implementing a simple statistical analysis. To try it out, install python dependencies and cmdstan, then run the analysis:

.. code:: sh
    $ cd my_cool_project
    $ pip install -r requirements.txt
    $ install_cmdstan
    $ make analysis

