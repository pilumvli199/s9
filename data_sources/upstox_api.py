import pandas as pd
from alerts.telegram_bot import send_alert, send_error_alert
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "instruments.csv")

def normalize_symbol(s: str) -> str:
    return str(s).upper().replace(" ", "").replace("-", "").replace("&", "AND")

def get_master_instruments(symbol: str):
    try:
        df = pd.read_csv(CSV_PATH)
        df["norm_symbol"] = df["trading_symbol"].apply(normalize_symbol)
        target = normalize_symbol(symbol)

        df = df[df["norm_symbol"].str.startswith(target)]
        if df.empty:
            send_error_alert(symbol, "Instrument key not found")
        return df
    except Exception as e:
        send_error_alert(symbol, f"Failed to fetch instruments: {e}")
        return pd.DataFrame()
