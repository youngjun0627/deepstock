import json


def read_key(path, key="ACCESS_KEY"):
    with open(path, "r") as f:

        data = json.loads(f.read())
        try:
            key = data[key]
        except KeyError as e:
            raise KeyError(e)
        else:
            return key


def candidate_coins(upbit, selected_coins=None):
    if selected_coins is not None:
        return map(lambda x: "KRW-{0}".format(x), selected_coins)
    candidate_coin = map(lambda x: x["market"], upbit.get_markets())
    return filter(lambda x: x.startswith("KRW"), candidate_coin)
