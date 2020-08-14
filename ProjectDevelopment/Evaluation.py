from DataIOUtilities.DataLib import DataLib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Evaluation():

    def __init__(self):
        dl = DataLib("SignalData")
        self.equities = dl.pull("EquityPrices")
        self.BondReturnIdx = dl.pull("BondRetIdx/LocalFX")

    def compare_with_equities_cumulative(self, other_ret):
        equity_ret = self.equities.loc[other_ret.index].dot(np.ones(10) * 0.10).pct_change(1)
        equity_risk_adj = equity_ret / equity_ret.std()
        other_risk_adj = other_ret / other_ret.std()

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1_label = 'Equity Risk-Adjusted Cumulative Returns '
        ax1.plot(equity_risk_adj.cumsum().to_timestamp(), color = "tab:red", label=ax1_label)
        ax1.set_ylabel(ax1_label)
        ax1.legend(loc = "lower right")
        ax2_label = 'Bond System Risk-Adjusted Cumulative Returns'
        ax2.plot(other_risk_adj.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        ax2.set_ylabel(ax2_label)
        ax2.legend(loc = "upper left")
        plt.title("Equity vs. Bond System Risk-Adjusted Cumulative Returns")
        ax1.set_ylim([-70, 200])
        ax2.set_ylim([-70, 200])
        plt.show()

    def bond_system_v_passive_bonds_quarterly(self, other_ret):
        passive_bonds = self.BondReturnIdx.dot(np.ones(10) * 0.10).pct_change(1).loc[other_ret.index]

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1_label = 'Passive Global Bond Returns'
        ax1.plot(passive_bonds.resample('Q').sum().to_timestamp(), color="tab:red", label=ax1_label)
        ax1.set_ylabel(ax1_label)
        ax1.legend(loc="upper left")
        ax2_label = 'Bond System Returns'
        ax2.plot(other_ret.resample('Q').sum().to_timestamp(), color='tab:blue', label=ax2_label)
        ax2.set_ylabel(ax2_label)
        ax2.legend(loc="lower right")
        ax1.set_ylim([-.05, 0.1])
        ax2.set_ylim([-.05, 0.1])
        plt.title("Passive Bonds vs. Bond System Quarterly Returns")
        plt.show()

    def corr_passive_active_bonds(self, other_ret):
        passive_bonds = self.BondReturnIdx.dot(np.ones(10) * 0.10).pct_change(1).sum(axis=1).loc[other_ret.index]
        return passive_bonds.astype('float64').corr(other_ret["Daily Return"].astype('float64'))

    def cross_indicator_corr(self, ind1_ret, ind2_ret):
        return ind1_ret["Daily Return"].astype('float64').corr(ind2_ret["Daily Return"].astype('float64'))

    def show_cum_returns(self, daily_ret):
        daily_ret.cumsum().plot()
        plt.title("Signal Cumulative Returns")
        plt.ylabel("Cumulative Returns")
        plt.legend()
        plt.show()

    def show_quarterly_returns(self, daily_ret):
        q_returns = daily_ret.resample('Q').sum()
        q_returns.plot()
        plt.title("Signal Quarterly Returns")
        plt.ylabel("Quarterly Returns")
        plt.legend()
        plt.show()
