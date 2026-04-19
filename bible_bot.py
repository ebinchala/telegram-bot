import requests
import telebot
import random
from datetime import date

# ================== YOUR SETTINGS ==================
TOKEN = "8537751985:AAFLIZJkJnVcX64BTHyoRYw9Lp-BthDqqf4"
CHAT_ID = "-1002240045747"
# ==================================================

bot = telebot.TeleBot(TOKEN)
BASE_URL = "https://bible-api-kappa.vercel.app/api/v1"

def post_daily_verse():
    try:
        # Same verse for everyone on the same day
        random.seed(date.today().toordinal())
        
        # Get books
        books_resp = requests.get(f"{BASE_URL}/listbookids").json()
        book_list = list(books_resp.get("data", {}).values())
        book = random.choice(book_list)

        # Get chapters
        info = requests.get(f"{BASE_URL}/book/info/{book}").json()["data"]
        chapters = info.get("chapters", 1)
        chapter = random.randint(1, chapters)

        # Get Amharic verses
        verses_resp = requests.get(f"{BASE_URL}/verses/amhara/{book}/{chapter}").json()
        verses = verses_resp.get("data", [])
        verse_obj = random.choice(verses)

        reference = f"{verse_obj.get('book', book)} {verse_obj.get('chapter')}:{verse_obj.get('verseNum')}"
        text = verse_obj.get("verse", "ጥቅስ አልተገኘም")

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{text}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        bot.send_message(CHAT_ID, message, parse_mode='HTML')
        print("✅ Verse posted successfully to the channel!")

    except Exception as e:
        print("❌ Error:", e)
        try:
            bot.send_message(CHAT_ID, "ዛሬ ጥቅስ ማግኘት አልቻልኩም 😔 ነገ እንደገና እንሞክራለን!", parse_mode='HTML')
        except:
            pass

if __name__ == "__main__":
    print("🤖 Starting Amharic Bible Bot...")
    post_daily_verse()   # This will post RIGHT NOW when the service starts
