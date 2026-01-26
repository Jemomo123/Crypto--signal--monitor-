import pandas as pd
from data_fetcher import fetch_ohlcv
from indicators import add_indicators
from config import SYMBOLS, TIMEFRAMES


# -------------------------
# Candle classification
# -------------------------

def classify_candle(row):
    body = abs(row["close"] - row["open"])
    range_ = row["high"] - row["low"]

    if range_ == 0:
        return "none"

    body_ratio = body / range_

    if body_ratio > 0.7:
        return "elephant"
    elif body_ratio < 0.3:
        return "tail"
    else:
        return "normal"


# -------------------------
# SQZ detection
# -------------------------

def is_squeeze(df):
    last = df.iloc[-1]
    distance = abs(last["sma_20"] - last["sma_100"])
    return distance / last["close"] < 0.0015


# -------------------------
# Expansion detection
# -------------------------

def expansion_direction(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    if last["close"] > prev["close"] and last["close"] > last["sma_20"]:
        return "bullish"
    if last["close"] < prev["close"] and last["close"] < last["sma_20"]:
        return "bearish"

    return None


# -------------------------
# SMA crossover detection
# -------------------------

def sma_crossover(df):
    prev = df.iloc[-2]
    last = df.iloc[-1]

    if prev["sma_20"] < prev["sma_100"] and last["sma_20"] > last["sma_100"]:
        return "bullish"
    if prev["sma_20"] > prev["sma_100"] and last["sma_20"] < last["sma_100"]:
        return "bearish"

    return None


# -------------------------
# Higher timeframe bias
# -------------------------

def higher_tf_bias(symbol):
    df_htf = fetch_ohlcv(symbol, "15m", limit=120)
    df_htf = add_indicators(df_htf)

    last = df_htf.iloc[-1]

    if last["close"] > last["sma_20"] > last["sma_100"]:
        return "bullish"
    if last["close"] < last["sma_20"] < last["sma_100"]:
        return "bearish"

    return "neutral"


# -------------------------
# RSI position
# -------------------------

def rsi_ok(df, direction):
    rsi = df.iloc[-1]["rsi"]

    if direction == "bullish" and rsi > 50:
        return True
    if direction == "bearish" and rsi < 50:
        return True

    return False


# -------------------------
# Main scanner
# -------------------------

def scan_markets():
    results = []

    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            try:
                df = fetch_ohlcv(symbol, tf, limit=150)
                df = add_indicators(df)

                last = df.iloc[-1]
                candle_type = classify_candle(last)

                reason = []
                conviction = "WAIT"

                htf_bias = higher_tf_bias(symbol)

                # -------- SQZ logic --------
                sqz = is_squeeze(df)
                expansion = expansion_direction(df)
k
                if sqz and expansion:
                    reason.append("SQZ occurred and expansion started")

                    if candle_type in ["elephant", "tail"]:
                        reason.append(f"{candle_type} candle confirms expansion")

                        if rsi_ok(df, expansion):
                            reason.append("RSI aligned")

                            if htf_bias == expansion:
                                conviction = "A+"
                                reason.append("Higher timeframe bias aligned")
                            elif htf_bias == "neutral":
                                conviction = "A"
                                reason.append("Higher timeframe neutral")
                            else:
                                conviction = "B"
                                reason.append("Against higher timeframe")

                # -------- Crossover logic --------
                cross = sma_crossover(df)

                if cross:
                    reason.append("SMA crossover detected")

                    if candle_type in ["elephant", "tail"]:
                        reason.append(f"{candle_type} candle confirms move")

                        if rsi_ok(df, cross):
                            reason.append("RSI aligned")

                            if htf_bias == cross:
                                conviction = max(conviction, "A")
                                reason.append("Higher timeframe bias aligned")
                            else:
                                conviction = max(conviction, "B")
                                reason.append("HTF not aligned")

                if conviction != "WAIT":
                    results.append({
                        "Symbol": symbol,
                        "Timeframe": tf,
                        "Direction": expansion or cross,
                        "Conviction": conviction,
                        "Reason": " | ".join(reason)
                    })

            except Exception as e:
                print(f"Error scanning {symbol} {tf}: {e}")

    return pd.DataFrame(results)
