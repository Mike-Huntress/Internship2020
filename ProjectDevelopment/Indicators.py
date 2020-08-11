from DataIOUtilities.DataLib import DataLib
import pandas as pd

class BaseIndicator:
    WEEKDAYS_IN_YEAR = 261
    DAYS_IN_MONTH = 20
    dl = DataLib("SignalData")
    BondReturnIdx = dl.pull("BondRetIdx/LocalFX")
    equities = dl.pull("EquityPrices")
    m1 = dl.pull("M1/inUSD")
    m2 = dl.pull("M2/inUSD")
    m3 = dl.pull("M3/inUSD")
    LongRates = dl.pull("LongRates")
    ShortRates = dl.pull("ShortRates")
    daily_long_return = BondReturnIdx.pct_change(1)

    def rolling_z_score(self, data, num_years, min_periods):
        rolling = data.rolling(num_years, min_periods=min_periods)
        rolling_mean = rolling.mean()
        rolling_std = rolling.std()
        return (data - rolling_mean) / rolling_std
