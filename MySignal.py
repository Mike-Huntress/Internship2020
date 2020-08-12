import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

from DataIOUtilities.DataLib import DataLib


def get_bond_indices(countries, beg_date, end_date):
    dl = DataLib("SignalData")
    bond_returns_index = dl.pull("BondRetIdx/LocalFX")[countries].resample('1D').ffill().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    return bond_returns_index

def get_total_index(indices):

    returns = indices.pct_change().fillna(0)
    cumulative_returns = get_rows_avg(returns)

    dates = cumulative_returns.index[1:]
    prev_dates = cumulative_returns.index[:-1]

    for date, prev_date in zip(dates, prev_dates):
        cumulative_returns[date] = ((1 + cumulative_returns[date]) *
                                             (1 + cumulative_returns[prev_date]) - 1)
    return cumulative_returns+1

def get_bond_returns(countries, beg_date, end_date):
    dl = DataLib("SignalData")
    bond_returns_index = dl.pull("BondRetIdx/LocalFX")[countries].resample('1D').ffill().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    bond_returns = bond_returns_index.pct_change().fillna(0)
    return bond_returns

def get_rows_avg(data):
    total_returns = data.mean(axis=1)
    return total_returns

def get_short_rates(countries, beg_date, end_date):
    dl = DataLib("SignalData")
    short_rates = dl.pull("ShortRates")[countries].resample('1D').ffill().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    return short_rates

def get_long_rates(countries, beg_date, end_date):
    dl = DataLib("SignalData")
    long_rates = dl.pull("LongRates")[countries].resample('1D').ffill().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    return long_rates

def standardize(x):
    mean = np.mean(x)
    std = np.std(x)
    return (x-mean)/std

def relativize(data):
    first = data.dropna().iloc[0]
    relativized_data = (data/first).fillna(1)
    return 100*(relativized_data-1)

def aug_sigmoid(data, scaling_factor=1.0):
    return 2 * ((1 / (1 + np.exp(-scaling_factor*data))) - 0.5)

def compound(data, n_periods=1):
    return ((1+data).prod()**(1/n_periods))-1

def annualize(data, n_years=1):
    return 100*data.rolling(n_years*261, min_periods=n_years*261).apply(lambda x: compound(x, n_years), raw=True)

def get_volatility(data, n_periods):
    return data.rolling(n_periods, n_periods).std()

def get_sharpe(excess_returns):
    return excess_returns.mean()/excess_returns.std()

def get_max_drawdown(returns):
    peak = 1
    curr_val = 1
    max_drawdown = 0
    for daily_return in returns:
        curr_val *= (1 + daily_return)
        if curr_val > peak:
            peak = curr_val
        drawdown = (curr_val - peak) / peak
        if drawdown < max_drawdown:
            max_drawdown = drawdown
    return max_drawdown

def get_R2(benchmark_returns, returns):
    lm = linear_model.LinearRegression()
    data = pd.DataFrame(data={'X': benchmark_returns, 'y': returns}).dropna()
    X = data[['X']]
    y = data['y']
    model = lm.fit(X, y)
    R2 = model.score(X, y)
    return R2

