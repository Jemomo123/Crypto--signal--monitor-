# =========================================================
# BASIC SETUP
# =========================================================

# Exchange used for data (Binance supports memecoin futures)
EXCHANGE_NAME = "binance"

# =========================================================
# SYMBOLS (WHAT YOU TRADE)
# =========================================================

# Major coins (for structure & market context)
MAJOR_SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
]

# Memecoins (your main scalping focus)
MEME_SYMBOLS = [
    "DOGE/USDT",
    "SHIB/USDT",
    "PEPE/USDT",
    "BONK/USDT",
    "FLOKI/USDT",
]

# All symbols the scanner checks
SYMBOLS = MAJOR_SYMBOLS + MEME_SYMBOLS

# =========================================================
# TIMEFRAMES
# =========================================================

# Execution timeframes (you enter here)
LOWER_TIMEFRAMES = ["3m", "5m"]

# Higher timeframe for bias confirmation
HIGHER_TIMEFRAME = "15m"

# =========================================================
# INDICATORS (CONFIRMATION ONLY)
# =========================================================

RSI_PERIOD = 14

SMA_FAST = 20
SMA_SLOW = 100

# =========================================================
# STRATEGY LOGIC SWITCHES
# =========================================================

# SQZ logic:
# - Price compresses near SMAs
# - You ONLY trade when expansion STARTS
ENABLE_SQZ_EXPANSION = True

# Crossover logic:
# - SMA 20 crosses SMA 100
# - You ONLY trade when expansion STARTS after the cross
ENABLE_CROSSOVER_EXPANSION = True

# =========================================================
# CONVICTION LEVELS (HUMAN READABLE)
# =========================================================

CONVICTION_LEVELS = [
    "A_PLUS",     # Elite: expansion + RSI + structure + elephant/tail + 15m bias + NO firewall
    "A",          # Strong: expansion + confirmations, minor friction
    "B",          # Tradable: expansion present but something is unclear
    "CAUTION",    # Mixed signals or HTF disagreement
    "WAIT",       # No expansion or rules not met
]

# =========================================================
# DASHBOARD SETTINGS
# =========================================================

# How often the dashboard refreshes (seconds)
REFRESH_SECONDS = 60
