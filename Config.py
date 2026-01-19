# =====================
# TRADER CONFIGURATION
# =====================

# Coins (memecoin futures focus)
SYMBOLS = [
    "DOGE/USDT",
    "PEPE/USDT",
    "BONK/USDT"
]

# Timeframes you trade
TIMEFRAMES = ["3m", "5m", "15m", "1h", "4h"]

# Moving averages
SMA_FAST = 20
SMA_SLOW = 100

# Volatility & squeeze
ATR_PERIOD = 14
SQUEEZE_THRESHOLD = 0.002  # how tight SMAs must be

# Risk limits (hard rules)
MAX_RISK_PER_TRADE = 0.01
MAX_TRADES_PER_SESSION = 3
MAX_CONSECUTIVE_LOSSES = 2
