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

    all_labels = [
        'bond_rets_local_fx',
        'equity_prices',
        'curr_acct_nom_usd',
        'curr_acct_pct_gdp',
        'fx_trd_wts_nom',
        'fx_trd_wts_real',
        'fx_vs_usd',
        'gdp_nom',
        'gdp_real',
        'short_rates',
        'long_rates',
        'core_cpi_sa',
        'm1_usd',
        'm2_usd',
        'm3_usd'
    ]

    prefix = 'Cleaned/' if cleaned else ''
    all_data = [
        dl.pull(prefix + 'BondRetIdx/LocalFX'),
        dl.pull(prefix + 'EquityPrices'),
        dl.pull(prefix + 'CurrAcctNom/inUSD'),
        dl.pull(prefix + 'CurrAcctPctGDP'),
        dl.pull(prefix + 'fxTrdWts/Nominal'),
        dl.pull(prefix + 'fxTrdWts/Real'),
        dl.pull(prefix + 'fxVsUSD'),
        dl.pull(prefix + 'GDP/Nominal'),
        dl.pull(prefix + 'GDP/Real'),
        dl.pull(prefix + 'ShortRates'),
        dl.pull(prefix + 'LongRates'),
        dl.pull(prefix + 'CoreCPI/SA'),
        dl.pull(prefix + 'M1/inUSD'),
        dl.pull(prefix + 'M2/inUSD'),
        dl.pull(prefix + 'M3/inUSD')
    ]

    return all_data, all_labels

