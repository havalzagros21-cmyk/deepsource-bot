import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


async def extract_article(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # العنوان
        title = ""


        og_title = soup.find(
            "meta",
            property="og:title"
        )

        if og_title:
            title = og_title.get("content", "")


        if not title and soup.title:
            title = soup.title.text.strip()



        # الصورة الرئيسية
        image = None


        og_image = soup.find(
            "meta",
            property="og:image"
        )


        if og_image:

            image = og_image.get(
                "content"
            )


            if image:
                image = urljoin(
                    url,
                    image
                )



        # استخراج النص
        paragraphs = []


        for p in soup.find_all("p"):

            text = p.get_text(
                " ",
                strip=True
            )

            if len(text) > 40:
                paragraphs.append(text)



        content = "\n".join(
            paragraphs[:30]
        )


        return {

            "title": title,

            "content": content,

            "image": image

        }



    except Exception as e:

        print(
            "❌ Scraper Error:",
            e
        )


        return {

            "title": "",

            "content": "",

            "image": None

        }