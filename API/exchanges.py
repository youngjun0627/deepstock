import hashlib
import uuid
from urllib.parse import urlencode

import jwt
import requests

from utils import read_key


class Exchanger(object):
    def __init__(self):
        self.BASE_URL = "https://api.upbit.com/v1/"
        self.access_key = read_key("API/keys.json")
        self.secret_key = read_key("API/keys.json", key="SECRET_KEY")

    def _create_payload(self):
        payload = {
            "access_key": self.access_key,
            "nonce": str(uuid.uuid4()),
        }
        return payload

    def _hash(self, query=None):
        payload = self._create_payload()
        if query is None:
            return payload
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload["query_hash"] = query_hash
        payload["query_hash_alg"] = "SHA512"

        return payload

    def _create_headers(self, payload):

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = "Bearer {}".format(jwt_token)
        headers = {"Authorization": authorize_token}
        return headers

    def _response(self, resp):
        if resp.status_code == 200 or resp.status_code == 201:
            return resp.json()
        else:
            return None

    def get_accounts(self):
        path = self.BASE_URL + "accounts"
        payload = self._hash()
        headers = self._create_headers(payload)

        resp = requests.get(path, headers=headers)
        return self._response(resp)

    def get_order_chance(self, market):
        path = self.BASE_URL + "orders/chance"
        query = {"market": market}
        payload = self._hash(query)
        headers = self._create_headers(payload)

        resp = requests.get(path, headers=headers, params=query)
        return self._response(resp)

    def get_order_list(self, market, state="done", page=1, order_by="asc"):
        path = self.BASE_URL + "orders"
        query = {"market": market, "state": state, "page": page, "order_by": order_by}
        payload = self._hash(query)
        headers = self._create_headers(payload)

        resp = requests.get(path, headers=headers, params=query)
        return self._response(resp)

    def get_order_individual(self, uuid):
        path = self.BASE_URL + "order"
        query = {"uuid": uuid}
        payload = self._hash(query)
        headers = self._create_headers(payload)

        resp = requests.get(path, headers=headers, params=query)
        return self._response(resp)

    def execute_order(self, market, side, volume, price, ord_type="limit"):
        path = self.BASE_URL + "order"
        query = {"market": market, "side": side, "volume": volume, "price": price, "ord_type": ord_type}
        payload = self._hash(query)
        headers = self._create_headers(payload)
        resp = requests.post(path, headers=headers, params=query)
        return self._response(resp)

    def cancel_order(self, uuid):
        path = self.BASE_URL + "order"
        query = {"uuid": uuid}
        payload = self._hash(query)
        headers = self._create_headers(payload)
        resp = requests.delete(path, headers=headers, params=query)
        return self._response(resp)
