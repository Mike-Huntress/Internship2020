
from .utils import binary_search


def get_interest_factor(interest_rate, periods, compound_freq=1):
    factor = (1 + (interest_rate / compound_freq)) ** (compound_freq * periods)
    return factor


def get_present_value(future_value, interest_rate, periods, compound_freq=1):
    factor = get_interest_factor(interest_rate, periods, compound_freq=compound_freq)
    return future_value / factor


def get_future_value(present_value, interest_rate, periods, compound_freq=1):
    factor = get_interest_factor(interest_rate, periods, compound_freq=compound_freq)
    return present_value * factor


def get_zero_rates(prices, coupon, principal=100):
    principal_factor = 100 / principal
    zrs = []
    coupon *= 100
    for i, price in enumerate(prices):
        instant_price = price * principal_factor
        for j in range(i):
            instant_price -= coupon / (1 + zrs[j])
        payout_ratio = (100 + coupon) / instant_price
        zero_factor = payout_ratio ** (1 / (i + 1))
        zero_rate = zero_factor - 1
        zrs.append(zero_rate)
    return zrs


def get_forward_rates(prices, coupon, principal=100, zrs=None):
    zrs = zrs if zrs else get_zero_rates(prices, coupon, principal=principal)
    frs = []
    for i, price in enumerate(prices):
        fr = (1 + zrs[i]) ** (i + 1)
        if i > 0:
            fr /= (1 + zrs[i - 1]) ** i
        fr -= 1
        frs.append(fr)
    return frs


def get_yield_to_maturity(periods, price, coupon, principal=100, precision=0.000001):
    principal_factor = 100 / principal
    price *= principal_factor
    coupon *= 100

    def make_guess(ytm):
        yield_factor = 1 + ytm
        price_guess = (100 + coupon) / (yield_factor ** periods)
        for i in range(1, periods):
            price_guess += coupon / (yield_factor ** i)
        return price_guess

    return binary_search(0, 1, price, make_guess, precision=precision)


def get_bond_price_from_ytm(periods, ytm, coupon, principal=100):
    coupon *= 100
    yield_factor = 1 + ytm
    price = (100 + coupon) / (yield_factor ** periods)
    for i in range(1, periods):
        price += coupon / (yield_factor ** i)
    price *= principal / 100
    return price


def get_bond_price_from_zero_rates(zero_rates, coupon, principal=100):
    coupon *= 100
    price = 0
    for i, zr in enumerate(zero_rates):
        payout = coupon
        if i == len(zero_rates) - 1:
            payout += principal
        price += get_present_value(payout, zr, i + 1)
    return price


def get_bond_price_from_forward_rates():
    pass
