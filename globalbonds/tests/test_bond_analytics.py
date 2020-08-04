"""Test suite for bond analytics functions."""

from unittest import TestCase

from globalbonds.bond_analytics.api import (
    get_zero_rates,
    get_forward_rates,
    get_yield_to_maturity,
    get_bond_price_from_ytm,
    get_bond_price_from_zero_rates,
)


class TestBondAnalytics(TestCase):
    """Test suite for bond analytics."""

    def test_get_zero_rates_1(self):
        prices = [101.96, 102.91]
        coupon = 0.04
        zrs = get_zero_rates(prices, coupon)
        self.assertEqual(len(zrs), 2)
        self.assertAlmostEqual(zrs[0], 0.02, places=4)
        self.assertAlmostEqual(zrs[1], 0.025, places=4)

    def test_get_zero_rates_2(self):
        prices = [98.04, 95.18, 91.52, 87.58, 83.41]
        coupon = 0
        zrs = get_zero_rates(prices, coupon)
        self.assertEqual(len(zrs), 5)
        self.assertAlmostEqual(zrs[0], 0.02, places=4)
        self.assertAlmostEqual(zrs[1], 0.025, places=4)
        self.assertAlmostEqual(zrs[2], 0.03, places=4)
        self.assertAlmostEqual(zrs[3], 0.0337, places=4)
        self.assertAlmostEqual(zrs[4], 0.0369, places=4)

    def test_get_zero_rates_3(self):
        prices = [101.96, 102.91, 102.91, 102.47, 101.64]
        coupon = 0.04
        zrs = get_zero_rates(prices, coupon)
        self.assertEqual(len(zrs), 5)
        self.assertAlmostEqual(zrs[0], 0.019992, places=4)
        self.assertAlmostEqual(zrs[1], 0.025, places=4)
        self.assertAlmostEqual(zrs[2], 0.03, places=2)
        self.assertAlmostEqual(zrs[3], 0.0337, places=2)
        self.assertAlmostEqual(zrs[4], 0.0369, places=2)

    def test_get_zero_rates_high_principal(self):
        prices = [1019.6, 1029.1]
        coupon = 0.04
        zrs = get_zero_rates(prices, coupon, principal=1000)
        self.assertEqual(len(zrs), 2)
        self.assertAlmostEqual(zrs[0], 0.02, places=4)
        self.assertAlmostEqual(zrs[1], 0.025, places=4)

    def test_get_yield_to_maturity(self):
        periods, price, coupon = 2, 102.91, 0.04
        ytm = get_yield_to_maturity(periods, price, coupon)
        self.assertAlmostEqual(ytm, 0.0249, places=4)

    def test_get_yield_to_maturity_high_principal(self):
        periods, price, coupon = 2, 1029.1, 0.04
        ytm = get_yield_to_maturity(periods, price, coupon, principal=1000)
        self.assertAlmostEqual(ytm, 0.0249, places=4)

    def test_get_bond_price(self):
        price = get_bond_price_from_ytm(2, 0.0249, 0.04)
        self.assertAlmostEqual(price, 102.91, places=2)

    def test_get_forward_rates_1(self):
        prices = [101.96, 102.91, 102.91, 102.47, 101.64]
        coupon = 0.04
        frs = get_forward_rates(prices, coupon)
        self.assertEqual(len(frs), 5)
        self.assertAlmostEqual(frs[0], 0.02, places=4)
        self.assertAlmostEqual(frs[1], 0.03, places=4)
        self.assertAlmostEqual(frs[2], 0.041, places=2)
        self.assertAlmostEqual(frs[3], 0.048, places=2)
        self.assertAlmostEqual(frs[4], 0.055, places=2)

    def test_get_forward_rates_2(self):
        zrs = [0.019992, 0.025, 0.03, 0.0337, 0.0369]
        prices = [101.96, 102.91, 102.91, 102.47, 101.64]
        coupon = 0.04
        frs = get_forward_rates(prices, coupon, zrs=zrs)
        print(frs)
        self.assertEqual(len(frs), 5)
        self.assertAlmostEqual(frs[0], 0.02, places=4)
        self.assertAlmostEqual(frs[1], 0.03, places=4)
        self.assertAlmostEqual(frs[2], 0.04, places=2)
        self.assertAlmostEqual(frs[3], 0.045, places=2)
        self.assertAlmostEqual(frs[4], 0.05, places=2)

    def test_get_bond_price_from_zrs(self):
        zrs = [0.019992, 0.025, 0.03, 0.0337]
        coupon = 0.03
        price = get_bond_price_from_zero_rates(zrs, coupon)
        self.assertAlmostEqual(price, 98.75, places=2)