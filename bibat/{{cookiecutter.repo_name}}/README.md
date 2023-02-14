{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

# How to run the analysis

To run the analysis, run the command `make analysis` from the project root. This
will install a fresh virtual environment if one doesn't exist already, activate
it and install python dependencies and cmdstan, then run the analysis with the
following commands:

- `python prepare_data.py`
- `python sample.py`
- `jupyter execute investigate.ipynb`

{% if cookiecutter.docs_format == "Quarto" %}# How to create a pdf report

First make sure you have installed [quarto](https://https://quarto.org/).

Now run this command from the `docs` directory:

```
make report
```
{% endif %}

{% if cookiecutter.create_tests_directory == "y" %}# How to run tests

Run this command from the project root:

```
python -m pytest
```
{% endif %}
