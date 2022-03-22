===============================================
Contributing to cookiecutter-cmdstanpy-analysis
===============================================

All contributions are very welcome!

If you have a specific suggestion for how cookiecutter-cmdstanpy-analysis could be
improved, or if you find a bug then please file an issue or submit a pull
request.

Alternatively, if you have any more general thoughts or questions, please post
them in the `discussions page <https://github.com/teddygroves/cookiecutter-cmdstanpy-analysis/discussions>`_.

If you'd like to contribute code changes, just follow the normal github workflow.

To test changes to the template locally, I recommend avoiding having to complete the wizard every time by making a `yaml <https://yaml.org/>`_ config file like this (copied from the file :literal:`tests/data/example_config.yml`):

.. code:: yaml

    default_context:
      project_name: "My Cool Project"
      repo_name: "my_cool_project"
      author_name: "Dr Statistics"
      description: "I used cookiecutter, cmdstanpy and arviz to do an analysis."
      open_source_license: "MIT"
      docs_format: "Markdown"
      create_tests_directory: "y"
      create_dotgithub_directory: "y"

You should now be able to create a :literal:`my_cool_project` cmdstanpy project like this:

.. code:: sh

    $ cookiecutter --no-input --config-file path/to/config.yml path/to/cookiecutter-cmdstanpy-analysis
