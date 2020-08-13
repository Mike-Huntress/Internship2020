from Signal import Signal
from Evaluation import Evaluation
import pandas as pd
from DataIOUtilities.DataLib import DataLib

import matplotlib.pyplot as plt

# monetary_signal = Signal('1995-01-01', '2000-01-01', '2000-01-02', '2019-12-31')
# premium_signal = Signal('1995-01-01', '2000-01-01', '2000-01-02', '2019-12-31')
# relative_signal = Signal('1995-01-01', '2000-01-01', '2000-01-02', '2019-12-31')
# #
# # print("avgs")
# monetary_signal.run_monetary_testing()
# m_returns = monetary_signal.get_daily_returns()
# premium_signal.run_premium_testing()
# p_returns = premium_signal.get_daily_returns()
# relative_signal.run_relative_testing()
# r_returns = relative_signal.get_daily_returns()
# #
# print("corrs")
# evaluate = Evaluation()
# print(evaluate.corr_passive_active_bonds(m_returns))
# print(evaluate.corr_passive_active_bonds(p_returns))
# print(evaluate.corr_passive_active_bonds(r_returns))
#
# print("Cross")
# evaluate.cross_indicator_corr(m_returns, "Monetary Base", p_returns, "Bond Premium")
# evaluate.cross_indicator_corr(m_returns, "Monetary Base", r_returns, "Relative Stock/Bond")
# evaluate.cross_indicator_corr(p_returns, "Bond Premium", r_returns, "Relative Stock/Bond")
#
# print("Indicator")
# print(m_returns.std())
# print(p_returns.std())
# print(r_returns.std())


#
signal = Signal('1995-01-01', '2000-01-01', '2000-01-02', '2019-12-31')
# # signal = Signal('1995-01-01', '1999-12-31', '2000-01-02', '2000-01-30')
signal.run_testing()

# # print(poss.std())
# # signal.run_monetary_testing()
# # signal.run_relative_testing()
# # signal.run_premium_testing()
# signal.run_testing()
# signal.show_cum_returns()
# #signal.show_cum_quarterly_returns()
# signal_ret = signal.get_daily_returns()
#
# evaluate = Evaluation()
# evaluate.bond_system_v_passive_bonds_risk_adj(signal_ret)
# evaluate.bond_system_v_passive_bonds_risk_adj_C(signal_ret)
# evaluate.compare_with_equities_cumulative(signal_ret)
# # evaluate.compare_with_equities(signal_ret)
#evaluate.bond_system_v_passive_bonds(signal_ret)
#evaluate.bond_system_v_passive_bonds_cumulative(signal_ret)
# print("Corr")
# print(evaluate.corr_passive_active_bonds(signal_ret))
#
# print("STD")
# print(signal_ret.std())
# #
# print("avg quarterly returns")
# print(signal.get_quarterly_returns().mean())


# print("System std")
# print(signal_ret.std())
# print(evaluate.corr_passive_active_bonds(signal_ret))

# #x.show_position_vs_returns()
# #x.calc_corr_pos_ret()
# #x.inter_indicator_corr()
# #x.get_indicator_return_metrics()
# #x.show_cum_returns()
# #x.get_indicator_return_metrics()
# daily_returns = signal.get_daily_returns()
# # print(daily_returns.std())
#
# evaluate = Evaluation()
# # evaluate.compare_with_equities(daily_returns)
# evaluate.bond_system_v_passive_bonds(daily_returns)
# print(evaluate.corr_passive_active_bonds(daily_returns))
# dl = DataLib("SignalData")
# LongRates = dl.pull("LongRates")
# m2 = dl.pull("M2/inUSD")
# m1 = dl.pull("M1/inUSD")
# m3 = dl.pull("M3/inUSD")
# change_m2 = m2.pct_change(1)
# smoothed_change_m2 = change_m2.rolling(3).mean()
# slope_smoothed_change_m2 = smoothed_change_m2.diff()
# rolling_slope = slope_smoothed_change_m2.rolling(5*12, min_periods = 12*2)
# rolling_slope_std = rolling_slope.std()
# start_date = '2015-01-01'
# end_date = '2017-01-01'
#
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1_label = 'Bond Yields'
# ax1.plot(LongRates["CAN"].loc[start_date:end_date].to_timestamp(), label = ax1_label)
# ax1.set_ylabel(ax1_label)
# ax1.legend(loc = "lower right")
# ax2_label = 'Change in M2'
# ax2.plot(change_m2["CAN"].loc[start_date:end_date].to_timestamp(), color = 'tab:red', label = ax2_label)
# ax2.set_ylabel(ax2_label)
# ax2.legend()
# plt.title("CAN" + " Bond Yields vs. Change in M2")
# plt.show()

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)
# est_m2 = (0.5*(m1 + m3))["AUS"]
# change_est_m2 = est_m2.pct_change(1)
# smoothed_change_est_m2 = change_est_m2.rolling(3).mean()
# slope_smoothed_change_m2_est = smoothed_change_est_m2.diff()
# rolling_slope_est = slope_smoothed_change_m2_est.rolling(5*12, min_periods = 12*2)
# rolling_slope_std_est = rolling_slope_est.std()
# sum = 0
# country = "CAN"
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1_label = 'Slope of Bond Yields'
# ax1.plot(LongRates[country].diff().loc[start_date:end_date].to_timestamp(), label = ax1_label)
# ax1.set_ylabel(ax1_label)
# ax1.legend(loc = "lower right")
# ax2_label = 'Slope of Change in M2'
# ax2.plot((slope_smoothed_change_m2/rolling_slope_std)["CAN"].loc[start_date:end_date].to_timestamp(), color = 'tab:red', label = ax2_label)
# ax2.set_ylabel(ax2_label)
# ax2.axhline(y= 0.5, color='g', linestyle='-')
# ax2.axhline(y=-0.5, color='g', linestyle='-')
# ax2.legend()
# align_yaxis(ax1, 0, ax2, 0)
# plt.title(country + " Slope of Bond Yields vs. Slope of Change in M2 (Standardized)")
# plt.show()
# # corr = LongRates[country].diff().loc[start_date:end_date].corr(((slope_smoothed_change_m2_est)/rolling_slope_std_est).shift(1).loc[start_date:end_date])
# # print(country)
# print(corr)
# sum += corr
# print("mean corr")
# print(sum / len(LongRates.columns.drop("AUS")))
