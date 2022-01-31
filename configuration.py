import os

BASE_DIR = "."
config = dict()
config["key_path"] = os.path.join(BASE_DIR, "API/keys.json")
config["selected_coins"] = [
    "BTC",
    "ETH",
    "XRP",
]
config["grow_period"] = 5
config["max_betting"] = 10000
config["max_num_coins"] = 4
config["spread_gap"] = 0.002
