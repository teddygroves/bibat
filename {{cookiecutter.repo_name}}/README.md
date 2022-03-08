{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

# How to install dependencies

Run this command from the project root:

```
pip install -r requirements.txt
install_cmdstan
```

# How to run the analysis

To run the analysis, run the command `make analysis` from the project root.

This will run the following python scripts:

- `prepare_data.py`
- `sample.py`
- `analyse.py`

{% if cookiecutter.docs_format == "Markdown" %}# How to create a pdf report

First make sure you have installed [pandoc](https://pandoc.org).

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
