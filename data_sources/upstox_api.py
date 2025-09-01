import pandas as pd
import requests
import io
from config import ACCESS_TOKEN
from alerts.telegram_bot import send_error_alert

CACHE_FILE = "instruments_cache.csv"

def get_master_instruments(symbol):
    try:
        url = "https://api.upstox.com/v2/instruments"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        df.to_csv(CACHE_FILE, index=False)
        return df
    except Exception as e:
        send_error_alert(symbol, f"Failed to fetch instruments: {e}")
        return None

def find_instrument_key(symbol):
    df = None
    try:
        df = pd.read_csv(CACHE_FILE)
    except:
        df = get_master_instruments(symbol)
    if df is None or df.empty:
        return None
    mapping = {"NIFTY50": "NIFTY 50", "MIDCPNIFTY": "NIFTY MIDCAP SELECT", "SENSEX": "SENSEX"}
    search_symbol = mapping.get(symbol, symbol)
    filter_df = df[df['tradingsymbol'] == search_symbol]
    return filter_df['instrument_key'].iloc[0] if not filter_df.empty else None

def get_nearest_expiry_options(instrument_key):
    url = f"https://api.upstox.com/v2/option/chain/expiries"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, params={"instrument_key": instrument_key})
        response.raise_for_status()
        expiries = response.json().get("data", [])
        if not expiries:
            return None, None
        nearest_expiry = sorted(expiries)[0]
        return nearest_expiry, []
    except Exception as e:
        send_error_alert(instrument_key, f"Failed to fetch expiries: {e}")
        return None, None

def fetch_option_chain(instrument_key, expiry_date):
    url = f"https://api.upstox.com/v2/option/chain"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"instrument_key": instrument_key, "expiry_date": expiry_date}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", [])
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        cols = [c for c in ["strike_price","open_interest","ltp","delta","theta","volume","option_type"] if c in df.columns]
        return df[cols]
    except Exception as e:
        send_error_alert(instrument_key, f"Failed to fetch option chain: {e}")
        return pd.DataFrame()
