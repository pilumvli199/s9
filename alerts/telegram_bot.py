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

