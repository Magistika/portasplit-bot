import re
import requests
from xml.etree import ElementTree as ET
from config import MAX_PRICE

SEARCH_TERMS = [
    "midea portasplit",
    "portasplit 12000",
    "portasplit 12.000",
    "portasplit 3,5 kw",
]

MYDEALZ_RSS = "https://www.mydealz.de/rss/search?q={query}"


def extract_price(text: str):
    text = text.replace(".", "").replace(",", ".")
    matches = re.findall(r"(\d+(?:\.\d{1,2})?)\s*€", text)
    prices = [float(m) for m in matches]
    return min(prices) if prices else None


def search_mydealz():
    offers = []

    for term in SEARCH_TERMS:
        url = MYDEALZ_RSS.format(query=requests.utils.quote(term))
        try:
            r = requests.get(url, timeout=20, headers={
                "User-Agent": "Mozilla/5.0"
            })
            if r.status_code != 200:
                print("mydealz error:", r.status_code, url)
                continue

            root = ET.fromstring(r.content)

            for item in root.findall(".//item"):
                title = item.findtext("title") or ""
                link = item.findtext("link") or ""
                description = item.findtext("description") or ""

                combined = f"{title} {description}"
                price = extract_price(combined)

                if not price:
                    continue

                lowered = combined.lower()

                if "portasplit" not in lowered:
                    continue

                if "midea" not in lowered:
                    continue

                if price <= MAX_PRICE:
                    offers.append({
                        "id": link,
                        "title": title.strip(),
                        "price": price,
                        "url": link,
                        "source": "mydealz"
                    })

        except Exception as e:
            print("mydealz exception:", e)

    return offers


def search_all_sources():
    results = []
    results.extend(search_mydealz())
    return results
