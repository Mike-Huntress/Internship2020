#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# test_returns.py
# This file contains the function to generate graphs and metrics that test returns
#

import math
import os,sys,inspect

import matplotlib.pyplot as plt
from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib, DatastreamPulls
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
from pandas.plotting import register_matplotlib_converters


class SignalGenerator:

    def __init__(self):
        self.dl = DataLib("SignalData")

    def test_returns(self, country, signal):
        bond_returns = self.dl.pull('BondRetIdx/LocalFX')

        earliest_date = signal.index.min()
        latest_date = signal.index.max()

        lagged_bond_returns = bond_returns[country].pct_change().shift(-1)[earliest_date:]
        daily_returns = lagged_bond_returns * signal

        sum_our_returns = daily_returns.cumsum()
        sum_bond_returns = lagged_bond_returns.cumsum()

        plt.figure(figsize=(20, 5))
        sum_our_returns.plot()
        sum_bond_returns.plot()
        plt.title('Cumulative Returns')
        plt.legend(['Our ' + country + ' Cumulative Returns', country + ' Cumulative Bond Returns'])
        plt.show()

        print('Starting Date: ' + str(earliest_date))
        print('Active Money Made: ' + str(sum_our_returns[latest_date - BDay(1)]))
        print('Passive Money Made: ' + str(sum_bond_returns[latest_date - BDay(1)]))

    def show_signals(self, signal):
        plt.figure(figsize=(20, 1))
        signal.plot()
        plt.title('Signals Over Time')
        plt.show()