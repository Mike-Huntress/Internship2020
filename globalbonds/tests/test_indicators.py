"""Test suite for globalbonds.indicators package."""

from unittest import TestCase
from os.path import join, dirname

from globalbonds.dataio.data_lib import DataLib
from globalbonds.indicators.signal import Signal
from globalbonds.indicators.api import yield_curve_indicator


DATA_LIB = DataLib(join(dirname(__file__), '../SignalData'))


class TestIndicators(TestCase):
    """Default Test suite for globalbonds Indicators."""

    def test_plot_signal(self):
        signal = Signal.from_ticker('BondRetIdx-LocalFX', DATA_LIB)
        signal.plot()

    def test_instantiate_signals(self):
        for ticker in DATA_LIB.list():
            Signal.from_ticker(ticker, DATA_LIB)

    def test_signal_countries(self):
        countries = ['AUS', 'DEU', 'CAN', 'ESP', 'FRA', 'ITA', 'JPN', 'NOR', 'SWE', 'CHE', 'GBR', 'USA']
        signal = Signal.from_ticker('BondRetIdx-LocalFX', DATA_LIB)
        signal_countries = signal.countries()
        for country in signal_countries:
            self.assertIn(country, countries)
        for country in countries:
            self.assertIn(country, signal_countries)

    def test_signal_at_date(self):
        signal = Signal.from_ticker('BondRetIdx-LocalFX', DATA_LIB)
        t1, t2 = signal.data_at_time('1995-01-01'), signal.data_at_time('1996-01-01')
        self.assertEqual(t1.shape[0] + 12, t2.shape[0])

    def test_yield_curve_indicator(self):
        yci = yield_curve_indicator(DATA_LIB)
        tbl = yci.get_values_at_all_times(subsample=0.01)
        self.assertEqual(tbl.shape[1], 4)
        self.assertGreater(tbl.shape[0], 20)
