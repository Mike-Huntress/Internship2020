from Indicators.IndicatorInflation import InflationSignalScaled, InflationSignal
from Indicators.IndicatorDemand import DemandSignalScaled, DemandSignal
from Indicators.IndicatorGrowth import GrowthSignalScaled, GrowthSignal
from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib, DatastreamPulls
import Indicators.IndicatorUtilities as Util
import pandas as pd
import numpy as np
import itertools

import matplotlib.pyplot as plt

countries = CountryMetaDataFile().readMetadata()
dl = DataLib("SignalData")

# print(InflationSignalScaled.tail())
# print(DemandSignalScaled.tail())
# print(GrowthSignalScaled.tail())

SignalsScaled = [InflationSignalScaled, DemandSignalScaled, GrowthSignalScaled]
Signals = [InflationSignal, DemandSignal, GrowthSignal]

TradingSignal = (1/3) * (InflationSignal + .873 * (DemandSignal + GrowthSignal))
TradingSignal *= 3 ** .5 # For making it std 1
TradingSignalScaled = Util.RescaleDF(TradingSignal)


# All signals have stdev close to 1
for Signal in Signals + [TradingSignal]:
    print("Mean: {}".format(Signal.mean().mean()))
    print("Std {}".format(Signal.std().mean()))

# Note that 0 is effectively uncorrelated with signals 1 and 2, while 1+2 have a correlation of r = 0.31.
# To transform these into a signal with stdev 1, we want to place weights so that the variance contributed by the
# correlated indicators is identical to the variance contributed if they were uncorrelated - this factor is 1/sqrt(1+r)
#

print("Correlations of each Signal's PL Streams")
for pair in [(0,1), (0,2), (1,2)]:
    i, j = pair
    PL1, PL2 = Util.PLRaw(Signals[i]), Util.PLRaw(Signals[j])
    sum = 0
    for country in PL1.columns:
        sum += PL1[country].corr(PL2[country])
    average_corr = sum / len(PL1.columns)
    print(pair, average_corr)


# Calculating Sharpe ratios for each signal
i = 0
for Signal in Signals + [TradingSignal]:
    print("Signal " + str(i))
    PL_Raw = Util.PLRaw(Signal)
    MeanReturn = PL_Raw.mean().mean() * 12
    AnnualStDev = PL_Raw.std().mean() * (12)**.5
    print("Mean: {}".format(MeanReturn))
    print("StDev: {}".format(AnnualStDev))
    print("Sharpe: {}".format(MeanReturn/AnnualStDev))
    i += 1

TradingSignalPLTotal = Util.PLTotal(TradingSignalScaled)

TradingSignalPLTotal.plot(figsize=(8, 6))
plt.title("Excess P+L from Trading Signal (Hedged Against Currency)")
plt.xlabel("Date")
plt.ylabel("Cumulative P+L")
plt.xlim(left=12 * 30)
plt.savefig('tradingsignal_pl.png')
plt.show()

# Plot signal
TradingSignalScaled.plot(figsize=(8, 6))
plt.title("Trading Signal")
plt.xlabel("Date")
plt.xlim(left=12 * 30)
plt.ylabel("Trading Signal")
plt.savefig('trading_signal.png')
plt.show()


# Calculate Total PL across all countries
TradingSignalPLRaw = Util.PLRaw(TradingSignalScaled)
TradingSignalPLRaw['Total'] = TradingSignalPLRaw.sum(axis = 1)

TradingSignalPLTotal_Aggregate = TradingSignalPLRaw['Total'].cumsum()
TradingSignalPLTotal_Aggregate = TradingSignalPLTotal_Aggregate[TradingSignalPLTotal_Aggregate!=0]

LongOnlySignal = TradingSignalScaled.apply(lambda x: [1 if pd.notnull(y) else y for y in x])
LongOnlySignalPLRaw = Util.PLRaw(LongOnlySignal)
LongOnlySignalPLRaw['Total'] = LongOnlySignalPLRaw.sum(axis = 1)

LongOnlySignalPLTotal_Aggregate = LongOnlySignalPLRaw['Total'].cumsum()
LongOnlySignalPLTotal_Aggregate = LongOnlySignalPLTotal_Aggregate[LongOnlySignalPLTotal_Aggregate!=0]

TradingSignalPLTotal_Aggregate.plot(label = "Trading Signal", figsize=(8, 6))
LongOnlySignalPLTotal_Aggregate.plot(label = "Long Only", figsize=(8, 6))
plt.title("Excess Total P+L for all countries")
plt.xlabel("Date")
plt.ylabel("Cumulative P+L")
plt.legend()
plt.savefig('aggregate_returns.png')
plt.show()

LongOnlySignalPLTotal_AggregateVolAdjusted = LongOnlySignalPLTotal_Aggregate * TradingSignalPLRaw['Total'].std() / LongOnlySignalPLRaw['Total'].std()
TradingSignalPLTotal_Aggregate.plot(label = "Trading Signal", figsize=(8, 6))
LongOnlySignalPLTotal_AggregateVolAdjusted.plot(label = "Long Only", figsize=(8, 6))
plt.title("Excess Total P+L for all countries (Volatility Matched)")
plt.xlabel("Date")
plt.ylabel("Cumulative P+L (Volatility Matched")
plt.legend()
plt.savefig('aggregate_returns_voladjusted.png')
plt.show()
