import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from DataIOUtilities.DataLib import DataLib


def get_bond_indices(countries, beg_date, end_date):
    dl = DataLib("SignalData")
    bond_returns_index = dl.pull("BondRetIdx/LocalFX")[countries].resample('1Q').last().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    return bond_returns_index


def get_bond_returns(countries, beg_date, end_date):
    dl = DataLib("SignalData")
    bond_returns_index = dl.pull("BondRetIdx/LocalFX")[countries].resample('1Q').last().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    bond_returns = bond_returns_index.pct_change()
    bond_returns_adjusted = bond_returns.iloc[1:]
    bond_returns_adjusted.index = bond_returns.index[1:]
    return bond_returns_adjusted

def standardize(x):
    mean = np.mean(x)
    std = np.std(x)
    return (x-mean)/std

def relativize(data):
    first = data[0]
    return 100*(data/first)-100

def aug_sigmoid(data):
    return 2 * ((1 / (1 + np.exp(-data))) - 0.5)

class Signal(object):

    def __init__(self, indicators_dict):
        self.indicators_dict = indicators_dict

    def send(self, country, date):
        indicators_values = {indicator_name: self.indicators_dict[indicator_name].get_value(country, date)
                                 for indicator_name in self.indicators_dict.keys()}
        return self.combine_indicators_values(indicators_values)

    def combine_indicators_values(self, indicators_values):
        pass

    def get_signals(self, countries, beg_date, end_date):
        bond_returns_index = get_bond_indices(countries, beg_date, end_date)
        signal_dates = bond_returns_index.index[:-1]

        signals = pd.DataFrame(index=signal_dates, columns=countries)

        for date in signal_dates:
            for country in countries:
                signals[country][date] = self.send(country, date)

        return signals

    def get_returns(self, countries, beg_date, end_date):
        bond_returns = get_bond_returns(countries, beg_date, end_date)
        signals = self.get_signals(countries, beg_date, end_date)

        signals_adjusted = signals.copy()
        signals_adjusted.index = bond_returns.index

        returns = signals_adjusted * bond_returns

        returns['TOTAL'] = sum([returns[country] for country in countries])

        return returns

    def get_cumulative_returns(self, countries, beg_date, end_date):
        returns = self.get_returns(countries, beg_date, end_date)

        cumulative_returns = returns.copy()

        dates = cumulative_returns.index[1:]
        prev_dates = cumulative_returns.index[:-1]

        for columns in cumulative_returns.columns:
            for date, prev_date in zip(dates, prev_dates):
                cumulative_returns[columns][date] = ((1 + cumulative_returns[columns][date]) *
                                                     (1 + cumulative_returns[columns][prev_date]) - 1)

        return cumulative_returns

    def plot_signal_index_returns(self, countries, beg_date, end_date, figsize=None):
        signals = self.get_signals(countries, beg_date, end_date)
        cum_returns = self.get_cumulative_returns(countries, beg_date, end_date)
        bond_indices = get_bond_indices(countries, beg_date, end_date)

        for country in countries:

            fig, ax1 = plt.subplots(figsize=figsize)
            ax2 = ax1.twinx()

            ax1.plot(100*signals[country].to_timestamp(), color='black', label='Signal')
            ax1.set_ylabel('Position (%)')
            ax1.set_ylim((-105, 105))
            ax1.legend(loc=2)

            ax2.plot(relativize(bond_indices[country]).to_timestamp(), color='blue', label='Bond Index')
            ax2.plot(100*cum_returns[country].to_timestamp(), color='red', label='Investment Strategy')
            ax2.set_ylabel('Returns (%)')
            ax2.legend(loc=1)

            plt.xlabel('Date')

            plt.title('{} Signal vs Bond Returns vs Strategy Returns'.format(country))
            plt.show()

class Indicator(object):
    def __init__(self, series_names):
        dl = DataLib("SignalData")
        self.series_dict = {series_name: dl.pull(series_name).resample('1Q').last() for series_name in series_names}

    def get_value(self, country, date):
        series_up_to_date = {series_name: self.series_dict[series_name].loc[:pd.Period(date)][country]
                             for series_name in self.series_dict.keys()}
        return self.combine_series(series_up_to_date)

    def combine_series(self, series_up_to_date):
        pass

    def get_values(self, countries, beg_date, end_date):
        bond_returns_index = get_bond_indices(countries, beg_date, end_date)
        values_dates = bond_returns_index.index[:-1]

        values = pd.DataFrame(index=values_dates, columns=countries)

        for date in values_dates:
            for country in countries:
                values[country][date] = self.get_value(country, date)

        return values

    def plot_indicator_returns(self, countries, beg_date, end_date, figsize=None):
        values = self.get_values(countries, beg_date, end_date)
        bond_returns = get_bond_returns(countries, beg_date, end_date)
        annualized_bond_returns = ((1+bond_returns)**4)-1

        for country in countries:
            fig, ax1 = plt.subplots(figsize=figsize)
            ax2 = ax1.twinx()

            ax1.plot(values[country].to_timestamp(), color='black', label='Indicator')
            ax1.set_ylabel('Value')
            ax1.legend(loc=2)

            ax2.plot(100*annualized_bond_returns[country].to_timestamp(), color='blue', label='Bond Returns')
            ax2.set_ylabel('Annualized Returns (%)')
            ax2.legend(loc=1)

            plt.xlabel('Date')

            plt.title('{} Indicaroe vs Bond Returns'.format(country))
            plt.show()


