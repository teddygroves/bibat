"""Some handy python functions."""


from typing import Tuple, Dict
import numpy as np
import pandas as pd
from scipy.stats import norm


def one_encode(s: pd.Series) -> pd.Series:
    """Replace a series's values with 1-indexed integer factors.

    :param s: a pandas Series that you want to factorise.

    """
    return pd.Series(pd.factorize(s)[0] + 1, index=s.index)


def make_columns_lower_case(df: pd.DataFrame) -> pd.DataFrame:
    """Make a DataFrame's columns lower case.

    :param df: a pandas DataFrame
    """
    new = df.copy()
    new.columns = [c.lower() for c in new.columns]
    return new


def get_lognormal_params_from_qs(
    x1: float, x2: float, p1: float, p2: float
) -> Tuple[float, float]:
    """Find parameters for a lognormal distribution from two quantiles.

    i.e. get mu and sigma such that if X ~ lognormal(mu, sigma), then pr(X <
    x1) = p1 and pr(X < x2) = p2.

    :param x1: the lower value
    :param x2: the higher value
    :param p1: the lower quantile
    :param p1: the higher quantile

    """
    logx1 = np.log(x1)
    logx2 = np.log(x2)
    denom = norm.ppf(p2) - norm.ppf(p1)
    sigma = (logx2 - logx1) / denom
    mu = (logx1 * norm.ppf(p2) - logx2 * norm.ppf(p1)) / denom
    return mu, sigma


def get_normal_params_from_qs(
    x1: float, x2: float, p1: float, p2: float
) -> Tuple[float, float]:
    """find parameters for a normal distribution from two quantiles.

    i.e. get mu and sigma such that if x ~ normal(mu, sigma), then pr(x <
    x1) = p1 and pr(x < x2) = p2.

    :param x1: the lower value
    :param x2: the higher value
    :param p1: the lower quantile
    :param p1: the higher quantile

    """
    denom = norm.ppf(p2) - norm.ppf(p1)
    sigma = (x2 - x1) / denom
    mu = (x1 * norm.ppf(p2) - x2 * norm.ppf(p1)) / denom
    return mu, sigma


def get_99_pct_params_ln(x1: float, x2: float):
    """Wrapper assuming you want the 0.5%-99.5% inter-quantile range.

    :param x1: the lower value such that pr(X > x1) = 0.005
    :param x2: the higher value such that pr(X < x2) = 0.995

    """
    return get_lognormal_params_from_qs(x1, x2, 0.005, 0.995)


def get_99_pct_params_n(x1: float, x2: float):
    """Wrapper assuming you want the 0.5%-99.5% inter-quantile range.

    :param x1: the lower value such that pr(X > x1) = 0.005
    :param x2: the higher value such that pr(X < x2) = 0.995

    """
    return get_normal_params_from_qs(x1, x2, 0.005, 0.995)
