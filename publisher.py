import os
import requests

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")


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


    print("TEXT RESPONSE:")
    print(response.json())


    return response.json()





def send_photo(photo, caption):

    url = f"{API_URL}/sendPhoto"


    data = {
        "chat_id": CHANNEL_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }



    if photo.startswith("http"):

        data["photo"] = photo


    else:

        data["photo"] = photo



    response = requests.post(
        url,
        data=data,
        timeout=60
    )


    print("PHOTO RESPONSE:")
    print(response.json())


    return response.json()





def send_video(video, caption):

    url = f"{API_URL}/sendVideo"


    data = {
        "chat_id": CHANNEL_ID,
        "video": video,
        "caption": caption,
        "parse_mode": "HTML"
    }



    response = requests.post(
        url,
        data=data,
        timeout=120
    )


    print("VIDEO RESPONSE:")
    print(response.json())


    return response.json()





async def publish_post(
    text,
    image=None,
    video=None
):


    print("📤 Publishing...")
    print("CHANNEL_ID:", CHANNEL_ID)
    print("TOKEN:", bool(BOT_TOKEN))
    print("IMAGE:", image)
    print("VIDEO:", video)



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




        if result.get("ok"):


            print("✅ PUBLISH SUCCESS")

            return True



        else:


            print("❌ PUBLISH FAILED")

            return False




    except Exception as e:


        print(
            "❌ Publisher Error:",
            e
        )


        return False