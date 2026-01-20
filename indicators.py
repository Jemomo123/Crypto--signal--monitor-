import numpy as np

def sma(values, period):
    if len(values) < period:
        return None
    return np.mean(values[-period:])

def add_indicators(ohlcv):
    """
    ohlcv format:
    [timestamp, open, high, low, close, volume]
    """

    closes = [c[4] for c in ohlcv]

    sma20 = sma(closes, 20)
    sma100 = sma(closes, 100)

    if sma20 is None or sma100 is None:
        return None

    squeeze = abs(sma20 - sma100) / sma100 < 0.002  # 0.2%
