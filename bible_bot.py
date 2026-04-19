import requests
import telebot
import random
from datetime import date

TOKEN = "8537751985:AAFLIZJkJnVcX64BTHyoRYw9Lp-BthDqqf4"
CHAT_ID = "-1002240045747"

bot = telebot.TeleBot(TOKEN)
BASE_URL = "https://bible-api-kappa.vercel.app/api/v1"

def post_daily_verse():
    print("🚀 Starting to fetch verse...")   # This will show in Railway logs
    
    try:
        random.seed(date.today().toordinal())
        
        # Step 1: Get list of books
        print("Fetching book list...")
        books_resp = requests.get(f"{BASE_URL}/listbookids", timeout=10)
        books_resp.raise_for_status()
        book_list = list(books_resp.json().get("data", {}).values())
        
        if not book_list:
            raise Exception("No books returned from API")
        
        book = random.choice(book_list)
        print(f"Selected book: {book}")

        # Step 2: Get book info
        info_resp = requests.get(f"{BASE_URL}/book/info/{book}", timeout=10)
        info_resp.raise_for_status()
        chapters = info_resp.json()["data"].get("chapters", 1)
        chapter = random.randint(1, chapters)
        print(f"Selected chapter: {chapter}")

        # Step 3: Get Amharic verses
        print("Fetching Amharic verse...")
        verses_resp = requests.get(f"{BASE_URL}/verses/amhara/{book}/{chapter}", timeout=10)
        verses_resp.raise_for_status()
        verses = verses_resp.json().get("data", [])
        
        if not verses:
            raise Exception("No verses returned for this chapter")

        verse_obj = random.choice(verses)
        reference = f"{verse_obj.get('book', book)} {verse_obj.get('chapter')}:{verse_obj.get('verseNum')}"
        text = verse_obj.get("verse", "ጥቅስ አልተገኘም")

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{text}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        bot.send_message(CHAT_ID, message, parse_mode='HTML')
        print("✅ Verse posted successfully to channel!")

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        try:
            bot.send_message(CHAT_ID, f"ዛሬ ጥቅስ ማግኘት አልቻልኩም 😔\n\n{error_msg}", parse_mode='HTML')
        except:
            pass

if __name__ == "__main__":
    print("🤖 Amharic Bible Bot is starting on Railway...")
    post_daily_verse()
