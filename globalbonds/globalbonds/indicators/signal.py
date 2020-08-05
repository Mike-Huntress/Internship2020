
import pandas as pd

from .timeseries_set import TimeSeriesSet
from .normalization import center_scale_using_historical_rolling


class Signal(TimeSeriesSet):
    """Base class to represent a signal or raw data as input to the model."""

    def __init__(self, name, data_tbl, normalizer=center_scale_using_historical_rolling):
        self.name = name
        self.raw = data_tbl
        self.data = normalizer(self.raw)
        self.tbl = self.data

    def countries(self):
        """Return a list of countries."""
        return set(self.data.columns)

    def dates(self):
        dates = self.data.index.to_series().map(lambda x: x.to_timestamp())
        return dates

    def data_at_time(self, date):
        """Return a timeseries as would have been available at `date`.

        Include `date` (if present).
        """
        dates = self.dates()
        mask = dates <= date
        before_or_on_date = self.data.loc[mask]
        return before_or_on_date

    @classmethod
    def from_ticker(cls, ticker, data_lib, normalizer=center_scale_using_historical_rolling):
        raw_tbl = data_lib.pull(ticker)
        return cls(ticker, raw_tbl, normalizer=normalizer)
