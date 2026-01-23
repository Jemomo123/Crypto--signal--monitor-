import pandas as pd
from config import RSI_PERIOD, SMA_FAST, SMA_SLOW


def calculate_rsi(series, period=14):
    """
    Simple RSI calculation (no external libraries)
    """
    delta = series.diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def add_indicators(df: pd.DataFrame):
    """
    Adds only what YOU trade:
    - SMA 20
    - SMA 100
    - RSI
    """
    df = df.copy()

    df["sma_20"] = df["close"].rolling(SMA_FAST).mean()
    df["sma_100"] = df["close"].rolling(SMA_SLOW).mean()

    df["rsi"] = calculate_rsi(df["close"], RSI_PERIOD)

    return df
