#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# signals.py
#
# This file contains functions that processes indicators, returns signals.
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


# generate signal for a single country
def generate_signal_single(indicator, country):
    country_ind = indicator[country]
    signal = country_ind.copy()
    signal[signal != 0] = 0

    for date in signal.index:
        today_z = country_ind[date]

        # if the indicator is nan, signal is nan
        if math.isnan(today_z):
            signal[date] = float('nan')
            continue

        # cap the z scores at -.5 and .5 for long and short positions respectively
        if today_z > .5:
            signal[date] = -1
        elif today_z < -.5:
            signal[date] = 1
        else:
            signal[date] = -1 * today_z / .5

    return signal


# generate signal for a country system
def generate_signal_system(indicator, weights):
    sum_of_weights = sum(weights.values())
    countries = weights.keys()

    # normalize the weights
    normal_weights = normalize_weights(weights)

    # create a new data frame for the signal
    signal = indicator[countries].copy()
    signal[signal != 0] = 0

    for date in signal.index:
        # create dictionary of indicator values
        today_vals = {}
        has_nan = False
        for country in countries:
            country_val = indicator[country][date]
            # just skip this date if any are NaN - keep track for later
            if math.isnan(country_val):
                has_nan = True
                break
            today_vals[country] = country_val

        # if any country has nan for indicator, fill signal on this date with nan and move on
        if has_nan:
            for country in countries:
                signal[country][date] = float('nan')
            continue

        sum_weighted_ind = sum([today_vals[country] * normal_weights[country] for country in countries])

        # adjust the positions so that the weighted average is 0
        positions = {}
        for country in countries:
            # negative 1 to flip the effect of the indicator (gdp and inflation negative effect)
            positions[country] = -1 * (indicator[country][date] - sum_weighted_ind)

        # scale the posititions down so that the max position is 1 in abs
        position_values = list(positions.values())
        scaling_factor = max(max(position_values), abs(min(position_values)))
        for country in countries:
            signal[country][date] = positions[country] / scaling_factor

    return signal


def show_signals(signal, country=None):
    country_string = ' '
    if country is None:
        country_string = ''
    else:
        country_string = country_string + country

    plt.figure(figsize=(20, 5))
    signal.plot()
    plt.title('Signals Over Time' + country_string)
    plt.show()


def normalize_weights(weights):
    sum_of_weights = sum(weights.values())
    normalized_weights = {}
    for key, value in weights.items():
        normalized_weights[key] = weights[key] / sum_of_weights
    return normalized_weights
