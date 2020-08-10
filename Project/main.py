#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# main.py
# This file puts all components of the trading system together. This file is the main executable
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

from ind_1_return_diff import Indicator1

ind1 = Indicator1()
ind1.graph_indicator('AUS') # this works!

