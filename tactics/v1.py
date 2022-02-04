import datetime
import time

import pyupbit
from pytz import timezone

from utils import get_high_volume_tickers
from utils import get_kvalue
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

    except_coins = []
    except_coins += EXCEPT_COINS
    buy_prices = {}
    markets = pyupbit.get_tickers(fiat="KRW")
    markets = get_high_volume_tickers(markets, count=5)
    access = read_key(path)
    secret = read_key(path, key="SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)
    for market, _ in markets:
        if market in except_coins:
            continue
        balance = get_balance(upbit, market.split("-")[1])
        if balance != 0:
            avg_buy_price = upbit.get_avg_buy_price(market.split("-")[1])
            buy_prices[market] = avg_buy_price
    start_time = datetime.datetime.now().astimezone(timezone("Asia/Seoul")).replace(tzinfo=None)

    while True:
        for market, _ in markets:
            if market in except_coins:
                continue
            time.sleep(1)
            try:
                now = datetime.datetime.now().astimezone(timezone("Asia/Seoul")).replace(tzinfo=None)
                if now < start_time + datetime.timedelta(seconds=60 * 60):
                    current_price = get_current_price(market)
                    if market in buy_prices:
                        if current_price < (buy_prices[market] * 0.95) or current_price > (buy_prices[market] * 1.05):
                            crypto = get_balance(upbit, market.split("-")[1])
                            result = upbit.sell_market_order(market, crypto)
                            if result is not None:
                                buy_prices.pop(market)
                                except_coins += [market]
                                slackbot.post_message(f"sell(d): {market} -> {crypto} won")
                        continue
                    k = get_kvalue(market)
                    target_price = get_target_price(market, k)
                    ma15 = get_ma15(market)
                    if target_price < current_price and ma15 < current_price:
                        krw = min(10000, get_balance(upbit, "KRW"))
                        if krw > 5000:
                            result = upbit.buy_market_order(market, krw * 0.9995)
                            if result is not None:
                                buy_prices[market] = current_price
                                slackbot.post_message(f"buy: {market} -> {krw * 0.9995} won")

                else:
                    buy_markets = list(buy_prices.keys())
                    for market in buy_markets:
                        crypto = get_balance(upbit, market.split("-")[1])
                        if (crypto * get_current_price(market)) > 5000:
                            result = upbit.sell_market_order(market, crypto)
                            if result is not None:
                                buy_prices.pop(market)
                                slackbot.post_message(f"sell: {market} -> {crypto} won")
                    markets = pyupbit.get_tickers(fiat="KRW")
                    markets = get_high_volume_tickers(markets, count=5)
                    start_time = now
                    except_coins = EXCEPT_COINS
            except Exception as e:
                slackbot.post_message(e)
                time.sleep(1)
