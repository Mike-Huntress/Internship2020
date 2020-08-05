
from .indicator import Indicator
from .signal import Signal


def yield_curve_indicator(data_lib):
    rate_2yr, rate_10yr = data_lib.pull('ShortRates'), data_lib.pull('LongRates')
    risk_premium = Signal('bond_risk_premium', rate_10yr - rate_2yr)
    curve_height = Signal('yield_curve_height', (rate_10yr + rate_2yr) / 2)
    yield_curve = Indicator('yield_curve', risk_premium, curve_height)
    return yield_curve
