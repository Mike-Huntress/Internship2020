#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# main_one_country.py
#
# This file puts all components of the trading system together for the USA. This file is a main executable
#

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import matplotlib.pyplot as plt

from DataIOUtilities.DataLib import DataLib, DatastreamPulls

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from returns import *
from signals import *
from indicators import *

# SEE RESULTS FOR ONE INDICATOR ONE COUNTRY
# THE ONE COUNTRY IS USA FOR MORE COMPLETE CPI DATA

country = 'USA'
indicator = get_ind_gdp_infla()
signal = generate_signal_single(indicator, country)

portfolio_returns, long_returns = get_returns_single(signal, country)
graph_returns(portfolio_returns, long_returns)

print('Portfolio Returns Mean, SD, and Sharpe Ratio')
p_mean, p_std, p_sharpe = get_stats(portfolio_returns)
print(p_mean)
print(p_std)
print(p_sharpe)

print('Long Returns Mean, SD, and Sharpe Ratio')
b_mean, b_std, b_sharpe = get_stats(long_returns)
print(b_mean)
print(b_std)
print(b_sharpe)

show_signals(signal)

print('Returns Correlation')
print(portfolio_returns.corr(long_returns)) # kind of positively correlated

# *******************************************************************************
# look at failure point of USA
country = 'USA'
dl = DataLib("SignalData")
bond_returns = dl.pull('BondRetIdx/LocalFX')
gdpReal = dl.pull("GDP/Real")

fig, ax1 = plt.subplots()
fig.set_figheight(6)
fig.set_figwidth(20)
ax2 = ax1.twinx()
ax1_label = 'Bond Returns'
ax1.plot(bond_returns[country].to_timestamp(), label = ax1_label)
ax1.set_ylabel(ax1_label)
ax1.legend()
ax2_label = 'Real GDP'
ax2.plot(gdpReal[country].to_timestamp(), color = 'tab:red', label = ax2_label)
ax2.set_ylabel(ax2_label)
ax2.legend()
plt.title('Bond Return and Real GDP')
handles, labels = ax1.get_legend_handles_labels()
plt.show()

short_rate = dl.pull('ShortRates')
plt.figure(figsize=(20,3))
short_rate['USA'].plot()
plt.title('US Short Rates')
plt.show()

# *******************************************************************************
# combining portfolio and benchmark into one portfolio

combined_returns = combine_returns(portfolio_returns, long_returns, 1, 1)

graph_returns(combined_returns, long_returns)

print('Combined Portfolio Returns Mean, SD, and Sharpe Ratio')
c_mean, c_std, c_sharpe = get_stats(combined_returns)
print(c_mean)
print(c_std)
print(c_sharpe)

print('Long Returns Mean, SD, and Sharpe Ratio')
b_mean, b_std, b_sharpe = get_stats(long_returns)
print(b_mean)
print(b_std)
print(b_sharpe)

print('\nRisk Adjusted Return')
# note that this function takes around 5-10 minutes to run, since it's constantly reevaluating the SD
risk_adjusted_returns = get_risk_adjusted_returns(combined_returns, long_returns)
graph_returns(risk_adjusted_returns, long_returns)

print('Risk Adjusted Returns Mean, SD, and Sharpe Ratio')
r_mean, r_std, r_sharpe = get_stats(risk_adjusted_returns)
print(r_mean)
print(r_std)
print(r_sharpe)

print('Long Returns Mean, SD, and Sharpe Ratio')
b_mean, b_std, b_sharpe = get_stats(long_returns)
print(b_mean)
print(b_std)
print(b_sharpe)
