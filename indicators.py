import pandas as pd
import numpy as np


def sma(series, length):
    return series.rolling(length).mean()


def rsi(series, length=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(length).mean()
    avg_loss = loss.rolling(length).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df["sma_20"] = sma(df["close"], 20)
    df["sma_100"] = sma(df["close"], 100)
    df["rsi"] = rsi(df["close"], 14)
    return df
