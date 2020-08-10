#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# ind_1_return_diff.py
# This file is an indicator object that calculates the indicator from the data and makes the data
# retrievable, either by country or as a complete data set
#
# LOGIC: Relative stock and bond performance
#        During relatively higher equity growth, people will tend to favor equity investment
#
# IMPLEMENTATION: Calculates running average of annual returns for equities and bonds. For each trading day,
#                 get the annual growth of equities and bonds and compare to the running average. This will
#                 provide a percentage higher or lower of this year's returns compared to average returns, which
#                 tells us performance relative to historical performance. This is a proxy for future expected
#                 performance. The difference of this "expected performance" will be the indicator (capped b.w. [-1,1])
#
# SELF NOTE: move on to the second indicator; this one is done
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


class Indicator1:

    def __init__(self):
        self.currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.parentdir = os.path.dirname(self.currentdir)
        sys.path.insert(0, self.parentdir)
        register_matplotlib_converters()

        self.dl = DataLib("SignalData")

        weekdays_in_year = 261
        quarter_year = 65
        bond_returns = self.dl.pull('BondRetIdx/LocalFX')
        equity_prices = self.dl.pull('EquityPrices')

        # this will be "future returns" (starting today) instead of past returns (starting 6 months ago)
        self.bond_semiannual_return = bond_returns.pct_change(quarter_year, fill_method=None)
        self.bond_semiannual_return = self.bond_semiannual_return.shift(-quarter_year)

        # calculate the rolling average annual growth of stocks and bonds, drop na so starts 1 year later
        average_annual_growth_bond = bond_returns.pct_change(weekdays_in_year, fill_method=None)
        average_annual_growth_equity = equity_prices.pct_change(weekdays_in_year, fill_method=None)
        rmag_bond = average_annual_growth_bond.rolling(len(average_annual_growth_bond), min_periods=1).mean()
        rmag_equity = average_annual_growth_equity.rolling(len(average_annual_growth_equity), min_periods=1).mean()

        # copy dates into a new indicator data frame
        self.ind_1_return_diff = rmag_bond.copy()
        self.ind_1_return_diff[self.ind_1_return_diff != 0] = 0

        # iterate and calculate the indicator
        for country, series in self.ind_1_return_diff.iteritems():
            for date, _ in series.iteritems():
                recent_bond_growth = average_annual_growth_bond[country][date]
                recent_equity_growth = average_annual_growth_equity[country][date]

                mean_bond_growth = rmag_bond[country][date]
                mean_equity_growth = rmag_equity[country][date]

                bond_growth_ratio = recent_bond_growth / mean_bond_growth - 1
                equity_growth_ratio = recent_equity_growth / mean_equity_growth - 1

                # take the difference of the growth ratios (limit to between -1 and 1); may be NaN
                self.ind_1_return_diff[country][date] = max(min((bond_growth_ratio - equity_growth_ratio), 1), -1)

    # returns the indicator data - assumes country is valid if provided
    def get_indicator(self, country = None):
        if country is None:
            return self.ind_1_return_diff
        else:
            try:
                country_indicator = self.ind_1_return_diff[country]
            except KeyError:
                print('invalid country: ' + str(country))
                country_indicator = None
            return country_indicator

    def graph_indicator(self, country):
        fig, ax1 = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(20)
        ax2 = ax1.twinx()
        ax1_label = 'Bond Quarterly Future Return'
        ax1.plot(self.bond_semiannual_return[country].to_timestamp(), label=ax1_label)
        ax1.set_ylabel(ax1_label)
        ax1.legend()
        ax2_label = 'Equity Bond Return Difference'
        ax2.plot(self.ind_1_return_diff[country].to_timestamp(), color='tab:red', label=ax2_label)
        ax2.set_ylabel(ax2_label)
        ax2.legend()
        plt.title('Bond Quarterly Forward Return and Equity Bond Return Difference')
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')
        plt.show()


