import os
import json
import re
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telethon import TelegramClient, events


load_dotenv()


api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")


with open("sources.json", "r", encoding="utf-8") as f:
    SOURCES = json.load(f)


client = TelegramClient(
    "deepsource_session",
    api_id,
    api_hash
)



def extract_url(text):

    if not text:
        return None

    urls = re.findall(
        r'https?://\S+',
        text
    )

    if urls:
        return urls[0]

    return None



def read_article(url):

    try:

        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )


        title = soup.find("title")

        if title:
            title = title.text.strip()
        else:
            title = "بدون عنوان"



        paragraphs = soup.find_all("p")

        content = "\n".join(
            p.text.strip()
            for p in paragraphs[:10]
        )


        image = None

        og_image = soup.find(
            "meta",
            property="og:image"
        )

        if og_image:
            image = og_image.get("content")


        return {
            "title": title,
            "content": content,
            "image": image
        }


    except Exception as e:

        print("❌ خطأ استخراج المقال:")
        print(e)

        return None





@client.on(events.NewMessage(chats=SOURCES))
async def handler(event):

    print("\n================")
    print("📩 خبر جديد")
    print("================")


    text = event.message.text


    url = extract_url(text)


    if url:

        print("🔗 الرابط:")
        print(url)


        article = read_article(url)


        if article:

            print("\n📰 العنوان:")
            print(article["title"])


            print("\n📄 المحتوى:")
            print(article["content"])


            if article["image"]:

                print("\n🖼 الصورة:")
                print(article["image"])



    else:

        print(text)



print("🚀 Telegram Reader Running...")


client.start()

client.run_until_disconnected()