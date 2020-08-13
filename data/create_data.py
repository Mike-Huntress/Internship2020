"""
File: create_data.py
Author: Jeremy Ephron
---------------------
This file implements the creation of data streams from the initial raw data 
provided or pulling new data streams.

"""

from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib, DatastreamPulls

from data import COUNTRIES
from utils import *


def create_data() -> None:
    """
    Creates several data streams through operations on existing data or 
    pulling new data streams.

    """

    dl = DataLib("SignalData")

    # Standardize the conventions of FX rates vs. USD
    fx_vs_usd = dl.pull('fxVsUSD')

    # All are USD to currency, except for Britain
    fx_vs_usd = 1 / fx_vs_usd
    fx_vs_usd['GBR'] = 1 / fx_vs_usd['GBR']

    dl.write_data('fxToUSD', fx_vs_usd.to_timestamp())

    # Bond risk premium
    long_rates = dl.pull('longRates')
    short_rates = dl.pull('shortRates')
    bond_premium = long_rates - short_rates

    dl.write_data('bondPremium', bond_premium.to_timestamp())

    # Curve height
    curve_height = (long_rates + short_rates) / 2

    dl.write_data('curveHeight', curve_height.to_timestamp())

    # Core inflation
    core_cpi_sa = dl.pull('CoreCPI/SA')
    inflation_rate_annual = core_cpi_sa.pct_change(MONTHS_PER_YEAR)

    dl.write_data('inflationRate/Annual', inflation_rate_annual)

    # Risk free rate
    countries = CountryMetaDataFile().readMetadata().loc[COUNTRIES]
    start_date = '1980-01'
    dsPuller = DatastreamPulls(countries)
    
    # Using U.S. 3M T-Bills as risk free rate
    risk_free_rate = dsPuller.ds_country_pull(
        lambda x: f'{x}GBILL3', start_date, '', 'D', ['USA']
    )
    risk_free_rate['USA'] = risk_free_rate['USA'] / 100
    risk_free_rate.rename(columns={'USA': 'US 3M T-Bill Yield'}, inplace=True)
    risk_free_rate.rename_axis('', axis='columns', inplace=True)
    
    dl.write_data('riskFreeRate', risk_free_rate)


if __name__ == '__main__':
    create_data()

