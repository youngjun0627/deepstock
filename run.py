from API.upbitAPI import Upbit

if __name__ == "__main__":
    upbit = Upbit()
    print(upbit.get_candles_per_minutes(unit=1, market="KRW-WEMIX"))
