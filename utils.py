import json
import time

import pyupbit


def read_key(path, key="ACCESS_KEY"):
    with open(path, "r") as f:

        data = json.loads(f.read())
        try:
            key = data[key]
        except KeyError as e:
            raise KeyError(e)
        else:
            return key


def get_high_volume_tickers(coins, count=10, interval="minute60"):
    result = []
    for coin in coins:
        volumes = (coin, pyupbit.get_ohlcv(ticker=coin, count=1, interval=interval)["value"].values[0])
        result.append(volumes)
        time.sleep(0.1)
    result.sort(key=lambda x: x[1])
    return result[-count:]


def get_kvalue(market):  # 인자로 받은 종목에 대한 20일 average noise ratio.
    try:
        ohlck = pyupbit.get_ohlcv(ticker=market, count=20, interval="day")
        ohlck["noiseratio"] = 1 - (abs(ohlck["open"] - ohlck["close"]) / (ohlck["high"] - ohlck["low"]))
        return round(ohlck["noiseratio"].mean(), 2)
    except Exception as ex:
        print("get_kvalue() -> 에러: " + str(ex))
        return None
