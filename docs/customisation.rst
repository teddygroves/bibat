========================
Customising the template
========================

You will almost definitely want to customise the template so that it implements your analysis, rather than the packaged example analysis. This section explains how to do this.

Adding a script for fetching raw data from the internet
=======================================================

Perhaps your analysis involves fetching some data from the internet, and you would like to include the code that does the fetching alongside the code that implements the rest of your analysis. A way to do this that fits in nicely with the rest of the template would be to write a new script :literal:`fetch_data.py` that writes to :literal:`data/raw` and possibly a library file :literal:`fetching.py` with code for the script to import.

Prepared data with extra tables
===============================

Perhaps you need to create a prepared dataset with two extra tables: :literal:`cats` and :literal:`hats`. This can be done by first adding optional attributes to the :literal:`PreparedData` class in the file :literal:`src/prepared_data.py`:

.. code:: python

    ...
    from typing import Any, Callable, Dict, List, Optional
    ...
    @dataclass
    class PreparedData:
        ...
        cats: Optional[pd.DataFrame] = None
        hats: Optional[pd.DataFrame] = None
        ...

Next go to :literal:`src/data_preparation.py` and add a new :literal:`prepare_data_` function:

.. code:: python

    def prepare_data_cats_hats(
        measurements_raw: pd.DataFrame,
        cats_raw: pd.DataFrame,
        hats_raw: pd.DataFrame
    ) -> PreparedData:
        """Prepare data involving cats, hats and measurements."""

        ... 

        return PreparedData(
            name="cats_hats",
            measurements=measurements,
            cats=cats,
            hats=hats,
            ...
        )

Finally go to :literal:`prepare_data.py` and add logic for reading and writing the :literal:`cats` and :literal:`hats`:

.. code:: python

    ...
    RAW_DATA_FILES = {
        "raw_measurements": os.path.join(RAW_DIR, "raw_measurements.csv"),
        "raw_cats": os.path.join(RAW_DIR, "raw_cats.csv"),
        "raw_hats": os.path.join(RAW_DIR, "raw_hats.csv"),
    }
    ...
    def main():
        ...
        for data_prep_function in [
            ...
            prepare_data_cats_hats,
        ]:
            prepared_data = data_prep_function(
                raw_data["raw_measurements"], 
                raw_data["raw_cats"],
                raw_data["raw_hats"]
            )
            ...
            measurements_file = os.path.join(output_dir, "measurements.csv")
            cats_file = os.path.join(output_dir, "cats.csv")
            hats_file = os.path.join(output_dir, "hats.csv")
            ...
            prepared_data.measurements.to_csv(measurements_file)
            prepared_data.cats.to_csv(cats_file)
            prepared_data.hats.to_csv(hats_file)
            ...

Now when you run the script :literal:`prepare_data.py`, a new folder should be created at :literal:`data/prepared/cats_hats` containing the new data in the correct shape.

Adding a partially pooled intercept effect for a categorical variable
=====================================================================

You might like to write a new statistical model including a term capturing the effect of a cat's hat type on its measurement. You don't have any quantitative information about how a particular hat type relates to its effect, or about how the different effects are related, so a nice option is to try a partially-pooled intercept parameter vector with independent priors.

The first step is to write a Stan program :literal:`src/stan/model_cats_hats.stan` including this effect. This can be done by adding the following lines to the provided program :literal:`model.stan`.

.. code:: stan

    data {
      // ...
      int<lower=1> H;  // types of hat
      int<lower=1> C;  // cats
      // ...
      array[N] int<lower=1,upper=C> cat;
      array[C] int<lower=1,upper=H> hat_type;
      // ...
    }
    parameters {
      // ...
      real<lower=0> tau_hat_type;
      vector<multiplier=tau_hat_type>[H] a_hat_type;
      // ...
    }
    // ...
    model {
      // ...
      a_hat_type ~ normal(0, tau_hat_type);
      tau_hat_type ~ lognormal(0, 0.3);
      // ...
        y[ix_train] ~ normal_id_glm(x_std[ix_train], a + a_hat_type[hat[cat]], b, sigma);
    }
    generated quantities {
    // ...
        yrep[n] = normal_rng(a + a_hat_type[hat[cat[n]]] + x_std[ix_test[n]] * b, sigma);
        llik[n] = normal_lpdf(y[ix_test[n]] | a + a_hat_type[hat[cat[n]]] x_std[ix_test[n]] * b, sigma);
    }

Next the python code needs to be edited so as to match the new input and output format: new functions :literal:`prepare_data_cats_hats` and :literal:`get_stan_input_cats_hats` are needed. Again these can mostly be copy/pasted from provided functions with similar names:

.. code:: python

    from src.util import one_encode
    ...
    def prepare_data_cats_hats(
        measurements_raw: pd.DataFrame,
        cats_raw: pd.DataFrame,
        hats_raw: pd.DataFrame
    ) -> PreparedData:
        """Prepare data involving cats, hats and measurements."""

        ...
        measurements["cat_fct"] = one_encode(measurements["cat"])
        hats["hat_type_fct"] = one_encode(hats["hat_type"])
        cats = cats.join(hats.set_index("id")["hat_type_fct"], on="hat_id")

        ...
        coords = CoordDict({
            "covariate": x_cols,
            "hat_type": pd.factorize(hats["hat_type"])[1],
        })
        dims = {"b": ["covariate"], "a_hat_type": ["hat_type"]}
        ...
        return PreparedData(
            name="cats_hats",
            measurements=measurements,
            cats=cats,
            hats=hats,
            coords=coords,
            dims=dims,
            stan_input_function=get_stan_input_cats_hats
        )

    ...

    def get_stan_input_cats_hats(
        measurements: pd.DataFrame,
        cats: pd.DataFrame,
        hats: pd.DataFrame,
    ) -> StanInput:
    ...
        return stanify_dict(
            {
                ...
                "H": hats["hat_type"].nunique(),
                "C": cats["id"].nunique(),
                ...
                "cat": measurements["cat_fct"],
                "hat_type": cats["hat_type_fct"],
                ...
            }
        )

The last step is to write a new model configuration:

.. code:: toml

    name = "cats_hats"
    stan_file = "src/stan/model_cats_hats.stan"
    data_dir = "data/prepared/cats_hats"
    modes = ["prior", "posterior", "cross_validation"]

    [stanc_options]
    warn-pedantic = true

    [sample_kwargs]
    show_progress = true
    save_warmup = false
    iter_warmup = 2000
    iter_sampling = 2000

    [sample_kwargs.cross_validation]
    chains = 1

Now when you run the python script :literal:`sample.py`, results for the new model configuration should be created and written alongside the other model configurations to :literal:`results/runs/cats_hats`.
