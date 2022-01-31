import json
import pyupbit
import time

def read_key(path, key="ACCESS_KEY"):
    with open(path, "r") as f:

        data = json.loads(f.read())
        try:
            key = data[key]
        except KeyError as e:
            raise KeyError(e)
        else:
            return key


def get_high_volume_tickers(coins, count=10):
    result = []
    for coin in coins:
        volumes = (coin, pyupbit.get_ohlcv(ticker=coin, count=1, interval='minute1')['value'].values[0])
        result.append(volumes)
        time.sleep(0.1)

    result.sort(key=lambda x:x[1])
    return result[-count:]
