.. _working_with_bibat:

==================
Working with bibat
==================

This page explains how to create custom statistical analyses using bibat,
including the :ref:`intended workflow <intended_workflow>`, instructions for
:ref:`editing the example analysis <editing_the_example_analysis>`,
:ref:`documenting your analysis <documenting_your_analysis>` and links to some
:ref:`vignettes`.

.. _intended_workflow:

Intended workflow
=================

Bibat assumes that a statistical analysis consists of the following components:

- **Raw data**
- **Data preparation** in which raw data is transformed to produce prepared data
  that fit a common structure.
- **Statistical models**
- **Inferences**, i.e. combinations of a prepared dataset, a statistical model,
  a choice of which modes to fit the model in and how exactly to do so, and the
  results of doing this fitting.
- **Investigations** that do things with inferences and prepared data, such as
  making plots.
- **Documentation**

The terms "Inference" and "mode" in this list have specific meanings.
"Inference" roughly matches the concept `InferenceData
<https://arviz-devs.github.io/arviz/api/inference_data.html>`_ from the library
arviz.

A "mode" means a way of fitting a statistical model to some data. Maud provides
modes called "prior", "posterior" and "kfold", which respectively trigger
priors-only inference, posterior inference and exact cross-validation. It is
possible to add more modes!

To perform a statistical analysis means running some data preparation
operations, then carrying out a set of inferences, doing some investigations
and providing some documentation. bibat provides functionality for conveniently
doing these things, as well as explicit and convenient representations of all
the components and even a ready-made working example project.

bibat's strategy for representing the components of a statistical analysis is as
follows:

- Raw data are files that live in the directory :code:`data/raw`.

- Source code lives in a folder with the same name as the analysis, for example
  `my_analysis`.

- Logic for data preparation, including a common structure given by a class
  PreparedData and functions producing data in this format, lives in the file
  `my_analysis/data_preparation.py`.

- Statistical models are represented by Stan programs in the directory
  :code:`my_analysis/stan/`

- Inferences are subdirectories of the directory :code:`inferences`. Each such
  subdirectory contains a file called :code:`config.toml` that chooses a
  prepared dataset, statistical model and some fitting modes, as well as sampler
  configuraiton. When the analysis is run the folder is populated with an
  :code:`InferenceData` object saved in the file :code:`idata.json`, containing
  samples and debug information.

- Investigations are performed literately using the notebook file
  :code:`my_analysis/investigate.ipynb`, which saves plots to the directory
  :code:`plots`.

- Documentation lives in the directory :code:`docs`, and can be written using a
  range of standard formats: see the section on
  :ref:`documenting your analysis <documenting_your_analysis>` for details.

The analysis is performed by setting up a suitable programming environment and
then running the Python scripts :code:`my_analysis/prepare_data.py` and
:code:`my_analysis/sample.py`, which live in the project root, executing the
notebook file :code:`my_analysis/investigate.ipynb` and building the
documentation. These tasks are automated using the makefile :code:`Makefile`,
so that the entire analysis can be performed using the command :code:`make
analysis` while avoiding unnecessarily re-running any tasks.

After running the analysis, the next step is to make some changes and run a new
analysis. This can be done by editing any of the files representing the
analysis's component parts, then re-running the command :code:`make analysis`.

.. _editing_the_example_analysis:

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
dataframe schema :code:`GroupsDF` to the file
:code:`my_analysis/data_preparation.py`, following the example of the already
existing schema :code:`MeasurementsDF`:

.. code-block:: python

    class GroupsDF(pa.SchemaModel):
        name: pa.typing.Series[str] = pa.Field(nullable=False, unique=True)
        colour: pa.typing.Series[str]
        number_of_legs: pa.typing.Series[int] = pa.Field(ge=0)

Next the :code:`PreparedData` definition and :code:`load_prepared_data`
function need to be updated to expect dataframes that follow this schema, and
the data preparation functions in :code:`my_analysis/data_preparation.py` need
to be updated so that they produce them.

Removing a data preparation operation
-------------------------------------

To remove a data preparation operation, simply make sure it is not run by the
function `prepare_data` in the file :code:`my_analysis/data_preparation.py`, then
remove any already prepared data manually or with the command :code:`make
clean-prepared-data`.

Adding a new data preparation function
--------------------------------------

