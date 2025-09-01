import time
import asyncio
import logging
from shared.market_guard import is_market_open
from data_sources.upstox_api import find_instrument_key, get_nearest_expiry_options, fetch_option_chain
from analysis.options_oi import analyze_option_chain
from analysis.candlesticks import fetch_candles, detect_pattern
from analysis.confidence import calculate_confidence
from alerts.telegram_bot import send_alert, send_error_alert
from config import STOCKS, INDICES, SCAN_INTERVAL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_symbol(symbol):
    try:
        key = find_instrument_key(symbol)
        if not key:
            raise ValueError(f"Instrument key not found for {symbol}")
        expiry, option_keys = get_nearest_expiry_options(key)
        chain = fetch_option_chain(key, expiry)
        if chain is None or chain.empty:
            raise ValueError(f"No option chain data for {symbol}")
        oi_data = analyze_option_chain(chain)
        candles = fetch_candles(key)
        pattern = detect_pattern(candles)
        volume = chain['volume'].sum() if not chain.empty else 0
        sentiment = 0
        trade, confidence = calculate_confidence(oi_data, candles, volume, pattern, sentiment)
        if trade:
            send_alert(symbol, {**oi_data, "pattern": pattern, "expiry": expiry, **trade, "confidence": confidence})
    except Exception as e:
        send_error_alert(symbol, str(e))
        logging.error(f"Error processing {symbol}: {e}")

async def process_batch(batch):
    tasks = [process_symbol(symbol) for symbol in batch]
    await asyncio.gather(*tasks)

def main():
    while True:
        if not is_market_open():
            logging.info("Market closed, sleeping for 60s")
            time.sleep(60)
            continue
        instruments = STOCKS + INDICES
        batches = [instruments[i:i+14] for i in range(0, len(instruments), 14)]
        for batch in batches:
            asyncio.run(process_batch(batch))
            time.sleep(1)
        logging.info(f"Completed scan, sleeping for {SCAN_INTERVAL}s")
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
