#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# indicator_values_plot.py
#
# This file creates the graphs for USA, CAN, and AUS indicator values. It is an executable.
#

import matplotlib.pyplot as plt
from returns import *
from signals import *
from indicators import *

# plot the indicator values for US, CAN, and AUS
country = 'USA'

indicator = get_ind_gdp_infla()

plt.figure(figsize=(20,8))
indicator['USA'].plot()
plt.axhline(0, color='black')
plt.title('Business Cycles Indicator USA')
plt.show()

plt.figure(figsize=(20,8))
indicator['AUS'].plot()
plt.axhline(0, color='black')
plt.title('Business Cycles Indicator AUS')
plt.show()

plt.figure(figsize=(20,8))
indicator['CAN'].plot()
plt.axhline(0, color='black')
plt.title('Business Cycles Indicator CAN')
plt.show()