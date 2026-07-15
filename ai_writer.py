import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


CHANNEL = os.getenv(
    "CHANNEL_LINK",
    "https://t.me/deepsourc"
)


WEBSITE = os.getenv(
    "WEBSITE_LINK",
    "https://deepsourcenews.vercel.app/"
)



def rewrite_news(content, title=""):

    prompt = f"""
أنت محرر أخبار محترف يعمل لصالح DeepSource News.

حدد نوع المنشور أولاً.

اختر نوعاً واحداً فقط:
تغريدة
عاجل
خبر
بيان
تقرير
تحليل


القواعد:
- إذا كان المحتوى منشوراً من حساب شخص أو منصة اجتماعية استخدم: تغريدة.
- إذا كان تطوراً سريعاً استخدم: عاجل.
- إذا كان خبراً عادياً استخدم: خبر.
- إذا كان تصريحاً رسمياً استخدم: بيان.
- إذا كان شرحاً معمقاً استخدم: تقرير أو تحليل.
- ترجم إلى العربية إذا كان النص بلغة أخرى.
- لا تضف معلومات غير موجودة.
- لا تستخدم مبالغات.
- اكتب بأسلوب صحفي احترافي.
- أنشئ نقاطاً مختصرة.
- أضف سياقاً مناسباً.
- أضف هاشتاغات.


أخرج النتيجة بهذا الشكل فقط:

TYPE:
نوع المنشور

TITLE:
العنوان

POINTS:
- النقطة الأولى
- النقطة الثانية
- النقطة الثالثة

CONTEXT:
السياق

HASHTAGS:
#هاشتاغ1 #هاشتاغ2 #هاشتاغ3


العنوان الأصلي:
{title}


النص:
{content}

"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3

    )


    return response.choices[0].message.content





def create_template(ai_text):


    post_type = "خبر"

    title = ""

    points = []

    context = ""

    hashtags = ""


    section = None



    for line in ai_text.splitlines():

        line = line.strip()



        if line == "TYPE:":
            section = "type"
            continue


        if line == "TITLE:":
            section = "title"
            continue


        if line == "POINTS:":
            section = "points"
            continue


        if line == "CONTEXT:":
            section = "context"
            continue


        if line == "HASHTAGS:":
            section = "hashtags"
            continue



        if section == "type" and line:

            post_type = line



        elif section == "title" and line:

            title = line



        elif section == "points" and line.startswith("-"):

            points.append(
                line.replace("-", "").strip()
            )



        elif section == "context" and line:

            context += line + " "



        elif section == "hashtags" and line:

            hashtags += line + " "




    post = f"""
🚨⚡️ {post_type} | {title}

"""



    for point in points:

        post += f"🔹 {point}\n\n"



    post += f"""
📊 سياق: {context.strip()}


{hashtags.strip()}


@deepsourc

👍 أكثر الأخبار أهمية وسرية عبر قناتنا:

🔵 <a href="{CHANNEL}">قناتنا</a>

🌐 <a href="{WEBSITE}">موقعنا</a>
"""


    return post.strip()