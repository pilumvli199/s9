import numpy as np
from config import OI_CHANGE_THRESHOLD

def analyze_option_chain(df):
    if df is None or df.empty:
        return {"resistance": 0, "support": 0, "pcr": 0, "oi_change": 0, "oi_strength": 0}
    call_oi = df[df['option_type'] == 'CE']['open_interest']
    put_oi = df[df['option_type'] == 'PE']['open_interest']
    resistance = df.loc[call_oi.idxmax()]['strike_price'] if not call_oi.empty else 0
    support = df.loc[put_oi.idxmax()]['strike_price'] if not put_oi.empty else 0
    pcr = put_oi.sum() / call_oi.sum() if call_oi.sum() > 0 else 0
    oi_change = 0  # TODO: implement with prev vs current
    return {
        "resistance": resistance,
        "support": support,
        "pcr": pcr,
        "oi_change": oi_change,
        "oi_strength": 1 if abs(oi_change) > OI_CHANGE_THRESHOLD else 0
    }
