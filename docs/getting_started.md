# Getting started

## How to copy bibat's template

To start a new Bayesian workflow project using bibat, first install [copier]
(https://copier.readthedocs.io/en/stable/), e.g. like this:

```sh
$ pipx install copier
```

Now choose a name for your project, for example `my_cool_project`, then copy
bibat's template like this:

```sh
$ copier copy gh:teddygroves/bibat my_cool_project
```

Running this command will trigger a command line wizard.

If you already know how you are going to answer the wizard's questions, you can
put your answers in a yaml file with relative path `my_yaml_file.yml` and run
copier like this:

```
$ copier copy --data-file my_yaml_file.yml gh:teddygroves/bibat my_cool_project
```

A new directory will now be created at `my_cool_project` that implements a
simple statistical analysis. To try out the example analysis, run the following
command from the root of the new directory:

```
$ cd my_cool_project
$ make analysis
```

## How to use bibat's Python code

You can install bibat as a python package like this (make sure you are in a
Python environment where you would like to install bibat):

```sh
$ pip install bibat
```

To install the latest version of bibat from GitHub:

```
$ pip install git+https://github.com/teddygroves/bibat.git@main
```

Now you can import bibat code in python:

```python
from bibat.inference_configuration import InferenceConfiguration
```

Check out bibat's [api documentation](api.md) for details about bibat's Python
code.
