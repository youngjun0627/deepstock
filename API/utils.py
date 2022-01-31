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
