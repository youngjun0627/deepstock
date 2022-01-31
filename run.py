from API.exchanges import Exchanger
from API.quotations import Quotator

if __name__ == "__main__":
    exchanger = Exchanger()
    quotator = Quotator()
    # print(exchanger.get_order_individual())
    print(quotator.get_markets())
    # print(upbit.get_candles_per_minutes(unit=1, market="KRW-WEMIX"))
    # print(candidate_coins(upbit))
