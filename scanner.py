import pandas as pd
from data_fetcher import fetch_ohlcv
from indicators import add_indicators
from config import SYMBOLS, TIMEFRAMES, EXCHANGE_NAME


def higher_tf_bias(symbol):
    df = fetch_ohlcv(symbol, timeframe="15m", limit=120)
    df = add_indicators(df)

    if df["close"].iloc[-1] > df["sma_20"].iloc[-1] > df["sma_100"].iloc[-1]:
        return "BULLISH"
    if df["close"].iloc[-1] < df["sma_20"].iloc[-1] < df["sma_100"].iloc[-1]:
        return "BEARISH"
    return "NEUTRAL"


def is_elephant_bar(df):
    body = abs(df["close"].iloc[-1] - df["open"].iloc[-1])
    avg_body = abs(df["close"] - df["open"]).rolling(20).mean().iloc[-1]
    return body > 1.5 * avg_body


def is_tail_bar(df):
    high = df["high"].iloc[-1]
    low = df["low"].iloc[-1]
    open_ = df["open"].iloc[-1]
    close = df["close"].iloc[-1]

    upper_wick = high - max(open_, close)
    lower_wick = min(open_, close) - low
    body = abs(close - open_)

    return upper_wick > body * 2 or lower_wick > body * 2


def detect_expansion(df):
    dist_now = abs(df["close"].iloc[-1] - df["sma_20"].iloc[-1])
    dist_prev = abs(df["close"].iloc[-2] - df["sma_20"].iloc[-2])
    return dist_now > dist_prev


def scan_markets():
    results = []

    for symbol in SYMBOLS:
        try:
            bias_15m = higher_tf_bias(symbol)

            for tf in TIMEFRAMES:
                df = fetch_ohlcv(symbol, tf)
                df = add_indicators(df)

                last = df.iloc[-1]
                prev = df.iloc[-2]

                reason = []
                direction = None
                conviction = "WAIT"

                # === SQZ EXPANSION (independent) ===
                if prev["squeeze"] and detect_expansion(df):
                    if last["close"] > last["sma_20"]:
                        direction = "LONG"
                    elif last["close"] < last["sma_20"]:
                        direction = "SHORT"

                    if direction:
                        reason.append("SQZ expansion")

                # === SMA CROSSOVER EXPANSION (independent) ===
                crossed_up = prev["sma_20"] < prev["sma_100"] and last["sma_20"] > last["sma_100"]
                crossed_down = prev["sma_20"] > prev["sma_100"] and last["sma_20"] < last["sma_100"]

                if crossed_up or crossed_down:
                    direction = "LONG" if crossed_up else "SHORT"
                    reason.append("SMA crossover")

                if not direction:
                    continue

                # === CONFIRMATIONS ===
                if detect_expansion(df):
                    reason.append("Price expanding from SMAs")

                if is_elephant_bar(df):
                    reason.append("Elephant bar")
                elif is_tail_bar(df):
                    reason.append("Tail bar")

                if direction == "LONG" and last["rsi"] > 50:
                    reason.append("RSI supportive")
                if direction == "SHORT" and last["rsi"] < 50:
                    reason.append("RSI supportive")

                if (direction == "LONG" and bias_15m == "BULLISH") or (
                    direction == "SHORT" and bias_15m == "BEARISH"
                ):
                    reason.append("15m bias aligned")

                # === CONVICTION LOGIC ===
                score = len(reason)

                if score >= 5:
                    conviction = "A+"
                elif score == 4:
                    conviction = "A"
                elif score == 3:
                    conviction = "B"
                else:
                    conviction = "WAIT"

                results.append({
                    "Symbol": symbol,
                    "Timeframe": tf,
                    "Direction": direction,
                    "Conviction": conviction,
                    "Reason": ", ".join(reason),
                    "15m Bias": bias_15m
                })

        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    return pd.DataFrame(results)
