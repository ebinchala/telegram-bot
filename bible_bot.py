import telebot
import random
from datetime import date

# ================== YOUR SETTINGS ==================
TOKEN = "8537751985:AAEizyZKR4SPqDkklxSdEKlNl0UyVWCRWgk"
CHAT_ID = "-1003925405554"     # ← Your new test channel
# ==================================================

bot = telebot.TeleBot(TOKEN)

# Built-in Amharic Bible Verses (No API needed)
verses = [
    {"text": "እግዚአብሔር ብርቱ ግንብ ነው፤ በእርሱ የሚያመን ሰው ደህንነት ይኖረዋል።", "ref": "ምሳሌ 18:10"},
    {"text": "በእግዚአብሔር ታመኑ፤ በእግዚአብሔር ታመኑ።", "ref": "ኢሳይያስ 26:4"},
    {"text": "እግዚአብሔር ከእኔ ጋር ነው፤ እፈራለሁን?", "ref": "መዝሙር 27:1"},
    {"text": "ነገር ግን እኔ በእግዚአብሔር ታይቼ ነገር ሁሉን በእርሱ እችላለሁ።", "ref": "ፊልጵስዩስ 4:13"},
    {"text": "እግዚአብሔር ለእናንተ ምን እንደሚያደርግ አስቡ።", "ref": "ኤርምያስ 29:11"},
    {"text": "የእግዚአብሔር ቃል ለዘላለም ይኖራል።", "ref": "ኢሳይያስ 40:8"},
    {"text": "ፍቅር ታጋሽ ነው፤ ፍቅር ቸር ነው።", "ref": "1 ቆሮንቶስ 13:4"},
    {"text": "በእግዚአብሔር ፊት ሁሉም ነገር ይቻላል።", "ref": "ማቴዎስ 19:26"},
    {"text": "እግዚአብሔር ይጠብቀናል። እኛ እንጠብቃለን።", "ref": "መዝሙር 130:5"},
    {"text": "ደስ ይበላችሁ፤ ሁልጊዜ ደስ ይበላችሁ።", "ref": "1 ተሰሎንቄ 5:16"}
    # You can add more verses later
]

def post_daily_verse():
    try:
        # Same verse for the whole day
        random.seed(date.today().toordinal())
        verse = random.choice(verses)

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{verse['text']}

<i>{verse['ref']}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        bot.send_message(CHAT_ID, message, parse_mode='HTML')
        print("✅ Verse posted successfully to @testbible")

    except Exception as e:
        print(f"❌ Error: {e}")
        try:
            bot.send_message(CHAT_ID, "ዛሬ ጥቅስ ማግኘት አልቻልኩም 😔 ነገ እንደገና እንሞክራለን!", parse_mode='HTML')
        except:
            pass

if __name__ == "__main__":
    print("🤖 Amharic Daily Bible Bot started on test channel...")
    post_daily_verse()        # Posts immediately for testing
