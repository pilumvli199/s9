from config import CONFIDENCE_THRESHOLD

def calculate_confidence(oi_data, candles, volume, pattern, sentiment_score):
    volume_score = min(volume / 1000000, 1)
    pattern_strength = 1 if pattern != "None" else 0
    score = (0.3 * oi_data['oi_strength'] + 0.2 * (oi_data['oi_change'] / 100 if oi_data['oi_change'] else 0) +
             0.2 * (1 if not candles.empty else 0) + 0.15 * volume_score +
             0.15 * pattern_strength + 0.05 * sentiment_score)
    score = min(score * 100, 100)
    if score >= CONFIDENCE_THRESHOLD:
        trade = {"entry": oi_data['support']+25, "sl": oi_data['support']-25, "target": oi_data['resistance']}
        return trade, score
    return None, score
