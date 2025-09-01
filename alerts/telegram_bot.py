def get_master_instruments(symbol: str):
    """
    Fetch master instruments from Upstox CSV and filter by trading_symbol
    """
    try:
        df = pd.read_csv(INSTRUMENTS_URL)
        df = df[df['trading_symbol'] == symbol]   # ✅ fixed column
        if df.empty:
            send_error_alert(symbol, "Instrument key not found")
        return df
    except Exception as e:
        send_error_alert(symbol, f"Failed to fetch instruments: {e}")
        return pd.DataFrame()

