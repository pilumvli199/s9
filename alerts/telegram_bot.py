import os
import telebot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

bot = None
if TELEGRAM_BOT_TOKEN and ":" in TELEGRAM_BOT_TOKEN:
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
else:
    print("⚠️ Invalid TELEGRAM_BOT_TOKEN: Please set a valid token with a colon.")

def send_alert(*args):
    if bot:
        try:
            chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
            if chat_id:
                message = " ".join(str(a) for a in args)
                bot.send_message(chat_id, f"ℹ️ ALERT: {message}")
            else:
                print("⚠️ TELEGRAM_CHAT_ID not set. Cannot send alert.")
        except Exception as e:
            print(f"⚠️ Failed to send Telegram alert: {e}")
    else:
        print(f"⚠️ Bot not initialized. Alert: {' '.join(str(a) for a in args)}")

def send_error_alert(*args):
    if bot:
        try:
            chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
            if chat_id:
                message = " ".join(str(a) for a in args)
                bot.send_message(chat_id, f"❌ ERROR: {message}")
            else:
                print("⚠️ TELEGRAM_CHAT_ID not set. Cannot send error alert.")
        except Exception as e:
            print(f"⚠️ Failed to send Telegram error alert: {e}")
    else:
        print(f"⚠️ Bot not initialized. Error: {' '.join(str(a) for a in args)}")
