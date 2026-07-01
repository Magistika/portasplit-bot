import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import MAX_PRICE

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SOURCES = [
    # Deutschland
    {"name": "Prosatech", "url": "https://www.prosatech.de/search?sSearch=midea%20portasplit"},
    {"name": "HORNBACH", "url": "https://www.hornbach.de/suche/?searchTerm=midea%20portasplit"},
    {"name": "Globus Baumarkt", "url": "https://www.globus-baumarkt.de/search?sSearch=midea%20portasplit"},
    {"name": "OTTO", "url": "https://www.otto.de/suche/midea%20portasplit/"},
    {"name": "BAUHAUS", "url": "https://www.bauhaus.info/suche/produkte?text=midea%20portasplit"},
    {"name": "OBI", "url": "https://www.obi.de/suche/midea%20portasplit/"},
    {"name": "hagebau", "url": "https://www.hagebau.de/suche/?q=midea%20portasplit"},
    {"name": "toom", "url": "https://toom.de/suche/?q=midea%20portasplit"},
    {"name": "Kaufland", "url": "https://www.kaufland.de/suche/?search_value=midea%20portasplit"},
    {"name": "Conrad", "url": "https://www.conrad.de/de/search.html?search=midea%20portasplit"},
    {"name": "Voelkner", "url": "https://www.voelkner.de/search?sSearch=midea%20portasplit"},
    {"name": "Galaxus DE", "url": "https://www.galaxus.de/de/search?q=midea+portasplit"},

    # Amazon
    {"name": "Amazon DE", "url": "https://www.amazon.de/s?k=midea+portasplit"},
    {"name": "Amazon PL", "url": "https://www.amazon.pl/s?k=midea+portasplit"},
    {"name": "Amazon IT", "url": "https://www.amazon.it/s?k=midea+portasplit"},
    {"name": "Amazon FR", "url": "https://www.amazon.fr/s?k=midea+portasplit"},
    {"name": "Amazon ES", "url": "https://www.amazon.es/s?k=midea+portasplit"},
    {"name": "Amazon NL", "url": "https://www.amazon.nl/s?k=midea+portasplit"},

    # Marktplätze
    {"name": "Kleinanzeigen", "url": "https://www.kleinanzeigen.de/s-midea-portasplit/k0"},
    {"name": "eBay DE", "url": "https://www.ebay.de/sch/i.html?_nkw=midea+portasplit"},
    {"name": "eBay FR", "url": "https://www.ebay.fr/sch/i.html?_nkw=midea+portasplit"},
    {"name": "eBay IT", "url": "https://www.ebay.it/sch/i.html?_nkw=midea+portasplit"},
    {"name": "eBay PL", "url": "https://www.ebay.pl/sch/i.html?_nkw=midea+portasplit"},

    # Preisvergleich
    {"name": "Idealo", "url": "https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q=midea+portasplit"},
    {"name": "Google Shopping", "url": "https://www.google.com/search?tbm=shop&q=midea+portasplit"},

    # Frankreich
    {"name": "ManoMano FR", "url": "https://www.manomano.fr/s/midea-portasplit"},
    {"name": "Leroy Merlin FR", "url": "https://www.leroymerlin.fr/recherche/?q=midea%20portasplit"},
    {"name": "Brico Depot FR", "url": "https://www.bricodepot.fr/recherche/midea%20portasplit"},
    {"name": "Fnac FR", "url": "https://www.fnac.com/SearchResult/ResultList.aspx?Search=midea+portasplit"},
    {"name": "Rakuten FR", "url": "https://fr.shopping.rakuten.com/s/midea+portasplit"},

    # Italien
    {"name": "Bricoman IT", "url": "https://www.bricoman.it/search?q=midea%20portasplit"},

    # Polen
    {"name": "Allegro PL", "url": "https://allegro.pl/listing?string=midea%20portasplit"},
    {"name": "Ceneo PL", "url": "https://www.ceneo.pl/;szukaj-midea+portasplit"},

    # Niederlande
    {"name": "Bol NL", "url": "https://www.bol.com/nl/nl/s/?searchtext=midea+portasplit"},

    # Schweiz
    {"name": "Galaxus CH", "url": "https://www.galaxus.ch/de/search?q=midea+portasplit"},
    {"name": "Digitec CH", "url": "https://www.digitec.ch/de/search?q=midea+portasplit"},
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

            offers.append({
                "id": f"{source['name']}-{price}-{link}",
                "title": text[:120],
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
