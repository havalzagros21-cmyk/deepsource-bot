import os
import re
import json
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from telethon import TelegramClient, events

from ai_writer import rewrite_news, create_template


load_dotenv()


API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")


TARGET_CHANNEL = "deepsourc"



with open(
    "sources.json",
    "r",
    encoding="utf-8"
) as f:

    SOURCES = json.load(f)



client = TelegramClient(
    "deepsource_session",
    API_ID,
    API_HASH
)



# ==========================
# استخراج الرابط
# ==========================

def extract_url(text):

    if not text:
        return None


    urls = re.findall(
        r"https?://\S+",
        text
    )


    if urls:

        return urls[0].rstrip(").,")
    

    return None




# ==========================
# قراءة المقال والصورة
# ==========================

def get_article(url):

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            },
            timeout=30
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        title = "خبر عاجل"


        if soup.title:

            title = soup.title.text.strip()



        paragraphs = soup.find_all("p")


        content = "\n".join(
            p.get_text(
                " ",
                strip=True
            )
            for p in paragraphs[:30]
        )



        image = None


        img = soup.find(
            "meta",
            property="og:image"
        )


        if img:

            image = img.get(
                "content"
            )



        return title, content, image



    except Exception as e:

        print(
            "Article Error:",
            e
        )

        return "خبر عاجل", "", None




# ==========================
# تحميل الصورة
# ==========================

def download_image(url):

    if not url:

        return None


    try:

        r = requests.get(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            },
            timeout=30
        )


        filename = "news_image.jpg"


        with open(
            filename,
            "wb"
        ) as f:

            f.write(
                r.content
            )


        return filename



    except Exception as e:

        print(
            "Image Error:",
            e
        )

        return None




# ==========================
# النشر
# ==========================

async def publish(post, media=None):


    if media and os.path.exists(media):

        await client.send_file(
            TARGET_CHANNEL,
            media,
            caption=post,
            parse_mode="html"
        )


    else:


        await client.send_message(
            TARGET_CHANNEL,
            post,
            parse_mode="html"
        )




# ==========================
# أخبار القنوات
# ==========================

@client.on(
    events.NewMessage(
        chats=SOURCES
    )
)

async def channel_news(event):


    print(
        "📩 New Channel Message"
    )


    text = event.message.message or ""


    media = None



    if event.message.media:

        media = await event.message.download_media()




    url = extract_url(text)



    if url:


        title, content, image = get_article(url)


        if not media:

            media = download_image(
                image
            )



    else:


        title = "خبر عاجل"

        content = text




    ai = rewrite_news(
        content,
        title
    )



    post = create_template(
        ai
    )



    await publish(
        post,
        media
    )


    print(
        "✅ Published"
    )





# ==========================
# الرسائل الخاصة منك
# ==========================

@client.on(
    events.NewMessage(
        incoming=True
    )
)

async def personal_input(event):


    if not event.is_private:

        return



    text = event.message.message or ""



    media = None



    if event.message.media:


        media = await event.message.download_media()



        ai = rewrite_news(
            text,
            "خبر عاجل"
        )


        post = create_template(
            ai
        )


        await publish(
            post,
            media
        )


        return





    url = extract_url(text)



    if not url:

        return




    print(
        "🔗 External URL"
    )



    title, content, image = get_article(
        url
    )



    ai = rewrite_news(
        content,
        title
    )



    post = create_template(
        ai
    )



    media = download_image(
        image
    )



    await publish(
        post,
        media
    )



    await event.reply(
        "✅ تم تجهيز الخبر ونشره"
    )




# ==========================
# التشغيل
# ==========================

async def main():


    await client.start()


    print(
        "🚀 DeepSource System Running..."
    )


    print(
        "👂 Listening:"
    )


    for s in SOURCES:

        print(
            "-",
            s
        )


    await client.run_until_disconnected()




client.loop.run_until_complete(
    main()
)