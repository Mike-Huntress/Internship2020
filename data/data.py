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


def get_all_data_and_labels() -> Tuple[List[str], List['pd.DataFrame']]:
    """
    Gets all data from the DataLib.

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

    all_data = [
        dl.pull('BondRetIdx/LocalFX'),
        dl.pull('EquityPrices'),
        dl.pull('CurrAcctNom/inUSD'),
        dl.pull('CurrAcctPctGDP'),
        dl.pull('fxTrdWts/Nominal'),
        dl.pull('fxTrdWts/Real'),
        dl.pull('fxVsUSD'),
        dl.pull('GDP/Nominal'),
        dl.pull('GDP/Real'),
        dl.pull('ShortRates'),
        dl.pull('LongRates'),
        dl.pull('CoreCPI/SA'),
        dl.pull('M1/inUSD'),
        dl.pull('M2/inUSD'),
        dl.pull('M3/inUSD')
    ]

    return all_data, all_labels

