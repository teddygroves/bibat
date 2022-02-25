import os

import arviz as az
import pandas as pd
import xarray

RESULTS_DIR = os.path.join("results", "runs")


def main():
    run_dirs = [
        os.path.join(RESULTS_DIR, d)
        for d in os.listdir(RESULTS_DIR)
        if os.path.isdir(os.path.join(".", RESULTS_DIR, d))
    ]
    priors = {}
    posteriors = {}
    for run_dir in run_dirs:
        prior_file = os.path.join(run_dir, "prior.nc")
        posterior_file = os.path.join(run_dir, "posterior.nc")
        llik_cv_file = os.path.join(run_dir, "llik_cv.nc")
        if os.path.exists(prior_file):
            priors[run_dir] = az.from_netcdf(prior_file)
        if os.path.exists(posterior_file):
            posterior = az.from_netcdf(posterior_file)
            if os.path.exists(llik_cv_file):
                llik_cv = xarray.load_dataset(llik_cv_file)
                posterior.add_groups({"log_likelihood_cv": llik_cv})
            posteriors[run_dir] = posterior
    posterior_loo_comparison = az.compare(posteriors)
    cv_comparison = {
        k: round(
            float(
                v.get("log_likelihood_cv")["llik"]
                .mean(dim=["chain", "draw"])
                .sum()
            ),
            2,
        )
        for k, v in posteriors.items()
    }
    print("*****PSIS Loo comparison******")
    print(posterior_loo_comparison)
    print("******************************")
    print("*****Exact cross-validation comparison******")
    print(pd.Series(cv_comparison, name="cv_log_likelihood"))
    print("********************************************")


if __name__ == "__main__":
    main()
