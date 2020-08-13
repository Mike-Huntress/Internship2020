# If the below code doesn't work uncomment this and run (this adds the parent directory to the path)
import sys
sys.path.insert(0,"C:\\Users\\Paolo\\.virtualenvs\\Internship2020-9r0W5TXr\\Lib\\site-packages")
sys.path.insert(1,"C:\\Users\\Paolo\\.virtualenvs\\Internship2020-9r0W5TXr")

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(2,parentdir)
sys.path.insert(3,"C:\\Users\\Paolo\\Google Drive\\Shared_Files\\3-Junior\\3-BW\\Project\\Internship2020\\Indicators")


from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib, DatastreamPulls
import pandas as pd
import numpy as np

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

import statistics

import importlib
import Indicators.IndicatorUtilities as Util
importlib.reload(Util)

countries = CountryMetaDataFile().readMetadata()
dl = DataLib("SignalData")

##################################################
# Data Stream 1: Relative Curve Height
##################################################
# Intuition -- A country with a higher relative curve height is more likely to experience demand for their bonds, thus
# raising prices


LongRates = dl.pull("LongRates")
ShortRates = dl.pull("ShortRates")

# Generate Curve Height as average of the two
CurveHeight = (LongRates + ShortRates) / 2

# Generate Relative Curve height as difference compared to the mean of all countries in that time period
RelativeCurveHeight = CurveHeight.sub(CurveHeight.mean(axis=1), axis=0)

# Normalize
RelativeCurveHeight_Normalized = Util.NormalizeDF(RelativeCurveHeight, 120)

# RelativeCurveHeight_Normalized.plot()
# plt.xlabel('Date')
# plt.ylabel('RelativeCurveHeight')
# plt.title('RelativeCurveHeight By Country')
# plt.show(block=True)

# TODO: do something to normalize by inflation expectations, currency hedging, because real returns matter?

all_countries = RelativeCurveHeight.columns

# Plots to see relative curve height and returns
# for country in all_countries:
#     temp = pd.DataFrame()
#
#     temp['Height'] = RelativeCurveHeight[country]
#     temp['Return'] = BondReturn_Future[country]
#
#     print(temp.corr())
#
#     plt.scatter(temp['Height'], temp['Return'])
#     plt.title("Real vs Signal for " + country)
#     plt.xlabel('Relative Curve Height')
#     plt.ylabel('Future Returns')
#     plt.show()


##################################################
# Data Stream 2: Risk Premium
##################################################
# Intuition: When risk premium is higher, there is likely to be more demand for long-term bonds, increasing prices

RiskPremium = LongRates - ShortRates
# Normalize over past 10 years
RiskPremium_Normalized = Util.NormalizeDF(RiskPremium, 120)

# # Plot to see how this changes over time
# RiskPremium_Normalized.plot()
# plt.xlabel('Date')
# plt.ylabel('RiskPremium')
# plt.title('RiskPremium By Country (Normalized)')
# plt.show(block=True)


# # Test how well it predicts
# for country in all_countries:
#     temp = pd.DataFrame()
#
#     temp['Premium'] = RiskPremium[country]
#     temp['Return'] = BondReturn_Future[country]
#
#     print(temp.corr())
#
#     plt.scatter(temp['Premium'], temp['Return'])
#     plt.title("Real vs Signal for " + country)
#     plt.xlabel('Risk Premium')
#     plt.ylabel('Future Returns')
#     plt.show()


##################################################
# Data Stream 3: Equity/Bond Relative performance
##################################################

# Intuition: When equities are doing well, investors expect this performance to continue, lowering demand for bonds

EquityPrices = dl.pull("EquityPrices")
BondPrices = dl.pull("BondRetIdx/LocalFX")
ShortRates = dl.pull("ShortRates")

