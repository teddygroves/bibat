---
title: 'cookiecutter-cmdstanpy-analysis: an interactive template for statisical analysis projects'
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
date: 13 August 2017
bibliography: bibliography.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary
A common task in many applied scientific fields is to write software that
carries out a statistical analysis involving a range of statistical models and
data-processing options. It is important for this software to have the best
possible quality, both to avoid errors and so that others can contribute,
borrow, extend and reproduce it. Unfortunately, writing a high quality software
project from scratch is time-consuming and difficult.

Interactive templates make it possible to avoid starting software projects from
scratch: instead, a custom project is created automatically after executing a
command and completing a short interactive form. If the template is
well-crafted, it is easier to edit the resulting files and folders so that they
implement a desired target project than it is to create the target project from
scratch. In addition to the saved effort, interactive project templates promote
the use of sensible defaults, thereby improving software quality. Popular
interactive project templates include [@drivendataCookiecutterdatascience2022],
[@salemTensorflowProjectTemplate2018], [@huangPytorchtemplate2020] and
[@cookiecutter-cmsdevelopersCookiecuttercmsCookiecutterComputational2022]. However,
interactive project templates are not widely used for statistical analysis
projects.

# Statement of need
`cookiecutter-cmdstanpy-analysis` is an interactive template for statistical
analysis projects written with Python 3 [@vanrossumPythonReferenceManual2009]
and Stan [@carpenterStanProbabilisticProgramming2017]. It aims to make it easier
for users to follow the workflow set out in [@gelmanBayesianWorkflow2020] for
any statistical analysis that can be implemented using these tools, and provides
functionality for users to automate, test, document and continuously integrate
their analysis. In addition, `cookiecutter-cmdstanpy-analysis` takes a
"batteries included" approach, so that users start from a complete working
example project rather than an incomplete skeleton project.

`cookiecutter-cmdstanpy-analysis` uses the widely-used interactive template
library `cookiecutter` [@greenfeldCookiecutter2021]. It targets projects that
use the standard scientific Python toolbox for data fetching and manipulation,
Stan for statistical model definitions and computation, `cmdstanpy`
[@standevelopmentteamCmdStanPy2022] for Python to Stan interface, `arviz`
[@kumarArviZUnifiedLibrary2019] for storing results and downstream analysis and
[@make] \citep{stallman1991gnu} for automation. Users can optionally document
their work using Sphinx [@georgbrandlandthesphinxteamSphinx2022] or markdown,
test it using pytest [@pytestdevelopersPytest2022] and implement continuous
integration using github actions
[@githubdevelopersGitHubActions2022]. `cookiecutter-cmdstanpy-analysis` itself
is continuously tested to ensure that it works on the operating systems Linux,
macos and Windows. Detailed documentation can be found at
\href{https://cookiecutter-cmdstanpy-analysis.readthedocs.io/en/latest/}{https://cookiecutter-cmdstanpy-analysis.readthedocs.io/en/latest/}.

# Usage
After installing `cookiecutter` with the command `pip install cookiecutter`,
`cookiecutter-cmdstanpy-analysis` can be used by running the command
`cookiecutter gh:teddygroves/cookiecutter-cmdstanpy-analysis`. An interactive
form then prompts the user for configuration information including project and
repository name, author name, a short description and choices of open source
license options, documentation formats and whether or not to include tests and
continuous integration.

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
analysis`. Since `cookiecutter-cmdstanpy-analysis` follows a modular design,
individual steps of the analysis can easily be tested in isolation by running
the corresponding Python script.

# Case study: mRNA regulation
![(a) Target system 
  (b) Sample of mRNA timecourses from the original analysis using ABC 
  (c) Sample of mRNA timecourses from a reproduction of the original analysis using MCMC. Note prior bias (most timecourses are too low) and posterior overfitting (every posterior timecourse is very close to every observation). 
  (d) Samples of mRNA timecourses from an improved analysis using lognormal priors and simulated data incorporating noise. \label{fig:01}
  ](fig.png)

Figure \ref{fig:01} shows the results of a case study demonstrating how
`cookiecutter-cmdstanpy-analysis` can be used in applied science. The full
analysis can be found at
[https://github.com/teddygroves/mrna](https://github.com/teddygroves/mrna).

The case study builds on an example in
[@liepeFrameworkParameterEstimation2014] which models measurements of the
translation and self-regulation of mRNA using the parameterised kinetic
mechanism shown in figure \ref{fig:01}, frame a. This mechanism was embedded
within a statistical model with a curated prior distribution and no explicit
likelihood, which was fitted using approximate Bayesian computation. This approach
cannot explicitly represent information about measurement error and generated
unrealistically jagged timecourses as shown in frame b.

The author used `cookiecutter-cmdstanpy-analysis` to augment the original
statistical model with a plausible explicit likelihood and fit it using
Hamiltonian Monte Carlo in prior and posterior modes. A sample of the resulting
timecourses is shown in frame c. This revealed problems with the statistical
model that were not obvious in the original analysis: the prior yielded
implausible timecourses and the posterior appeared over-fitted due to the
absence of noise in the original measurements. These problems were addressed by
adding a new model configuration with better prior distributions and more
realistic simulated measurements, leading to the timecourses shown in frame d.

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
important for a statistical analysis project template because of the large
number of interacting components, many of which are typically under active
development and may become incompatible with each other over time. Second,
providing a complete project makes it easier for users to learn how to use the
template, as the intended end state and usage is immediately visible.

# Acknowledgements
The author wishes to thank Lars Keld Nielsen for helpful feedback, and Mitzi
Morris, Bob Carpenter, Brian Ward for development advice.

# Funding
The development of `cookiecutter-cmdstanpy-analysis` was supported by the Novo
Nordisk Foundation, specifically by grant numbers NNF20CC0035580 and
NNF14OC0009473.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References
