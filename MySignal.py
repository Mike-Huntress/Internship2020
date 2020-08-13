import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

from DataIOUtilities.DataLib import DataLib

###############################
########### CLASSES ###########
###############################


class Indicator(object):
    """
    Abstracts a daily indicator as float calculated from a set of DataSeries for a country in a
    given date
    """
    def __init__(self, series_names, time_window):
        """
        Initializes the Indicator by saving the DataSeries it uses
        :param series_names: names of the DataSeries that are used to calculate the indicator
        :param time_window: length of the past period (in days) used to calculate the indicator
        """
        dl = DataLib("SignalData")
        self.series_dict = {series_name: dl.pull(series_name).resample('D').ffill() for series_name in series_names}
        self.time_window = time_window
        self.dp_table = {}

    def get_value(self, country, date):
        """
        Calculates the value of the indicator for a given country in a given date
        :param country: Country to be analyzed
        :param date: Date to be analyzed
        :return: The value of the indicator for country on date
        """
        if (country, date) in self.dp_table:
            return self.dp_table[(country, date)]
        series_up_to_date = {series_name: self.series_dict[series_name].loc[pd.Period(date)-self.time_window:\
                                                                            pd.Period(date)][country]
                             for series_name in self.series_dict.keys()}

        self.dp_table[(country, date)] = self.combine_series(series_up_to_date)
        return self.dp_table[(country, date)]

    def combine_series(self, series_up_to_date):
        """
        Function that calculates the value of the indicator at the end of the period described by series_up_to_date
        :param series_up_to_date: DataSeries
        :return: The value of the indicator for series_up_to_date
        """
        pass

    def get_values(self, countries, beg_date, end_date):
        """
        Returns a DataFrame with the values of the indicator for different countries at each weekday of a given time
        period. Each column is a DataSeries with the indicator values for a country. Also return a "World" column
        with the daily average signal from all countries in countries
        :param countries: Countries to be analyzed
        :param beg_date: Beginning of analyzed period
        :param end_date: End of analyzed period
        :return: DataFrame with indicator values
        """
        bond_returns_index = get_bond_indices(countries, beg_date, end_date)
        values_dates = bond_returns_index.index

        values = pd.DataFrame(index=values_dates, columns=countries)

        for date in values_dates:
            for country in countries:
                values[country][date] = self.get_value(country, date)

        values['World'] = get_rows_avg(values)

        return values


