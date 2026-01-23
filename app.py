import streamlit as st
import pandas as pd

from data_fetcher import fetch_ohlcv
from scanner import scan_markets
from config import SYMBOLS, LOWER_TIMEFRAME, HIGHER_TIMEFRAME, EXCHANGE_NAME


st.set_page_config(page_title="SMA Expansion Scanner", layout="wide")

st.title("📈 SMA Expansion Scanner")
st.caption("SQZ Expansion & SMA Crossover — human-readable reasons")


results = []

for symbol in SYMBOLS:
    try:
        # Lower timeframe (3m / 5m)
        df_ltf = fetch_ohlcv(
            exchange_name=EXCHANGE_NAME,
            symbol=symbol,
            timeframe=LOWER_TIMEFRAME,
            limit=200
        )

        # Higher timeframe (15m bias)
        df_htf = fetch_ohlcv(
            exchange_name=EXCHANGE_NAME,
            symbol=symbol,
            timeframe=HIGHER_TIMEFRAME,
            limit=200
        )

        signal = scan_markets(df_ltf, df_htf)

        if signal:
            results.append({
                "Symbol": symbol,
                "Direction": signal["direction"],
                "Setup": signal["setup"],
                "Conviction": signal["conviction"],
                "Higher TF Bias": signal["htf_bias"],
                "Reason": " | ".join(signal["reason"])
            })

    except Exception as e:
        st.warning(f"{symbol}: {e}")


if results:
    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)
else:
    st.info("No valid expansion setups right now.")
