"""Get an input to cmdstanpy.CmdStanModel.sample from a pd.DataFrame."""

from typing import List, Dict
import pandas as pd


def get_stan_input(
    measurements: pd.DataFrame,
    x_cols: List[str],
    priors: Dict,
    likelihood: bool,
) -> Dict:
    """Get an input to cmdstanpy.CmdStanModel.sample.

    :param measurements: a pandas DataFrame whose rows represent measurements

    :param model_config: a dictionary with keys "priors", "likelihood" and
    "x_cols".

    """
    return {
        **priors,
        **{
            "N": len(measurements),
            "K": len(x_cols),
            "x": measurements[x_cols].values,
            "y": measurements["y"].values,
            "N_test": len(measurements),
            "x_test": measurements[x_cols].values,
            "y_test": measurements["y"].values,
            "likelihood": int(likelihood),
        },
    }
