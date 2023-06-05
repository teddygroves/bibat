.. _contributing:

============
Contributing
============

All contributions are very welcome!

Make sure to read the `code of conduct
<https://github.com/teddygroves/bibat/CODE_OF_CONDUCT.md>`_ and follow its
recommendations.

If you have a specific suggestion for how bibat could be improved, or if you
find a bug then please file an issue or submit a pull request.

Alternatively, if you have any more general thoughts or questions, please post
them in the `discussions page
<https://github.com/teddygroves/bibat/discussions>`_.

If you would like to contribute code changes, just follow the normal `GitHub
workflow <https://docs.github.com/en/get-started/quickstart/github-flow>`_:
make a local branch with the changes then create a pull request.

Developing bibat locally
------------------------

To develop bibat locally you will probably need to install it with development
dependencies. Here is how to do so:

.. code:: sh

    $ pip install bibat'[development]'

You can see what these dependencies are by checking the
:code:`[project.optional-dependencies]` table in bibat's `pyproject.toml file
<https://github.com/teddygroves/bibat/blob/main/pyproject.toml>`_. Some
important ones are `black <https://github.com/psf/black>`_,
`isort <https://pycqa.github.io/isort/>`_,
`pre-commit <https://pre-commit.com/>`_ and `tox <https://tox.wiki/en/latest/>`_.

Another thing you will want to do while developing bibat locally is use it to
create projects. For this I recommend avoiding having to complete
the wizard every time by making a `yaml <https://yaml.org/>`_ config file like
this (copied from the file :literal:`tests/data/example_config.yml`):

.. literalinclude:: ../tests/data/example_config.yml
    :language: yaml

After making such a file you will be able to create a bibat project without
completing the wizard like this:

.. code:: sh

    $ bibat --config-file path/to/config.yml


Cmdstan
-------

Bibat depends on `cmdstan <https://github.com/stan-dev/cmdstan>`__, which can be
tricky to install. If you run the commands :code:`make env` or :code:`make
analysis` from a bibat project, it will attempt to install cmdstan
automatically. If this doesn't work, please check the `cmdstan
<https://mc-stan.org/users/interfaces/cmdstan>`__ and `cmdstanpy
<https://cmdstanpy.readthedocs.io/en/v1.1.0/installation.html#cmdstan-installation>`__
documentation.

Releasing new versions of bibat
-------------------------------

To release a new version of bibat, edit the field :code:`version` in the file
:code:`setup.cfg`, e.g. to :code:`0.2.1` then make a pull request with this
change.

Once the changes are merged into the :code:`origin/master` branch, add a tag
whose name begins with :code:`v`, followed by the new version number to your
local :code:`master` branch, for example like this:

.. code:: bash

          git tag v0.2.1

Now push the new tag to GitHub:

.. code:: bash

          git push origin "v0.2.1"