class Signal(object):
    """
    Abstracts a daily signal as a decimal in interval (-1, 1) calculated from a set of Indicator
    values for a country in a given date
    """
    def __init__(self, indicators_dict):
        """
        Initializes a Signal by setting the dictionary of indicators used in it
        :param indicators_dict:
        """
        self.indicators_dict = indicators_dict
        self.dp_table = {}

    def send_independent(self, country, date):
        """
        Calculates the independent signal of a single country by combining the indicators for it on a given date.
        This is not the final signal, since more calculations can be done once these initial signals are calculated in
        the method send(), which is the last output of a Signal
        :param country: Country to be analyzed
        :param date: Date to be analyzed
        :return: The independent signal for country on date
        """
        if (country, date) in self.dp_table:
            return self.dp_table[(country, date)]

        indicators_values = {indicator_name: self.indicators_dict[indicator_name].get_value(country, date)
                                 for indicator_name in self.indicators_dict.keys()}

        self.dp_table[(country, date)] = self.combine_indicators_values(indicators_values)
        return self.dp_table[(country, date)]

    def combine_indicators_values(self, indicators_values):
        """
        Combines the various indicators in the signal for a single country to calculate the independent signal
        :param indicators_values: values of the indicators for a given country
        :return: The independent signal given the indicators
        """
        pass

    def send(self, country, date):
        """
        Calculates the final Signal sent for a country using the independent signals
        :param country: Country to be analyzed
        :param date: Date to be analyzed
        :return: THe final Signal
        """
        return self.send_independent(country, date)

    def get_signals(self, countries, beg_date, end_date, add_world_column=True):
        """
        Creates a DataFrame in which each column is a DataSeries with the value of the final signal for a country during
        a given period.
        :param countries: Countries to be Analyzed
        :param beg_date: Beginning of analyzed period
        :param end_date: End of analyzed period
        :param add_world_column: If True, adds a "World" column with the average signal of all countries in countries
                                 for each date
        :return:
        """
        bond_returns_index = get_bond_indices(countries, beg_date, end_date)
        signal_dates = bond_returns_index.index

        signals = pd.DataFrame(index=signal_dates, columns=countries)

        for date in signal_dates:
            for country in countries:
                signals[country][date] = self.send(country, date)
        if add_world_column:
            signals['World'] = get_rows_avg(signals)

        return signals

    def get_total_returns(self, countries, beg_date, end_date):
        """
        Creates a DataFrame in which each column is a DataSeries with the daily returns of the signal for a country
        in countries during a given period. Also adds a "World" column with the average returns of all countries
        :param countries: Countries to be analyzed
        :param beg_date: Beginning of analyzed period
        :param end_date: End of analyzed period
        :return: DataFrame of all returns
        """
        bond_returns = get_bond_returns(countries, beg_date, end_date, add_world_column=False)
        signals = self.get_signals(countries, beg_date, end_date, add_world_column=False)

        bond_returns_shifted = bond_returns.shift(periods=-1)

        returns = signals * bond_returns_shifted

        returns['World'] = get_rows_avg(returns)

        return returns.dropna()

    def get_cumulative_returns(self, countries, beg_date, end_date):
        """
        Creates a DataFrame in which each column is a DataSeries with the cumulative returns of the signal for a country
        in countries in each day during a given period. Also adds a "World" column with the average cumulative returns
        of all countries
        :param countries: Countries to be analyzed
        :param beg_date: Beginning of analyzed period
        :param end_date: End of analyzed period
        :return: DataFrame of all cumulative returns
        """
        total_returns = self.get_total_returns(countries, beg_date, end_date)
        cumulative_returns = get_returns_index(total_returns) - 1
        return cumulative_returns

    def plot_signal_alpha_returns(self, countries, beg_date, end_date, figsize=None):
        signals = self.get_signals(countries, beg_date, end_date)
        cum_returns = self.get_cumulative_returns(countries, beg_date, end_date)
        bond_alpha_returns = get_bond_alpha_returns(countries, beg_date, end_date)

        for country in ['World'] + countries:

            fig, ax1 = plt.subplots(figsize=figsize)
            ax2 = ax1.twinx()

            ax1.plot(100*signals[country].to_timestamp(), color='black', label='Signal')
            ax1.set_ylabel('Position (%)')
            ax1.set_ylim((-105, 105))
            ax1.legend(loc=2)

            ax2.plot(100*(get_returns_index(bond_alpha_returns[country])-1).to_timestamp(), color='blue', label='Bond Alpha Index')
            ax2.plot(100*cum_returns[country].to_timestamp(), color='red', label='Investment Strategy')
            ax2.set_ylabel('Cumulative Returns (%)')
            ax2.legend(loc=1)

            plt.xlabel('Date')

            plt.title('{} Signal vs Bond Returns vs Strategy Returns'.format(country))
            plt.show()

    def plot_signal_sharpe(self, countries, beg_date, end_date, n_days=365, figsize=None):
        signals = self.get_signals(countries, beg_date, end_date)
        strategy_total_returns = self.get_total_returns(countries, beg_date, end_date)
        bond_total_returns = get_bond_returns(countries, beg_date, end_date)

        strategy_excess_returns = get_excess_returns(strategy_total_returns)
        annualized_strategy_excess_returns = annualize(strategy_excess_returns)
        strategy_sharpe_ratios = annualized_strategy_excess_returns.rolling(n_days, n_days).apply(get_sharpe, raw=True)

        bond_excess_returns = get_excess_returns(bond_total_returns)
        annualized_bond_excess_returns = annualize(bond_excess_returns)
        bond_sharpe_ratios = annualized_bond_excess_returns.rolling(n_days, n_days).apply(get_sharpe, raw=True)


        for country in ['World'] + countries:

            fig, ax1 = plt.subplots(figsize=figsize)
            ax2 = ax1.twinx()

            ax1.plot(100*signals[country].to_timestamp(), color='black', label='Signal')
            ax1.set_ylabel('Position (%)')
            ax1.set_ylim((-105, 105))
            ax1.legend(loc=2)

            ax2.plot(bond_sharpe_ratios[country].to_timestamp(), color='blue', label='Holding Bonds')
            ax2.plot(strategy_sharpe_ratios[country].to_timestamp(), color='red', label='Investment Strategy')
            ax2.set_ylabel('Sharpe Ratio')
            ax2.legend(loc=1)

            plt.xlabel('Date')

            plt.title('{} Signal vs Bond and Strategy Sharpe Ratios '.format(country))
            plt.show()

    def get_metrics(self, countries, beg_date, end_date):

        n_days = pd.to_timedelta(pd.Period(end_date)-pd.Period(beg_date)).days

        strategy_returns = self.get_total_returns(countries, beg_date, end_date)
        strategy_excess_returns = strategy_returns.apply(get_excess_returns)
        bond_returns = get_bond_returns(countries, beg_date, end_date)
        strategy_alpha_returns = (strategy_returns - bond_returns).fillna(0)

        metrics = pd.DataFrame(index=['Sharpe Ratio', 'Annualized Total Return (%)', 'Annualized Excess Return (%)',
                                      'Annualized Alpha Return (%)', 'Maximum Drawdown (%)', 'R-Squared',
                                      'Excess Return Volatility', 'Total Return Volatility', 'Alpha Return Volatility'],
                               columns=['World']+countries)

        for country in ['World'] + countries:
            metrics[country]['Annualized Total Return (%)'] = 100*((1+strategy_returns[country]).prod()**(365/n_days)-1)
            metrics[country]['Annualized Excess Return (%)'] = 100*((1+strategy_excess_returns[country]).prod()**(365/n_days)-1)
            metrics[country]['Annualized Alpha Return (%)'] = 100*((1+strategy_alpha_returns[country]).prod()**(365/n_days)-1)
            metrics[country]['Excess Return Volatility'] = annualize(strategy_excess_returns[country]).std()
            metrics[country]['Total Return Volatility'] = annualize(strategy_returns[country]).std()
            metrics[country]['Alpha Return Volatility'] = annualize(strategy_alpha_returns[country]).std()
            metrics[country]['Sharpe Ratio'] = get_sharpe(annualize(strategy_excess_returns[country]))
            metrics[country]['Maximum Drawdown (%)'] = 100 * get_max_drawdown(strategy_returns[country])
            metrics[country]['R-Squared'] = get_R2(bond_returns[country], strategy_returns[country])

        return metrics


