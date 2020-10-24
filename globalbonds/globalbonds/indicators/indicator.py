
import pandas as pd

from random import random

from .combiners import Combiner


class Indicator:
    """Base class to represent an indicator.

    A single time series summarizing several signals.
    """
    metrics = {
        'mean': Combiner.mean_value,
        'median': Combiner.median_value,
        'mean_first_deriv': Combiner.mean_first_derivative,
        'median_first_deriv': Combiner.median_first_derivative,
    }

    def __init__(self, name, *signals):
        self._signals = signals

    def get_values_at_all_times(self, subsample=1):
        all_vals = pd.concat([
            self.get_values(date) for date in self.dates()
            if random() < subsample
        ])
        return all_vals

    def get_values(self, date):
        """Return a longform DataFrame with values representing this indicator for each country.

        Should be < 10 values. Values can include
         - derivatives
         - diagnostic values
         - different averages
        """
        wide = pd.DataFrame({
            metric_name: self._combine_signals(metric, date)
            for metric_name, metric in self.metrics.items()
        }).T
        wide['metric'] = wide.index.to_series()
        longform = wide.melt(id_vars='metric')
        longform['date'] = date
        return longform

    def dates(self):
        """Return dates where this indicator can be calculated.

        TODO make better
        """
        return self._signals[0].dates()

    def countries(self):
        """Return a set of countries this indicator is valid for."""
        countries = self._signals[0].countries()
        for signal in self._signals[1:]:
            countries &= signal.countries()
        return countries

    def _combine_signals(self, combiner, date):
        """Return a Series of combined values by country.

        Combiner is a function that takes a DataFrame for all signals
        from one country and returns a single number.
        """
        combined = {}
        for country in self.countries():
            country_tbl = pd.DataFrame({
                signal.name: signal.data_at_time(date)[country]
                for signal in self._signals
            })
            combined[country] = combiner(country_tbl)
        combined = pd.Series(combined)
        return combined
