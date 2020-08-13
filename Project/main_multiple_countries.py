#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# main_multiple_countries.py
#
# This file puts all components of the trading system together for USA, CAN, and AUS. This file is a main executable
# Positions are taken as globally neutral
#

from returns import *
from signals import *
from indicators import *

# SEE RESULTS FOR SEVERAL COUNTRIES (USA, CAN, AUS)

weights = {'USA': 1, 'CAN': 1, 'AUS': 1}  # use these three because they have most CPI data
indicator = get_ind_gdp_infla()
signal = generate_signal_system(indicator, weights)

portfolio_returns, long_returns = get_returns_system(signal, weights)

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

for country in weights.keys():
    show_signals(signal[country], country)

print('Returns Correlation')
print(portfolio_returns.corr(long_returns))  # the two return streams have a slightly positive correlation

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
