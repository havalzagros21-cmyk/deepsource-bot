import os
import requests

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

CHANNEL_ID = (
    os.getenv("CHANNEL_ID")
    or os.getenv("CHANNEL_LINK")
)


API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"



def send_text(text):

    url = f"{API_URL}/sendMessage"


    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }


    response = requests.post(
        url,
        data=data,
        timeout=30
    )


    return response.json()



def send_photo(photo, caption):

    url = f"{API_URL}/sendPhoto"


    data = {
        "chat_id": CHANNEL_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }


    files = None


    # صورة Telegram file_id
    if not photo.startswith("http") and len(photo) > 20:

        data["photo"] = photo



    # رابط صورة
    elif photo.startswith("http"):

        data["photo"] = photo



    else:

        return None



    response = requests.post(
        url,
        data=data,
        timeout=60
    )


    return response.json()





def send_video(video, caption):

    url = f"{API_URL}/sendVideo"


    data = {
        "chat_id": CHANNEL_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }



    # فيديو Telegram file_id
    if not video.startswith("http"):

        data["video"] = video



    # رابط فيديو مباشر
    else:

        data["video"] = video



    response = requests.post(
        url,
        data=data,
        timeout=120
    )


    return response.json()





async def publish_post(
    text,
    image=None,
    video=None
):

    print("📤 Publishing...")


    try:


        if video:

            result = send_video(
                video,
                text
            )


        elif image:

            result = send_photo(
                image,
                text
            )


        else:

            result = send_text(
                text
            )



        print(result)



        if result and result.get("ok"):

            return True



        return False



    except Exception as e:


        print(
            "❌ Publisher Error:",
            e
        )


        return False