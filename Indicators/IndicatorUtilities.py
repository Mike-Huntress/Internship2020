from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

dl = DataLib("SignalData")

def AnnualizedChangeTimeSeries(series, datafreq = None, period = None):
    """
    Takes a series (column of data frame) with data at frequency datafreq and returns a dataframe where the value at time
    T is the annualized growth from T-period to T.

    :param series: A time series, most likely taken as a column from dl
    :param datafreq: string of 'D', 'M', or 'Y', indicating whether data is daily, monthly, or yearly
    :param period: an integer representing the number of units of datafreq to calculate percent change over; eg, if
            datafreq = 'M', period = 12 would indicate taking intervals of 12 months
    :return: series with annualized percent change from T-period to T.

    Implicitly assumes that period > datafreq.
    """

    # Get number of observations per year
    UNITS_IN_YEAR = {'D': 261, 'M': 12, 'Y': 1, 'Q': 4}
    assert datafreq in UNITS_IN_YEAR
    Annual_Units = UNITS_IN_YEAR[datafreq]

    assert type(period) == int
    series_ChangeUnannualized = series.pct_change(period, fill_method = None).dropna(how='all')
    series_ChangeAnnualized = (series_ChangeUnannualized + 1)**(Annual_Units/period) - 1

    return series_ChangeAnnualized