class StandardizedRollingGrowthDiff(Indicator):
    def __init__(self, series_names, weights_dict, world, time_window, n_rolling_periods=365):
        super(StandardizedRollingGrowthDiff, self).__init__(series_names, time_window)
        self.weights_dict = weights_dict
        self.world = world

        for series_name in series_names:
            self.series_dict[series_name] = standardize(self.series_dict[series_name].pct_change() \
                                                            .rolling(n_rolling_periods, n_rolling_periods).apply(
                lambda x: (1 + x).prod() - 1, raw=True))

            self.series_dict[series_name]['World'] = self.series_dict[series_name].mean(axis=1)

        for series_name in series_names:
            for country in self.world:
                self.series_dict[series_name][country] -= self.series_dict[series_name]['World']

    def combine_series(self, series_up_to_date):
        last_values = {series_name: series_up_to_date[series_name].iloc[-1] for series_name in series_up_to_date.keys()}
        return weighted_avg(last_values, self.weights_dict)

    def plot_indicator_returns_diff(self, countries, beg_date, end_date, figsize=None):
        values = self.get_values(countries, beg_date, end_date)
        bond_returns = get_bond_returns(self.world, beg_date, end_date)
        #annualized_bond_returns = ((1 + bond_returns) ** 365) - 1

        for country in countries:
            fig, ax1 = plt.subplots(figsize=figsize)
            ax2 = ax1.twinx()

            ax1.plot(values[country].to_timestamp(), color='black', label='Indicator')
            ax1.set_ylabel('Value')
            ax1.legend(loc=2)

            ax2.plot(100 * (get_returns_index(bond_returns[country]-bond_returns['World'])-1).to_timestamp(),
                     color='blue', label='Bond Alpha Returns')
            ax2.set_ylabel('Total Returns (%)')
            ax2.legend(loc=1)

            plt.xlabel('Date')

            plt.title('{} Indicators vs Bond Alpha Returns'.format(country))
            plt.show()


