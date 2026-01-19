from data_fetcher import fetch_ohlcv
from indicators import add_indicators
from signal_engine import generate_signal


def scan_markets(exchange, symbols, timeframes, limit=200):
    """
    Scans multiple symbols and timeframes.
    Returns a list of signal dictionaries.
    """

    signals = []

    for symbol in symbols:
        for tf in timeframes:
            try:
                df = fetch_ohlcv(exchange, symbol, tf, limit)

                if df is None or df.empty:
                    continue

                df = add_indicators(df)

                signal = generate_signal(df, symbol, tf)

                if signal:
                    signals.append(signal)

            except Exception:
                # We fail silently to avoid stopping the scan
                continue

    return signals
