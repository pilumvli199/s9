import pandas as pd
import requests
from io import StringIO
from alerts.telegram_bot import send_alert, send_error_alert

# ✅ Upstox instruments CSV (public link)
INSTRUMENTS_URL = "https://assets.upstox.com/market-quote/instruments/upstox_instruments.csv"


def get_master_instruments(symbol: str):
    """
    Fetch master instruments from Upstox CSV and filter by trading_symbol
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; StockBot/1.0)"}
        r = requests.get(INSTRUMENTS_URL, headers=headers, timeout=30)
        r.raise_for_status()

        # CSV pandas मध्ये load करा
        df = pd.read_csv(StringIO(r.text))

        # ✅ Flexible match: RELIANCE → RELIANCE-EQ, NIFTY50 → NIFTY 50
        df = df[df['trading_symbol'].str.contains(symbol, case=False, na=False)]

        if df.empty:
            send_error_alert(symbol, "Instrument key not found")
        return df
    except Exception as e:
        send_error_alert(symbol, f"Failed to fetch instruments: {e}")
        return pd.DataFrame()


def find_instrument_key(symbol: str):
    """
    Return instrument key for given symbol
    """
    df = get_master_instruments(symbol)
    if not df.empty:
        return df.iloc[0]["instrument_key"]
    return None


def get_nearest_expiry_options(symbol: str):
    """
    Return nearest expiry option contracts for given symbol
    """
    df = get_master_instruments(symbol)
    if df.empty:
        return []

    # Filter only options
    options = df[df['instrument_type'].isin(['OPTIDX', 'OPTSTK'])]
    if options.empty:
        return []

    # Get nearest expiry
    options['expiry'] = pd.to_datetime(options['expiry'])
    nearest_expiry = options['expiry'].min()
    return options[options['expiry'] == nearest_expiry]


def fetch_option_chain(symbol: str):
    """
    Return option chain for given symbol
    """
    df = get_nearest_expiry_options(symbol)
    return df if not df.empty else pd.DataFrame()
