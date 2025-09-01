import os
import telebot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

bot = None
if TELEGRAM_BOT_TOKEN and ":" in TELEGRAM_BOT_TOKEN:
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
else:
    print("⚠️ Invalid TELEGRAM_BOT_TOKEN: Please set a valid token with a colon.")

def send_error_alert(message: str):
    if bot:
        try:
            # Replace with your chat_id or set TELEGRAM_CHAT_ID as env var
            chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
            if chat_id:
                bot.send_message(chat_id, f"❌ ERROR: {message}")
            else:
                print("⚠️ TELEGRAM_CHAT_ID not set. Cannot send alert.")
        except Exception as e:
            print(f"⚠️ Failed to send Telegram alert: {e}")
    else:
        print(f"⚠️ Bot not initialized. Error: {message}")
