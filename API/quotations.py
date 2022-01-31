import requests

from utils import read_key


class Quotator(object):
    def __init__(self):
        self.BASE_URL = "https://api.upbit.com/v1/"
        self.access_key = read_key("API/keys.json")
        self.secret_key = read_key("API/keys.json", key="SECRET_KEY")

    def _response(self, resp):
        if resp.status_code == 200 or resp.status_code == 201:
            return resp.json()
        else:
            print(resp.status_code)
            return None

    def get_markets(self):
        path = self.BASE_URL + "market/all"
        resp = requests.get(path)
        return self._response(resp)

    def get_candles_per_minutes(self, minute, market, to="", count=1, cursor=0):
        # minute is one of list [1, 3, 5, 15, 10, 30, 60, 240]
        path = self.BASE_URL + f"candles/minutes/{minute}"
        query = {"market": market, "to": to, "count": count, "cursor": cursor}
        resp = requests.get(path, params=query)
        return self._response(resp)

    def get_candles_daily(self, market, to="", count=1):
        path = self.BASE_URL + "candles/days"
        query = {"market": market, "to": to, "count": count}
        resp = requests.get(path, params=query)
        return self._response(resp)

    def get_candles_weekly(self, market, to="", count=1):
        path = self.BASE_URL + "candles/weeks"
        query = {"market": market, "to": to, "count": count}
        resp = requests.get(path, params=query)
        return self._response(resp)

    def get_candles_monthly(self, market, to="", count=1):
        path = self.BASE_URL + "candles/months"
        query = {"market": market, "to": to, "count": count}
        resp = requests.get(path, params=query)
        return self._response(resp)

    def get_trading_history(self, market, to="", count=1, cursor=""):
        path = self.BASE_URL + "trades/ticks"
        query = {"market": market, "to": to, "count": count, "cursor": cursor}
        resp = requests.get(path, params=query)
        return self._response(resp)

    def get_ticker(self, markets):

        path = self.BASE_URL + "ticker"
        query = {"markets": markets}
        resp = requests.get(path, params=query)
        return self._response(resp)