class Signal(object):

    def __init__(self, indicators_dict):
        self.indicators_dict = indicators_dict
        self.dp_table = {}

    def send_one_country(self, country, date):
        if (country, date) in self.dp_table:
            return self.dp_table[(country, date)]

        indicators_values = {indicator_name: self.indicators_dict[indicator_name].get_value(country, date)
                                 for indicator_name in self.indicators_dict.keys()}

        self.dp_table[(country, date)] = self.combine_indicators_values(indicators_values)
        return self.dp_table[(country, date)]

    def combine_indicators_values(self, indicators_values):
        pass

    def send(self, country, date):
        return self.send_one_country(country, date)

    def get_signals(self, countries, beg_date, end_date):
        bond_returns_index = get_bond_indices(countries, beg_date, end_date)
        signal_dates = bond_returns_index.index

        signals = pd.DataFrame(index=signal_dates, columns=countries)

        for date in signal_dates:
            for country in countries:
                signals[country][date] = self.send(country, date)

        return signals

    def get_returns(self, countries, beg_date, end_date):
        bond_returns = get_bond_returns(countries, beg_date, end_date).fillna(0)
        signals = self.get_signals(countries, beg_date, end_date).fillna(0)

        bond_returns_shifted = bond_returns.shift(periods=-1)

        returns = signals * bond_returns_shifted

        returns['TOTAL'] = get_rows_avg(returns)

        return returns.dropna()

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
        signals['TOTAL'] = signals.mean(axis=1)
        cum_returns = self.get_cumulative_returns(countries, beg_date, end_date)
        bond_indices = get_bond_indices(countries, beg_date, end_date)
        bond_indices['TOTAL'] = get_total_index(bond_indices)

        for country in ['TOTAL'] + countries:

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

    def plot_signal_sharpe(self, countries, beg_date, end_date, n_periods=261, figsize=None):
        signals = self.get_signals(countries, beg_date, end_date)
        signals['TOTAL'] = signals.mean(axis=1)
        returns = self.get_returns(countries, beg_date, end_date)
        bond_returns = get_bond_returns(countries, beg_date, end_date)
        bond_returns['TOTAL'] = get_rows_avg(bond_returns)

        annualized_returns = (1+returns)**261-1
        annualized_bond_returns = (1+bond_returns**261-1)

        risk_free_rate = get_short_rates(countries, beg_date, end_date)

        excess_returns = 100*annualized_returns - risk_free_rate
        sharpe_ratios = excess_returns.rolling(n_periods, n_periods).apply(get_sharpe, raw=True)

        bond_excess_returns = 100*annualized_bond_returns - risk_free_rate
        bond_sharpe_ratios = bond_excess_returns.rolling(n_periods, n_periods).apply(get_sharpe, raw=True)


        for country in ['TOTAL'] + countries:

            fig, ax1 = plt.subplots(figsize=figsize)
            ax2 = ax1.twinx()

            ax1.plot(100*signals[country].to_timestamp(), color='black', label='Signal')
            ax1.set_ylabel('Position (%)')
            ax1.set_ylim((-105, 105))
            ax1.legend(loc=2)

            ax2.plot(bond_sharpe_ratios[country].to_timestamp(), color='blue', label='Holding Bonds')
            ax2.plot(sharpe_ratios[country].to_timestamp(), color='red', label='Investment Strategy')
            ax2.set_ylabel('Sharpe Ratio')
            ax2.legend(loc=1)

            plt.xlabel('Date')

            plt.title('{} Signal vs Bond and Strategy Sharpe Ratios '.format(country))
            plt.show()

    def get_metrics(self, countries, beg_date, end_date):

        n_days = pd.to_timedelta(pd.Period(end_date)-pd.Period(beg_date)).days

        returns = self.get_returns(countries, beg_date, end_date)
        risk_free = ((1+(get_short_rates(countries, beg_date, end_date)/100))**(1/261))-1
        risk_free['TOTAL'] = risk_free['USA'].copy()
        bond_returns = get_bond_returns(countries, beg_date, end_date)
        bond_returns['TOTAL'] = get_rows_avg(bond_returns)

        metrics = pd.DataFrame(index=['Sharpe Ratio', 'Total Return (%)', 'Excess Return (%)', 'Maximum Drawdown (%)',
                                      'R-Squared', 'Volatility'], columns=countries + ['TOTAL'])

        for country in ['TOTAL'] + countries:
            metrics[country]['Total Return (%)'] = 100 * compound(returns[country], n_days/261)
            metrics[country]['Excess Return (%)'] = 100 * compound(returns[country] - risk_free[country], n_days/261)
            metrics[country]['Volatility'] = ((1+returns[country])**261-(1+risk_free[country])**261).std()
            metrics[country]['Sharpe Ratio'] = metrics[country]['Excess Return (%)']/metrics[country]['Volatility']
            metrics[country]['Maximum Drawdown (%)'] = 100 * get_max_drawdown(returns[country])
            metrics[country]['R-Squared'] = get_R2(bond_returns[country], returns[country])

        return metrics


