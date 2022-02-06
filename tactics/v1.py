import datetime
import time

import pyupbit
from pytz import timezone

from .helpers import get_balance
from .helpers import get_current_price
from .helpers import get_having_tickers
from .helpers import get_high_volume_tickers
from .helpers import get_kvalue
from .helpers import get_ma15
from .helpers import get_target_price


class Executor:
    def __init__(self, upbit, slackbot, except_tickers):
        self.INIT_EXCEPT_TICKERS = except_tickers
        self.except_tickers = []
        self.except_tickers += self.INIT_EXCEPT_TICKERS
        self.slackbot = slackbot
        self.upbit = upbit
        self.start_time = datetime.datetime.now().astimezone(timezone("Asia/Seoul")).replace(tzinfo=None)
        self.cycle_time = 60 * 60
        self.buy_tickers = {}
        self.under_percent = 0.05
        self.over_percent = 0.05
        self.max_budget = 20000
        self.count_tickers = 3

    def select_tickers(self):
        tickers = pyupbit.get_tickers(fiat="KRW")
        tickers = get_high_volume_tickers(tickers, count=self.count_tickers)
        tickers = [ticker for ticker, _ in tickers]
        return tickers

    def init_buy_tickers(self, tickers):
        self.buy_tickers = get_having_tickers(self.upbit, tickers, self.except_tickers)

    def _is_sell(self, current_price, ticker):
        buy_price = self.buy_tickers[ticker]
        if current_price < (buy_price * (1 - self.under_percent)) or current_price > (
            buy_price * (1 + self.over_percent)
        ):
            return True
        return False

    def _is_buy(self, current_price, target_price, ma15):
        if target_price < current_price and ma15 < current_price:
            return True
        return False

    def _process_in_cycle(self, ticker):
        try:
            current_price = get_current_price(ticker)
            if ticker in self.buy_tickers:
                if self._is_sell(current_price, ticker):
                    crypto = get_balance(self.upbit, ticker.split("-")[1])
                    result = self.upbit.sell_market_order(ticker, crypto)
                    if result is not None:
                        self.buy_tickers.pop(ticker)
                        self.except_tickers += [ticker]
                        self.slackbot.post_message(f"sell(d): {ticker} -> {crypto * current_price} won")
            else:
                k = get_kvalue(ticker)
                target_price = get_target_price(ticker, k)
                ma15 = get_ma15(ticker)
                if self._is_buy(current_price, target_price, ma15):
                    krw = self.max_budget  # min(self.max_budget, current_price)
                    if krw > 5000:
                        result = self.upbit.buy_market_order(ticker, krw * 0.9995)
                        if result is not None:
                            self.buy_tickers[ticker] = current_price
                            self.slackbot.post_message(f"buy: {ticker} -> {krw * 0.9995} won")
            time.sleep(1)
        except Exception as e:
            self.slackbot.post_message(e)
            time.sleep(1)

    def _process_out_cycle(self, ticker):
        crypto = get_balance(self.upbit, ticker.split("-")[1])
        current_price = get_current_price(ticker)
        if (crypto * current_price) > 5000:
            result = self.upbit.sell_market_order(ticker, crypto)
            if result is not None:
                self.slackbot.post_message(f"sell: {ticker} -> {crypto * current_price} won")
        time.sleep(1)

    def run(self):
        tickers = self.select_tickers()
        self.init_buy_tickers(tickers)
        start_time = datetime.datetime.now().astimezone(timezone("Asia/Seoul")).replace(tzinfo=None)
        while True:
            now = datetime.datetime.now().astimezone(timezone("Asia/Seoul")).replace(tzinfo=None)
            if now < start_time + datetime.timedelta(seconds=self.cycle_time):
                for ticker in tickers:
                    if ticker not in self.except_tickers:
                        self._process_in_cycle(ticker)

            else:
                for ticker in tickers:
                    self._process_out_cycle(ticker)
                tickers = self.select_tickers()
                self.init_buy_tickers(tickers)
                self.except_tickers = self.INIT_EXCEPT_TICKERS
                start_time = now
