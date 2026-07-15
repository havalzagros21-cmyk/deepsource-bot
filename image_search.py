import requests
from urllib.parse import quote


async def find_image(query):

    try:

        if not query:
            return None


        api_url = "https://commons.wikimedia.org/w/api.php"


        params = {

            "action": "query",

            "format": "json",

            "generator": "search",

            "gsrsearch": query,

            "gsrnamespace": 6,

            "gsrlimit": 5,

            "prop": "imageinfo",

            "iiprop": "url"

        }


        response = requests.get(
            api_url,
            params=params,
            timeout=20
        )


        data = response.json()


        pages = (
            data
            .get("query", {})
            .get("pages", {})
        )


        for page in pages.values():

            info = page.get(
                "imageinfo"
            )


            if info:

                return info[0].get(
                    "url"
                )


        return None



    except Exception as e:

        print(
            "❌ Image Search Error:",
            e
        )

        return None