class Indicator(object):
    def __init__(self, series_names):
        dl = DataLib("SignalData")
        self.series_dict = {series_name: dl.pull(series_name).resample('1D').ffill() for series_name in series_names}
        self.dp_table = {}

    def get_value(self, country, date):
        if (country, date) in self.dp_table:
            return self.dp_table[(country, date)]

        series_up_to_date = {series_name: self.series_dict[series_name].loc[:pd.Period(date)][country]
                             for series_name in self.series_dict.keys()}

        self.dp_table[(country, date)] = self.combine_series(series_up_to_date)
        return self.dp_table[(country, date)]

    def combine_series(self, series_up_to_date):
        pass

    def get_values(self, countries, beg_date, end_date):
        bond_returns_index = get_bond_indices(countries, beg_date, end_date)
        values_dates = bond_returns_index.index

        values = pd.DataFrame(index=values_dates, columns=countries)

        for date in values_dates:
            for country in countries:
                values[country][date] = self.get_value(country, date)

        return values

    def plot_indicator_returns(self, countries, beg_date, end_date, figsize=None):
        values = self.get_values(countries, beg_date, end_date)
        bond_returns = get_bond_returns(countries, beg_date, end_date)
        annualized_bond_returns = ((1+bond_returns)**261)-1

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

            plt.title('{} Indicators vs Bond Returns'.format(country))
            plt.show()


class StandardizedGrowth(Indicator):
    def __init__(self, series_names, weights_dict):
        super(StandardizedGrowth, self).__init__(series_names)
        self.weights_dict = weights_dict

    def combine_series(self, series_up_to_date):
        weighted_values = {}
        for series_name in series_up_to_date.keys():
            weighted_values[series_name] = (self.weights_dict[series_name] *
                                            standardize(series_up_to_date[series_name].pct_change()).iloc[-1])
        return sum(weighted_values.values()) / sum(self.weights_dict.values())


class StandardizedSeries(Indicator):
    def __init__(self, series_names, weights_dict):
        super(StandardizedSeries, self).__init__(series_names)
        self.weights_dict = weights_dict

    def combine_series(self, series_up_to_date):
        weighted_values = {}
        for series_name in series_up_to_date.keys():
            weighted_values[series_name] = (self.weights_dict[series_name] *
                                            standardize(series_up_to_date[series_name]).iloc[-1])
        return sum(weighted_values.values()) / sum(self.weights_dict.values())


class StandardizedRollingGrowth(Indicator):
    def __init__(self, series_names, weights_dict, function=np.mean, n_periods=261):
        super(StandardizedRollingSeries, self).__init__(series_names)
        self.weights_dict = weights_dict
        self.function = function
        self.n_periods = n_periods

    def combine_series(self, series_up_to_date):
        weighted_values = {}
        for series_name in series_up_to_date.keys():
            weighted_values[series_name] = (self.weights_dict[series_name] *
                                            standardize(series_up_to_date[series_name].rolling(
                                                self.n_periods, self.n_periods).apply(self.function)).iloc[-1])
        return sum(weighted_values.values()) / sum(self.weights_dict.values())


class SigmoidNormalizerSignal(Signal):
    def __init__(self, indicators_dict, weights_dict, sigmoid_scaling_factor=1.0):
        super(SigmoidNormalizerSignal, self).__init__(indicators_dict)
        self.weights_dict = weights_dict
        self.sigmoid_scaling_factor = sigmoid_scaling_factor

    def combine_indicators_values(self, indicators_values):
        weighted_values = {}
        for indicator_name in indicators_values.keys():
            weighted_values[indicator_name] = (self.weights_dict[indicator_name] *
                                               aug_sigmoid(indicators_values[indicator_name],
                                                           scaling_factor=self.sigmoid_scaling_factor))
        return sum(weighted_values.values()) / sum(np.abs(list(self.weights_dict.values())))