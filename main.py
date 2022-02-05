import pyupbit

from slack.bot import SlackBot
from tactics.v1 import Executor
from utils import read_key


def main():
    slackbot = SlackBot()
    path = "keys.json"
    access = read_key(path)
    secret = read_key(path, key="SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)
    executor = Executor(upbit, slackbot, except_tickers=["KRW-ADA", "KRW-FLOW"])
    executor.run()


if __name__ == "__main__":
    main()
