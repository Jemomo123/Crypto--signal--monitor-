import pandas as pd

def detect_elephant_bar(row, atr_multiplier=1.2):
    """
    Elephant bar:
    - Large range relative to ATR
    - Strong body (not lots of wicks)
    """
    candle_range = row["high"] - row["low"]
    body = abs(row["close"] - row["open"])

    if pd.isna(row["atr"]):
        return False

    large_range = candle_range > row["atr"] * atr_multiplier
    strong_body = body > candle_range * 0.6

    return large_range and strong_body


def detect_tail_bar(row, tail_ratio=2.0):
    """
    Tail bar:
    - Long wick showing rejection
    """
    body = abs(row["close"] - row["open"])
    upper_wick = row["high"] - max(row["close"], row["open"])
    lower_wick = min(row["close"], row["open"]) - row["low"]

    # Bullish rejection (long lower wick)
    if lower_wick > body * tail_ratio:
        return "bullish"

    # Bearish rejection (long upper wick)
    if upper_wick > body * tail_ratio:
        return "bearish"

    return None


def price_action_signal(row):
    """
    Returns a dictionary describing candle behavior.
    """
    elephant = detect_elephant_bar(row)
    tail = detect_tail_bar(row)

    direction = None
    if row["close"] > row["open"]:
        direction = "bullish"
    elif row["close"] < row["open"]:
        direction = "bearish"

    return {
        "elephant": elephant,
        "tail": tail,
        "direction": direction
    }
