import ccxt
import pandas as pd

# Initialize exchange (MEXC)
exchange = ccxt.mexc({
    "enableRateLimit": True,
})

def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 200) -> pd.DataFrame:
    """
    Fetch OHLCV data for a symbol and timeframe.
    Returns a pandas DataFrame.
    """
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

        df = pd.DataFrame(
            ohlcv,
            columns=["timestamp", "open", "high", "low", "close", "volume"]
        )

        # Convert timestamp to readable time (optional, useful later)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        return df

    except Exception as e:
        print(f"Error fetching {symbol} {timeframe}: {e}")
        return pd.DataFrame()
