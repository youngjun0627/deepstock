import time
from unittest import TestCase

from API.quotations import Quotator


class QuotatorTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.quotator = Quotator()
        cls.test_market = "KRW-BTC"
        cls.test_market2 = "KRW-ETH"

    def setUp(self):
        time.sleep(1)

    def test_get_market(self):
        result = self.quotator.get_markets()
        self.assertNotEqual(result, None)

    def test_get_candles_per_minutes(self):
        for minute in [1, 3, 5, 15, 10, 30, 60, 240]:
            with self.subTest(minute=minute):
                result = self.quotator.get_candles_per_minutes(minute, self.test_market)
                self.assertNotEqual(result, None)

    def test_get_candles_daily(self):
        result = self.quotator.get_candles_daily(self.test_market)
        self.assertNotEqual(result, None)

    def test_get_candles_weekly(self):
        result = self.quotator.get_candles_weekly(self.test_market)
        self.assertNotEqual(result, None)

    def test_get_candles_monthly(self):
        result = self.quotator.get_candles_monthly(self.test_market)
        self.assertNotEqual(result, None)

    def test_get_trading_history(self):
        result = self.quotator.get_trading_history(self.test_market)
        self.assertNotEqual(result, None)

    def test_get_ticker(self):
        result = self.quotator.get_ticker([self.test_market, self.test_market2])
        self.assertNotEqual(result, None)
