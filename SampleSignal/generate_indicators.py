import math

#Takes in risk premium and curve height data and returns a signal dataframe
def generate_indicator_one(bond_risk_premium, curve_height, window_size=4):
    indicator_one_risk = bond_risk_premium
    risk_mean = indicator_one_risk.mean(axis=1)
    risk_diff_from_mean = indicator_one_risk.subtract(risk_mean, axis=0)
    risk_avg_diff_from_mean = risk_diff_from_mean.shift(1).rolling(window_size * 12, min_periods=window_size * 12).mean()
    country_risk_norm = risk_avg_diff_from_mean.add(risk_mean, axis=0)
    risk_signal = 0.4 * (indicator_one_risk.subtract(risk_mean, axis=0)) + 0.6 * (indicator_one_risk - country_risk_norm)

    indicator_one_height = curve_height
    height_mean = indicator_one_height.mean(axis=1)
    height_diff_from_mean = indicator_one_height.subtract(height_mean, axis=0)
    height_avg_diff_from_mean = height_diff_from_mean.shift(1).rolling(window_size * 12, min_periods=window_size * 12).mean()
    country_height_norm = height_avg_diff_from_mean.add(height_mean, axis=0)
    height_signal = 0.4 * (indicator_one_height.subtract(height_mean, axis=0)) + 0.6 * (indicator_one_height - country_height_norm)

    signal = risk_signal / (risk_signal.max().max() - risk_signal.min().min()) + \
             height_signal / (height_signal.max().max() - height_signal.min().min())

    signal_mean = signal.mean(axis=1)
    signal_centered = signal.subtract(signal_mean, axis=0)
    return signal_centered

#Takes money supply data and returns a signal dataframe
def generate_indicator_two(m1, m2, m3):
    m2_proxy = 0.5 * m1 + 0.5 * m3
    m2_proxy["USA"] = m2["USA"]
    change_in_m2 = m2_proxy.rolling(3).mean() / m2_proxy.rolling(12).mean()
    change_in_m2 = change_in_m2 - 1
    return change_in_m2


"""Takes in exchange rates (modified fxVsUSD) and TWI data - returns proxied TWI dataframe

Canada most similar to US by top 15 trading partners but has US making up 75% of exports
Euro countries (Italy, Spain, France, Germany) most similar to Switzerland construction
Idea: can proxy change in twi by converting local currency to USD or CHE and tracking change in those twis
Assumption: "similar" countries trade with the same partners in relatively similar proportions
In actuality, we need to subtract off a bit accounting for countries trading with themselves and add on effect of the 
bilateral exchange rate - the subtraction doesn't make a huge difference so we don't do it, but the addition makes a 
large difference for Canada so we do account for that.
Note: xr_to_usd has the USA column filled with exchange rate from USD to Euro
Represents xr * foreign currency = 1USD or xr USD = 1 euro
"""


def create_twi_proxy(xr_to_usd, trd_wts):
    twi_proxy = trd_wts
    twi_proxy["ITA"] = (1 / xr_to_usd["ITA"] * xr_to_usd["CHE"] * trd_wts["CHE"])
    twi_proxy["FRA"] = (1 / xr_to_usd["FRA"] * xr_to_usd["CHE"] * trd_wts["CHE"])
    twi_proxy["DEU"] = (1 / xr_to_usd["DEU"] * xr_to_usd["CHE"] * trd_wts["CHE"])
    twi_proxy["ESP"] = (1 / xr_to_usd["ESP"] * xr_to_usd["CHE"] * trd_wts["CHE"])
    twi_proxy["CAN"] = (1 / xr_to_usd["CAN"] * trd_wts["USA"])
    change_in_twi_proxy = twi_proxy.rolling(3).mean() / twi_proxy.shift(3).rolling(12).mean() - 1

    USA_to_fx = 1 / xr_to_usd
    change_in_USA_to_fx = USA_to_fx.rolling(3).mean() / USA_to_fx.shift(3).rolling(12).mean() - 1

    CHE_to_fx = (1 / xr_to_usd).mul(xr_to_usd["CHE"], axis=0)
    change_in_CHE_to_fx = CHE_to_fx.rolling(3).mean() / CHE_to_fx.shift(3).rolling(12).mean() - 1

    proxy_weights = [.05, .03, .04, .015, .75]
    proxied = list(change_in_twi_proxy.columns[-5:])
    for ix, country in enumerate(proxied):
        if country == "CAN":
            change_in_twi_proxy[country] = change_in_twi_proxy[country] * (1 - proxy_weights[ix]) + \
                                           change_in_USA_to_fx[country] * proxy_weights[ix]
        else:
            change_in_twi_proxy[country] = change_in_twi_proxy[country] * (1 - proxy_weights[ix]) + \
                                           change_in_CHE_to_fx[country] * proxy_weights[ix]
    return change_in_twi_proxy


#Takes TWI data and returns a signal dataframe
def generate_indicator_three(change_in_twi):
    historical_avg_change = change_in_twi.expanding().mean()
    diff_from_mean = change_in_twi - historical_avg_change
    global_mean = diff_from_mean.mean(axis=1)
    indicator_three_centered = diff_from_mean.subtract(global_mean, axis=0)
    return indicator_three_centered


#Takes indicator output from risk premium + bond height and maps to the range [-1, 1]
def rescale_mapping_one(x):
    std = .12
    if x > 0:
        return 1 - math.e ** ((-1/2)*(x / std) ** 2)
    elif x == 0:
        return 0
    else:
        return -1 * (1 - math.e ** ((-1/2)*(x / std) ** 2))


#Takes indicator output from currency appreciation and maps to the range [-1, 1]
def rescale_mapping_three(x):
    std = .04
    if x > 0:
        return 1 - math.e ** ((-1 / 2) * (x / std) ** 2)
    elif x == 0:
        return 0
    else:
        return -1 * (1 - math.e ** ((-1 / 2) * (x / std) ** 2))
