"""
File: indicators.py
Author: Jeremy Ephron
---------------------
This file implements each indicator and indicator related functions.

To create each indicator, the desired data is put in terms of a difference 
from the global mean, and then put in terms of number of standard deviations 
away from each country's historical mean.

"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy.stats import norm

from stats import standardize, relativize_to_avg, sigmoid
from utils import *


def fx_appreciation_indicator(
    fx_to_usd: pd.DataFrame,
    window: int = 6
) -> pd.Series:
    """
    Computes the FX appreciation indicator, a percent change in each country's
    currency vs. the USD over the specified window in months.

    Args:
        fx_to_usd: A DataFrame containing each country's currency to USD 
            exchange rate (only changes need to matter).
        window: The number of months over which to take the change.

    Returns:
        Today's indicator values.

    """
    
    fx_apprec_win = fx_to_usd.pct_change(window)
    fx_apprec_win_relative = relativize_to_avg(fx_apprec_win)
    fx_apprec_win_z = standardize(fx_apprec_win_relative)

    indicator = fx_apprec_win_z.iloc[-1].fillna(0)
    return indicator


def bond_premium_and_curve_height_indicator(
    long_rates: pd.DataFrame,
    short_rates: pd.DataFrame
) -> pd.Series:
    """
    Computes the bond premium and curve height indicator.

    Args:
        long_rates: A DataFrame containing each country's long rates.
        short_rates: A DataFrame containing each country's short rates.

    Returns:
        Today's indicator values.
    
    """

    bond_premium_indic = bond_premium_indicator(long_rates, short_rates)
    curve_height_indic = curve_height_indicator(long_rates, short_rates)
    
    indicator = -curve_height_indic * bond_premium_indic
    return indicator


def bond_premium_indicator(
    long_rates: pd.DataFrame,
    short_rates: pd.DataFrame
) -> pd.Series:
    """
    Computes the bond premium indicator, the long rates minus the short rates 
    in each country.

    Args:
        long_rates: A DataFrame containing each country's long rates.
        short_rates: A DataFrame containing each country's short rates.

    Returns:
        Today's indicator values.
    
    """

    bond_premium = long_rates - short_rates
    bond_premium_relative = relativize_to_avg(bond_premium)
    bond_premium_z = standardize(bond_premium_relative)

    indicator = bond_premium_z.iloc[-1].fillna(0)
    return indicator
    

def curve_height_indicator(
    long_rates: pd.DataFrame,
    short_rates: pd.DataFrame
) -> pd.Series:
    """
    Computes the curve height indicator, the average of the long and short 
    rates for each country.

    Args:
        long_rates: A DataFrame containing each country's long rates.
        short_rates: A DataFrame containing each country's short rates.

    Returns:
        Today's indicator values.

    """

    curve_height = (long_rates + short_rates) / 2
    curve_height_relative = relativize_to_avg(curve_height)
    curve_height_z = standardize(curve_height_relative)

    indicator = curve_height_z.iloc[-1].fillna(0)
    return indicator


def monetary_base_indicator(m2_usd: pd.DataFrame) -> pd.Series:
    """
    Computes the monetary base indicator, the difference between the 12-month
    change in M2 and the 3-month change in M2.

    Args:
        m2_usd: A DataFrame containing each country's M2 money supply in USD.

    Returns:
        Today's indicator values.

    """

    # Make sure the data is sampled in months
    assert m2_usd.index.freq == 'M'

    m2_pct_change_3m = m2_usd.pct_change(3)
    m2_pct_change_12m = m2_usd.pct_change(12)
    m2_change_3m_12m = m2_pct_change_12m / m2_pct_change_3m
    m2_change_3m_12m_relative = relativize_to_avg(m2_change_3m_12m)
    m2_change_3m_12m_z = standardize(m2_change_3m_12m_relative)

    indicator = m2_change_3m_12m_z.iloc[-1].fillna(0)
    return indicator


def curr_acct_pct_gdp_indicator(curr_acct_pct_gdp: pd.DataFrame) -> pd.Series:
    """
    Computes the current account / GDP indicator, the difference between the 
    1-year and 4-year change in current account / GDP.

    Args:
        curr_acct_pct_gdp: A DataFrame containing each country's current 
            account balance as a percentage of GDP.

    Returns:
        Today's indicator values.

    """

    # Make sure the data is sampled quarterly
    assert curr_acct_pct_gdp.index.freq == 'Q-DEC'

    curr_acct_1y = curr_acct_pct_gdp.diff(QUARTERS_PER_YEAR)
    curr_acct_4y = curr_acct_pct_gdp.diff(4 * QUARTERS_PER_YEAR)
    curr_acct_1y_4y = curr_acct_4y - curr_acct_1y

    curr_acct_1y_4y_relative = relativize_to_avg(curr_acct_1y_4y)
    curr_acct_1y_4y_z = standardize(curr_acct_1y_4y_relative)

    indicator = curr_acct_1y_4y_z.iloc[-1].fillna(0)
    return indicator


def stock_bond_performance_indicator(
    stock_prices: pd.DataFrame,
    bond_prices: pd.DataFrame
) -> pd.Series:
    """
    Computes the relative stock/bond performance indicator, the difference
    between the yearly returns of stocks and bonds.

    Args:
        stock_prices: A DataFrame containing each country's stock prices.
        bond_prices: A DataFrame containing each country's bond prices.

    Returns:
        Today's indicator values.

    """

    stock_rets_1y = stock_prices.pct_change(WEEKDAYS_PER_YEAR)
    bond_rets_1y = bond_prices.pct_change(WEEKDAYS_PER_YEAR)
    bond_stock_spread = bond_rets_1y - stock_rets_1y

    bond_stock_spread_relative = relativize_to_avg(bond_stock_spread)
    bond_stock_spread_z = standardize(bond_stock_spread_relative)

    indicator = -bond_stock_spread_z.iloc[-1].fillna(0)
    return indicator


def change_in_gdp_indicator(
    gdp: pd.DataFrame
) -> pd.Series:
    """
    Computes the change in GDP indicator, each country's quarter over quarter 
    change in GDP. A two-quarter rolling average is taken to increase 
    accuracy.

    Args:
        gdp: A DataFrame containing each country's GDP data.

    Returns:
        Today's indicator values.

    """

    # Make sure the data is sampled quarterly
    assert gdp.index.freq == 'Q-DEC'

    gdp_change = gdp.pct_change().rolling(2).mean()
    gdp_change_relative = relativize_to_avg(gdp_change)
    gdp_change_z = standardize(gdp_change_relative)

    indicator = gdp_change_z.iloc[-1].fillna(0)
    return indicator


def indicator_to_trading_signal(indicator: pd.Series) -> pd.Series:
    """
    Converts indicator values for each country to a trading signal as a smooth
    function how of how unlikely it is to see those standard deviation values.

    Args:
        indicator: The indicator values for each country.

    Returns:
        The trading signal, each number between -1 and 1.

    """
    cdf_complement = 1 - 2 * norm.cdf(-np.abs(indicator))
    signed_cdf_complement = np.sign(indicator) * cdf_complement
    sigmoid_res = sigmoid(signed_cdf_complement, scale=4.5, deg=2) 

    return sigmoid_res


def calculate_returns(
    signal: Union[pd.DataFrame, pd.Series],
    bond_rets: Union[pd.DataFrame, pd.Series],
    weights: Optional[List[float]] = None,
    shift: int = 1
) -> Union[Tuple[pd.DataFrame, pd.Series], pd.Series]:
    """
    Calculates the overall bond returns from the given trading signal.

    Args:
        signal: The trading signal representing how long or short to go on 
            10-year bonds for each country. All values in the range [-1, 1].
        bond_rets: The daily percent change in bond prices for each country.
        weights: The weights for each country. If None, countries are 
            uniformly weighted.
        shift: How many days back to shift the bond return data. Default 1 day.

    Returns:
        If signal is for multiple countries, returns the weighted average over 
        all countries' daily returns, and the individual countries' returns. 
        
        If signal is for just one country, returns only the daily returns.

    """

    assert signal.index.freq == bond_rets.index.freq

    rets = signal * bond_rets.shift(-shift)
    
    if isinstance(signal, pd.DataFrame):
        weighted_rets = rets * weights if weights else rets
        overall_rets = weighted_rets.mean(axis=1)
        return (overall_rets, rets)
    else:
        return rets


def test_indicator(
    indicator_fn: Callable[..., pd.Series],
    index: pd.Index,
    data: Tuple[pd.DataFrame, ...],
    args: Tuple[Any, ...] = None,
    kwargs: Dict[str, Any] = None
):
    """
    Tests an indicator by generating a sequence of indicator values and 
    trading signals through time.

    Args:
        indicator_fn: The indicator function to test.
        index: The period index over which to compute the indicator values.
        data: A tuple of data streams required for the indicator.
        args: A tuple of any positional arguments required for the indicator 
            after the data.
        kwargs: A dictionary of any keyword arguments required for the 
            indicator after the data and positional args.

    Returns:
        indicators: The indicator values for each country, every day over the 
            period index.
        signals: The trading signal generated from the indicator, every day 
            over the period index.

    """
    
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = {}

    indicators = []
    signals = []

    for i, period in enumerate(index):
        indicator = indicator_fn(
            *(d[:period] for d in data),
            *args,
            **kwargs
        )
        indicators.append(indicator)

        trading_signal = indicator_to_trading_signal(indicator)
        assert (trading_signal <= 1).all() and (trading_signal >= -1).all()

        signals.append(trading_signal)

    indicators = pd.concat(indicators, axis=1).T
    signals = pd.concat(signals, axis=1).T

    # Convert to daily signal if the data is not daily
    if signals.index.freq in ['M', 'Q-DEC']:

        # TODO: is this correct? I think the wrong frequencies might be used.
        # Since 'M' and 'Q-DEC' are timed at month or quarter *end*, we don't
        # have access to a month's number until the following month.
        # Thus, we shift down by 1 and forward fill, so each day of this 
        # month/quarter has last month's/quarter's values.
        # signals = signals.shift(1).resample('B').ffill()
        signals = signals.resample('B').ffill()

    if indicators.index.freq in ['M', 'Q-DEC']:
        # indicators = indicators.shift(1).resample('B').ffill()
        indicators = indicators.resample('B').ffill()

    return indicators, signals
    
