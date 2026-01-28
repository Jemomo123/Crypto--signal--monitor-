import pandas as pd
import ta


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # === SMAs ===
    df["sma_20"] = df["close"].rolling(20).mean()
    df["sma_100"] = df["close"].rolling(100).mean()

    # === RSI ===
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()

    # === SQZ LOGIC ===
    bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    kc = ta.volatility.KeltnerChannel(close=df["close"], window=20)

    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["kc_upper"] = kc.keltner_channel_hband()
    df["kc_lower"] = kc.keltner_channel_lband()

    df["squeeze"] = (df["bb_lower"] > df["kc_lower"]) & (df["bb_upper"] < df["kc_upper"])

    return df