class SigmoidNormalizerDiff(Signal):
    def __init__(self, indicators_dict, weights_dict, world,
                 sigmoid_scaling_factor=1.0, beta_overlay=0):
        super(SigmoidNormalizerDiff, self).__init__(indicators_dict)
        self.weights_dict = weights_dict
        self.sigmoid_scaling_factor = sigmoid_scaling_factor
        self.world = world
        self.beta_overlay = beta_overlay

    def combine_indicators_values(self, indicators_values):
        sigmoid_normalized_indicators = {indicator_name: aug_sigmoid(indicators_values[indicator_name],
                                                                     scaling_factor=self.sigmoid_scaling_factor)
                                         for indicator_name in indicators_values.keys()}
        return weighted_avg(sigmoid_normalized_indicators, self.weights_dict)

    def send(self, country, date):
        # Calculate Sum of World Independent Signals
        world_signals = {}
        for world_country in self.world:
            world_signals[world_country] = self.send_independent(world_country, date)
        signals_sum = sum(world_signals.values())

        # Adjust Signals to Represent a Pure Alpha Strategy
        adjusted_signals = {}
        for world_country in self.world:
            adjusted_signals[world_country] = world_signals[world_country] - signals_sum / len(self.world)

        # Scale Signals to range (-1, 1)
        max_signal = np.max(np.abs(list(adjusted_signals.values())))
        normalized_signals = {}
        if max_signal > 1:
            for world_country in self.world:
                normalized_signals[world_country] = adjusted_signals[world_country] / max_signal
        else:
            normalized_signals = adjusted_signals

        # Adjust to a Beta Overlay
        beta_adjusted_signals = {}
        beta = self.beta_overlay
        alpha = 1 - self.beta_overlay
        for world_country in self.world:
            beta_adjusted_signals[world_country] = beta + alpha * normalized_signals[world_country]

        return beta_adjusted_signals[country]


####################################
######### HELPER FUNCTIONS #########
####################################

def relativize(indices):
    """
    Transforms indices initialized at arbitrary values in a standard dataset of indices which all begin with value 1
    :param data: DataDrame with one index time series per column
    :return: DataFrame of relativized indices with one index time series per column
    """
    pct_change = indices.pct_change().fillna(0)
    relativized_indices = (1+pct_change).cumprod()
    return relativized_indices

def get_bond_indices(countries, beg_date, end_date, add_world_column=True):
    """
    Returns the relativized bond returns indices
    :param countries: countries whose indices will be analyzed
    :param beg_date: beginning of analyzed period
    :param end_date: end of analyzed period
    :param add_world_column: if True, adds an extra "World" column with an aggregate index of all countries
    :return: a DataFrame with all indices
    """
    dl = DataLib("SignalData")
    bond_returns_index = dl.pull("BondRetIdx/LocalFX")[countries].resample('D').ffill().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    relativized_bond_returns_index = relativize(bond_returns_index)
    if add_world_column:
        relativized_bond_returns_index['World'] = get_rows_avg(relativized_bond_returns_index)
    return relativized_bond_returns_index

def get_total_index(indices):
    """
    Creates an index formed by the average return of all indices
    :param indices: DataFrame with different indices
    :return: new Series with index from average return of all indices
    """
    returns = indices.pct_change().fillna(0)
    total_returns = get_rows_avg(returns)
    total_index = (1+total_returns).cumprod()
    return total_index

def get_bond_returns(countries, beg_date, end_date, add_world_column=True):
    """
    Creates a DataFrame with bond returns of a set of countries within a time period.
    :param countries: Countries being analyzed
    :param beg_date: Beginning of analyzed period
    :param end_date: End of analyzed period
    :param add_world_column: If True,  creates an extra column "World" with average returns of all countries.
    :return: a DataFrame with the returns
    """
    dl = DataLib("SignalData")
    bond_returns_index = dl.pull("BondRetIdx/LocalFX")[countries].resample('D').ffill().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    bond_returns = bond_returns_index.pct_change().fillna(0)
    if add_world_column:
        bond_returns['World'] = get_rows_avg(bond_returns)
    return bond_returns

def get_bond_alpha_returns(countries, beg_date, end_date, add_world_column=True):
    """
    Creates a DataFrame with bond alpha returns (diff to world) of a set of countries within a time period.
    :param countries: Countries being analyzed
    :param beg_date: Beginning of analyzed period
    :param end_date: End of analyzed period
    :param add_world_column: If True, creates an extra column "World" with average alpha returns of all countries.
                             This is a sanity check and should be zero.
    :return: a DataFrame with the alpha returns
    """
    bond_returns = get_bond_returns(countries, beg_date, end_date)
    bond_alpha_returns = pd.DataFrame()
    for country in countries:
        bond_alpha_returns[country] = bond_returns[country] - bond_returns['World']

    if add_world_column:
        bond_alpha_returns['World'] = get_rows_avg(bond_alpha_returns)
    return bond_alpha_returns

