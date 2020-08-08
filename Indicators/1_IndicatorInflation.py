# TODO: Reduce noise in M2 signal
# TODO: Find better way to aggregate the two raw data series
# TODO: Deal with missing data in 1980s

# Generate signal for how the central bank will change interest rates as a response to everything except inflation
# Include economic growth and current account

from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib
import Indicators.IndicatorUtilities as Util
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import scipy


countries = CountryMetaDataFile().readMetadata()
dl = DataLib("SignalData")

##################################################
# Data Stream 1: Inflation Differential
##################################################
# Intuition -- in developing world, inflation is generally stable; expect inflation to move towards the mean of
# inflation for the previous3 years

# Generate Measure of Inflation
CoreCPI = dl.pull("CoreCPI/SA")
Inflation = Util.AnnualizedChangeTimeSeries(CoreCPI, 'M', 1)

# Take 3Y mean
Inflation_3Y_Mean = Inflation.rolling(36).mean()

# Compute difference between inflation and its recent average
Inflation_Difference = Inflation - Inflation_3Y_Mean

# Test Code to see how well it performs in one specific country
############

# Inflation['DEU'].plot(label = 'Level')
# Inflation_3Y_Mean['DEU'].plot(label = '3Y mean')
# Inflation_Difference['DEU'].plot(label = 'Difference')
#
# plt.xlabel('Date')
# plt.ylabel('Inflation')
# plt.title('German Inflation')
# plt.show(block = True)


# Note that we need not normalize this by recentering the mean -- what matters is the actual raw differential from the
# current period to historical average

print(Inflation_Difference.stack().mean())

# Overall mean is fairly close to 0, meaning it is a net-neutral signal

##################################################
# Data Stream 2: Changes in M2 Money Supply
##################################################
# Intuition: When money supply increases, there is more money chasing the same amount of goods, so price levels rise

M2 = dl.pull("M2/inUSD")

# Generate 3M Series
M2_3M_PctChange = Util.AnnualizedChangeTimeSeries(M2, 'M', 3)
# Generate 1Y series
M2_1Y_PctChange = Util.AnnualizedChangeTimeSeries(M2, 'M', 12)

# Generate Difference
M2_3M_Minus_1Y_Change = M2_3M_PctChange - M2_1Y_PctChange

# Generate series for AUS -- assume percent changes are identical to M3
M3 = dl.pull("M3/inUSD")

# Generate 3M Series
M3_3M_PctChange = Util.AnnualizedChangeTimeSeries(M3, 'M', 3)
M3_1Y_PctChange = Util.AnnualizedChangeTimeSeries(M3, 'M', 12)
M3_3M_Minus_1Y_Change = M3_3M_PctChange - M3_1Y_PctChange

# replace in M2
M2_3M_Minus_1Y_Change['AUS'] = M3_3M_Minus_1Y_Change['AUS']

# Normalize Data across past 10 years
M2_3M_Minus_1Y_Change_Normalized = Util.NormalizeDF(M2_3M_Minus_1Y_Change, 120)

# Plot
# M2_3M_Minus_1Y_Change_Normalized.plot()
# plt.xlabel('Date')
# plt.ylabel('3M - 1Y Growth, Normalized')
# plt.title('M2, 3M - 1Y growth rate')
# plt.show(block = False)

# Testing how well it predicts -- not well
# df['M2'] = M2_3M_Minus_1Y_Change_Normalized['DEU']
# print(df.head())
#
# plt.scatter(df['M2'], df['FutureChange'])
# plt.show()

##################################################
# Data Stream 3: FX Appreciation
##################################################
# Intuition: When currency appreciates, it is cheaper to buy foreign goods, and so price levels net decrease
# Note: Idiosyncrasies in GBR and USA Rates to be fixed

fxVsUSD = dl.pull('fxVsUSD')

# For only GBR, invert GBR foreign rate to get number of pounds per dollar (data reporting is in reverse)
fxVsUSD['GBR'] = 1 / fxVsUSD['GBR']

# print(fxVsUSD.tail())

# Turn data into average growth over past 6 months
fxVsUSD_PctChange = Util.AnnualizedChangeTimeSeries(fxVsUSD, 'M', 6)

# Normalize over past 10 Years
fxVsUSD_PctChange_Normalized = Util.NormalizeDF(fxVsUSD_PctChange, 120)

# Set USA changes to 0, since it is the base currency
fxVsUSD_PctChange_Normalized['USA'] = 0

# Plot
# fxVsUSD_PctChange_Normalized.plot()
# plt.xlabel('Date')
# plt.ylabel('fx Growth vs USD over last 6 months, Normalized')
# plt.title('FX Percent Change (normalized)')
# plt.show(block = True)

# Testing how well it predicts -- not well
# df['FX'] = fxVsUSD['DEU']
# print(df.head(200))
#
# plt.scatter(df['FX'], df['FutureChange'])
# plt.show()

##################################################
# Create Overall Signal
##################################################

# Difference creates negative pressure on inflation
# M2 creates positive pressures on inflation
# FX Creates negative pressures on inflation

# Test each signal independently -- M2 and FX have similar characteristics, and so only one should be used.
# NB: The multipliers here are simply to make the two on the same relative "scale".
# TODO actually normalize Inflation signal, rather than scaling it manually like this. (Requires STD across all countries?)

# InflationSignal = (-Inflation_Difference * 100 - fxVsUSD_PctChange_Normalized) / 1
# InflationSignal = -Inflation_Difference / 1
# InflationSignal = M2_3M_Minus_1Y_Change_Normalized / 1
# InflationSignal = -fxVsUSD_PctChange_Normalized / 1

for country in ['DEU']:
    for Signal in [-Inflation_Difference , M2_3M_Minus_1Y_Change_Normalized, -fxVsUSD_PctChange_Normalized ]:
        InflationFuture = Inflation.shift(-1)
        df = pd.DataFrame()
        df['y'] = InflationFuture[country]
        df['x'] = Signal[country]
        plt.scatter(df['x'], df['y'])
        plt.show()

InflationSignal = InflationFuture

# Graphically examine validity across all countries

# Assume invest at each month using signals at that point in time
BondPrices = dl.pull("BondRetIdx/LocalFX")
BondPrices_Monthly = BondPrices.resample('1M').first()

# Get Monthly returns, hedged from currency

BondPrices = dl.pull("BondRetIdx/LocalFX")
FXvsUSD = dl.pull('fxVsUSD')

# Get daily return
BondReturn_Daily = BondPrices.pct_change(1).shift(-1)

# Sum return over month
BondReturn_Monthly = BondReturn_Daily.resample('1M').sum()

# Net out currency
fxVsUSD_Monthly = FXvsUSD.pct_change(1).shift(-1)
NetReturn = BondReturn_Monthly - fxVsUSD_Monthly

# Calculate cumulative PL, assuming no reinvestment
PL_Raw = NetReturn * (InflationSignal)
PL_Total = PL_Raw.cumsum()

PL_Total.plot()
plt.title("PL from Inflation Signal")
plt.show()
