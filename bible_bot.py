import json
import random
import telebot
from datetime import date

# ================== SETTINGS ==================
TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "-1003925405554"
# ==============================================

bot = telebot.TeleBot(TOKEN)

# Load Amharic Bible (LOCAL FILE)
with open("amharic_bible.json", "r", encoding="utf-8") as f:
    bible = json.load(f)


# ================== DAILY VERSE ==================
def post_daily_verse():
    try:
        random.seed(date.today().toordinal())

        reference = random.choice(list(bible.keys()))
        verse = bible[reference]

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{verse}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        bot.send_message(CHAT_ID, message, parse_mode="HTML")
        print("✅ Daily verse sent!")

    except Exception as e:
        print("❌ Error:", e)


# ================== RANDOM VERSE COMMAND ==================
@bot.message_handler(commands=['verse'])
def send_verse(message):
    try:
        reference = random.choice(list(bible.keys()))
        verse = bible[reference]

        bot.reply_to(message, f"{verse}\n\n<i>{reference}</i>", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, "Error getting verse 😔")


# ================== START COMMAND ==================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🙏 Amharic Bible Bot is running!\nUse /verse for random verse.")


# ================== RUN BOT ==================
if __name__ == "__main__":
    print("🤖 Bot started...")

    # Send one verse immediately (test)
    post_daily_verse()

    # Keep bot running
    bot.polling()
