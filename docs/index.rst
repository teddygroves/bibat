=================================
Welcome to bibat's documentation!
=================================


bibat is an interactive template for Bayesian statistical analysis projects that
uses `cookiecutter <https://cookiecutter.readthedocs.io/en/latest/>`_, `Stan
<https://mc-stan.org/>`_, `cmdstanpy <https://cmdstanpy.readthedocs.io/>`_ and
`arviz <https://arviz-devs.github.io/arviz/>`_. It takes a 'batteries-included'
approach, creating a whole working project rather than a skeleton.

The :ref:`getting started` section explains how to install bibat and use
it to easily create a folder containing a complete example Bayesian statistical
analysis project.

The next thing you will probably want to do is edit the example analysis so that
it does something different. To find out how to do that, get acquainted with
bibat's :ref:`intended workflow`, check out the section on :ref:`editing the
example analysis` or explore some of the :ref:`vignettes`.

But wait, why did you do all of that? What was the point of this so-called
"batteries-included template" anyway? The :ref:`motivation` section attempts to
explain.

If you would like to contribute to bibat in any way (please do this!), the
:ref:`contributing` section has some useful information.

.. _getting started:

Getting started
===============

You can use bibat to start your statistical analysis project like this:

.. code:: shell

   pip install bibat
   bibat

After asking you some questions through a wizard, bibat will create a directory
containing a complete Bayesian statistical analysis project, whose results you
can reproduce like this:

.. code:: shell

   cd my_cool_project
   make analysis


.. _intended workflow:

Intended workflow
=================

bibat assumes that a statistical analysis consists of the following components:

- **Raw data**
- **Data prepratation functions** each of which take in raw data and produce prepared data
  that fit a common structure.
- **Statistical models**
- **Inferences**, i.e. combinations of a prepared dataset, a statistical model,
  a choice of which modes to fit the model in (for example
  prior mode, posterior mode and exact k-fold cross-validation mode) and how
  exactly to do so, and the results of doing this fitting.
- **Investigations** that do things with inferences and prepared data, such as
  making plots.
- **Documentation**

These terms are all pretty standard, except "Inference", which has a more
specific than normal meaning in this context. This choice was made to avoid
creating new jargon, and in order to match the arviz concept of `InferenceData
<https://arviz-devs.github.io/arviz/api/inference_data.html>`_.
  
To perform a statistical analysis means running a set of data preparation
functions, then carrying out a set of inferences, doing some investigations and
providing some documentation. bibat provides functionality for conveniently
doing these things, as well as explicit and convenient representations of all
the components and even a ready-made working example project.

bibat's strategy for representing the components of a statistical analysis is as
follows:

- Raw data are files that live in the directory :code:`data/raw`.
- A common structure for prepared data is specified by a Python class
  :code:`PreparedData` in the directory :code:`src/prepared_data.py`, which can
  be saved to files in the directory :code:`prepared_data` and later recovered
  from those files.
- Data preparation functions are python functions in the file
  :code:`src/data_preparation.py`, each of which returns a `PreparedData`.
- Statistical models are Stan programs in the directory :code:`src/stan`
- Inferences are subdirectories of the directory :code:`inferences`. Each such
  subdirectory contains a file called :code:`config.toml` that chooses a
  prepared dataset, statistical model and some fitting modes, as well as sampler
  configuraiton. When the analysis is run the folder is populated with an
  :code:`InferenceData` object saved in the file :code:`idata.json`, containing
  samples and debug information.
- Investigations are performed literately using the notebook file
  :code:`investigate.ipynb`, which saves plots to the directory :code:`plots`.
- Documentation lives in the directory :code:`docs`, and can be written using a
  range of standard formats including markdown and Sphinx.

The analysis is performed by setting up a suitable programming environment and
then running the Python scripts :code:`prepare_data.py` and :code:`sample.py`,
which live in the project root, executing the notebook file
:code:`execute.ipynb` and building the documentation. These tasks are automated
using the makefile :code:`Makefile`, so that the entire analysis can be
performed using the command :code:`make analysis` while avoiding unnecessarily
re-running any tasks.

After running the analysis, the next step is to make some changes and run a new analysis. This can be done by editing any of the files representing the analysis's component parts, then re-running the command :code:`make analysis`.

.. _editing the example analysis:

Editing the example analysis
============================

This section illustrates how to create a custom statistical analysis using bibat
through examples of common tasks.

Changing the definition of prepared data
----------------------------------------

Bibat's starting analysis has a :code:`PreparedData` class with three
attributes: :code:`name`, :code:`coords` and :code:`measurements`. Perhaps, for
your analysis you would prefer a different definition of prepared data with
another attribute: a pandas DataFrame called :code:`groups`, with columns
:code:`name`, :code:`colour` and :code:`number_of_legs`. You would also like
some rules to be enforced: names should be non-null and unique and numbers of
legs should be integers greater than zero.

