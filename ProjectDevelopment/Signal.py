import pandas as pd
from MonetaryBase import MonetaryBase
from BondPremium import BondPremium
from RelativeStockBond import RelativeStockBond
import matplotlib.pyplot as plt
from DataIOUtilities.DataLib import DataLib
import numpy as np
import sys

class Signal():

    def __init__(self, start_train_date, end_train_date, start_test_date, end_test_date):
        dl = DataLib("SignalData")
        self.BondReturnIdx = dl.pull("BondRetIdx/LocalFX")
        self.start_train_date = start_train_date
        self.end_train_date = end_train_date
        self.start_test_date = start_test_date
        self.end_test_date = end_test_date
        self.monetary_ind = MonetaryBase(self.start_train_date, self.end_train_date)
        self.bond_premium_ind = BondPremium(self.start_train_date, self.end_train_date)
        self.relative_ind = RelativeStockBond(self.start_train_date, self.end_train_date)
        trade_range = pd.date_range(self.start_test_date, self.end_test_date, freq='B')
        self.daily_ret = pd.DataFrame(index = trade_range.to_period("B"), columns = ["Daily Return"])
        self.position_trace = pd.DataFrame(index = trade_range.to_period("B"), columns = self.BondReturnIdx.columns)
        self.one_day_bond_return = self.BondReturnIdx.pct_change(1)

        self.monetary_trace = pd.DataFrame(index=trade_range.to_period("B"), columns=self.BondReturnIdx.columns)
        self.premium_trace = pd.DataFrame(index=trade_range.to_period("B"), columns=self.BondReturnIdx.columns)
        self.relative_trace = pd.DataFrame(index=trade_range.to_period("B"), columns=self.BondReturnIdx.columns)
        self.daily_ret_m = pd.DataFrame(index = trade_range.to_period("B"), columns = ["Daily Return"])
        self.daily_ret_p = pd.DataFrame(index = trade_range.to_period("B"), columns = ["Daily Return"])
        self.daily_ret_r = pd.DataFrame(index = trade_range.to_period("B"), columns = ["Daily Return"])
        self.annual_ret_m = pd.DataFrame(index=pd.date_range(self.start_test_date, self.end_test_date, freq='A'), columns=["Annual Return"])
        self.annual_ret_p = pd.DataFrame(index=pd.date_range(self.start_test_date, self.end_test_date, freq='A'), columns=["Annual Return"])
        self.annual_ret_r = pd.DataFrame(index=pd.date_range(self.start_test_date, self.end_test_date, freq='A'), columns=["Annual Return"])
        self.annual_ret_m.fillna(0, inplace = True)
        self.annual_ret_p.fillna(0, inplace=True)
        self.annual_ret_r.fillna(0, inplace=True)

    def run_testing(self):
        for date in pd.date_range(self.start_test_date, self.end_test_date, freq='B').date:
            positions = self.update_signal(date)
            self.position_trace.loc[date,] = positions
            self.daily_ret.loc[date] = positions.dot(self.one_day_bond_return.loc[date])
            if sum(abs(positions)) != 0:
                self.daily_ret.loc[date] = self.daily_ret.loc[date] / sum(abs(positions))

    def get_position_trace(self):
        return self.position_trace

    def update_signal(self, date):
        monetary_weight = self.monetary_ind.update_indicator(date)
        premium_weight = self.bond_premium_ind.update_indicator(date)
        relative_weight = self.relative_ind.update_indicator(date)
        combined_weights = 0.4 * monetary_weight.values + 0.35 * relative_weight.values + 0.25 * premium_weight.values
        # combined_weights = 0.25 * monetary_weight.values + 1 * relative_weight.values + 0.25 * premium_weight.values
        #combined_weights =  0.5 * monetary_weight.values + 0.25 * relative_weight.values + 0.25 * premium_weight.values
        #return self.scale_signal(combined_weights)
        return self.scale_signal_absolute(combined_weights)

    def measure_avg_quarterly_returns(self):
        return self.daily_ret.resample('Q').sum().mean()

    def run_monetary_testing(self):
        for date in pd.date_range(self.start_test_date, self.end_test_date, freq='B').date:
            positions = self.monetary_ind.update_indicator(date).values
            self.daily_ret.loc[date] = positions.dot(self.one_day_bond_return.loc[date]) / sum(abs(positions))

    def run_premium_testing(self):
        for date in pd.date_range(self.start_test_date, self.end_test_date, freq='B').date:
            positions = self.bond_premium_ind.update_indicator(date).values
            self.daily_ret.loc[date] = positions.dot(self.one_day_bond_return.loc[date])
            if sum(positions) != 0:
                self.daily_ret.loc[date] = self.daily_ret.loc[date] / sum(abs(positions))

    def run_relative_testing(self):
        for date in pd.date_range(self.start_test_date, self.end_test_date, freq='B').date:
            positions = self.relative_ind.update_indicator(date).values
            self.daily_ret.loc[date] = positions.dot(self.one_day_bond_return.loc[date]) / sum(abs(positions))

    def scale_signal_absolute(self, positions):
        shorts = (positions < 0) * positions
        short_weights = sum(abs(shorts))
        longs = (positions > 0) * positions
        long_weights = sum(abs((longs)))
        if short_weights != 0:
            scaler = long_weights / short_weights
            shorts = shorts * scaler
        return longs + shorts

    def scale_signal(self, positions):
        #to help create neutral exposure to global bonds market
        min_val = positions.min()
        max_val = positions.max()
        scaler_v = np.vectorize(lambda x: (2 * (x - min_val) / (max_val - min_val)) - 1) #scales from -1 to 1
        weighted_positions =  scaler_v(positions)
        shorts = (weighted_positions < 0) * weighted_positions
        short_weights = sum(abs(shorts))
        longs = (weighted_positions > 0) * weighted_positions
        long_weights = sum(abs((longs)))
        scaler = long_weights / short_weights
        shorts = shorts * scaler
        return longs + shorts

    def show_cum_returns(self):
        self.daily_ret.cumsum().plot()
        plt.title("Signal Cumulative Returns")
        plt.ylabel("Cumulative Returns")
        plt.legend()
        plt.show()

    def show_cum_quarterly_returns(self):
        q_returns = self.daily_ret.resample('Q').sum()
        q_returns.plot()
        plt.title("Signal Annual Returns")
        plt.ylabel("Annual Returns")
        plt.legend()
        plt.show()

    def get_quarterly_returns(self):
        return self.daily_ret.resample('Q').sum()

    def show_position_vs_returns(self):
        for country in self.BondReturnIdx.columns:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1_label = 'Bond Returns'
            ax1.plot(self.one_day_bond_return[country].loc[self.start_test_date:self.end_test_date].to_timestamp(), label=ax1_label)
            ax1.set_ylabel(ax1_label)
            ax1.legend()
            ax2_label = 'Position'
            ax2.plot(self.position_trace[country].loc[self.start_test_date:self.end_test_date].to_timestamp(), color='tab:red', label=ax2_label)
            ax2.set_ylabel(ax2_label)
            ax2.legend()
            plt.title(country + " One Day Bond Returns vs. Position (long v. short & magnitude)")
            plt.show()

    def calc_corr_pos_ret(self):
        # for country in self.BondReturnIdx.columns:
        #     x = self.position_trace[country].loc[self.start_test_date:self.end_test_date].astype('float64').corr(self.one_day_bond_return[country].loc[self.start_test_date:self.end_test_date].astype('float64'))
        #     print(country + " " + str(x))
        for country in self.BondReturnIdx.columns:
            mapped_position = self.position_trace[country].loc[self.start_test_date:self.end_test_date].apply(lambda x: 1 if x >= 0 else -1)
            mapped_returns = self.one_day_bond_return[country].loc[self.start_test_date:self.end_test_date].apply(lambda x: 1 if x >= 0 else -1)
            corr = mapped_position.astype('float64').corr(mapped_returns.astype('float64'))
            print(country + " " + str(corr))

            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1_label = 'Bond Returns'
            ax1.plot(mapped_returns.to_timestamp(), label=ax1_label)
            ax1.set_ylabel(ax1_label)
            ax1.legend()
            ax2_label = 'Position'
            ax2.plot(mapped_position.to_timestamp(), color='tab:red', label=ax2_label)
            ax2.set_ylabel(ax2_label)
            ax2.legend()
            plt.title(country + " One Day Bond Returns vs. Position (Mapped)")
            plt.show()

    def run_indicators_separately(self):
        for date in pd.date_range(self.start_test_date, self.end_test_date, freq='B').date:
            r_positions = self.relative_ind.update_indicator(date).values
            self.relative_trace.loc[date,] = r_positions
            self.daily_ret_r.loc[date,] = r_positions.dot(self.one_day_bond_return.loc[date,]) / sum(abs(r_positions))
            p_positions = self.bond_premium_ind.update_indicator(date).values
            self.premium_trace.loc[date,] = p_positions
            self.daily_ret_p.loc[date,] = p_positions.dot(self.one_day_bond_return.loc[date,]) / sum(abs(p_positions))
            m_positions = self.monetary_ind.update_indicator(date).values
            self.monetary_trace.loc[date,] = m_positions
            self.daily_ret_m.loc[date,] = m_positions.dot(self.one_day_bond_return.loc[date,]) / sum(abs(m_positions))

    def inter_indicator_corr(self):
        self.run_indicators_separately()
        for country in self.BondReturnIdx.columns:
            print(country)
            print("Monetary and Relative")
            print(self.monetary_trace[country].astype('float64').corr(self.relative_trace[country].astype('float64')))
            print("Monetary and Premium")
            print(self.monetary_trace[country].astype('float64').corr(self.premium_trace[country].astype('float64')))
            print("Premium and Relative")
            print(self.premium_trace[country].astype('float64').corr(self.relative_trace[country].astype('float64')))

            self.monetary_trace[country].plot(color = "tab:red")
            self.premium_trace[country].plot(color = "tab:blue")
            self.relative_trace[country].plot(color = "tab:green")
            plt.title(country + " indicator graphs")
            plt.show()

    def get_indicator_return_metrics(self):
        self.run_indicators_separately()

        self.daily_ret_r.cumsum().plot()
        plt.title("Relative Stock Bond Cumulative Returns")
        plt.show()

        self.daily_ret_m.cumsum().plot()
        plt.title("Monetary Base Cumulative Returns")
        plt.show()

        self.daily_ret_p.cumsum().plot()
        plt.title("Bond Premium Returns")
        plt.show()

        print("Avg daily return - monetary")
        print(self.daily_ret_m.mean())
        print("Avg daily return - relative")
        print(self.daily_ret_r.mean())
        print("Avg daily return - monetary")
        print(self.daily_ret_p.mean())
        print("Relative S/B Returns Vol")
        print(self.daily_ret_r.std())
        print("Bond Premium Returns Vol")
        print(self.daily_ret_p.std())
        print("Monetary Base Returns Vol")
        print(self.daily_ret_m.std())

        print("Relative S/B and Bond Premium Returns Correlation")
        print(self.daily_ret_p["Daily Return"].astype('float64').corr(self.daily_ret_r["Daily Return"].astype('float64')))

        print("Monetary Base and Bond Premium Returns Correlation")
        print(self.daily_ret_p["Daily Return"].astype('float64').corr(self.daily_ret_m["Daily Return"].astype('float64')))

        print("Relative S/B and Monetary Base Returns Correlation")
        print(self.daily_ret_m["Daily Return"].astype('float64').corr(self.daily_ret_r["Daily Return"].astype('float64')))

    def calc_annual_returns(self):
        # for date in pd.date_range(self.start_test_date, self.end_test_date, freq='A').date:
        #     self.annual_ret_m.loc[str(date.year) + '-12-31'] += self.daily_ret_m.loc[date].values[0]
        #     self.annual_ret_p.loc[str(date.year)+ '-12-31'] += self.daily_ret_p.loc[date].values[0]
        #     self.annual_ret_r.loc[str(date.year)+ '-12-31'] += self.daily_ret_r.loc[date].values[0]
        # print(self.annual_ret_m)
        # print("M")
        # print(self.annual_ret_m.mean(skipna=True))
        # print(self.daily_ret_m.std())
        # print("P")
        # print(self.annual_ret_p.mean(skipna=True))
        # print(self.daily_ret_p.std())
        # print("R")

        print(self.annual_ret_r.mean(skipna=True))
        print(self.daily_ret_r.std())
        print("Corr M,P")
        print(self.daily_ret_p["Daily Return"].astype('float64').corr(self.daily_ret_m["Daily Return"].astype('float64')))
        print("Corr M,R")
        print(self.daily_ret_m["Daily Return"].astype('float64').corr(self.daily_ret_r["Daily Return"].astype('float64')))
        print("Corr R,P")
        print(self.daily_ret_p["Daily Return"].astype('float64').corr(self.daily_ret_r["Daily Return"].astype('float64')))

    def get_daily_returns(self):
        return self.daily_ret