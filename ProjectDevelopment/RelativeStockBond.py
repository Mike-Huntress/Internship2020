import pandas as pd
from Indicators import BaseIndicator


class RelativeStockBond(BaseIndicator):

    def __init__(self, start_train_date, end_train_date):
        BaseIndicator.__init__(self)
        self.start_train_date = start_train_date
        self.end_train_date = end_train_date
        self.equity_ret = self.equities.pct_change(self.WEEKDAYS_IN_YEAR)
        self.bond_ret = self.BondReturnIdx.pct_change(self.WEEKDAYS_IN_YEAR)

    def update_indicator(self, date):
        outperformance = self.get_smoothed_outperformance()
        positions = -1 * self.normalize_outperformance(outperformance)
        positions = self.scale_signal_weights(positions)
        self.end_train_date = date
        return positions

    def scale_signal_weights(self, positions):
        shorts = (positions < 0) * positions
        short_weights = sum(abs(shorts))
        longs = (positions > 0) * positions
        long_weights = sum(abs((longs)))
        if short_weights != 0:
            shorts = shorts / short_weights
        if long_weights != 0:
            longs = longs/long_weights
        return longs + shorts

    def get_smoothed_outperformance(self):
        equity_training = self.equity_ret.loc[self.start_train_date:self.end_train_date]
        equity_risk_adjusted = equity_training / equity_training.std()
        bond_training = self.bond_ret.loc[self.start_train_date:self.end_train_date]
        bond_risk_adjusted = bond_training / bond_training.std()
        outperformance = equity_risk_adjusted - bond_risk_adjusted
        return outperformance.rolling(self.DAYS_IN_MONTH).mean()

    def normalize_outperformance(self, outperformance):
        global_mean = outperformance.loc[self.end_train_date].mean()
        global_std = outperformance.loc[self.end_train_date].std()
        return (outperformance.loc[self.end_train_date] - global_mean) / global_std
