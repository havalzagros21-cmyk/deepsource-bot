import os
import logging

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters
)

from ai_writer import rewrite_news, create_template
from scraper import extract_article
from publisher import publish_post
from image_search import find_image


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


logging.basicConfig(
    level=logging.INFO
)


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("🔥 PROCESS MESSAGE STARTED")

    message = update.message

    if not message:
        return


    await message.reply_text(
        "📥 تم استلام المحتوى..."
    )


    text = message.caption or message.text or ""

    image = None
    video = None

    title = ""
    content = text


    # فيديو Telegram
    if message.video:
        video = message.video.file_id


    # صورة Telegram
    elif message.photo:
        image = message.photo[-1].file_id



    # رابط خارجي
    if text.startswith("http"):

        await message.reply_text(
            "🌐 جاري قراءة الرابط..."
        )

        article = await extract_article(text)

        title = article.get(
            "title",
            ""
        )

        content = article.get(
            "content",
            ""
        )


        if article.get("video"):
            video = article.get("video")


        elif article.get("image"):
            image = article.get("image")



    # البحث عن صورة
    if not image and not video:

        image = await find_image(
            title or content
        )


    print("✍️ AI START")

    ai_text = rewrite_news(
        content,
        title
    )


    final_post = create_template(
        ai_text
    )


    print("🚀 CALLING PUBLISH POST")


    result = await publish_post(
        text=final_post,
        image=image,
        video=video
    )


    print("📌 PUBLISH RESULT:", result)


    await message.reply_text(
        "✅ تم الانتهاء"
    )



def main():

    print(
        "🚀 DeepSource Bot Running..."
    )


    app = Application.builder()\
        .token(TOKEN)\
        .build()


    app.add_handler(
        MessageHandler(
            filters.ALL,
            process_message
        )
    )


    app.run_polling()



if __name__ == "__main__":
    main()