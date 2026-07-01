import re
import requests
from bs4 import BeautifulSoup
from config import MAX_PRICE

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SOURCES = [
    # Deutschland
    {"name": "BAUHAUS", "url": "https://www.bauhaus.info/suche/produkte?text=midea%20portasplit"},
    {"name": "OBI", "url": "https://www.obi.de/search/midea%20portasplit/"},
    {"name": "Amazon DE", "url": "https://www.amazon.de/s?k=midea+portasplit"},
    {"name": "toom Baumarkt", "url": "https://toom.de/suche/?search=midea%20portasplit"},
    {"name": "idealo", "url": "https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q=midea%20portasplit"},
    {"name": "Prosatech", "url": "https://www.prosatech.de/search?sSearch=midea%20portasplit"},

    # weiteres Deutschland / Marktplätze
    {"name": "HORNBACH", "url": "https://www.hornbach.de/suche/?searchTerm=midea%20portasplit"},
    {"name": "hagebau", "url": "https://www.hagebau.de/suche/?q=midea%20portasplit"},
    {"name": "Globus Baumarkt", "url": "https://www.globus-baumarkt.de/search?sSearch=midea%20portasplit"},
    {"name": "Kaufland", "url": "https://www.kaufland.de/s/?search_value=midea%20portasplit"},
    {"name": "OTTO", "url": "https://www.otto.de/suche/midea%20portasplit/"},

    # benachbartes Ausland / EU
    {"name": "Amazon FR", "url": "https://www.amazon.fr/s?k=midea+portasplit"},
    {"name": "Amazon IT", "url": "https://www.amazon.it/s?k=midea+portasplit"},
    {"name": "Amazon NL", "url": "https://www.amazon.nl/s?k=midea+portasplit"},
    {"name": "Amazon PL", "url": "https://www.amazon.pl/s?k=midea+portasplit"},
    {"name": "Leroy Merlin FR", "url": "https://www.leroymerlin.fr/recherche/?q=midea%20portasplit"},
    {"name": "ManoMano DE", "url": "https://www.manomano.de/suche/midea+portasplit"},
    {"name": "ManoMano FR", "url": "https://www.manomano.fr/recherche/midea-portasplit"},
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


def shipping_possible_text(text):
    text = text.lower()
    bad_words = [
        "kein versand nach deutschland",
        "nicht nach deutschland",
        "not ship to germany",
        "does not ship to germany",
        "livraison non disponible en allemagne",
    ]

    for word in bad_words:
        if word in text:
            return False

    return True


def search_generic(source):
    offers = []

    try:
        r = requests.get(source["url"], headers=HEADERS, timeout=25)
        print(source["name"], "status:", r.status_code)

        if r.status_code != 200:
            return offers

        soup = BeautifulSoup(r.text, "lxml")
        page_text = clean_text(soup.get_text(" ", strip=True))

        if not looks_relevant(page_text):
            return offers

        if not shipping_possible_text(page_text):
            return offers

        price = extract_price(page_text)

        if price and price <= MAX_PRICE:
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
        results.extend(search_generic(source))

    return results