def get_rows_avg(dataframe):
    """
    :param data: A DataFrame
    :return: A Series with the average values of each row of data
    """
    average = dataframe.mean(axis=1)
    return average

def get_risk_free(beg_date, end_date):
    """
    Returns the daily risk free rates for a given period using USA Short Rates.
    :param beg_date: Beginning of analyzed period
    :param end_date: End of analyzed period
    :return: The daily risk free rate for that period
    """
    dl = DataLib("SignalData")
    short_rates = dl.pull("ShortRates")['USA'].resample('1D').ffill().loc[
                         pd.Period(beg_date):pd.Period(end_date)]
    daily_short_rates = (1 + (short_rates / 100)) ** (1 / 365) - 1
    return daily_short_rates

def get_excess_returns(total_returns):
    """
    Converts a DataSeries of Daily Total Returns in Excess Returns
    :param total_returns: DataSeries of Daily Total Returns
    :param beg_date: Beginning of analyzed period
    :param end_date: End of analyzed period
    :return: DataSeries of Daily Excess Returns
    """
    beg_date = str(total_returns.index[0])
    end_date = str(total_returns.index[-1])
    risk_free = get_risk_free(beg_date, end_date)
    return total_returns-risk_free.fillna(0)

def standardize(dataseries):
    """
    Standardizes a DataSeries using its Z-Score
    :param dataseries: Original DataSeries
    :return: the Z-Score of dataseries
    """
    mean = np.mean(dataseries)
    std = np.std(dataseries)
    return (dataseries-mean)/std

def aug_sigmoid(data, scaling_factor=1.0):
    """
    Applies an augmented sigmoid function - designed to have the interval (-1,1) as its image - to a DataFrame or a
    DataSeries
    :param data: DataFrame or DataSeries
    :param scaling_factor: A scaling factor proportional to the slope at x=0
    :return: A DataFrame or DataSeries obtained by applying the augmented sigmoid function elementwise in data
    """
    return 2 * ((1 / (1 + np.exp(-scaling_factor*data))) - 0.5)

def get_sharpe(excess_returns):
    """
    Returns the Sharpe Ratio of a DataSeries of Excess Returns
    :param excess_returns: DataSeries of Excess Returns
    :return: Sharpe Ratio of returns in excess_returns
    """
    return excess_returns.mean()/excess_returns.std()

def get_returns_index(total_returns):
    """
    Converts a DataSeries of daily returns to a index with initial value 1
    :param total_returns: DataSeries of Total Returns
    :return: index relative to total_returns
    """
    returns_index = (1+total_returns.fillna(0)).cumprod()
    return returns_index

def get_max_drawdown(total_returns):
    """
    Returns the maximum drawdown of a DataSeries of returns. THe maximum drawdown is the return of the interval within
    the DataSeries with the worst total return (point of largest loss relative to last peak
    :param total_returns: DataSeries of Total Returns
    :return: Maximum drawdown in total_returns
    """
    returns_index = get_returns_index(total_returns.fillna(0))
    cum_max = returns_index.cummax()

    drawdown = (returns_index - cum_max) / cum_max
    return drawdown.min()

def get_R2(benchmark_returns, total_returns):
    """
    Returns the R-squared metrics, a score of how much the variance in the Total Returns of a portfolio can be
    explained simply by the variance in the Total Returns of a given benchmark. An R-squared of 1 means perfect
    explainablility.
    :param benchmark_returns:
    :param returns:
    :return:
    """
    lm = linear_model.LinearRegression()
    data = pd.DataFrame(data={'X': benchmark_returns, 'y': total_returns}).dropna()
    X = data[['X']]
    y = data['y']
    model = lm.fit(X, y)
    R_squared = model.score(X, y)
    return R_squared

def weighted_avg(vals, weights):
    """
    Returns the weighted sum of a set of values. Negative weights have their sign taken into account when calculating
    the weighted sum, but not when calculating the sum of the weights for the denominator
    :param vals: dict of values
    :param weights: dict of weights
    :return: weighted average of values in val
    """
    weighted_sum = sum([vals[key] * weights[key] for key in vals.keys()])
    return weighted_sum / np.sum(np.abs(list(weights.values())))

def annualize(daily_rates):
    """
    Annualizes a Series or a DataFrame of daily rates
    :param daily_rates: Series or a DataFrame of daily rates
    :return: Annualized Rates
    """
    return ((1 + daily_rates) ** 365) - 1
