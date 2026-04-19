import requests
import telebot
import random
from datetime import date

# ================== YOUR SETTINGS ==================
TOKEN = "8537751985:AAEizyZKR4SPqDkklxSdEKlNl0UyVWCRWgk"
CHAT_ID = "-1002240045747"
# ==================================================

bot = telebot.TeleBot(TOKEN)

# New working Amharic Bible API
BASE_URL = "https://ethiopic-bible-api.vercel.app"

def post_daily_verse():
    print("🚀 Starting to fetch Amharic verse...")
    try:
        random.seed(date.today().toordinal())

        # Get list of books (in Amharic where possible)
        books_resp = requests.get(f"{BASE_URL}/books", timeout=15)
        books_resp.raise_for_status()
        book_list = books_resp.json()

        if not book_list:
            raise Exception("No books found")

        # Pick random book
        book = random.choice(book_list)
        book_id = book.get("id") or book.get("book_id")
        book_name_am = book.get("name_am") or book.get("name") or "መጽሐፍ ቅዱስ"

        print(f"Selected book: {book_name_am}")

        # Get chapters count
        info_resp = requests.get(f"{BASE_URL}/books/{book_id}", timeout=10)
        info_resp.raise_for_status()
        chapters = info_resp.json().get("chapters", 1)
        chapter = random.randint(1, chapters)

        # Get verses in that chapter (Amharic)
        verses_resp = requests.get(f"{BASE_URL}/verses/{book_id}/{chapter}", timeout=10)
        verses_resp.raise_for_status()
        verses = verses_resp.json().get("verses", [])

        if not verses:
            raise Exception("No verses found")

        verse_obj = random.choice(verses)
        verse_text = verse_obj.get("text") or verse_obj.get("verse")
        verse_num = verse_obj.get("verse") or verse_obj.get("number") or "?"

        reference = f"{book_name_am} {chapter}:{verse_num}"

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{verse_text}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        bot.send_message(CHAT_ID, message, parse_mode='HTML')
        print("✅ Verse posted successfully!")

    except Exception as e:
        error_text = str(e)[:200]
        print(f"❌ Error: {error_text}")
        try:
            bot.send_message(CHAT_ID, f"ዛሬ ጥቅስ ማግኘት አልቻልኩም 😔\n\n{error_text}", parse_mode='HTML')
        except:
            pass

if __name__ == "__main__":
    print("🤖 Amharic Daily Bible Bot is starting...")
    post_daily_verse()