To achieve this with the help of `pandera
<https://pandera.readthedocs.io/en/stable/index.html>`_, we can add a new
dataframe schema :code:`GroupsDF` to the file :code:`src/prepared_data.py`,
following the example of the already existing schema :code:`MeasurementsDF`:

.. code-block:: python

    class GroupsDF(pa.SchemaModel):
        name: pa.typing.Series[str] = pa.Field(nullable=False, unique=True)
        colour: pa.typing.Series[str]
        number_of_legs: pa.typing.Series[int] = pa.Field(ge=0)

Next the :code:`PreparedData` definition and :code:`load_prepared_data` function
need to be updated to expect dataframes that follow this schema, and the data
preparation functions in :code:`src/data_preparation.py` need to be updated so
that they produce them.

Removing a data preparation function
------------------------------------

To remove a data preparation function, simply delete it from :code:`src/data_preparation.py`, remove any already prepared data manually or with the command :code:`make clean-prepared-data` and remember not to import it in :code:`prepare_data.py` or refer to the prepared data in any inference configuration files.

Adding a new data preparation function
--------------------------------------

Perhaps you would like to add a new data preparation function that ignores
measurements with odd-numbered index values, but is otherwise the same as the
function :code:`prepare_data_no_interaction`.

First add a new function to the file :code:`src/data_preparation.py` like so:

.. code:: python

     def prepare_data_no_interaction_even_only(
         measurements_raw: pd.DataFrame
     ) -> PreparedData:
     """Prepare data with no interaction covariate or odd observations."""

     measurements = (
         process_measurements(measurements_raw)
         .loc[lambda df: df.index % 2 == 0]  # remainder dividing by 2 is 0
         .copy()
     )
     return PreparedData(
         name="no_interaction",
         coords=CoordDict({
               "covariate": ["x1", "x2"],
               "observation": measurements.index.tolist(),
         }),
         measurements=measurements,
     )

Next import the new function in the file :code:`prepare_data.py`:

.. code:: python

    DATA_PREPARATION_FUNCTIONS_TO_RUN = [
        data_preparation_functions.prepare_data_fake_interaction,
        data_preparation_functions.prepare_data_interaction,
        data_preparation_functions.prepare_data_no_interaction,
        data_preparation_functions.prepare_data_no_interaction_even_only,
    ]


Finally, create one or more new inferences and configure them to use the new
prepared data, for example by creating a folder
:code:`inferences/no_interaction_even_only` with the following
:code:`config.toml` file:

.. code:: toml

    name = "no_interaction_even_only"
    stan_file = "multilevel-linear-regression.stan"
    prepared_data_dir = "no_interaction_even_only"
    stan_input_function = "get_stan_input_no_interaction"
    modes = ["prior", "posterior", "kfold"]
    kfold_folds = 5
    
    [dims]
    b = ["covariate"]
    y = ["observation"]
    x = ["observation", "covariate"]
    
    [stanc_options]
    warn-pedantic = true
    
    [sample_kwargs]
    save_warmup = false
    iter_warmup = 2000
    iter_sampling = 2000
    
    [sample_kwargs.kfold]
    chains = 1
    iter_warmup = 1000
    iter_sampling = 1000          



Adding a new statistical model
------------------------------

To add a new statistical model, first write a new Stan program in the folder
:code:`src/stan`, then check whether the model is compatible with any of the
functions in the folder :code:`src/stan_input_functions.py`; if not, write a new
function. Finally, create a new inference folder and configure it to use the new model and a suitable stan input function, for example like this:

.. code:: toml

    name = "no_interaction_new_model"
    stan_file = "new_model.stan"
    prepared_data_dir = "no_interaction"
    stan_input_function = "get_stan_input_new_model"
    modes = ["prior", "posterior", "kfold"]
    kfold_folds = 5
    
    [dims]
    b = ["covariate"]
    y = ["observation"]
    x = ["observation", "covariate"]
    
    [stanc_options]
    warn-pedantic = true
    
    [sample_kwargs]
    save_warmup = false
    iter_warmup = 2000
    iter_sampling = 2000
    
    [sample_kwargs.kfold]
    chains = 1
    iter_warmup = 1000
    iter_sampling = 1000          


.. _vignettes:

Vignettes
=========

.. _motivation:

Motivation
==========

Following a `Bayesian workflow <https://arxiv.org/abs/2011.01808>`_ often leads
to an analysis that considers multiple custom models, data manipulation choices,
diagnostic checks, algorithm settings and parameterisation choices, all of which
need to be handled reproducibly, analysed and documented.

