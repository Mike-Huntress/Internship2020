"""
File: create_denoised_data.py
Author: Jeremy Ephron
-----------------------------
This script creates denoised data from the available signals and writes them
to the DataLib.

"""

import logging

import pandas as pd

from DataIOUtilities.DataLib import DataLib

from data import COUNTRIES, get_all_data_and_labels
from signal_math import denoise_emd_dfa


def create_denoised_data():
    """
    Creates denoised raw data from the available signals using EMD+DFA.

    """

    all_data, all_labels = get_all_data_and_labels()
    
    # Write destinations
    dests = [
        'BondRetIdx/LocalFX',
        'EquityPrices',
        'CurrAcctNom/inUSD',
        'CurrAcctPctGDP',
        'fxTrdWts/Nominal',
        'fxTrdWts/Real',
        'fxVsUSD',
        'GDP/Nominal',
        'GDP/Real',
        'ShortRates',
        'LongRates',
        'CoreCPI/SA',
        'M1/inUSD',
        'M2/inUSD',
        'M3/inUSD'
    ]
    dests = ['Cleaned/' + d for d in dests]
    
    dl = DataLib('SignalData')
    
    # For each signal
    for i in range(len(all_data)):
        logging.info(f'Started {all_labels[i]}')

        # For each country available for the signal
        country_series = []
        for country in all_data[i].columns:
            logging.info(f'-- Started country {country}')

            x = all_data[i][country].dropna()

            # Set window parameters based on frequency
            w_min = 2
            w_max = 5
            if x.index.freq == 'B':
                w_max = 9
            elif x.index.freq == 'M':
                w_max = 5
            elif x.index.freq == 'Q-DEC':
                w_min = 1
                w_max = 3

            # Reconstruct the signal without noisy IMFs
            denoised = denoise_emd_dfa(
                x,
                max_n_imfs=4,
                w_min=w_min,
                w_max=w_max,
                w_step=0.5,
                spline_method='cubic',
                extrema_method='simple'
            )

            country_series.append(denoised)

            logging.info(f'-- Finished country {country}')

        # Combine the series for each country
        denoised_data = pd.concat(
            country_series, keys=all_data[i].columns, axis=1
        )

        dl.write_data(dests[i], denoised_data)

        logging.info(f'Finished writing {all_labels[i]}')
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    create_denoised_data()

