#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# returns.py
#
# This file contains functions that help calculate and visualize returns
#

import math
import statistics
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import matplotlib.pyplot as plt
from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib, DatastreamPulls
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
from signals import normalize_weights


def get_returns_single(signal, country):
    dl = DataLib("SignalData")
    bond_returns = dl.pull('BondRetIdx/LocalFX')

    # upsample in case dates are not by business days
    upsampled_signal = signal.resample('1B').ffill()

    earliest_date = upsampled_signal.index.min()
    latest_date = bond_returns.index.max()

    lagged_bond_returns = bond_returns[country].pct_change().shift(-1)[earliest_date:latest_date]
    portfolio_returns = lagged_bond_returns * upsampled_signal[:latest_date]

    return portfolio_returns, lagged_bond_returns


def get_returns_system(signal, weights):
    dl = DataLib("SignalData")
    bond_returns = dl.pull('BondRetIdx/LocalFX')

    # upsample in case dates are not by business days
    upsampled_signal = signal.resample('1B').ffill()

    countries = weights.keys()

    # normalize the weights
    normal_weights = normalize_weights(weights)

    lagged_bond_returns = bond_returns[countries].pct_change().shift(-1)

    # copy the dates of the signal, create returns for our positions and fully long
    portfolio_returns = lagged_bond_returns[list(countries)[0]].copy()
    portfolio_returns[portfolio_returns != 0] = 0
    long_returns = lagged_bond_returns[list(countries)[0]].copy()
    long_returns[long_returns != 0] = 0

    for date in lagged_bond_returns.index:
        # get the bond returns and positions for this date
        today_positions = {}
        today_returns = {}
        has_nan = False
        for country in countries:
            country_signal = upsampled_signal[country][date]
            country_returns = lagged_bond_returns[country][date]
            # just skip this date if any are NaN - keep track for later
            if math.isnan(country_signal) or math.isnan(country_returns):
                has_nan = True
                break
            today_positions[country] = country_signal
            today_returns[country] = country_returns

        # if any country has nan for signal, fill returns on this date with nan and move on
        if has_nan:
            long_returns[date] = float('nan')
            portfolio_returns[date] = float('nan')
            continue

        # take a weighted average for long returns, include position for portfolio returns
        long_returns[date] = sum([normal_weights[country] * today_returns[country] for country in countries])
        portfolio_returns[date] = sum(
            [normal_weights[country] * today_returns[country] * today_positions[country] for country in countries])

    return portfolio_returns, long_returns


def graph_returns(portfolio_returns, benchmark_returns):
    sum_portfolio_returns = portfolio_returns.cumsum()
    sum_benchmark_returns = benchmark_returns.cumsum()

    plt.figure(figsize=(20, 5))
    sum_portfolio_returns.plot()
    sum_benchmark_returns.plot()
    plt.title('Cumulative Returns')
    plt.legend(['Portfolio Returns', 'Benchmark Returns'])
    plt.show()

    latest_date = sum_portfolio_returns.index.max()
    print('Active Money Made: ' + str(sum_portfolio_returns[latest_date - BDay(1)]))
    print('Passive Money Made: ' + str(sum_benchmark_returns[latest_date - BDay(1)]))


# combine the returns into one portfolio
def combine_returns(portfolio_returns, benchmark_returns, portfolio_weight=1, benchmark_weight=1):
    n_portfolio_weight = portfolio_weight / (portfolio_weight + benchmark_weight)
    n_benchmark_weight = benchmark_weight / (portfolio_weight + benchmark_weight)

    return portfolio_returns * n_portfolio_weight + benchmark_returns * n_benchmark_weight


# note that this function takes around 5-10 minutes to run, since it's constantly reevaluating the SD
def get_risk_adjusted_returns(portfolio_returns, benchmark_returns):
    # get rolling SD of benchmark returns - cut through for risk of benchmark
    benchmark_sd = benchmark_returns.rolling(len(portfolio_returns), min_periods=1).std()

    risk_adjust_returns = portfolio_returns.copy()
    risk_adjust_returns[risk_adjust_returns != 0] = 0

    # skip risk adjustment for the first 100 days to estimate SD
    cnt = 100
    rar_history = []
    for date in portfolio_returns.index:
        today_port_returns = portfolio_returns[date]

        # don't count nan days
        if math.isnan(today_port_returns):
            risk_adjust_returns[date] = float('nan')
            continue

        if cnt > 0:
            cnt -= 1
            rar_history.append(today_port_returns)
            risk_adjust_returns[date] = today_port_returns
            continue

        today_port_sd = statistics.stdev(rar_history)
        today_bench_sd = benchmark_sd[date - BDay(1)]

        # avoid doing math with nan
        if math.isnan(today_port_sd) or math.isnan(today_bench_sd):
            risk_adjust_returns[date] = float('nan')
            continue

        # leverage portfolio returns by the ratio of risk to benchmark
        risk_ratio = today_bench_sd / today_port_sd
        risk_adjust_return = today_port_returns * risk_ratio

        rar_history.append(risk_adjust_return)
        risk_adjust_returns[date] = risk_adjust_return

    return risk_adjust_returns


# calculates annualized mean, sd, and Sharpe ratio for returns
def get_stats(returns):
    annualized_returns = []

    # sum through all returns of a particular year, for all years
    year = 0
    curr_sum = 0
    for date in returns.index:
        if math.isnan(returns[date]):
            continue

        curr_year = date.year

        if not curr_year == year:
            annualized_returns.append(curr_sum)
            year = curr_year
            curr_sum = returns[date]
        else:
            curr_sum += returns[date]

    mean_annual_return = statistics.mean(annualized_returns)
    annual_return_sd = statistics.stdev(annualized_returns)
    annual_sharpe = mean_annual_return / annual_return_sd

    return mean_annual_return, annual_return_sd, annual_sharpe
