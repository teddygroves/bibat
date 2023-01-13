====================================================
Bibat: Batteries-Included Bayesian Analysis Template
====================================================

Bibat is a Python package that wraps a `cookiecutter
<https://cookiecutter.readthedocs.io/>`_ template for Bayesian statistical
analyses. 

It aims to make it easier for authors of statistical analyses to follow best
practices from both software development and statistics, and to be flexible
enough that any analysis can be implemented - even ones involving many complex
data processing options and statistical models.

Bibat is "batteries-included" in the sense that the template provides a complete
statistical analysis that you can run immediately.

Documentation
=============

Check out bibat's documentation at `https://bibat.readthedocs.io
<https://bibat.readthedocs.io>`_.

In particular, you may find it useful to have a look at `some projects that have
previously used bibat <https://bibat.readthedocs.io/en/latest/examples.html>`_.

Quick Start
===========

You can try out bibat like this:

.. code:: sh

    $ pip install bibat
    $ bibat

After following the wizard's instructions, you should now have a new directory
implementing a simple statistical analysis. To try it out, run the following
command from the root of the new directory:

.. code:: sh

    $ make analysis


