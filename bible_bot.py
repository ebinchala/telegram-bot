import requests
import telebot
from apscheduler.schedulers.blocking import BlockingScheduler
import random
from datetime import date

TOKEN = "8537751985:AAFLIZJkJnVcX64BTHyoRYw9Lp-BthDqqf4"
CHAT_ID = "-1002240045747"

bot = telebot.TeleBot(TOKEN)
BASE_URL = "https://bible-api-kappa.vercel.app/api/v1"

def get_amharic_daily_verse():
    try:
        random.seed(date.today().toordinal())
        
        books_resp = requests.get(f"{BASE_URL}/listbookids").json()
        book_list = list(books_resp.get("data", {}).values())
        if not book_list:
            raise Exception("No books found")
        
        book = random.choice(book_list)
        
        info = requests.get(f"{BASE_URL}/book/info/{book}").json()["data"]
        chapters = info.get("chapters", 1)
        chapter = random.randint(1, chapters)

        verses_resp = requests.get(f"{BASE_URL}/verses/amhara/{book}/{chapter}").json()
        verses = verses_resp.get("data", [])
        if not verses:
            raise Exception("No verses returned")

        verse_obj = random.choice(verses)
        
        book_name = verse_obj.get("book", book)
        reference = f"{book_name} {verse_obj.get('chapter')}:{verse_obj.get('verseNum')}"
        text = verse_obj.get("verse", "ጥቅስ አልተገኘም")

        message = f"""🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

{text}

<i>{reference}</i>

#DailyBibleVerse #መጽሐፍቅዱስ #አማርኛ"""

        return message

    except Exception as e:
        print("Error:", e)
        return """🌟 <b>የዛሬው መጽሐፍ ቅዱስ ጥቅስ</b> 🌟

እግዚአብሔር ከእናንተ ጋር ይሁን። ነገ እንደገና እንገናኛለን!

<i>መጽሐፍ ቅዱስ</i>
#DailyBibleVerse"""

# Scheduler
scheduler = BlockingScheduler(timezone='Africa/Addis_Ababa')

@scheduler.scheduled_job('cron', hour=23, minute=0)
def post_daily_verse():
    message = get_amharic_daily_verse()
    try:
        bot.send_message(CHAT_ID, message, parse_mode='HTML')
        print(f"✅ Posted at {date.today()} 11:00 PM EAT")
    except Exception as e:
        print(f"❌ Failed to post: {e}")

# ================== START ==================
if __name__ == "__main__":
    print("🤖 Amharic Daily Bible Verse Bot started...")
    print("   → Will post every day at 11:00 PM Ethiopian time")
    
    # === TEST LINE - REMOVE LATER ===
    post_daily_verse()   # This posts NOW for testing
    
    scheduler.start()
