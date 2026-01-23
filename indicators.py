import pandas as pd
import ta


def add_indicators(df):
    """
    Add core indicators used in the strategy
    """

    df = df.copy()

    # Simple Moving Averages
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_100"] = df["close"].rolling(window=100).mean()

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(
        close=df["close"],
        window=14
    ).rsi()

    return df
