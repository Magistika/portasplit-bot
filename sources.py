import re
import requests
from bs4 import BeautifulSoup
from config import MAX_PRICE

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SOURCES = [
    {
        "name": "Prosatech",
        "url": "https://www.prosatech.de/search?sSearch=midea%20portasplit"
    },
    {
        "name": "HORNBACH",
        "url": "https://www.hornbach.de/suche/?searchTerm=midea%20portasplit"
    },
    {
        "name": "Globus Baumarkt",
        "url": "https://www.globus-baumarkt.de/search?sSearch=midea%20portasplit"
    },
    {
        "name": "OTTO",
        "url": "https://www.otto.de/suche/midea%20portasplit/"
    },
    {
        "name": "Amazon IT",
        "url": "https://www.amazon.it/s?k=midea+portasplit"
    },
    {
        "name": "Amazon PL",
        "url": "https://www.amazon.pl/s?k=midea+portasplit"
    }
]


def extract_price(text):
    text = text.replace(".", "").replace(",", ".")
    matches = re.findall(r"(\d+(?:\.\d{1,2})?)\s*€", text)
    prices = [float(x) for x in matches]
    return min(prices) if prices else None


def clean_text(text):
    return " ".join(text.split())


def looks_relevant(text):
    text = text.lower()

    return (
        "midea" in text
        and "portasplit" in text
    )


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

        page_text = clean_text(
            soup.get_text(" ", strip=True)
        )

        if not looks_relevant(page_text):
            return offers

        price = extract_price(page_text)

        if not price:
            return offers

        if price > MAX_PRICE:
            return offers

        offers.append({
            "id": source["url"],
            "title": "Midea PortaSplit gefunden",
            "price": price,
            "url": source["url"],
            "source": source["name"]
        })

    except Exception as e:
        print(source["name"], "exception:", e)

    return offers


def search_all_sources():
    results = []

    for source in SOURCES:
        results.extend(
            search_generic(source)
        )

    return results
