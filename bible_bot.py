import requests
import telebot
import random
from datetime import date

# ================== YOUR SETTINGS ==================
TOKEN = "8537751985:AAEizyZKR4SPqDkklxSdEKlNl0UyVWCRWgk"
CHAT_ID = "-1003925405554"   # Your test channel
# ==================================================

bot = telebot.TeleBot(TOKEN)

# New / Alternative Amharic Bible API
BASE_URL = "https://bible-api-five.vercel.app"

def post_daily_verse():
    print("🚀 Trying to fetch Amharic verse from API...")
    try:
        random.seed(date.today().toordinal())

        # 1. Get list of books (Amharic version)
        print("Fetching book list...")
        books_resp = requests.get(f"{BASE_URL}/listbookids", timeout=15)
        books_resp.raise_for_status()
        book_list = list(books_resp.json().get("data", {}).values())

        if not book_list:
            raise Exception("No books found")

        book = random.choice(book_list)
        print(f"Selected book: {book}")

        # 2. Get number of chapters
        info = requests.get(f"{BASE_URL}/book/info/{book}", timeout=10).json()["data"]
        chapters = info.get("chapters", 1)
        chapter = random.randint(1, chapters)
        print(f"Selected chapter: {chapter}")

        # 3. Get Amharic verses
        print("Fetching verses...")
        verses_resp = requests.get(f"{BASE_URL}/verses/amhara/{book}/{chapter}", timeout=15)
        verses_resp.raise_for_status()
        verses = verses_resp.json().get("data", [])

        if not verses:
            raise Exception("No verses returned")

        verse_obj = random.choice(verses)

        reference = f"{verse_obj.get('book', book)} {verse_obj.get('chapter')}:{verse_obj.get('verseNum')}"
        text = verse_obj.get("verse", "ጥቅስ አልተገኘም")

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{text}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        bot.send_message(CHAT_ID, message, parse_mode='HTML')
        print("✅ Verse posted successfully to @testbible !")

    except Exception as e:
        error_text = str(e)[:250]
        print(f"❌ Error: {error_text}")
        try:
            bot.send_message(CHAT_ID, f"ዛሬ ጥቅስ ማግኘት አልቻልኩም 😔\n\nError: {error_text}", parse_mode='HTML')
        except:
            pass

if __name__ == "__main__":
    print("🤖 Amharic Daily Bible Bot (API version) started on test channel...")
    post_daily_verse()   # Posts immediately for testing
