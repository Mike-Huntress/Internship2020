import pandas as pd
from Indicators import BaseIndicator


class BondPremium(BaseIndicator):

    def __init__(self, start_train_date, end_train_date):
        self.start_train_date = start_train_date
        self.end_train_date = end_train_date
        self.bond_premium = self.LongRates - self.ShortRates
        self.curve_height = (self.LongRates + self.ShortRates) * 0.5
        self.max_curve_height = self.curve_height.max(axis=1)

    def update_indicator(self, date):
        pos_normalized_premiums = self.normalize_bond_premium(6, 6)
        weights = self.curve_height_weights()
        long_weights = self.get_long_positions(weights, pos_normalized_premiums)
        self.end_train_date = date
        return long_weights

    def normalize_bond_premium(self, num_years, min_years):
        bond_premium_training = self.bond_premium[self.start_train_date:self.end_train_date]
        normalized_bond_premium = self.rolling_z_score(bond_premium_training, 12 * num_years, 12 * min_years)
        curr_bond_premium = normalized_bond_premium.loc[self.end_train_date]
        pos_normalized_premiums = curr_bond_premium.multiply(curr_bond_premium.gt(0))
        return pos_normalized_premiums

    def curve_height_weights(self):
        curr_curve_heights = self.curve_height.loc[self.end_train_date]
        curr_max_curve_height = self.max_curve_height.loc[self.end_train_date]
        return curr_curve_heights.multiply(1 / curr_max_curve_height, axis=0)

    def get_long_positions(self, weights, premiums):
        long_positions = weights.multiply(premiums)
        weights_total = long_positions.sum()
        if weights_total != 0:
            long_positions = long_positions/weights_total
        return long_positions
