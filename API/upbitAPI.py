import hashlib
import uuid
from urllib.parse import urlencode

import jwt
import requests

from .utils import read_key

PROTOCOL = "https"
HOST = "api.upbit.com"
VERSION = "v1"


class Upbit(object):
    def __init__(self, key_path="API/keys.json"):
        self.host_url = f"{PROTOCOL}://{HOST}/{VERSION}".format(PROTOCOL, HOST, VERSION)
        self.access_key = read_key(key_path)
        self.secret_key = read_key(key_path, key="SECRET_KEY")

    def _fetch(self, authorization=False, path=None, method="get", query=None):
        headers = {"format": "applications/json"}
        url = f"{self.host_url}/{path}"
        if authorization:
            payload = {
                "access_key": self.access_key,
                "nonce": str(uuid.uuid4()),
            }
            if query is not None:
                query_string = urlencode(query).encode()

                m = hashlib.sha512()
                m.update(query_string)
                query_hash = m.hexdigest()

                payload["query_hash"] = query_hash
                payload["query_hash_alg"] = "SHA512"

            jwt_token = jwt.encode(payload, self.secret_key)
            authorize_token = "Bearer {}".format(jwt_token)
            headers = {"Authorization": authorize_token}
        if method == "get":
            resp = requests.get(url=url, headers=headers, params=query)
        elif method == "post":
            resp = requests.post(url=url, headers=headers, params=query)
        elif method == "delete":
            resp = requests.delete(url=url, headers=headers, params=query)
        return resp.json() if resp.status_code == 200 or resp.status_code == 201 else None

    def get_markets(self):
        return self._fetch(path="market/all", method="get")

    def get_candles_per_minutes(self, unit, market, to="", count=1, cursor=0):
        # minute -> one of [1, 3, 5, 15, 10, 30, 60, 240]

        params = {"market": market, "to": to, "count": count, "cursor": cursor}
        return self._fetch(path=f"candles/minutes/{unit}", method="get", query=params)

    def get_candles_daily(self, market, to="", count=1):
        params = {"market": market, "to": to, "count": count}
        return self._fetch(path="candles/days", method="get", query=params)

    def get_candles_weekly(self, market, to="", count=1):
        params = {"market": market, "to": to, "count": count}
        return self._fetch(path="candles/weeks", method="get", query=params)

    def get_candles_monthly(self, market, to="", count=1):
        params = {"market": market, "to": to, "count": count}
        return self._fetch(path="candles/months", method="get", query=params)

    def get_trading_history(self, market, to="", count=1, cursor=""):
        params = {"market": market, "to": to, "count": count, "cursor": cursor}
        return self._fetch(path="trades/ticks", method="get", query=params)

    def get_ticker(self, markets):
        params = {"markets": markets}
        return self._fetch(path="ticker", method="get", query=params)

    def get_accounts(self):
        return self._fetch(authorization=True, path="accounts", method="get")

    def get_order_chance(self, market):
        params = urlencode({"market": market})
        return self._fetch(authorization=True, path="orders/chance", method="get", query=params)

    def get_order_list(self, market, state="wait", page=1, order_by="asc"):
        params = urlencode({"market": market, "state": state, "page": page, "order_by": order_by})
        return self._fetch(authorization=True, path="orders", method="get", query=params)

    def get_order(self, uuid):
        params = urlencode({"uuid": uuid})
        return self._fetch(authorization=True, path="order", method="get", query=params)

    def place_order(self, market, side, volume, price, ord_type="limit"):
        params = urlencode({"market": market, "side": side, "volume": volume, "price": price, "ord_type": ord_type})
        return self._fetch(authorization=True, path="orders", method="post", query=params)

    def cancel_order(self, uuid):
        params = urlencode({"uuid": uuid})
        return self._fetch(authorization=True, path="order", method="delete", query=params)

    def get_withdraw_list(self, currency, state, limit=100):
        params = urlencode({"currency": currency, "state": state, "limit": limit})
        return self._fetch(authorization=True, path="withdraws", method="get", query=params)

    def get_withdraw(self, uuid):
        params = urlencode({"uuid": uuid})
        return self._fetch(authorization=True, path="withdraw", method="get", query=params)

    def get_withdraw_chance(self, currency):
        params = urlencode({"currency": currency})
        return self._fetch(authorization=True, path="withdraws/chance", method="get", query=params)

    def withdraw_crypto(self, currency, amount, address):
        params = urlencode({"currency": currency, "amount": amount, "address": address})
        return self._fetch(authorization=True, path="withdraws/coin", method="post", query=params)

    def withdraw_krw(self, amount):
        params = urlencode({"amount": amount})
        return self._fetch(authorization=True, path="withdraws/krw", method="post", query=params)
