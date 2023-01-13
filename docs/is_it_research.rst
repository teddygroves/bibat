But is bibat *research* software?
---------------------------------

`The Journal of Open Source Software
<https://joss.readthedocs.io/en/latest/submitting.html#what-we-mean-by-research-software>`_
defines "research software" as follows:

| JOSS publishes articles about research software. This definition includes software that: solves complex modeling problems in a scientific context (physics, mathematics, biology, medicine, social science, neuroscience, engineering); supports the functioning of research instruments or the execution of research experiments; extracts knowledge from large data sets; offers a mathematical library, or similar. While useful for many areas of research, pre-trained machine learning models and notebooks are not in-scope for JOSS.

Based on this Whether bibat satisfies the definition above therefore depends on how
much directness the authors intended to be implicit in the terms "solves" and
"extracts".

At one extreme, it might be argued that no software can really solve scientific
problems or extract knowledge from data, as general artificial intelligences
with the ability to do science or know things have not yet been invented. On the
other extreme, it might also be argued that any software that could potentially
be used as part of a scientific project or knowledge-extraction exercise
satisfies the definition. To find out where the original authors sit between
these extremes, we can look at some examples of comparable software projects
that has been found to satisfy JOSS's research software definition.

`fseval <https://github.com/dunnkers/fseval>`_ is a Python package that provides
a framework for feature selection benchmarking projects in the context of
machine learning, and was considered research software by JOSS. fseval and bibat
are fundamentally similar, except for the difference in target project. Both
packages solve complex modelling problems and extract knowledge from data in the
same way: by providing abstract structures defining the inputs, outputs and
components of a data analysis workflow and helping scientists to use them. In
particular, neither package contains an original data analysis algorithm.

`Asimov <https://git.ligo.org/asimov/asimov>`_ is a Python package for creating,
automating and monitoring arbitrary scientific data analysis workflows that JOSS
considers research software. Like bibat and fseval it does not provide novel
modelling algorithms, but helps scientists to solve problems and extract
knowledge from data by providing abstractions. Like bibat, Asimov provides a
curated directory structure and convenience commands for running an analysis.

`datawizard <https://github.com/easystats/datawizard>`_ is an R package that
provides functions that carry out common data manipulation tasks in the context
of statistical analyses and is considered research software by JOSS. It does not
contain novel modelling algorithms, but like bibat is a tool for helping
scientists to solve complex modelling problems and extract knowledge from
data. Incidentally many of the data manipulation functions provided by
datawizard are either accessible to bibat users using the standard Python data
analysis stack or else provided by the :code:`util` module that bibat provides.

Taken together, these examples show that the JOSS definition is intended to
accommodate software that does not contain original data analysis algorithms,
but that helps scientists to solve problems and extract knowledge from data with
about the same level of indirectness as bibat. Further, software of this kind
that is specifically aimed at statistical analysis projects is considered within
scope, as is software that creates a custom directory structure and that defines
conventions that abstract parts of a data analysis workflow.
