import lightgbm as lgb
import numpy as np
import pyupbit

'''
from fbprophet import Prophet


def predict_price_using_prophet(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    predicted_close_price = 0
    df = pyupbit.get_ohlcv(ticker, interval="minute60")
    df = df.reset_index()
    df["ds"] = df["index"]
    df["y"] = np.log(df[1:].reset_index()["close"] / df[:-1].reset_index()["close"])
    df = df[1:-1]
    data = df[["ds", "y"]]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq="H")
    forecast = model.predict(future)
    closeDf = forecast[forecast["ds"] == forecast.iloc[-1]["ds"].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast["ds"] == data.iloc[-1]["ds"].replace(hour=9)]
    closeValue = closeDf["yhat"].values[0]
    predicted_close_price = closeValue
    return predicted_close_price
'''


def predict_price_using_lgbm(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day")
    df["VWAP"] = df["value"] / df["volume"]

    """
    x = feature_adjust(df)
    y = np.log(x[1:].reset_index()['close'] / x[:-1].reset_index()['close'])

    x = x[1:]
    """
    x = refeature(df)
    train_x = x[:-1]
    train_y = np.log(train_x[1:].reset_index()["close"] / train_x[:-1].reset_index()["close"])
    train_x = train_x[1:]

    train_x, test_x = train_x[:-1], train_x[-1:]
    train_y, test_y = train_y[:-1], train_y[-1:]
    model = get_model(train_x, train_y)
    return model.predict(test_x)[0]


def refeature(df):
    columns = ["close", "high", "low", "open", "VWAP", "volume"]

    x = df[columns].copy()

    return x


def get_model(x, y):
    lgb_params = {
        "objective": "regression",
        "n_estimators": 500,
        "num_leaves": 300,
        "learning_rate": 0.09,
        "random_seed": 2022,
    }

    model = lgb.LGBMRegressor(**lgb_params)
    model.fit(x, y)

    return model


if __name__ == "__main__":

    print(predict_price_using_lgbm("KRW-KAVA"))
