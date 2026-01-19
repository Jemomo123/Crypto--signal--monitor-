import streamlit as st
import ccxt
import pandas as pd
from scanner import scan_markets
from session_manager import get_trading_session
from config import SYMBOLS, TIMEFRAMES, EXCHANGE_NAME, REFRESH_SECONDS

st.set_page_config(
    page_title="Crypto Signal Dashboard",
    layout="wide"
)

st.title("📊 Crypto Market Signal Dashboard")
st.caption("Scalping first • Swing second • Plain-language signals")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    auto_refresh = st.checkbox("Auto refresh", value=True)
    st.markdown("---")
    st.write("**Exchange:**", EXCHANGE_NAME)
    st.write("**Session:**", get_trading_session())

# Exchange init
@st.cache_resource
def init_exchange():
    if EXCHANGE_NAME == "mexc":
        return ccxt.mexc({"enableRateLimit": True})
    elif EXCHANGE_NAME == "gateio":
        return ccxt.gateio({"enableRateLimit": True})
    else:
        raise ValueError("Unsupported exchange")

exchange = init_exchange()

# Auto refresh
if auto_refresh:
    st.experimental_rerun()

# Scan button
if st.button("🔍 Scan Market Now"):
    with st.spinner("Scanning markets..."):
        signals = scan_markets(
            exchange=exchange,
            symbols=SYMBOLS,
            timeframes=TIMEFRAMES
        )

        if not signals:
            st.info("No valid signals right now. Market not ready.")
        else:
            df = pd.DataFrame(signals)

            # Human-readable reasons
            df["Reason"] = df["reasons"].apply(lambda r: " • ".join(r))
            df = df.drop(columns=["reasons"])

            st.subheader(f"✅ {len(df)} Active Signals")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

# Footer
st.markdown("---")
st.caption("Signals require trend + squeeze + price action alignment")
