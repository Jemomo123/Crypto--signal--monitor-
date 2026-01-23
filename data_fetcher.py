import ccxt
import pandas as pd
from config import EXCHANGE_NAME


def get_exchange():
    """
    Connect to the exchange defined in config.py
    """
    exchange_class = getattr(ccxt, EXCHANGE_NAME)
    exchange = exchange_class({
        "enableRateLimit": True,
        "options": {
            "defaultType": "future"  # futures for memecoin trading
        }
    })
    return exchange


def fetch_ohlcv(symbol, timeframe, limit=200):
    """
    Fetch OHLCV data and return a clean DataFrame
    """
    exchange = get_exchange()

    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except Exception as e:
        print(f"Error fetching {symbol} {timeframe}: {e}")
        return None

    df = pd.DataFrame(
        ohlcv,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df
