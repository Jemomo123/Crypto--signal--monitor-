import ta


def add_indicators(df):
    rsi_indicator = ta.momentum.RSIIndicator(close=df["close"])
    df["rsi"] = rsi_indicator.rsi()

    macd_indicator = ta.trend.MACD(close=df["close"])
    df["macd"] = macd_indicator.macd()
    df["macd_signal"] = macd_indicator.macd_signal()

    return df
