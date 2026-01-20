import ccxt
import time

exchanges = {
    "mexc": ccxt.mexc(),
    "gate": ccxt.gate()
}

def fetch_ohlcv(exchange_name, symbol, timeframe, limit=200):
    exchange = exchanges.get(exchange_name)

    if not exchange:
        return []

    try:
        exchange.load_markets()
        data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        time.sleep(exchange.rateLimit / 1000)
        return data
    except Exception as e:
        return []
