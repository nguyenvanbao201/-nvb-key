import requests
from config import LINK4M_TOKEN

def create_link(url):
    api = "https://link4m.co/api-shorten/v2"

    params = {
        "api": LINK4M_TOKEN,
        "url": url
    }

    try:
        r = requests.get(api, params=params, timeout=15)
        data = r.json()

        if data.get("status") == "success":
            return data["shortenedUrl"]

        return None

    except Exception as e:
        print("Link4m Error:", e)
        return None