Perhaps you would like to add a new data preparation function that ignores
measurements with odd-numbered index values, but is otherwise the same as the
function :code:`prepare_data_no_interaction`.

First add a new function to the file :code:`my_analysis/data_preparation.py`
like so:

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

Next update the new function `prepare_data` so that it calls the new function:

.. code:: python

  def prepare_data():
      """Main function."""
      print("Reading raw data...")
      raw_data = {
          k: pd.read_csv(v, index_col=None) for k, v in RAW_DATA_FILES.items()
      }
      data_preparation_functions_to_run = [
          prepare_data_interaction,
          prepare_data_no_interaction,
          prepare_data_fake_interaction
          prepare_data_no_interaction_even_only,
      ]
      print("Preparing data...")
      for dpf in data_preparation_functions_to_run:
          print(f"Running data preparation function {dpf.__name__}...")
          prepared_data = dpf(raw_data["raw_measurements"])
          output_dir = os.path.join(PREPARED_DIR, prepared_data.name)
          print(f"\twriting files to {output_dir}")
          if not os.path.exists(PREPARED_DIR):
              os.mkdir(PREPARED_DIR)
          write_prepared_data(prepared_data, output_dir)
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
:code:`my_analysis/stan`, then check whether the model is compatible with any
of the functions in the folder :code:`my_analysis/stan_input_functions.py`; if
not, write a new function. Finally, create a new inference folder and configure
it to use the new model and a suitable stan input function, for example like
this:

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

.. _documenting_your_analysis:

Documenting your analysis
=========================

Bibat makes it easy to document your analysis using the popular tools `Quarto
<https://quarto.org/>`_ and `Sphinx
<https://www.sphinx-doc.org/en/master/index.html>`_.

If you choose one of these options when completing bibat's cli wizard, the
folder :literal:`docs` will be populated with documentation source files, which
you can convert to a prettier format by running the command :literal:`make
docs` from the project root.

Sphinx is an excellent choice for documenting projects that involve Python code
that you would like to share with others, as it supports automatic
documentation via directives like `automodule
<https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-automodule>`_.

Quarto is specialised for producing nicely-formatted documents in a range of
formats, starting from a source document written in `pandoc markdown
<https://pandoc.org/MANUAL.html#pandocs-markdown>`_. One relevant usecase is
when you want to write a paper based on your analysis and update any figures
automatically. Note that, unlike sphinx, bibat is not set up to install or
configure quarto automatically. See `quarto's 'getting started' page
<https://quarto.org/docs/get-started/>`_ for official installation
instructions.

To get an idea for how to get started with writing documentation using Quarto
and Sphinx, the official documentation for both tools are very good. The
`Quarto guide is here <https://quarto.org/docs/guide/>`_ and resources for
learning Sphinx and its primary document format reStructuredText are linked
from the `Sphinx homepage <https://www.sphinx-doc.org/en/master/>`_. For a more
focused intoduction, try looking at the example source documents that bibat
provides. The example `quarto report is here
<https://github.com/teddygroves/bibat/blob/main/bibat/%7B%7Bcookiecutter.repo_name%7D%7D/docs/report.qmd>`_
and the `Sphinx index document can be found here
<https://github.com/teddygroves/bibat/blob/main/bibat/%7B%7Bcookiecutter.repo_name%7D%7D/docs/index.rst>`_.

.. _vignettes:

Vignettes
=========

`This vignette <_static/report.html>`_ provides a step by step description of
how to create a complex analysis of baseball data starting with bibat's example
project. You can see the complete analysis `here
<https://github.com/teddygroves/bibat/tree/main/bibat/examples/baseball>`_. This is
probably the most useful example project as it is kept up to date as bibat is
developed.

For even more inspiration, check out these projects that used bibat:

* `mrna <https://github.com/teddygroves/mrna>`_ A published analysis of mRNA
  regulation, made fully Bayesian and then improved.
* `putting <https://github.com/teddygroves/putting>`_ A Bayesian analysis of putting data
* `km-stats <https://github.com/biosustain/km-stats>`_ Statistical analysis of
  Michaelis constant measurements from online databases
* `biothermostat <https://github.com/biosustain/biothermostat>`_ Statistical
  analysis of biochemical thermodynamics data.

If you used bibat to start your analysis, feel free to `add it to this list
<https://github.com/teddygroves/bibat/blob/main/docs/index.rst>`_!
