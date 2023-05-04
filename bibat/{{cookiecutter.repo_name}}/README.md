{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

# How to run the analysis

To run the analysis, run the command `make analysis` from the project root. This
will install a fresh virtual environment if one doesn't exist already, activate
it and install python dependencies and cmdstan, then run the analysis with the
following commands:

- `python {{cookiecutter.repo_name}}/prepare_data.py`
- `python {{cookiecutter.repo_name}}/sample.py`
- `jupyter execute {{cookiecutter.repo_name}}/investigate.ipynb`

{% if cookiecutter.docs_format == "Quarto" %}# How to create a pdf report

First make sure you have installed [quarto](https://https://quarto.org/).

Now run this command from the project root:

```
make docs
```
{% endif %}

{% if cookiecutter.docs_format == "Sphinx" %}# How to build Sphinx documentation

Run this command from the project root:

```
make docs
```
{% endif %}

{% if cookiecutter.create_tests_directory == "y" %}# How to run tests

Run this command from the project root:

```
python -m pytest
```
{% endif %}
