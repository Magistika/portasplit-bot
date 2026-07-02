import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import MAX_PRICE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/"
}

SOURCES = [
    {"name": "Prosatech", "url": "https://www.prosatech.de/search?sSearch=midea%20portasplit"},
    {"name": "HORNBACH DE", "url": "https://www.hornbach.de/suche/?searchTerm=midea%20portasplit"},
    {"name": "Globus Baumarkt", "url": "https://www.globus-baumarkt.de/search?sSearch=midea%20portasplit"},
    {"name": "OTTO", "url": "https://www.otto.de/suche/midea%20portasplit"},
    {"name": "Kleinanzeigen 80km", "url": "https://www.kleinanzeigen.de/s-midea-portasplit/92224/radius:80/k0"},
    {"name": "BAUHAUS DE", "url": "https://www.bauhaus.info/suche/produkte?text=midea%20portasplit"},
    {"name": "OBI DE", "url": "https://www.obi.de/suche/midea%20portasplit/"},
    {"name": "toom DE", "url": "https://toom.de/suche/?q=midea%20portasplit"},
    {"name": "Voelkner", "url": "https://www.voelkner.de/search?sSearch=midea%20portasplit"},
    {"name": "Kältebringer", "url": "https://www.kaeltebringer.de/search?sSearch=midea%20portasplit"},

    {"name": "Amazon DE", "url": "https://www.amazon.de/s?k=midea+portasplit"},
    {"name": "Amazon FR", "url": "https://www.amazon.fr/s?k=midea+portasplit"},
    {"name": "Amazon IT", "url": "https://www.amazon.it/s?k=midea+portasplit"},
    {"name": "Amazon ES", "url": "https://www.amazon.es/s?k=midea+portasplit"},
    {"name": "Amazon NL", "url": "https://www.amazon.nl/s?k=midea+portasplit"},
    {"name": "Amazon PL", "url": "https://www.amazon.pl/s?k=midea+portasplit"},

    {"name": "Willhaben AT", "url": "https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz?keyword=midea%20portasplit"},
    {"name": "Bazos CZ", "url": "https://www.bazos.cz/search.php?hledat=midea%20portasplit"},
    {"name": "Ceneo PL", "url": "https://www.ceneo.pl/;szukaj-midea+portasplit"},
    {"name": "BraucheKlima", "url": "https://braucheklima.de/"},
    {"name": "Hornbach AT", "url": "https://www.hornbach.at/suche/?searchTerm=midea%20portasplit"},
    {"name": "Hornbach CH", "url": "https://www.hornbach.ch/de/search/?q=midea%20portasplit"},
    {"name": "Hornbach CZ", "url": "https://www.hornbach.cz/hledat/?q=midea%20portasplit"},
    {"name": "Landi CH", "url": "https://www.landi.ch/shop/search?text=midea%20portasplit"},
    {"name": "OBI CZ", "url": "https://www.obi.cz/search/midea%20portasplit"},
    {"name": "Google Shopping", "url": "https://www.google.com/search?tbm=shop&q=midea+portasplit"},
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
        except Exception:
            pass

    return min(prices) if prices else None


def is_relevant(text):
    t = text.lower()

    if "midea" not in t:
        return False

    porta_patterns = [
        "portasplit",
        "porta split",
        "porta-split",
        "mppd",
        "12000 btu",
        "12.000 btu",
        "12 000 btu",
        "mobile split",
        "mobiles split",
        "split klimaanlage",
        "split-klimaanlage",
        "mobiles klimagerät",
    ]

    if not any(pattern in t for pattern in porta_patterns):
        return False

    bad_words = [
        "zubehör",
        "ersatzteil",
        "filter",
        "schlauch",
        "fernbedienung",
        "halterung",
        "abdeckung",
        "adapter",
        "leitung",
        "ersatz",
        "bedienungsanleitung",
        "manual",
        "spare",
        "cover",
        "ersatzfilter",
        "dichtung",
    ]

    return not any(word in t for word in bad_words)


def search_generic(source):
    offers = []

    try:
        r = requests.get(
            source["url"],
            headers=HEADERS,
            timeout=30,
            allow_redirects=True
        )

        print(source["name"], "status:", r.status_code)

        if r.status_code != 200:
            return offers

        soup = BeautifulSoup(r.text, "lxml")
        blocks = soup.find_all(["article", "li", "div", "section"])

        for block in blocks:
            text = clean_text(block.get_text(" ", strip=True))

            if "midea" in text.lower():
                print(source["name"], "MATCH:", text[:200])

            if len(text) < 20:
                continue

            if len(text) > 1200:
                continue

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

            offers.append({
                "id": f"{source['name']}-{price}-{link}",
                "title": text[:150],
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
