"""
File: stats.py
Author: Jeremy Ephron
---------------------
This file implements various statistical functions.

"""

from typing import Optional, Union, Tuple, List

import numpy as np
import pandas as pd
import scipy.optimize as sco

from utils import *


def normalize(
    a: Union[pd.DataFrame, pd.Series]
) -> Union[pd.DataFrame, pd.Series]:
    """
    Normalizes a data stream.

    Args:
        a: The DataFrame or Series to normalize.

    Returns:
        The DataFrame or Series min-max normalized.

    """

    return (a - a.min()) / (a.max() - a.min())


def standardize(
    a: Union[pd.DataFrame, pd.Series],
    window: Optional[int] = None
) -> Union[pd.DataFrame, pd.Series]:
    """
    Standardizes a data stream.

    Args:
        a: The DataFrame or Series to standardize.
        window: TODO:

    Returns:
        The DataFrame or Series with mean of 0 and standard deviation of 1.

    """
    
    if not window:
        window = a.shape[0]

    a_window = a.rolling(window, min_periods=1)
    return (a - a_window.mean()) / a_window.std()


def relativize_to_avg(a: pd.DataFrame) -> pd.DataFrame:
    """
    Subtracts the daily global average from each day's values.

    Args:
        a: The DataFrame to relativize.

    Returns:
        The DataFrame with each row's average subtracted out.

    """

    return a.sub(a.mean(axis=1), axis=0)


def sigmoid(
    x: Union[float, pd.Series],
    lb: float = -1, 
    ub: float = 1, 
    scale: float = 1,
    deg: int = 1,
) -> Union[float, pd.Series]:
    """
    Applies a sigmoid function to x that is asymptotically bounded between ub
    and lb.
    
    Args:
        x: The value or series of values to apply the sigmoid to.
        lb: The lower bound.
        ub: The upper bound.

    Returns:
        The sigmoid function evaluated on x (or each value within x), bounded 
        between ub and lb.

    """
    
    sig = (1 / (1 + np.exp(-scale * x**deg))) * (ub - lb) + lb
    if deg % 2 == 0:
        return np.sign(x) * sig
    else:
        return sig


def compute_corrcoef(
    a: Union[pd.DataFrame, pd.Series],
    b: Union[pd.DataFrame, pd.Series]
) -> Union[float, np.array]:
    """
    Computes the correlation coefficients country-wise between two DataFrames.
    
    If a and b are series simply returns the correlation coefficient between 
    the two.

    Args:
        a: The first DataFrame or series.
        b: The second DataFrame or series.

    Returns:
        coef: An array containing the correlation coefficients between each 
            country's corresponding series in a and b, or the coefficent 
            between the two series if a and b are Series objects.

    """

    assert type(a) == type(b)
    
    if isinstance(a, pd.Series):
        return np.corrcoef(*make_comparable(a, b))[0,1]

    b = b[a.columns]
    assert (a.columns == b.columns).all()

    coef = np.zeros(a.shape[1])
    for i, country in enumerate(a.columns):
        coef[i] = np.corrcoef(*make_comparable(a[country], b[country]))[0,1]

    return coef


def compute_annualized_return(
    rets: Union[pd.Series, pd.DataFrame]
) -> Union[float, pd.Series]:
    """
    TODO: 
    """

    assert rets.index.freq == 'B'

    total_ret = compute_total_return(rets)
    n_years = (rets.index[-1] - rets.index[0]).n / WEEKDAYS_PER_YEAR
    return (1 + total_ret)**(1 / n_years) - 1


def compute_total_return(
    rets: Union[pd.Series, pd.DataFrame],
    risk_free_rate: Optional[pd.Series] = None
) -> Union[float, pd.Series]:
    """
    Computes the total cumulative return of the investment(s) over their 
    lifetime.

    Args:
        rets: The return stream of the investment or investments.
        risk_free_rate: The annual risk free rate of return quoted monthly. If
            provided will compute total excess return.

    Returns:
        The total return of each investment.

    """

    if risk_free_rate is not None:
        assert risk_free_rate.index.freq == 'M'

        risk_free_rate_daily = ((1 + risk_free_rate).pow(1 / WEEKDAYS_PER_YEAR)
                                - 1).resample('B').ffill()
        rets = (rets - risk_free_rate_daily)

    return (1 + rets).product() - 1


