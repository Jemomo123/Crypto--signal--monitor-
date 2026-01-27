import ccxt
import pandas as pd
from indicators import add_indicators
from config import SYMBOLS, TIMEFRAMES, EXCHANGE_NAME

def scan_markets():
    exchange = getattr(ccxt, EXCHANGE_NAME)()

    results = []

    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=120)
                df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])

                df = add_indicators(df)

                latest = df.iloc[-1]
                prev = df.iloc[-2]

                reason = []
                direction = None
                conviction = "B"

                squeeze = abs(latest["sma20"] - latest["sma100"]) / latest["close"] < 0.002

                expanding_up = latest["close"] > latest["sma20"] > latest["sma100"]
                expanding_down = latest["close"] < latest["sma20"] < latest["sma100"]

                cross_up = prev["sma20"] < prev["sma100"] and latest["sma20"] > latest["sma100"]
                cross_down = prev["sma20"] > prev["sma100"] and latest["sma20"] < latest["sma100"]

                rsi_bull = latest["rsi"] > 50
                rsi_bear = latest["rsi"] < 50

                body = abs(latest["close"] - latest["open"])
                range_ = latest["high"] - latest["low"]

                elephant = body > range_ * 0.6
                tailbar = (
                    (latest["high"] - max(latest["close"], latest["open"])) > range_ * 0.5
                    or (min(latest["close"], latest["open"]) - latest["low"]) > range_ * 0.5
                )

                htf_ohlcv = exchange.fetch_ohlcv(symbol, timeframe="15m", limit=120)
                htf_df = pd.DataFrame(htf_ohlcv, columns=["time","open","high","low","close","volume"])
                htf_df = add_indicators(htf_df)
                htf_latest = htf_df.iloc[-1]

                htf_bull = htf_latest["sma20"] > htf_latest["sma100"]
                htf_bear = htf_latest["sma20"] < htf_latest["sma100"]

                if squeeze and expanding_up and rsi_bull and (elephant or tailbar):
                    direction = "BULLISH"
                    reason.append("SQZ → expansion up")
                    if htf_bull:
                        reason.append("HTF bullish")

                if squeeze and expanding_down and rsi_bear and (elephant or tailbar):
                    direction = "BEARISH"
                    reason.append("SQZ → expansion down")
                    if htf_bear:
                        reason.append("HTF bearish")

                if cross_up and rsi_bull and (elephant or tailbar):
                    direction = "BULLISH"
                    reason.append("SMA crossover up")
                    if htf_bull:
                        reason.append("HTF bullish")

                if cross_down and rsi_bear and (elephant or tailbar):
                    direction = "BEARISH"
                    reason.append("SMA crossover down")
                    if htf_bear:
                        reason.append("HTF bearish")

                if direction:
                    score = 0
                    if squeeze: score += 1
                    if elephant: score += 1
                    if tailbar: score += 1
                    if (direction == "BULLISH" and htf_bull) or (direction == "BEARISH" and htf_bear):
                        score += 1

                    if score >= 4:
                        conviction = "A+"
                    elif score == 3:
                        conviction = "A"

                    results.append({
                        "Symbol": symbol,
                        "Timeframe": tf,
                        "Direction": direction,
                        "Conviction": conviction,
                        "Reason": " | ".join(reason)
                    })

            except Exception as e:
                print(f"Error scanning {symbol} {tf}: {e}")

    return pd.DataFrame(results)