# # Plot prices
# for country in ["USA"]:
#     EquityPrices[country].plot(label="Equities")
#     BondPrices[country].plot(label="Bonds")
#     plt.xlabel('Date')
#     plt.ylabel('Prices')
#     plt.legend()
#     plt.title('Equities vs Bonds')
#     plt.show(block = True)


# Compute average daily return over past year
EquityPrices_PctChange = Util.AnnualizedChangeTimeSeries(EquityPrices, 'D', 261)
BondPrices_PctChange = Util.AnnualizedChangeTimeSeries(BondPrices, 'D', 261)

# # Plot example of these returns
# for country in ["USA"]:
#     EquityPrices_PctChange[country].plot(label="Equities")
#     BondPrices_PctChange[country].plot(label="Bonds")
#     plt.xlabel('Date')
#     plt.ylabel('Return')
#     plt.legend()
#     plt.title('Equities vs Bonds Return (Raw)')
#     plt.show(block = True)

# Compute Risk-adjusted returns for equities and bonds
ShortRatesDaily = ShortRates.resample('1B').ffill() / 100

EquityPrices_PctChangeSharpe = (EquityPrices_PctChange - ShortRatesDaily) / EquityPrices_PctChange.rolling(261 * 10).std()
BondPrices_PctChangeSharpe = (BondPrices_PctChange - ShortRatesDaily) / BondPrices_PctChange.rolling(261 * 10).std()

# # Plot Risk-adjusted returns
# for country in ["USA"]:
#     EquityPrices_PctChangeSharpe[country].plot(label="Equities Risk-Adjusted")
#     BondPrices_PctChangeSharpe[country].plot(label="Bonds Risk-Adjusted")
#     plt.xlabel('Date')
#     plt.ylabel('Return (Risk-adjusted)')
#     plt.legend()
#     plt.title('Equities vs Bonds Return (Risk-Adjusted)')
#     plt.show()

# Compute normalized relative monthly growth, with center at 0
EquityBondRelative = (EquityPrices_PctChangeSharpe - BondPrices_PctChangeSharpe) / 100
EquityBondRelative_Normalized = Util.NormalizeDF(EquityBondRelative, 2610, center = 0)
EquityBondRelativeMontly_Normalized = EquityBondRelative_Normalized.resample('1M').first()

DemandSignal1 = RelativeCurveHeight_Normalized
DemandSignal2 = RiskPremium_Normalized
DemandSignal3 = - EquityBondRelativeMontly_Normalized

# Graphically examine validity across all countries
# Demand Signal 2 does best
# Demand Signal 3 has somehwat positive returns
# Demand Signal 1 does not do well, looks effectively like noise

# Appears that good signal would be 2 (risk premium) + 3 (equity/bond), rescaled to be mean 0 std 1
DemandSignal = (DemandSignal2 + DemandSignal3) * (2 ** .5) / 2

# Rescale
DemandSignalScaled = Util.RescaleDF(DemandSignal)


PL_Total = Util.PLTotal(DemandSignalScaled)

if __name__ == '__main__':
    for i in [DemandSignal1, DemandSignal2, DemandSignal3]:
        # i.plot()
        # plt.show()
        print(i.mean().mean())

    print(DemandSignalScaled.mean().mean())

    PL_Total.plot(figsize=(8, 6))
    plt.title("Excess P+L from Demand Signal (Hedged Against Currency)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative P+L")
    plt.xlim(left=12*30)
    plt.savefig('demand_pl.png')
    plt.show(block = False)

    # Plot signal
    DemandSignal.plot(figsize=(8, 6))
    plt.title("Demand Signal")
    plt.xlabel("Date")
    plt.ylabel("Demand Signal")
    plt.xlim(left=12*30)
    plt.savefig('demand_signal.png')
    plt.show(block = False)


# PL1, PL2 = Util.PLRaw(DemandSignal2), Util.PLRaw(DemandSignal3)
# sum = 0
# for country in PL1.columns:
#     sum += PL1[country].corr(PL2[country])
# average_corr = sum / len(PL1.columns)
# print(average_corr)
