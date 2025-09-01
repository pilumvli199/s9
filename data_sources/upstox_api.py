import pandas as pd
import requests
from alerts.telegram_bot import send_alert, send_error_alert

# ✅ नवा instruments CSV URL (Upstox public link)
INSTRUMENTS_URL = "https://assets.upstox.com/market-quote/instruments/upstox_instruments.csv"

def get_master_instruments(symbol: str):
    """
    Fetch master instruments from Upstox CSV and filter by symbol
    """
    try:
        df = pd.read_csv(INSTRUMENTS_URL)
        df = df[df['symbol'] == symbol]   # filter by symbol column
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

