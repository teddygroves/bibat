.. _contributing:

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

If you'd like to contribute code changes, just follow the normal github
workflow.

You can install bibat with development dependencies like this:

.. code:: sh

    $ pip install bibat'[development]'

To test changes to the template locally, I recommend avoiding having to complete
the wizard every time by making a `yaml <https://yaml.org/>`_ config file like
this (copied from the file :literal:`tests/data/example_config.yml`):

.. literalinclude:: ../tests/data/example_config.yml
    :language: yaml

You should now be able to create a :literal:`my_cool_project` bibat project like this:

.. code:: sh

    $ bibat --config-file path/to/config.yml

To release a new version of bibat, edit the field :code:`version` in the file
:code:`setup.cfg`, e.g. to :code:`0.2.1` then make a pull request with this
change.

Once the changes are merged into the :code:`origin/master` branch, add a tag
whose name begins with :code:`v`, followed by the new version number to your
local :code:`master` branch, for example like this:

.. code:: bash

          git tag v0.2.1

Now push the new tag to github:

.. code:: bash

          git push origin "v0.2.1"
