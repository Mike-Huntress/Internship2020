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
        #equity_ret = self.equities.mean(axis=1).pct_change(1)
        equity_ret = self.equities.loc[other_ret.index].dot(np.ones(10) * 0.10).pct_change(1)

        # fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()
        # ax1_label = 'Equity Returns '
        # ax1.plot(equity_ret.cumsum().to_timestamp(), color = "tab:red", label=ax1_label)
        # ax1.set_ylabel(ax1_label)
        # ax1.legend(loc = "upper left")
        # ax2_label = 'Bond System Returns'
        # ax2.plot(other_ret.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.set_ylabel(ax2_label)
        # ax2.legend(loc = "lower right")
        # plt.title("Equity vs. Bond System Returns")
        # ax1.set_ylim([-0.3, 0.6])
        # ax2.set_ylim([-0.3, 0.6])
        # plt.show()

        # print("equity std")
        # print(equity_ret.std())
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

        # fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()
        # ax1_label = 'Equity Risk-Adjusted Quarterly Returns'
        # ax1.plot(equity_risk_adj.resample('Q').sum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.set_ylabel(ax1_label)
        # ax1.legend(loc="lower right")
        # ax2_label = 'Bond System Risk-Adjusted Quarterly Returns'
        # ax2.plot(other_risk_adj.resample('Q').sum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.set_ylabel(ax2_label)
        # ax2.legend(loc="upper left")
        # plt.title("Equity vs. Bond System Risk-Adjusted Quarterly Returns")
        # # ax1.set_ylim([-20, 300])
        # # ax2.set_ylim([-20, 300])
        # plt.show()

    def bond_system_v_passive_bonds_risk_adj(self, other_ret):
        #passive_bonds = self.BondReturnIdx.mean(axis=1).pct_change(1).loc[other_ret.index]
        passive_bonds = self.BondReturnIdx.pct_change(1).dot(np.ones(10) * 0.10).loc[other_ret.index]
        passive_bonds_std = passive_bonds.std()

        # fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()
        # ax1_label = 'Passive Global Bond Returns '
        # ax1.plot(passive_bonds.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.set_ylabel(ax1_label)
        # ax1.legend(loc="upper left")
        # ax2_label = 'Bond System Returns'
        # ax2.plot(other_ret.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.set_ylabel(ax2_label)
        # ax2.legend(loc="lower right")
        # plt.title("Passive Bonds vs. Bond System Returns")
        # # ax1.set_ylim([-0.05, 0.30])
        # # ax2.set_ylim([-0.05, 0.30])
        # plt.show()

        passive_bonds_risk_adj = passive_bonds / passive_bonds_std
        other_ret_risk_adj = other_ret / other_ret.std()

        # fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()
        # ax1_label = 'Passive Global Bond Returns Risk-Adjusted'
        # #ax1.plot(passive_bonds_risk_adj.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.plot(passive_bonds_risk_adj.resample('Q').sum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.set_ylabel(ax1_label)
        # ax1.legend(loc="upper left")
        # ax2_label = 'Bond System Returns Risk-Adjusted'
        # #ax2.plot(other_ret_risk_adj.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.plot(other_ret_risk_adj.resample('Q').sum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.set_ylabel(ax2_label)
        # ax2.legend(loc="lower right")
        # plt.title("Passive Bonds vs. Bond System Quarterly Returns Risk-Adjusted")
        # ax1.set_ylim([-25, 40])
        # ax2.set_ylim([-25, 40])
        # plt.show()

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1_label = 'Passive Global Bond Returns'
        #ax1.plot(passive_bonds_risk_adj.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        ax1.plot(passive_bonds.resample('Q').sum().to_timestamp(), color="tab:red", label=ax1_label)
        ax1.set_ylabel(ax1_label)
        ax1.legend(loc="upper left")
        ax2_label = 'Bond System Returns'
        #ax2.plot(other_ret_risk_adj.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        ax2.plot(other_ret.resample('Q').sum().to_timestamp(), color='tab:blue', label=ax2_label)
        ax2.set_ylabel(ax2_label)
        ax2.legend(loc="lower right")
        ax1.set_ylim([-.05, 0.1])
        ax2.set_ylim([-.05, 0.1])
        plt.title("Passive Bonds vs. Bond System Quarterly Returns")
        plt.show()

    def bond_system_v_passive_bonds_risk_adj_C(self, other_ret):
        #passive_bonds = self.BondReturnIdx.mean(axis=1).pct_change(1).loc[other_ret.index]
        passive_bonds = self.BondReturnIdx.dot(np.ones(10) * 0.10).pct_change(1).loc[other_ret.index]
        passive_bonds_std = passive_bonds.std()
        print("STD DEV")
        print(passive_bonds_std)
        # fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()
        # ax1_label = 'Passive Global Bond Returns '
        # ax1.plot(passive_bonds.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.set_ylabel(ax1_label)
        # ax1.legend(loc="upper left")
        # ax2_label = 'Bond System Returns'
        # ax2.plot(other_ret.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.set_ylabel(ax2_label)
        # ax2.legend(loc="lower right")
        # plt.title("Passive Bonds vs. Bond System Returns")
        # # ax1.set_ylim([-0.05, 0.30])
        # # ax2.set_ylim([-0.05, 0.30])
        # plt.show()

        passive_bonds_risk_adj = passive_bonds / passive_bonds_std
        other_ret_risk_adj = other_ret / other_ret.std()

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1_label = 'Passive Global Bond Returns Risk-Adjusted'
        #ax1.plot(passive_bonds_risk_adj.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        ax1.plot(passive_bonds_risk_adj.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        ax1.set_ylabel(ax1_label)
        ax1.legend(loc="upper left")
        ax2_label = 'Bond System Returns Risk-Adjusted'
        #ax2.plot(other_ret_risk_adj.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        ax2.plot(other_ret_risk_adj.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        ax2.set_ylabel(ax2_label)
        ax2.legend(loc="lower right")
        plt.title("Passive Bonds vs. Bond System Cumulative Returns Risk-Adjusted")
        ax1.set_ylim([-30, 540])
        ax2.set_ylim([-30, 540])
        plt.show()

        # fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()
        # ax1_label = 'Passive Global Bond Returns'
        # #ax1.plot(passive_bonds_risk_adj.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.plot(passive_bonds.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.set_ylabel(ax1_label)
        # ax1.legend(loc="upper left")
        # ax2_label = 'Bond System Returns'
        # #ax2.plot(other_ret_risk_adj.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.plot(other_ret.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.set_ylabel(ax2_label)
        # ax2.legend(loc="lower right")
        # plt.title("Passive Bonds vs. Bond System Cumulative Returns")
        # # ax1.set_ylim([-30, 540])
        # # ax2.set_ylim([-30, 540])
        # plt.show()


    def bond_system_v_passive_bonds(self, other_ret):
        #passive_bonds = self.BondReturnIdx.mean(axis=1).pct_change(1).loc[other_ret.index]
        passive_bonds = self.BondReturnIdx.pct_change(1).loc[other_ret.index].dot(np.ones(10) * 0.10)

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
        plt.title("Passive Bonds vs. Bond System Quarterly Returns")
        # ax1.set_ylim([-0.1, 0.30])
        # ax2.set_ylim([-0.1, 0.30])
        plt.show()

    def bond_system_v_passive_bonds_cumulative(self, other_ret):
        #passive_bonds = self.BondReturnIdx.mean(axis=1).pct_change(1).loc[other_ret.index]
        passive_bonds = self.BondReturnIdx.pct_change(1).loc[other_ret.index].dot(np.ones(10) * 0.10)

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1_label = 'Passive Global Bond Returns'
        ax1.plot(passive_bonds.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        ax1.set_ylabel(ax1_label)
        ax1.legend(loc="upper left")
        ax2_label = 'Bond System Returns'
        ax2.plot(other_ret.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        ax2.set_ylabel(ax2_label)
        ax2.legend(loc="lower right")
        plt.title("Passive Bonds vs. Bond System Quarterly Returns")
        # ax1.set_ylim([-0.1, 0.30])
        # ax2.set_ylim([-0.1, 0.30])
        plt.show()

    def std_passive(self):
        passive_bonds = (self.BondReturnIdx.pct_change(1) * np.ones(10) * 0.1).sum(axis=1).loc['2000-01-02':'2019-12-31']
        return passive_bonds.std()

    def corr_passive_active_bonds(self, other_ret):
        passive_bonds = (self.BondReturnIdx.pct_change(1) * np.ones(10)*0.1).sum(axis=1).loc[other_ret.index]
        # smoothed_passive = passive_bonds.rolling(5).mean()
        # compare_ret = other_ret.rolling(5).mean()
        corr = passive_bonds.astype('float64').corr(other_ret["Daily Return"].astype('float64'))
        return corr

    def cross_indicator_corr(self, ind1_ret, ind1_name, ind2_ret, ind2_name):
        # fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()
        # ax1_label = ind1_name + ' Cumulative Returns'
        # ax1.plot(ind1_ret.cumsum().to_timestamp(), color="tab:red", label=ax1_label)
        # ax1.set_ylabel(ax1_label)
        # ax1.legend(loc="upper left")
        # ax2_label = ind2_name + ' Cumulative Returns'
        # ax2.plot(ind2_ret.cumsum().to_timestamp(), color='tab:blue', label=ax2_label)
        # ax2.set_ylabel(ax2_label)
        # ax2.legend(loc="lower right")
        # plt.title(ind1_name + " Cumulative Returns vs." + ind2_name + " Bond Premium Cumulative Returns")
        # ax1.set_ylim([y_min, y_max])
        # ax2.set_ylim([y_min, y_max])
        # plt.show()

        print(ind1_ret["Daily Return"].astype('float64').corr(ind2_ret["Daily Return"].astype('float64')))
        print(ind1_ret["Daily Return"].astype('float64').rolling(5).mean().corr(ind2_ret["Daily Return"].astype('float64').rolling(5).mean()))



