This page explains how to create custom statistical analyses using bibat,
including the [intended workflow](#intended-workflow), instructions for
[editing the example analysis](#editing-the-example-analysis)
and [documenting your analysis](#documenting-your-analysis).

## Intended workflow

Bibat assumes that a statistical analysis consists of the following components:

- **Raw data**
- **Data preparation** in which raw data is transformed to produce prepared data
  that fit a common structure.
- **Statistical models**
- **Inferences**, i.e. combinations of a prepared dataset, a statistical model,
  a choice of how to run the model, and the results of doing so.
- **Investigations** that do things with inferences and prepared data, such as
  making plots.
- **Documentation**

To perform a statistical analysis means running some data preparation
operations, performing some inferences, doing some investigations and providing
some documentation. Bibat provides functionality for conveniently doing these
things, as well as explicit and convenient representations of all the
components and even a ready-made working example project.

Bibat's strategy for representing the components of a statistical analysis is as
follows:

- Raw data are files that live in the directory `data/raw`.

- Prepared data are created on the fly whenever the analysis is run, and
  serialised to json files in the folder `data/prepared`.

- Source code lives in a folder called `src`.

- Logic for data preparation, including a common structure given by a class
  `PreparedData` and functions producing data in this format, lives in the file
  `src/data_preparation.py`.

- Statistical models are represented by Stan programs in the directory
  `src/stan/`

- Inferences are subdirectories of the directory `inferences`. Each inference
  subdirectory contains a file called `config.toml` that chooses a prepared
  dataset, statistical model and [fitting modes](api.md#bibat.fitting_mode),
  as well as sampler configuration.  When the analysis is run the folder is
  populated with an :code:`InferenceData` object saved in a folder called
  `idata`. This folder contains everything needed to analyse the results of the
  inference, including samples, debug information and sometimes predictions.

- Investigations are performed literately using Jupyter notebooks that live in
  the folder `notebooks` and save plots to the directory `plots`.

- Documentation lives in the directory `docs`, and can be written using
  either sphinx or quarto: see the section on [documenting your analysis](#documenting-your-analysis) for details.

The analysis is performed by setting up a suitable programming environment and
then running the Python files `src/data_preparation.py` and `src/fitting.py`,
executing the notebooks and building the documentation. These tasks are
automated using the makefile `Makefile`, so that the entire analysis can
be performed using the command `make analysis` while avoiding unnecessarily
re-running any tasks.

After running the analysis, the next step is to make some changes and run a new
analysis. This can be done by editing any of the files representing the
analysis's component parts, then re-running the command `make analysis`.

## Editing the example analysis

This section illustrates how to create a custom statistical analysis using bibat
through examples of common tasks.

### Changing the definition of prepared data

Bibat's starting analysis has a `PreparedData` class with three attributes:
`name`, `coords` and `measurements`. Perhaps, for your analysis, you would
prefer a different definition of prepared data with another attribute: a table
called `groups`, with columns `name`, `colour` and `number_of_legs`. You would
also like some rules to be enforced: names should be non-null and unique and
numbers of legs should be integers greater than zero.

To achieve this with the help of [pandera](https://pandera.readthedocs.io/en/stable/index.html), we can add a new
schema `GroupsDF` to the file
`src/data_preparation.py`, following the example of the already
existing schema `MeasurementsDF`:

``` python
class GroupsDF(pa.SchemaModel):
    name: pa.typing.Series[str] = pa.Field(nullable=False, unique=True)
    colour: pa.typing.Series[str]
    number_of_legs: pa.typing.Series[int] = pa.Field(ge=0)
```

Next the `PreparedData` definition and `load_prepared_data` function need to be
updated to expect dataframes that follow this schema, and the data preparation
functions in `src/data_preparation.py` need to be updated so that they produce
them.

### Removing a data preparation operation

To remove a data preparation operation, simply make sure it is not run by the
function `prepare_data` in the file `src/data_preparation.py`, then
remove any already prepared data.

### Adding a new data preparation function

Perhaps you would like to add a new data preparation function that ignores
measurements with odd-numbered index values, but is otherwise the same as the
function :code:`prepare_data_no_interaction`.

First add a new function to the file `src/data_preparation.py` like so:

```python
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
```

Next update the new function `prepare_data` so that it calls the new function:

```python
def prepare_data() -> None:
    """Run main function."""
    raw_data = {
        k: pd.read_csv(v, index_col=None) for k, v in RAW_DATA_FILES.items()
    }
    for prepare_data_func in [
        prepare_data_interaction,
        prepare_data_no_interaction,
        prepare_data_fake_interaction,
          prepare_data_no_interaction_even_only,
    ]:
        prepared_data = prepare_data_func(raw_data["measurements"])
        output_file = prepared_data.name + ".json"
        output_path = PREPARED_DIR / output_file
        if not PREPARED_DIR.exists():
            PREPARED_DIR.mkdir()
        with output_path.open("w") as f:
            f.write(prepared_data.model_dump_json())
```

Finally, create one or more new inferences and configure them to use
the new prepared data, for example by creating a folder `inferences/no_interaction_even_only` with the following `config.toml` file:


```toml
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

    [mode_options.kfold]
    chains = 1
    iter_warmup = 1000
    iter_sampling = 1000
```

### Adding a new statistical model

To add a new statistical model, first write a new Stan program in the folder
`src/stan`, then check whether the model is compatible with any of the functions
in the folder `src/stan_input_functions.py`; if not, write a new function
and add it to the `LOCAL_FUNCTIONS` dictionary in the file `src/fitting`.
You can probably take some inspiration from the example functions in `src/stan_input_functions.py`. Finally, create a new inference folder and configure
it to use the new model and a suitable Stan input function, for example like
this:

```toml
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

    [mode_options.kfold]
    chains = 1
    iter_warmup = 1000
    iter_sampling = 1000
```

## Documenting your analysis

Bibat makes it easy to document your analysis using the popular tools [Quarto](https://quarto.org/) and [Sphinx](https://www.sphinx-doc.org/en/master/index.html).

If you choose one of these options when creating your project, the folder
`docs` will be populated with documentation source files, which you can convert
into formatted documentation files by running the command `make docs` from the
project root.

Sphinx is an excellent choice for documenting projects that involve Python code
that you would like to share with others, as it supports automatic
documentation via directives like [automodule](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-automodule).

Quarto is specialised for producing nicely-formatted documents in a range of
formats, starting from a source document written in [pandoc markdown](https://pandoc.org/MANUAL.html#pandocs-markdown). One relevant use case is
when you want to write a paper based on your analysis and update any figures
automatically. Note that, unlike sphinx, bibat is not set up to install or
configure quarto automatically. See [quarto's 'getting started' page](
https://quarto.org/docs/get-started/) for official installation
instructions.

To get an idea for how to get started with writing documentation using Quarto
and Sphinx, the official documentation for both tools are very good. The
[Quarto guide is here](https://quarto.org/docs/guide/) and resources for
learning Sphinx and its primary document format reStructuredText are linked
from the [Sphinx homepage](https://www.sphinx-doc.org/en/master/). For a more
focused introduction, try looking at the example source documents that bibat
provides. The example [quarto report is here](https://github.com/teddygroves/bibat/blob/copier/bibat/template/%7B%25%20if%20docs_format%20!%3D%20'None'%20%25%7Ddocs%7B%25%20endif%20%25%7D/%7B%25%20if%20docs_format%20%3D%3D%20'Quarto'%20%25%7Dreport.qmd%7B%25%20endif%20%25%7D.jinja)
and the [Sphinx index document can be found here](https://github.com/teddygroves/bibat/blob/copier/bibat/template/%7B%25%20if%20docs_format%20!%3D%20'None'%20%25%7Ddocs%7B%25%20endif%20%25%7D/%7B%25%20if%20docs_format%20%3D%3D%20'Sphinx'%20%25%7Dindex.rst%7B%25%20endif%20%25%7D.jinja).
