---
title: 'Bibat: batteries-included Bayesian analysis template'
tags:
  - Python
  - Statistical computing
  - Bayesian workflow
  - tooling
  - Interactive project template
authors:
  - name: Teddy Groves
    orcid: 0000-0002-7109-3270
    equal-contrib: true
    affiliation: 1
affiliations:
 - name: The Novo Nordisk Foundation Center for Biosustainability
   index: 1
date: 17 Feb 2023
bibliography: bibliography.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary
Bibat is a Python package providing a flexible interactive template for Bayesian
statistical analysis projects. 

It aims to make it easier to create software projects that implement a Bayesian
workflow that scales to arbitrarily many inter-related statistical models, data
transformations, inferences and computations. Bibat also aims to promote
software quality by providing a modular, automated and reproducible project that
takes advantage of and integrates together the most up to date statistical
software.

Bibat comes with "batteries included" in the sense that it creates a working
example project, which the user can adapt so that it implements their desired
analysis. We believe this style of template makes for better usability and
easier testing of Bayesian workflow projects compared with the alternative
approach of providing an incomplete skeleton project.

# Statement of need
[@gelmanBayesianWorkflow2020] makes a compelling argument that, both in theory
and practice, statisticians should explicitly recognise that applied data
analysis projects typically involve many inter-related statistical models, data
transformations, inferences and computations.

However, there is currently little software that addresses Bayesian data
analysis at the level of workflows. As a result, software that implements a
Bayesian workflow for the purposes of a particular analysis is largely written
by hand from scratch, following the design choices of an individual practitioner
or team at the time they wrote the project. This practice wastes effort as much
work is duplicated, and leads to sub-optimal software quality as expertise is
not shared between practitioners (or between the same practitioner at different
times).

Interactive project templates are an obvious solution to this problem, as they
are already commonly used by software developers and machine learning
practitioners to avoid wasted effort and share best practices when creating
software projects that implement complex workflows. 

There is currently there is no popular interactive project template that
specifically targets software implementing a Bayesian workflow. There are some
templates that arguably encompass Bayesian workflow as a special case of data
analysis project, such as [@drivendataCookiecutterdatascience2022], but these
are of limited use compared with a specialised template due to the many
specificities of Bayesian workflow. For example, MCMC sampling produces data
that is best represented using more-than-two-dimensional labelled arrays, which
are not part of many data analysis workflows and are therefore not addressed by
[@drivendataCookiecutterdatascience2022].

Bibat targets projects that use Python 3 [@vanrossumPythonReferenceManual2009]
and its standard scientific toolbox for data manipulation, Stan
[@carpenterStanProbabilisticProgramming2017] for specifying statistical models
and performing inference, cmdstanpy [@standevelopmentteamCmdStanPy2022] for
interfacing between Python and Stan, arviz [@kumarArviZUnifiedLibrary2019] for
storing and analysing completed inferences, pydantic
[@pydanticdevelopersPydantic2022] and pandera [@niels_bantilan-proc-scipy-2020]
for validation and make [@stallman1991gnu] for automation. Bibat also optionally
provides for documentation using Sphinx [@georgbrandlandthesphinxteamSphinx2022]
or Quarto [@Allaire_Quarto_2022], testing using pytest
[@pytestdevelopersPytest2022] and continuous integration using github actions
[@githubdevelopersGitHubActions2022].

Bibat is implemented using Python 3, the popular interactive template library
`cookiecutter` [@greenfeldCookiecutter2021], as well as pydantic and click
[@clickdevelopersClickPythonComposable2022]. Bibat is continuously tested to
ensure that it works on the operating systems Linux, macos and Windows. 

Detailed documentation can be found at
<https://bibat.readthedocs.io/en/latest/>.

bibat is linked on the [cmdstanpy community
website](https://mc-stan.org/cmdstanpy/community.html) and is used in several
active research projects: see [this documentation page](https://bibat.readthedocs.io/en/latest/examples.html) for a list.

# Installation and usage
Bibat is installed by running the command `pip install bibat` and then used by
running the command `bibat`.

This command triggers an interactive form which prompts the user for
configuration information including project and repository name, author name, a
short description and choices of open source license options, documentation
formats and whether or not to include tests and continuous integration.

A folder with the chosen repository name will then be created in the current
working directory, containing code that implements the provided example
analysis, from raw data to results and documentation.

This analysis includes two data processing rules, a single statistical model
(additional models can easily be added) and two model configuration files each
specifying a statistical model, prepared dataset and computation settings.

The user can now navigate to the new folder and run the command `make
analysis`. This will install a Python 3 virtual environment, activate it,
install dependencies including `cmdstan`, run all data preparation operations,
perform inference for all model configurations in all specified modes (provided
modes are prior, posterior and exact k-fold cross-validation), save the results
of these inferences and perform downstream analysis.

The next step is to edit the project so that it implements the target analysis
rather than the provided one. This can be done incrementally: after any change
the user can check that the whole analysis works by repeating the command `make
analysis`. Since bibat follows a modular design, individual steps of the
analysis can easily be tested in isolation by running the corresponding Python
script.

# Case study: baseball
![Results of a statistical analysis implemented using bibat, involving two
models and two datasets. The blue and orange lines show the 1% to 99% marginal
posterior quantiles for latent success probabilities from two statistical
models, alongside the actually realised probabilities, represented as black
dots. \label{fig:01}](docs/_static/posterior_quantiles.png)

Figure \autoref{fig:01} shows the results of a case study demonstrating how
bibat can be used in a Bayesian workflow.

The case study compares two Bayesian hierarchical regression models fit to two
datasets from major league baseball. One statistical model assumes that batters
have latent success probabilities that follow a normal distribution on logit
scale; the other model assumes that these quantities follow a generalised Pareto
distribution. One dataset is copied from a previous analysis by another author
for validation and easy comparison with other work, while the other, larger
dataset is taken from a public data repository. The larger dataset required
several additional transformation and filtering operations in order to be
useable.

The full analysis, as well as an explanatory vignette, can be found at
<https://github.com/teddygroves/bibat/bibat/examples/baseball>.

# Discussion
It is somewhat unusual for an interactive project template to take a "batteries
included" approach rather than providing an incomplete skeleton project as in,
for example, [@drivendataCookiecutterdatascience2022]. Compared to "batteries
included" templates, skeleton style templates can be smaller and less
opinionated, reducing the potential for errors and potentially allowing them to
be used in more situations.

The "batteries included" approach was preferred in this case for two main
reasons. First, it makes it possible to test the template from end to end simply
by running the provided example. Easy and relevant testing is especially
important for a Bayesian workflow template given the need to integrate many
state of the art libraries that are under active development. Since the overall
workflow depends on all these libararies inter-operating, it is important to
quickly surface and fix bugs or interface changes. Second, providing a complete
project makes it easier for users to learn how to use the template, as the
intended end state and usage is immediately visible.

# Acknowledgements
The author wishes to thank Lars Keld Nielsen for helpful feedback, and Mitzi
Morris, Bob Carpenter, Brian Ward for development advice.

# Funding
The development of `bibat` was supported by the Novo Nordisk Foundation,
specifically by grant numbers NNF20CC0035580 and NNF14OC0009473.

# References
