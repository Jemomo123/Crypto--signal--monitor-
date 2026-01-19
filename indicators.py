import ta
import pandas as pd
from config import SMA_FAST, SMA_SLOW, ATR_PERIOD, SQUEEZE_THRESHOLD

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds technical indicators to OHLCV dataframe.
    """

    if df.empty:
        return df

    # Moving averages
    df["sma_fast"] = ta.trend.sma_indicator(df["close"], SMA_FAST)
    df["sma_slow"] = ta.trend.sma_indicator(df["close"], SMA_SLOW)

    # SMA squeeze (how close they are)
    df["sma_distance"] = abs(df["sma_fast"] - df["sma_slow"]) / df["close"]
    df["sma_squeeze"] = df["sma_distance"] < SQUEEZE_THRESHOLD

    # RSI (momentum)
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)

    # ATR (volatility, stops later)
    df["atr"] = ta.volatility.average_true_range(
        df["high"], df["low"], df["close"], window=ATR_PERIOD
    )

    return df
