from slack.bot import SlackBot
from tactics.v1 import func_version1


def main():
    EXCEPT_COINS = ["KRW-FLOW", "KRW-ETH", "KRW-ADA", "KRW-MANA"]
    slackbot = SlackBot()
    func_version1(EXCEPT_COINS, slackbot)


if __name__ == "__main__":
    main()
