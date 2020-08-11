import pandas as pd
from MonetaryBase import MonetaryBase
from BondPremium import BondPremium
from RelativeStockBond import RelativeStockBond

class Signal():

    def __init__(self, start_train_date, end_train_date, start_test_date, end_test_date):
        self.start_train_date = start_train_date
        self.end_train_date = end_train_date
        self.start_test_date = start_test_date
        self.end_test_date = end_test_date
        self.monetary_ind = MonetaryBase(self.start_train_date, self.end_train_date)
        self.bond_premium_ind = BondPremium(self.start_train_date, self.end_train_date)
        self.relative_ind = RelativeStockBond(self.start_train_date, self.end_train_date)

    def run_testing(self):
        

    def update_signal(self, date):
        monetary_weight = self.monetary_ind.update_indicator(date)
        premium_weight = self.bond_premium_ind.update_indicator(date)
        relative_weight = self.relative_ind.update_indicator(date)
