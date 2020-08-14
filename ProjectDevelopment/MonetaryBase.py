import pandas as pd
from Indicators import BaseIndicator


class MonetaryBase(BaseIndicator):

    def __init__(self, start_train_date, end_train_date):
        BaseIndicator.__init__(self)
        self.start_train_date = start_train_date
        self.end_train_date = end_train_date

        self.est_aus_data = ((self.m1 + self.m3) * 0.5)["AUS"]
        self.prior_weights = pd.Series()

    def update_indicator(self, date):
        slope_change_m2 = self.get_m2_second_diff()
        curr_slopes_standardized = self.standardize_m2_time(slope_change_m2, norm_period=5)
        if self.prior_weights.empty:
            self.prior_weights = curr_slopes_standardized
        # hold prior position if the slope is < .5 standard deviations from 0
        curr_slopes_standardized = curr_slopes_standardized.where(curr_slopes_standardized.abs() > 0.5, self.prior_weights)
        positions = curr_slopes_standardized * -1
        total_weight = positions.abs().sum()
        if total_weight != 0:
            positions = positions / total_weight
        self.end_train_date = date
        self.prior_weights = curr_slopes_standardized
        return positions

    def get_m2_second_diff(self):
        m2_training = self.m2.loc[self.start_train_date:self.end_train_date]
        m2_training.loc[:, "AUS"] = self.est_aus_data.loc[self.start_train_date : self.end_train_date]
        change_m2_1mo = m2_training.pct_change(1)
        smoothed_m2_training = change_m2_1mo.rolling(3).mean()
        return smoothed_m2_training.diff()

    def standardize_m2_time(self, slope_change_m2, norm_period):
        rolling_slope = slope_change_m2.rolling(norm_period * 12, min_periods=12 * 2)
        rolling_slope_std = rolling_slope.std()
        time_standardized_slopes = (slope_change_m2)/ rolling_slope_std
        return time_standardized_slopes.loc[self.end_train_date]