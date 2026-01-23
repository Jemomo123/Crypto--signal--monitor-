import pandas as pd
from indicators import add_indicators
from config import (
    RSI_BULL_MIN,
    RSI_BEAR_MAX,
    SMA_FAST,
    SMA_SLOW,
    HIGHER_TIMEFRAME
)


# -----------------------------
# Candle classification
# -----------------------------
def candle_type(row):
    body = abs(row["close"] - row["open"])
    range_ = row["high"] - row["low"]

    if range_ == 0:
        return "neutral"

    body_ratio = body / range_

    if body_ratio > 0.6:
        return "elephant"
    elif body_ratio < 0.25:
        return "tail"
    else:
        return "normal"


# -----------------------------
# Detect SMA squeeze
# -----------------------------
def is_squeeze(df, lookback=5):
    spread = (df["sma_20"] - df["sma_100"]).abs()
    recent = spread.tail(lookback)

    return recent.max() < spread.mean()


# -----------------------------
# Detect expansion WITHOUT crossover
# -----------------------------
def expansion_without_cross(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    moving_up = last["close"] > prev["close"] and last["sma_20"] > prev["sma_20"]
    moving_down = last["close"] < prev["close"] and last["sma_20"] < prev["sma_20"]

    no_cross = (
        (prev["sma_20"] > prev["sma_100"] and last["sma_20"] > last["sma_100"]) or
        (prev["sma_20"] < prev["sma_100"] and last["sma_20"] < last["sma_100"])
    )

    return (moving_up or moving_down) and no_cross


# -----------------------------
# Detect SMA crossover expansion
# -----------------------------
def crossover_expansion(df):
    prev = df.iloc[-2]
    last = df.iloc[-1]

    bullish_cross = prev["sma_20"] < prev["sma_100"] and last["sma_20"] > last["sma_100"]
    bearish_cross = prev["sma_20"] > prev["sma_100"] and last["sma_20"] < last["sma_100"]

    return bullish_cross or bearish_cross


# -----------------------------
# Higher timeframe bias (15m)
# -----------------------------
def higher_tf_bias(htf_df):
    htf_df = add_indicators(htf_df)

    last = htf_df.iloc[-1]

    if last["sma_20"] > last["sma_100"] and last["rsi"] > 50:
        return "bullish"
    elif last["sma_20"] < last["sma_100"] and last["rsi"] < 50:
        return "bearish"
    else:
        return "neutral"


# -----------------------------
# MAIN SCANNER
# -----------------------------
def scan_markets(df, higher_tf_df):
    df = add_indicators(df)

    last = df.iloc[-1]

    direction = None
    setup = None
    conviction = "WAIT"
    reason = []

    # Candle confirmation
    candle = candle_type(last)

    # RSI positioning
    rsi_bull_ok = last["rsi"] >= RSI_BULL_MIN
    rsi_bear_ok = last["rsi"] <= RSI_BEAR_MAX

    # Higher timeframe bias
    htf_bias = higher_tf_bias(higher_tf_df)

    # -------- SQZ EXPANSION --------
    if is_squeeze(df) and expansion_without_cross(df):
        setup = "SQZ Expansion"

        if last["close"] > last["sma_20"]:
            direction = "LONG"
        else:
            direction = "SHORT"

    # -------- CROSSOVER EXPANSION --------
    elif crossover_expansion(df):
        setup = "SMA Crossover Expansion"

        if last["sma_20"] > last["sma_100"]:
            direction = "LONG"
        else:
            direction = "SHORT"

    else:
        return None

    # -------- CONFIRMATIONS --------
    if direction == "LONG":
        if not rsi_bull_ok:
            return None
        if htf_bias != "bullish":
            conviction = "B"
            reason.append("Lower TF long but 15m not aligned")
        else:
            conviction = "A"

    if direction == "SHORT":
        if not rsi_bear_ok:
            return None
        if htf_bias != "bearish":
            conviction = "B"
            reason.append("Lower TF short but 15m not aligned")
        else:
            conviction = "A"

    # Candle strength
    if candle == "elephant":
        conviction = "A+"
        reason.append("Elephant candle confirms expansion")
    elif candle == "tail":
        reason.append("Tail bar rejection confirms expansion")

    # Reason text
    reason.insert(0, f"{setup} detected")
    reason.append(f