def compute_cumulative_return_history(
    rets: Union[pd.Series, pd.DataFrame]
) -> Union[pd.Series, pd.DataFrame]:
    """
    Computes the cumulative return at each point over the investment's history.

    Args:
        rets: The return stream of the investment or investments.

    Returns:
        The history of the cumulative return of each investment.

    """

    return (1 + rets).cumprod() - 1


def compute_sharpe_ratio(
    rets: pd.Series,
    risk_free_rate: pd.Series
) -> float:
    """
    Computes the Sharpe ratio of a return stream given the time series of risk 
    free rates.

    Args:
        rets: The daily return percentages of an investment.
        risk_free_rate: The annual risk free rate each month.

    Returns:
        The Sharpe ratio of the given return stream.

    """

    assert rets.index.freq == 'B'
    assert risk_free_rate.index.freq == 'M'

    risk_free_rate_daily = ((1 + risk_free_rate).pow(1 / WEEKDAYS_PER_YEAR)
                            - 1).resample('B').ffill()

    rets, risk_free_rate_daily = make_comparable(rets, risk_free_rate_daily)
    sharpe_ratio_daily = (rets.mean() - risk_free_rate_daily.mean()) \
                         / (rets - risk_free_rate_daily).std()
    sharpe_ratio = sharpe_ratio_daily * (WEEKDAYS_PER_YEAR**0.5)

    return sharpe_ratio


def compute_annualized_volatility(
    rets: pd.Series,
    risk_free_rate: Optional[pd.Series] = None
) -> float:
    """
    Computes the annualized volatility of the return stream or excess return 
    stream.

    Args:
        rets: The daily return percentages of an investment.
        risk_free_rate: The annual risk free rate each month. If None, 
            calculates the volatility of the return stream as is (not in 
            excess of the risk free rate).

    Returns:
        The annualized volatility (standard deviation) of the return stream or 
        of the returns in excess of the risk free rate.

    """

    assert rets.index.freq == 'B'
    assert risk_free_rate is None or risk_free_rate.index.freq == 'M'

    if risk_free_rate is not None:
        risk_free_rate_daily = ((1 + risk_free_rate).pow(1 / WEEKDAYS_PER_YEAR)
                                - 1).resample('B').ffill()
        volatility_daily = (rets - risk_free_rate_daily).std()
    else:
        volatility_daily = rets.std()

    volatility_annualized = volatility_daily * (WEEKDAYS_PER_YEAR**0.5)
    return volatility_annualized


def maximize_sharpe_ratio(
    rets: Union[pd.DataFrame, List[pd.Series]],
    risk_free_rate: pd.Series
) -> Tuple[np.array, float]:
    """
    TODO: write docstring

    """

    def neg_sharpe_ratio(weights, rets, risk_free_rate) -> float:
        return -compute_sharpe_ratio(
            sum(r * weights[i] for i, r in enumerate(rets)),
            risk_free_rate
        )

    n_assets = len(rets)
    args = (rets, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n_assets))
    res = sco.minimize(neg_sharpe_ratio, [1 / n_assets] * n_assets, args=args,
                       method='SLSQP', bounds=bounds, constraints=constraints)
    return res.x, -res.fun


def maximize_diversification(rets: pd.DataFrame) -> Tuple[np.array, float]:
    """
    TODO: write docstring

    """

    def neg_vol_sharpe(weights, std, cov) -> float:
        weights = np.array([weights])
        return -(
            weights.dot(std) / np.sqrt(weights.dot(cov).dot(weights.T))
        )[0][0]

    n_assets = len(rets) if isinstance(rets, list) else rets.shape[1]
    args = (rets.std(), rets.cov())
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # +/-60% arbitrarily chosen
    uniform_weight = 1 / n_assets
    bounds = tuple((uniform_weight * 0.4, uniform_weight * 1.6)
                   for _ in range(n_assets))
    res = sco.minimize(neg_vol_sharpe, [uniform_weight] * n_assets, args=args,
                       method='SLSQP', bounds=bounds, constraints=constraints)
    return res.x, -res.fun







