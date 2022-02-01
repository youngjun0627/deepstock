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


def func_version1(EXCEPT_COINS, path="keys.json"):

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
                            print(f"buy: {market} -> {krw*0.9995} won")
                else:
                    crypto = get_balance(upbit, market.split("-")[1])
                    if crypto > 0.00008:
                        upbit.sell_market_order(market, crypto * 0.9995)
                        print(f"sell: {market} -> {crypto*0.9995} won")
                    markets = pyupbit.get_tickers(fiat="KRW")
                    markets = get_high_volume_tickers(markets)
                time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)
