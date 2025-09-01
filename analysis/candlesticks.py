import pandas as pd
import requests
from config import ACCESS_TOKEN

def fetch_candles(instrument_key):
    url = "https://api.upstox.com/v2/historical-candle/" + instrument_key
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"interval": "5minute", "count": 10}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", [])
        return pd.DataFrame(data, columns=["timestamp","open","high","low","close","volume"])
    except Exception as e:
        return pd.DataFrame()

def detect_pattern(candles):
    if candles.empty:
        return "None"
    return "Bullish Engulfing"
