"""
File: data.py
Author: Jeremy Ephron
---------------------
This file creates and implements global variables and functions related to the
retrieval, storage, and labeling of data.

"""

from typing import Tuple, List


COUNTRIES = [
    'USA', 'AUS', 'JPN', 'CAN', 'CHE', 'GBR', 'ESP', 'FRA', 'ITA', 'DEU'
]


def get_all_data_and_labels(
    cleaned: bool = False
) -> Tuple[List[str], List['pd.DataFrame']]:
    """
    Gets all data from the DataLib.

    Args:
        cleaned: whether to retrieve the cleaned data.

    Returns:
        all_labels: a list of string labels for each corresponding DataFrame.
        all_data: a list of DataFrame for each data source.

    """

    from DataIOUtilities.DataLib import DataLib

    dl = DataLib("SignalData")

    suffix = '_clean' if cleaned else ''
    all_labels = [
        'bond_rets_local_fx' + suffix,
        'equity_prices' + suffix,
        'curr_acct_nom_usd' + suffix,
        'curr_acct_pct_gdp' + suffix,
        'fx_trd_wts_nom' + suffix,
        'fx_trd_wts_real' + suffix,
        'fx_vs_usd' + suffix,
        'fx_to_usd' + suffix,
        'gdp_nom' + suffix,
        'gdp_real' + suffix,
        'short_rates' + suffix,
        'long_rates' + suffix,
        'core_cpi_sa' + suffix,
        'm1_usd' + suffix,
        'm2_usd' + suffix,
        'm3_usd' + suffix,
    ]

    if not cleaned:
        all_labels.append('inflation_rate_annual')
        all_labels.append('bond_premium')
        all_labels.append('curve_height')
        all_labels.append('risk_free_rate')

    prefix = 'Cleaned/' if cleaned else ''
    all_data = [
        dl.pull(prefix + 'BondRetIdx/LocalFX'),
        dl.pull(prefix + 'EquityPrices'),
        dl.pull(prefix + 'CurrAcctNom/inUSD'),
        dl.pull(prefix + 'CurrAcctPctGDP'),
        dl.pull(prefix + 'fxTrdWts/Nominal'),
        dl.pull(prefix + 'fxTrdWts/Real'),
        dl.pull(prefix + 'fxVsUSD'),
        dl.pull(prefix + 'fxToUSD'),
        dl.pull(prefix + 'GDP/Nominal'),
        dl.pull(prefix + 'GDP/Real'),
        dl.pull(prefix + 'ShortRates'),
        dl.pull(prefix + 'LongRates'),
        dl.pull(prefix + 'CoreCPI/SA'),
        dl.pull(prefix + 'M1/inUSD'),
        dl.pull(prefix + 'M2/inUSD'),
        dl.pull(prefix + 'M3/inUSD'),
    ]

    if not cleaned:
        all_data.append(dl.pull('inflationRate/Annual'))
        all_data.append(dl.pull('bondPremium'))
        all_data.append(dl.pull('curveHeight'))
        all_data.append(dl.pull('riskFreeRate')['US 3M T-Bill Yield'])

    return all_data, all_labels

