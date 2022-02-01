import datetime
import time

import pyupbit

from utils import get_high_volume_tickers
from utils import read_key


def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]["close"] + (df.iloc[0]["high"] - df.iloc[0]["low"]) * k
    return target_price


def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df["close"].rolling(15).mean().iloc[-1]
    return ma15


def get_balance(upbit, ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b["currency"] == ticker:
            if b["balance"] is not None:
                return float(b["balance"])
            else:
                return 0
    return 0


def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


def func_version1(EXCEPT_COINS, slackbot, path="keys.json"):

    buy_dict = {}
    markets = pyupbit.get_tickers(fiat="KRW")
    markets = get_high_volume_tickers(markets)

    access = read_key(path)
    secret = read_key(path, key="SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)

    while True:
        for market, _ in markets:
            if market in EXCEPT_COINS:
                continue
            try:
                now = datetime.datetime.now()
                start_time = get_start_time(market)
                end_time = start_time + datetime.timedelta(days=1)

                if start_time < now < end_time - datetime.timedelta(seconds=10):
                    target_price = get_target_price(market, 0.5)
                    ma15 = get_ma15(market)
                    current_price = get_current_price(market)
                    if target_price < current_price and ma15 < current_price:
                        krw = get_balance(upbit, "KRW")
                        if krw > 5000:
                            upbit.buy_market_order(market, krw * 0.9995)
                            slackbot.post_message(f"buy: {market} -> {krw * 0.9995} won")
                            buy_dict[market] = krw * 0.9995
                    if market in buy_dict:
                        if current_price < (buy_dict[market] * 0.95):
                            upbit.sell_market_order(market, current_price)
                            slackbot.post_message(f"sell(d): {market} -> {current_price} won")

                else:
                    crypto = get_balance(upbit, market.split("-")[1])
                    crypto = get_current_price(market) * crypto
                    if crypto > 5000:
                        upbit.sell_market_order(market, crypto)
                        slackbot.post_message(f"sell: {market} -> {crypto} won")
                    markets = pyupbit.get_tickers(fiat="KRW")
                    markets = get_high_volume_tickers(markets)
                time.sleep(1.5)
            except Exception as e:
                slackbot.post_message(e)
                print(e)
                time.sleep(1.5)
