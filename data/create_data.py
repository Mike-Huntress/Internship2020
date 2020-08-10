"""
File: create_data.py
Author: Jeremy Ephron
---------------------
This file implements the creation of data streams from the initial raw data 
provided.

"""

from DataIOUtilities.DataLib import DataLib


def create_data() -> None:
    """
    Creates several data streams through operations on existing data.

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


if __name__ == '__main__':
    create_data()

