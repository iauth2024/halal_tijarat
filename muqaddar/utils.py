
from telegram import Bot

# Your bot token and chat ID
BOT_TOKEN = "7182564091:AAHHtu6Rbes8GCnXVyWO-PMWYtXteYRg2rg"
CHAT_ID = "5212928367"

# Initialize bot
bot = Bot(token=BOT_TOKEN)

def send_telegram_alert(stock_name, screener_name, stock_details):
    """
    Send an alert to Telegram when a unique stock is detected.
    """
    message = (
        f"🚨 **Stock Alert!**\n\n"
        f"**Stock Name:** {stock_name}\n"
        f"**Screener:** {screener_name}\n"
        f"**Details:** {stock_details}\n"
        f"Check more details on your platform!"
    )
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

# Example usage:
# send_telegram_alert("TEST_SYMBOL", "Test Screener", "Close Price: ₹1234   | Triggered At: 2024-12-18")