#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# indicators.py
#
# This file contains functions that return the indicators.
#

import math
import statistics
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import matplotlib.pyplot as plt
from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib, DatastreamPulls
import pandas as pd
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# get indicator about business cycles
# inflation and gdp growth have a negative effect on bond returns
def get_ind_gdp_infla():
    dl = DataLib("SignalData")
    gdpReal = dl.pull("GDP/Real")
    inflation = dl.pull("CoreCPI/SA")

    # graph of the GDP growth vs. future quarter bond returns
    rgdp_growth = gdpReal.pct_change()
    inflation_growth = inflation.pct_change()

    # rolling 5-year average and SD of the inflation growth
    rmg_inflation = inflation_growth.rolling(len(inflation_growth), min_periods=1).mean()
    rsd_inflation = inflation_growth.rolling(len(inflation_growth), min_periods=1).std()

    # rolling 10-year average and SD of RGDP growth
    rmg_rgdp = rgdp_growth.rolling(len(rgdp_growth), min_periods=1).mean()
    rsd_rgdp = rgdp_growth.rolling(len(rgdp_growth), min_periods=1).std()

    inflation_growth_z = (inflation_growth - rmg_inflation) / rsd_inflation
    rgdp_growth_z = (rgdp_growth - rmg_rgdp) / rsd_rgdp

    # copy dates into a new indicator data frame
    ind_gdp_infla = inflation_growth_z.copy()
    ind_gdp_infla[ind_gdp_infla != 0] = 0

    # iterate and calculate the indicator
    for country, series in ind_gdp_infla.iteritems():
        # running weighted average of gdp_z and inflation_z per country
        raw_value_history = []

        for date, _ in series.iteritems():
            inflation_z = inflation_growth_z[country][date]
            gdp_z = rgdp_growth_z[country][date]

            # case, since inflation or gdp value may be NaN
            curr_val = None
            if math.isnan(inflation_z) or math.isnan(gdp_z):
                ind_gdp_infla[country][date] = float('nan')
                continue
            else:
                # take weighted average of z scores
                weights = {'inflation': 1, 'gdp': 2}
                sum_weights = sum(weights.values())
                curr_val = (weights['inflation'] / sum_weights) * inflation_z + (weights['gdp'] / sum_weights) * gdp_z

            raw_value_history.append(curr_val)

            if len(raw_value_history) < 2:
                ind_gdp_infla[country][date] = 0
            else:
                curr_sd = statistics.stdev(raw_value_history)
                curr_mean = statistics.mean(raw_value_history)
                # make sure sd is not 0, if it is, make it 1 to divide by 1
                if curr_sd == 0:
                    curr_sd += 1
                ind_gdp_infla[country][date] = (curr_val - curr_mean) / curr_sd

    return ind_gdp_infla