def NormalizeDF(df, window, center = None):
    """
    Normalize each column of a dataframe df to mean 0, stdev 1
    :param df: dataframe
    :param window: number of periods to calculate std over
    :param center: optional argument for scaling around a specific value (most useful if relative to 0 mean is meaningful)
    :return: dataframe where each column has mean 0 and standard deviation 1
    """

    if center is None:
        normalized_df = (df - df.rolling(window, min_periods=window//1).mean()) / df.rolling(window, min_periods=window//1).std()

    else:
        normalized_df = (df - center) / df.rolling(window, min_periods=window//1).std()


    return normalized_df

    # TODO: calculate standard deviation using only past data

    # df = dataframe.copy()
    # cols = df.columns
    #
    # for col in cols:
    #     mean = df[col].dropna().mean()
    #     std = df[col].dropna().std()
    #     df[col] = (df[col] - mean) / std
    #
    # return df

def GraphDifferentAxes(series, title, xlim = None):
    """
    Creates graph of 2 or 3 different time series, each with their own axis
    
    :param series: a list of either 2 or 3 elements, where each element is a list of the form
            [Time Series data (as Pandas series), ylabel (string), label in legend (string)]
    :param title: a string to be the title of the graph
    :param xlim: optional tuple specifiying limits on x
            
    :return: None outputs graph using matplotlib
    """

    assert (len(series) == 2 or len(series) == 3 or len(series) == 4)

    series0, ylabel0, legendlabel0 = series[0]
    series1, ylabel1, legendlabel1 = series[1]

    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()

    host.set_xlabel("Date")
    host.set_ylabel(ylabel0)
    par1.set_ylabel(ylabel1)

    p1, = host.plot(series0.to_timestamp(), label=legendlabel0)
    p2, = par1.plot(series1.to_timestamp(), label=legendlabel1)

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())

    if xlim is not None:
        host.set_xlim(xlim)
        par1.set_xlim(xlim)

    if len(series) >= 3:
        series2, ylabel2, legendlabel2 = series[2]
        par2 = host.twinx()

        offset = 60
        new_fixed_axis = par2.get_grid_helper().new_fixed_axis
        par2.axis["right"] = new_fixed_axis(loc="right",
                                            axes=par2,
                                            offset=(offset, 0))

        par2.axis["right"].toggle(all=True)
        par2.set_ylabel(ylabel2)
        p3, = par2.plot(series2.to_timestamp(), label=legendlabel2)
        par2.axis["right"].label.set_color(p3.get_color())

        if xlim is not None:
            par2.set_xlim(xlim)

    if len(series) == 4:
        series3, ylabel3, legendlabel3 = series[3]
        par3 = host.twinx()

        offset = 120
        new_fixed_axis = par3.get_grid_helper().new_fixed_axis
        par3.axis["right"] = new_fixed_axis(loc="right",
                                            axes=par3,
                                            offset=(offset, 0))

        par3.axis["right"].toggle(all=True)
        par3.set_ylabel(ylabel3)
        p4, = par3.plot(series3.to_timestamp(), label=legendlabel3)
        par3.axis["right"].label.set_color(p4.get_color())

        if xlim is not None:
            par3.set_xlim(xlim)

    host.legend()

    plt.title(title)

    plt.draw()

    plt.show()


def RescaleDF(df):
    """
    Rescales a DF so that values from [-2,2] have an image of [-1,1]. Observations beyond bounds set at -1 and 1.
    :param df: Dataframe
    :return: Dataframe with no values larger than 1 or less than -1 (rescaling form (-2, 2)
    """
    df_new = df.copy()
    df_new = df_new / 2
    df_new = df_new.apply(lambda x: [y if y > -1 else -1 if pd.notnull(y) else y for y in x])
    df_new = df_new.apply(lambda x: [y if y < 1 else 1 if pd.notnull(y) else y for y in x])

    return df_new

def PLTotal(Signal):
    """
    Given a monhtly signal from -1 to 1, and return df of cumulativeExcess PL (hedging with currency and removing
        excess returns)
    :param Signal: a dataframe for each country with a monthly signal in range -1 to 1
    :return: dataframe with Excess PL made from trading on that signal (cumulative)
    """

    # Calculate cumulative PL, assuming no reinvestment
    PL_Raw = PLRaw(Signal)
    PL_Total = PL_Raw.cumsum()

    return PL_Total

def PLRaw(Signal):
    """
    Given a monhtly signal from -1 to 1, and return df of Excess PL (hedging with currency and removing excess returns)
    :param Signal: a dataframe for each country with a monthly signal in range -1 to 1
    :return: dataframe with Excess PL made from trading on that signal (raw)
    """

    # Get raw data streams
    BondPrices = dl.pull("BondRetIdx/LocalFX")
    FXvsUSD = dl.pull('fxVsUSD')
    RiskfreeRates = dl.pull('RiskfreeRates') / 100

    # Get daily return
    BondReturn_Daily = BondPrices.pct_change(1).shift(-1)

    # Sum return over month
    BondReturn_Monthly = BondReturn_Daily.resample('1M').sum()

    # Hedge out currency
    fxVsUSD_Monthly = FXvsUSD.pct_change(1).shift(-1)
    HedgedReturn = BondReturn_Monthly - fxVsUSD_Monthly

    # Calculate Excess Returns, subtracting out Signal * Riskfree-rate
    RiskfreeRatesMonthly = (1 + RiskfreeRates) ** (1 / 12) - 1
    ExcessReturn = HedgedReturn.sub(Signal.multiply(RiskfreeRatesMonthly['USA'], axis = 0), axis = 0)

    # Calculate raw PL, assuming no reinvestment
    PL_Raw = ExcessReturn * (Signal)

    return PL_Raw

#
# BondPrices = dl.pull("BondRetIdx/LocalFX")
# FXvsUSD = dl.pull('fxVsUSD')
# RiskfreeRates = dl.pull('RiskfreeRates') / 100
#
# # Get daily return
# BondReturn_Daily = BondPrices.pct_change(1).shift(-1)
#
# # Sum return over month
# BondReturn_Monthly = BondReturn_Daily.resample('1M').sum()
#
# # Hedge out currency
# fxVsUSD_Monthly = FXvsUSD.pct_change(1).shift(-1)
# HedgedReturn = BondReturn_Monthly - fxVsUSD_Monthly
#
# # Calculate Excess Returns
# RiskfreeRatesMonthly = (1 + RiskfreeRates) ** (1 / 12) - 1
# ExcessReturn = HedgedReturn.sub(RiskfreeRatesMonthly['USA'], axis = 0)
#
# # Calculate cumulative PL, assuming no reinvestment
# PL_Raw = RiskfreeRatesMonthly * (1)
# PL_Total = PL_Raw.cumsum()
#
# PL_Total.plot()
# plt.show()