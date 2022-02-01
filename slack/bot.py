from datetime import datetime

import requests

from utils import read_key


def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)


token = read_key("keys.json", key="SLACK_TOKEN")


class SlackBot(object):
    def __init__(self, key_path="keys.json", channel="test"):
        self.token = read_key(key_path, key="SLACK_TOKEN")
        self.channel = channel

    def post_message(self, msg):
        url = "https://slack.com/api/chat.postMessage"

        text = f"{datetime.now().strftime('[%m/%d %H:%M:%S]')} {msg}"
        response = requests.post(
            url, headers={"Authorization": "Bearer " + self.token}, data={"channel": self.channel, "text": text}
        )
        if response.status_code != 200:
            print(response)
