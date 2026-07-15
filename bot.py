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


async def process_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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


    # فيديو تيليجرام
    if message.video:
        video = message.video.file_id


    # صورة تيليجرام
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


    print("========== DEBUG ==========")
    print("TITLE:", title)
    print("IMAGE:", image)
    print("VIDEO:", video)
    print("===========================")



    # كتابة الخبر بالذكاء الاصطناعي
    ai_text = rewrite_news(
        content,
        title
    )


    final_post = create_template(
        ai_text
    )


    print("🚀 Sending to publisher...")


    result = await publish_post(
        text=final_post,
        image=image,
        video=video
    )


    print("PUBLISH RESULT:", result)



    if result:

        await message.reply_text(
            "✅ تم النشر بنجاح"
        )

    else:

        await message.reply_text(
            "❌ فشل النشر"
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