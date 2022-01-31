import time
from unittest import TestCase

from API.exchanges import Exchanger


class exchangerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exchanger = Exchanger()
        cls.test_market = "KRW-BTC"
        cls.test_market2 = "KRW-ETH"

    def setUp(self):
        time.sleep(1)

    def test_get_accounts(self):
        result = self.exchanger.get_accounts()
        self.assertNotEqual(result, None)

    def test_get_order_chance(self):
        result = self.exchanger.get_order_chance(self.test_market)
        self.assertNotEqual(result, None)

    def test_get_order_list(self):
        result = self.exchanger.get_order_list(self.test_market)
        self.assertNotEqual(result, None)
