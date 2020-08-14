import pandas as pd
from MonetaryBase import MonetaryBase
from BondPremium import BondPremium
from RelativeStockBond import RelativeStockBond
import matplotlib.pyplot as plt
from DataIOUtilities.DataLib import DataLib
import numpy as np

class Signal():

    def __init__(self, start_train_date, end_train_date, start_test_date, end_test_date):
        dl = DataLib("SignalData")
        self.BondReturnIdx = dl.pull("BondRetIdx/LocalFX")
        self.one_day_bond_return = self.BondReturnIdx.pct_change(1)

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

    def run_testing(self):
        for date in pd.date_range(self.start_test_date, self.end_test_date, freq='B').date:
            positions = self.update_signal(date)
            self.position_trace.loc[date,] = positions #to capture other metrics, i.e. by-country total position-allocation
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
        return self.scale_signal(combined_weights)

    def scale_signal(self, positions):
        shorts = (positions < 0) * positions
        short_weights = sum(abs(shorts))
        longs = (positions > 0) * positions
        long_weights = sum(abs((longs)))
        if short_weights != 0:
            scaler = long_weights / short_weights
            shorts = shorts * scaler
        return longs + shorts

    def get_daily_returns(self):
        return self.daily_ret

    def get_quarterly_returns(self):
        return self.daily_ret.resample('Q').sum()
