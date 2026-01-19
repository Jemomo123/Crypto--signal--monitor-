from datetime import datetime

def get_trading_session():
    """
    Returns the current trading session based on UTC hour.
    """
    hour = datetime.utcnow().hour

    if 0 <= hour < 7:
        return "ASIA"
    elif 7 <= hour < 13:
        return "LONDON"
    elif 13 <= hour < 21:
        return "NEW_YORK"
    else:
        return "OFF_HOURS"
