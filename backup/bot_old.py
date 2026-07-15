import os
import json
import re
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

from telethon import TelegramClient, events


load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")


with open("sources.json", "r", encoding="utf-8") as f:
    SOURCES = json.load(f)



# جلسة قراءة القنوات
reader = TelegramClient(
    "deepsource_session",
    API_ID,
    API_HASH
)



def get_url(text):

    if not text:
        return None

    urls = re.findall(
        r'https?://\S+',
        text
    )

    return urls[0] if urls else None



def read_article(url):

    try:

        r = requests.get(
            url,
            headers={
                "User-Agent":"Mozilla/5.0"
            },
            timeout=15
        )


        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )


        title = soup.title.text if soup.title else "خبر جديد"


        paragraphs = soup.find_all("p")


        content = "\n".join(
            p.text.strip()
            for p in paragraphs[:8]
        )


        return title, content


    except Exception as e:

        return "خطأ", str(e)



def make_post(title, content):

    return f"""

🚨⚡️ عاجل | {title}


🔹 {content[:800]}


📌 المصدر: DeepSource


#أخبار #عاجل


@deepsourc


👍 أكثر الأخبار أهمية وسرية عبر:


🔵 قناتنا
🌐 موقعنا

"""



# استقبال رابط منك

async def user_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    url = get_url(text)


    if url:

        title, content = read_article(url)


        post = make_post(
            title,
            content
        )


        await update.message.reply_text(
            post
        )



# قراءة القنوات

@reader.on(
    events.NewMessage(
        chats=SOURCES
    )
)
async def channel_reader(event):


    text = event.message.text


    url = get_url(text)


    if url:

        title, content = read_article(url)


        print(
            make_post(
                title,
                content
            )
        )

    else:

        print(
            make_post(
                "خبر من تيليجرام",
                text
            )
        )



async def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        MessageHandler(
            filters.TEXT,
            user_message
        )
    )


    await reader.start()


    await app.initialize()

    await app.start()

    await app.updater.start_polling()


    print(
        "🚀 DeepSource Bot Running..."
    )


    await reader.run_until_disconnected()



import asyncio

asyncio.run(main())