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
# Data Stream 1: Real GDP
##################################################
# Intuition: Direct measure of growth; when growth increases, expect central bank to increase interest rates, lowering
# yields

GDPReal = dl.pull("GDP/Real")
GDPReal_PctChange = Util.AnnualizedChangeTimeSeries(GDPReal, 'Q', 1)
GDPReal_PctChange_Normalized = Util.NormalizeDF(GDPReal_PctChange, 40)
GDPReal_PctChange_Normalized_Monthly = GDPReal_PctChange_Normalized.resample('1M').ffill()


# # Plotting GDP
# GDPReal_PctChange_Normalized.plot()
# plt.show()


##################################################
# Create Overall Signal
##################################################

# GDP experiences

GrowthSignal = GDPReal_PctChange_Normalized_Monthly

BondPrices = dl.pull("BondRetIdx/LocalFX")
FXvsUSD = dl.pull('fxVsUSD')

BondReturn_Daily = BondPrices.pct_change(1).shift(-1)
BondReturn_Monthly = BondReturn_Daily.resample('1M').sum()
fxVsUSD_Monthly = FXvsUSD.pct_change(1).shift(-1)
print(fxVsUSD_Monthly.tail())
print(BondReturn_Monthly.tail())

NetReturn = BondReturn_Monthly - fxVsUSD_Monthly

PL_Raw = NetReturn * ( - GrowthSignal)
PL_Total = PL_Raw.cumsum()

PL_Total.plot()
plt.title("PL from Growth Signal")
plt.show()