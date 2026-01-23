import ccxt
import pandas as pd


def fetch_ohlcv(exchange_name, symbol, timeframe, limit=200):
    """
    Fetch OHLCV data and return a clean pandas DataFrame
    """

    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class({
        "enableRateLimit": True
    })

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    df = pd.DataFrame(
        ohlcv,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df
