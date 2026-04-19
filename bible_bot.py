import requests
import telebot
from apscheduler.schedulers.blocking import BlockingScheduler
import random
from datetime import date
import pytz

# ================== YOUR SETTINGS ==================
TOKEN = "8537751985:AAFLIZJkJnVcX64BTHyoRYw9Lp-BthDqqf4"
CHAT_ID = "-1002240045747"
# ==================================================

bot = telebot.TeleBot(TOKEN)

# Reliable Amharic Bible API (free & public)
BASE_URL = "https://bible-api-kappa.vercel.app/api/v1"

def get_amharic_daily_verse():
    try:
        # Make the verse the same for everyone on the same day
        random.seed(date.today().toordinal())

        # Get list of books
        books_resp = requests.get(f"{BASE_URL}/listbookids").json()
        book_list = list(books_resp.get("data", {}).values())

        if not book_list:
            raise Exception("No books found")

        # Pick random book
        book = random.choice(book_list)

        # Get book info (number of chapters)
        info = requests.get(f"{BASE_URL}/book/info/{book}").json()["data"]
        chapters = info.get("chapters", 1)

        # Pick random chapter
        chapter = random.randint(1, chapters)

        # Get verses in Amharic
        verses_resp = requests.get(f"{BASE_URL}/verses/amhara/{book}/{chapter}").json()
        verses = verses_resp.get("data", [])

        if not verses:
            raise Exception("No verses returned")

        # Pick random verse
        verse_obj = random.choice(verses)

        book_name = verse_obj.get("book", book)
        verse_num = verse_obj.get("verseNum", "?")
        text = verse_obj.get("verse", "ጥቅስ አልተገኘም")

        reference = f"{book_name} {verse_obj.get('chapter', chapter)}:{verse_num}"

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{text}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        return message

    except Exception as e:
        print("Error fetching verse:", e)
        return """🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

እግዚአብሔር ከእናንተ ጋር ይሁን። ነገ እንደገና እንገናኛለን!

<i>መጽሐፍ ቅዱስ</i>

#DailyBibleVerse"""

# ================== SCHEDULER (11:00 PM EAT) ==================
scheduler = BlockingScheduler(timezone='Africa/Addis_Ababa')

@scheduler.scheduled_job('cron', hour=23, minute=0)
def post_daily_verse():
    message = get_amharic_daily_verse()
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='HTML'
        )
        print(f"✅ Bible verse posted successfully at {date.today()} 11:00 PM EAT")
    except Exception as e:
        print(f"❌ Failed to post: {e}")

# ================== START THE BOT ==================
if __name__ == "__main__":
    print("🤖 Amharic Daily Bible Verse Bot is now running...")
    print("   → It will post every day at 11:00 PM Ethiopian time")
    scheduler.start() 