Carrying out such a project often leads to non-trivial software development
choices. Questions like *where should this file go?* *what is the right level of
abstraction?* and *how can I get these libraries to talk to each other?* start to come up.

Bibat aims to make this process easier by providing a flexible and extendable
project structure based on popular and powerful statistical modelling
tools.

Isn't that kind of trivial?
---------------------------

No! Here are some things that bibat does which are pretty hard, in my opinion:

- Carrying out exact k-fold cross validation using cmdstanpy and using `xarray
  <https://docs.xarray.dev/en/stable/>`_ to integrate them with arviz.
- Installing `Cmdstan <https://mc-stan.org/users/interfaces/cmdstan>`_ on
  windows.
- Providing a framework for arbitrary data preparation procedures that conform
  to a customisable common interface and can share code with each other.
- Ensuring that labels with arbitary dimensions are correctly handled.
- Allowing run-specific MCMC settings, input generation, model, parameter
  dimensions and inference modes to be specified concisely and transparently in
  one file.
- Using all of the features of arviz's :code:`InferenceData` object, for example
  allowing the creation of plots using the :code:`plot_lm` function thanks to
  correct specification of the :code:`posterior_predictive` and
  :code:`prior_predictive` groups.
- Accommodating fake data generation and easy comparison between inferences
  based on real and fake data.
- Ensuring that the analysis can be run from end to end with a single command
  :code:`make analysis` for easy reproducibility
p
But is bibat *research* software?
---------------------------------

`The Journal of Open Source Software
<https://joss.readthedocs.io/en/latest/submitting.html#what-we-mean-by-research-software>`_
defines "research software" as follows:

| JOSS publishes articles about research software. This definition includes software that: solves complex modeling problems in a scientific context (physics, mathematics, biology, medicine, social science, neuroscience, engineering); supports the functioning of research instruments or the execution of research experiments; extracts knowledge from large data sets; offers a mathematical library, or similar. While useful for many areas of research, pre-trained machine learning models and notebooks are not in-scope for JOSS.

Bibat does not directly solve complex scientific modelling problems or extract
knowledge from data; rather, it is a tool that helps scientists do these
things. Whether bibat satisfies the definition above therefore depends on how
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

Why not just shrink my analysis to a managable size using formulas?
-------------------------------------------------------------------

One approach to making statistical modelling projects easier is to trivialise
the process of defining statistical models. Packages like `lme4
<https://arxiv.org/abs/1406.5823>`_, `brms
<https://paul-buerkner.github.io/brms/q>`_ and `bambi
<https://bambinos.github.io/bambi/main/index.html>`_ use very concise formula
languages to reduce the amount of code spent on this task to a few lines or
even a few characters.

In contrast, bibat requires statistical models to be specified using Stan, a
more expressive but less concise language. It is also made on the assumption
that code implementing an analysis is best split into multiple files with a
non-trivial structure, whereas most analyses implemented using formula based
languages consist of a single file or a handful of files in the same
directory.

If possible, it is preferable to define statistical models as concisely as
possible and to use the fewest possible files to carry out an analysis. However,
when an analysis unavoidably requires multiple files and/or rich statistical
models, it is better to use an approach that accommodates this possibility. A
key benefit of concise statistical model definitions---allowing model definition
code to sit alongside other code and markup without compromising
readability---is also less important for larger projects.

In our experience it often happens that a statistical analysis project starts
out small enough to fit in a single file and then grows in ways that could not
have been foreseen at the start as more combinations of data manipulations,
models, diagnostics and plots become relevant in response to initial
results. Switching from one approach to another after starting a project is
inconvenient, so some users may prefer to use bibat's approach as a default even
for initially small seeming analyses.

.. _contributing:

Contributing
============

All contributions are very welcome!

If you have a specific suggestion for how cookiecutter-cmdstanpy-analysis could
be improved, or if you find a bug then please file an issue or submit a pull
request.

Alternatively, if you have any more general thoughts or questions, please post
them in the `discussions page
<https://github.com/teddygroves/bibat/discussions>`_.

If you'd like to contribute code changes, just follow the normal github
workflow.

To test changes to the template locally, I recommend avoiding having to complete
the wizard every time by making a `yaml <https://yaml.org/>`_ config file like
this (copied from the file :literal:`tests/data/example_config.yml`):

.. literalinclude:: ../tests/data/example_config.yml
    :language: yaml

You should now be able to create a :literal:`my_cool_project` cmdstanpy project like this:

.. code:: sh

    $ cookiecutter --no-input --config-file path/to/config.yml path/to/cookiecutter-cmdstanpy-analysis



.. toctree::
   :maxdepth: 2
              

..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
