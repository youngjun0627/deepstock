import time

import pyupbit


def get_high_volume_tickers(coins, count=10, interval="minute60"):
    result = []
    for coin in coins:
        volumes = (coin, pyupbit.get_ohlcv(ticker=coin, count=1, interval=interval)["value"].values[0])
        result.append(volumes)
        time.sleep(0.1)
    result.sort(key=lambda x: x[1])
    return result[-count:]


def get_kvalue(market):
    try:
        ohlck = pyupbit.get_ohlcv(ticker=market, count=20, interval="day")
        ohlck["noiseratio"] = 1 - (abs(ohlck["open"] - ohlck["close"]) / (ohlck["high"] - ohlck["low"]))
        return round(ohlck["noiseratio"].mean(), 2)
    except Exception as ex:
        print("get_kvalue() -> 에러: " + str(ex))
        return None


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


def get_having_tickers(upbit, tickers, except_tickers):
    ticker_price_dict = {}
    for ticker in tickers:
        time.sleep(1)
        if ticker in except_tickers:
            continue
        ticker_name = ticker.split("-")[1]
        balance = get_balance(upbit, ticker_name)
        if balance != 0:
            avg_buy_price = upbit.get_avg_buy_price(ticker_name)
            ticker_price_dict[ticker] = avg_buy_price
    return ticker_price_dict
