========================================
Why use a statistical analysis template?
========================================

A small statistical statistical analysis can often be done by a single script or notebook file. This is really nice because the file is easy to keep track of and work with. Unfortunately the single file often starts to get a bit big: a few models have to be compared, there are a few data input options to consider, several plots need drawing, it would be nice to test the models against some fake data, and so on.

Luckily `Stan <https://mc-stan.org/>`_ and python libraries like `cmdstanpy <https://cmdstanpy.readthedocs.io/>`_ and `arviz <https://arviz-devs.github.io/arviz/>`_ support splitting your analysis up into multiple files when it starts getting unwieldy. Still, lots of decisions need to be made about how exactly to do this and it can be tricky and tedious to choose and implement a good layout and then remember it at the start of every new project.

cookiecutter-cmdstanpy-analysis addresses this problem by implementing a flexible but still effort-saving template. Instead of writing everything from scratch, you can start with this template and edit it to match your specific use case.

The structure is meant to be general enough to support a range of typical statistical workflows, from fitting a single model once to a single dataset to fitting arbitrary combinations of models and datasets in prior, posterior and kfold-cross-validation modes. 
