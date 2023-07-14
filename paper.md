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

Bibat is a Python package that provides an interactive template for Bayesian
statistical analysis projects.

Bibat aims to make it easier to create software projects that implement a
Bayesian workflow that scales to arbitrarily many statistical models, data
transformations and fitting methods. It also aims to promote software
quality by providing a modular, automated and reproducible project that follows
Python programming best practices and integrates together many popular
statistical programming tools.

Bibat is "batteries included" in the sense that it creates a working example
project which the user can adapt so that it implements their desired analysis.
This style of template makes for better usability and easier testing of
Bayesian workflow projects compared with the alternative approach of providing
an incomplete skeleton project.

# Statement of need

There is a growing interest in the concept of Bayesian workflow, as shown by
papers like [@gelmanBayesianWorkflow2020],
[@grinsztajnBayesianWorkflowDisease2021] and
[@gabryVisualizationBayesianWorkflow2019]. There are software tools that
address most individual aspects of a Bayesian workflow, from fetching and
manipulating data to specifying, computing, storing, inspecting and documenting
statistical inferences. However, there are relatively few software tools that
address the problem of implementing a whole Bayesian workflow.

This issue is especially pronounced for non-trivial Bayesian workflows
involving many interacting, polytomous components (e.g. datasets, statistical
models, diagnostics). Software that implements such workflows is difficult to
write, and resources teaching how to do so are scarce, as pedagogical examples
typically focus on simple cases.

Interactive project templates are commonly used to address analogous issues
in software engineering and machine learning. Compared with writing software
from scratch, using a template is usually faster, promotes better code quality
and provides a focal point for practitioners to share and improve best
practices.

There is currently there is no popular interactive project template that
specifically targets software implementing a Bayesian workflow. There are some
templates that arguably encompass Bayesian workflow as a special case of data
analysis project, such as [@drivendataCookiecutterdatascience2022], but these
are of limited use compared with a specialised template due to the many
specificities of Bayesian workflow. For example, MCMC sampling produces data
that is best represented using more-than-two-dimensional labelled arrays, which
are not part of many data analysis workflows and are therefore not addressed by
[@drivendataCookiecutterdatascience2022].

# How bibat works

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
short description and choices of open source licence options, documentation
formats and whether to include tests and continuous integration.

Bibat then creates a folder with the chosen repository name in the current
working directory, containing code that implements bibat's example analysis.

The user can now navigate to the new folder and run the command `make
analysis`. Bibat will then install and activate a Python 3 virtual environment,
install dependencies including `cmdstan` and then run the example analysis and
save the results.

The next step is to edit the project so that it implements the target analysis
rather than the provided one. Bibat's documentation provides detailed
instructions for how to do this. The editing can be done incrementally: at each
step the user can check their work by repeating the command `make analysis`.

# Technical details about bibat

Bibat is implemented using Python 3. Its main dependencies are cookiecutter
[@greenfeldCookiecutter2021], pydantic [@pydanticdevelopersPydantic2022] and
click [@clickdevelopersClickPythonComposable2022]. Bibat is continuously tested
to ensure that it works on the operating systems Linux, macOS and Windows.

Bibat creates projects that use the following tools:

* Python 3 [@vanrossumPythonReferenceManual2009] and standard scientific Python
packages for data manipulation
* Stan [@carpenterStanProbabilisticProgramming2017] for specifying statistical
models and performing inferences
* cmdstanpy [@standevelopmentteamCmdStanPy2022] for interfacing between Python
and Stan
* arviz [@kumarArviZUnifiedLibrary2019] for storing and analysing completed
inferences
* pydantic and pandera [@niels_bantilan-proc-scipy-2020] for validation
* make [@stallman1991gnu] for automation.

Bibat also optionally sets up documentation using Sphinx
[@georgbrandlandthesphinxteamSphinx2022] or Quarto [@Allaire_Quarto_2022],
testing using pytest [@pytestdevelopersPytest2022] and continuous integration
using GitHub actions [@githubdevelopersGitHubActions2022].

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
several additional transformations and filtering operations in order to be
useable.

The full analysis can be found at
<https://github.com/teddygroves/bibat/bibat/examples/baseball>. A vignette
describing how the analysis was created, starting with bibat's example project,
is at <https://bibat.readthedocs.io/en/latest/_static/report.html>.

# Discussion
It is somewhat unusual for an interactive project template to take a "batteries
included" approach rather than providing an incomplete skeleton project as in,
for example, [@drivendataCookiecutterdatascience2022]. Compared to "batteries
included" templates, skeleton style templates can be smaller and less
opinionated, reducing the potential for errors and potentially allowing them to
be used in more situations.

The "batteries included" approach was preferred in this case for two main
reasons. First, it makes it possible to test the template from end to end
simply by running the provided example. Easy and relevant testing is especially
important for a Bayesian workflow template given the need to integrate many
third-party components that are under active development. The
batteries-included approach makes it easier to quickly surface and fix bugs or
interface changes resulting from changes to these components. Second, providing
a complete project makes it easier for users to learn how to use the template,
as the intended end state and usage is immediately visible.

# Acknowledgements
The author wishes to thank Lars Keld Nielsen for helpful feedback, and Mitzi
Morris, Bob Carpenter and Brian Ward for development advice.

# Funding
The development of `bibat` was supported by the Novo Nordisk Foundation,
specifically by grant numbers NNF20CC0035580 and NNF14OC0009473.

# References
