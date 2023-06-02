Baseball
==============================

Comparison of distributions for modelling baseball hitting

# How to run the analysis

To run the analysis, run the command `make analysis` from the project root. This
will install a fresh virtual environment if one doesn't exist already, activate
it and install python dependencies and cmdstan, then run the analysis with the
following commands:

- `python baseball/prepare_data.py`
- `python baseball/sample.py`
- `jupyter execute baseball/investigate.ipynb`

# How to create a pdf report

First make sure you have installed [quarto](https://https://quarto.org/).

Now run this command from the project root:

```
make docs
```
