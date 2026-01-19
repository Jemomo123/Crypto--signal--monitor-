from price_action import price_action_signal

def generate_signal(df, symbol, timeframe):
    """
    Evaluates the most recent candle and decides if a signal exists.
    Returns None or a signal dictionary.
    """

    if len(df) < 5:
        return None

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # Trend bias
    bullish_bias = latest["sma_fast"] > latest["sma_slow"]
    bearish_bias = latest["sma_fast"] < latest["sma_slow"]

    # Squeeze condition
    squeeze = latest["sma_squeeze"]

    # Price action
    pa = price_action_signal(latest)

    pa_valid = pa["elephant"] or pa["tail"] is not None

    if not squeeze or not pa_valid:
        return None

    # Direction alignment
    if bullish_bias and pa["direction"] != "bullish":
        return None
    if bearish_bias and pa["direction"] != "bearish":
        return None

    direction = "LONG" if bullish_bias else "SHORT"

    reasons = []

    reasons.append(
        "Fast SMA is above slow SMA" if bullish_bias else "Fast SMA is below slow SMA"
    )

    reasons.append("Moving averages were compressed (squeeze)")

    if pa["elephant"]:
        reasons.append("Strong momentum candle (elephant bar)")
    if pa["tail"]:
        reasons.append(f"Clear rejection shown by {pa['tail']} tail bar")

    reasons.append("Candle direction agrees with trend")

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "direction": direction,
        "price": latest["close"],
        "reasons": reasons
    }
