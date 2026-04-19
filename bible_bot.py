import requests
import telebot
import random
from datetime import date

TOKEN = "8537751985:AAEizyZKR4SPqDkklxSdEKlNl0UyVWCRWgk"   # ← Use your CURRENT token
CHAT_ID = "-1002240045747"

bot = telebot.TeleBot(TOKEN)
BASE_URL = "https://bible-api-kappa.vercel.app/api/v1"

def post_daily_verse():
    print("🤖 Bot started - trying to post verse...")
    try:
        random.seed(date.today().toordinal())

        # Get books
        print("Fetching book list from API...")
        books_resp = requests.get(f"{BASE_URL}/listbookids", timeout=15)
        books_resp.raise_for_status()
        book_data = books_resp.json()
        book_list = list(book_data.get("data", {}).values()) if isinstance(book_data.get("data"), dict) else book_data.get("data", [])
        
        if not book_list:
            raise Exception("No books found in API response")

        book = random.choice(book_list)
        print(f"Selected book: {book}")

        # Get chapter
        info = requests.get(f"{BASE_URL}/book/info/{book}", timeout=10).json()["data"]
        chapters = info.get("chapters", 1)
        chapter = random.randint(1, chapters)
        print(f"Selected chapter: {chapter}")

        # Get Amharic verse
        print("Fetching Amharic verse...")
        verses_resp = requests.get(f"{BASE_URL}/verses/amhara/{book}/{chapter}", timeout=10)
        verses_resp.raise_for_status()
        verses = verses_resp.json().get("data", [])
        
        if not verses:
            raise Exception("No Amharic verses returned")

        verse_obj = random.choice(verses)
        reference = f"{verse_obj.get('book', book)} {verse_obj.get('chapter')}:{verse_obj.get('verseNum')}"
        text = verse_obj.get("verse", "ጥቅስ አልተገኘም")

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{text}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        bot.send_message(CHAT_ID, message, parse_mode='HTML')
        print("✅ Verse successfully sent to channel!")

    except Exception as e:
        error_text = f"❌ Error: {str(e)[:300]}"
        print(error_text)
        try:
            bot.send_message(CHAT_ID, f"ዛሬ ጥቅስ ማግኘት አልቻልኩም 😔\n\n{error_text}", parse_mode='HTML')
        except Exception as send_error:
            print("Could not send error message:", send_error)

if __name__ == "__main__":
    print("🚀 Amharic Daily Bible Bot is starting on Railway...")
    post_daily_verse()
