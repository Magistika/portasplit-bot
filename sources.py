import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import MAX_PRICE

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SOURCES = [
    {"name": "Prosatech", "url": "https://www.prosatech.de/search?sSearch=midea%20portasplit"},
    {"name": "HORNBACH", "url": "https://www.hornbach.de/suche/?searchTerm=midea%20portasplit"},
    {"name": "Globus Baumarkt", "url": "https://www.globus-baumarkt.de/search?sSearch=midea%20portasplit"},
    {"name": "OTTO", "url": "https://www.otto.de/suche/midea%20portasplit/"},
    {"name": "Amazon PL", "url": "https://www.amazon.pl/s?k=midea+portasplit"},
]


def clean_text(text):
    return " ".join(text.split())


def extract_price(text):
    text = text.replace(".", "").replace(",", ".")
    matches = re.findall(r"(\d+(?:\.\d{1,2})?)\s*€", text)
    prices = []

    for match in matches:
        try:
            price = float(match)
            if 100 <= price <= 2000:
                prices.append(price)
        except:
            pass

    return min(prices) if prices else None


def is_relevant(text):
    t = text.lower()

    if "midea" not in t:
        return False

    if "portasplit" not in t:
        return False

    bad_words = [
        "zubehör",
        "ersatzteil",
        "filter",
        "schlauch",
        "fernbedienung",
        "abdeckung",
        "halterung",
    ]

    for word in bad_words:
        if word in t:
            return False

    return True


def search_generic(source):
    offers = []

    try:
        r = requests.get(
            source["url"],
            headers=HEADERS,
            timeout=30
        )

        print(source["name"], "status:", r.status_code)

        if r.status_code != 200:
            return offers

        soup = BeautifulSoup(r.text, "lxml")

        blocks = soup.find_all(["article", "li", "div", "section"])

        for block in blocks:
            text = clean_text(block.get_text(" ", strip=True))

            if not is_relevant(text):
                continue

            price = extract_price(text)

            if not price:
                continue

            if price > MAX_PRICE:
                continue

            link = source["url"]

            a = block.find("a", href=True)
            if a:
                link = urljoin(source["url"], a["href"])

            title = text[:120]

            offers.append({
                "id": f"{source['name']}-{price}-{link}",
                "title": title,
                "price": price,
                "url": link,
                "source": source["name"]
            })

    except Exception as e:
        print(source["name"], "exception:", e)

    return offers


def search_all_sources():
    results = []

    for source in SOURCES:
        results.extend(search_generic(source))

    return results
