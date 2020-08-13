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

import matplotlib.pyplot as plt
import Indicators.IndicatorUtilities as Util

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

GrowthSignal = -GDPReal_PctChange_Normalized_Monthly
GrowthSignalScaled = Util.RescaleDF(GrowthSignal)

# GrowthSignalScaled.plot()
# plt.show()

PL_Total = Util.PLTotal(GrowthSignalScaled)

if __name__ == '__main__':

    PL_Total.plot(figsize=(8, 6))
    plt.title("Excess P+L from Growth Signal (Hedged Against Currency)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative P+L")
    plt.xlim(left=12*19)
    plt.savefig('growth_pl.png')
    plt.show(block = False)

    # Plot signal
    GrowthSignal.plot(figsize=(8, 6))
    plt.title("Growth Signal")
    plt.xlabel("Date")
    plt.ylabel("Growth Signal")
    plt.xlim(left=12*19)
    plt.savefig('growth_signal.png')
    plt.show(block = False)