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
    {"name": "Kleinanzeigen", "url": "https://www.kleinanzeigen.de/s-midea-portasplit/k0"},

    {"name": "BAUHAUS", "url": "https://www.bauhaus.info/suche/produkte?text=midea%20portasplit"},
    {"name": "OBI", "url": "https://www.obi.de/suche/midea%20portasplit/"},
    {"name": "hagebau", "url": "https://www.hagebau.de/suche/?q=midea%20portasplit"},
    {"name": "toom", "url": "https://toom.de/suche/?q=midea%20portasplit"},

    {"name": "MediaMarkt DE", "url": "https://www.mediamarkt.de/de/search.html?query=midea%20portasplit"},
    {"name": "Saturn", "url": "https://www.saturn.de/de/search.html?query=midea%20portasplit"},
    {"name": "Expert", "url": "https://www.expert.de/shop/search?query=midea%20portasplit"},
    {"name": "Conrad", "url": "https://www.conrad.de/de/search.html?search=midea%20portasplit"},
    {"name": "Voelkner", "url": "https://www.voelkner.de/search?sSearch=midea%20portasplit"},

    {"name": "Kaufland", "url": "https://www.kaufland.de/suche/?search_value=midea%20portasplit"},
    {"name": "Idealo", "url": "https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q=midea%20portasplit"},
    {"name": "Geizhals", "url": "https://geizhals.de/?fs=midea+portasplit"},

    {"name": "Klimaworld", "url": "https://www.klimaworld.com/catalogsearch/result/?q=midea%20portasplit"},
    {"name": "Selfio", "url": "https://www.selfio.de/catalogsearch/result/?q=midea%20portasplit"},
    {"name": "Kältebringer", "url": "https://www.kaeltebringer.de/search?sSearch=midea%20portasplit"},

    # Amazon
    {"name": "Amazon DE", "url": "https://www.amazon.de/s?k=midea+portasplit"},
    {"name": "Amazon FR", "url": "https://www.amazon.fr/s?k=midea+portasplit"},
    {"name": "Amazon IT", "url": "https://www.amazon.it/s?k=midea+portasplit"},
    {"name": "Amazon ES", "url": "https://www.amazon.es/s?k=midea+portasplit"},
    {"name": "Amazon NL", "url": "https://www.amazon.nl/s?k=midea+portasplit"},
    {"name": "Amazon PL", "url": "https://www.amazon.pl/s?k=midea+portasplit"},

    # eBay
    {"name": "eBay DE", "url": "https://www.ebay.de/sch/i.html?_nkw=midea+portasplit"},
    {"name": "eBay FR", "url": "https://www.ebay.fr/sch/i.html?_nkw=midea+portasplit"},
    {"name": "eBay IT", "url": "https://www.ebay.it/sch/i.html?_nkw=midea+portasplit"},
    {"name": "eBay PL", "url": "https://www.ebay.pl/sch/i.html?_nkw=midea+portasplit"},

    # Österreich
    {"name": "MediaMarkt AT", "url": "https://www.mediamarkt.at/de/search.html?query=midea%20portasplit"},
    {"name": "Willhaben", "url": "https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz?keyword=midea%20portasplit"},
    {"name": "Geizhals AT", "url": "https://geizhals.at/?fs=midea+portasplit"},
    {"name": "Alza AT", "url": "https://www.alza.at/search.htm?exps=midea%20portasplit"},

    # Schweiz
    {"name": "Ricardo CH", "url": "https://www.ricardo.ch/de/s/midea%20portasplit"},
    {"name": "Digitec CH", "url": "https://www.digitec.ch/de/search?q=midea%20portasplit"},
    {"name": "Galaxus CH", "url": "https://www.galaxus.ch/de/search?q=midea%20portasplit"},
    {"name": "Brack CH", "url": "https://www.brack.ch/search?query=midea%20portasplit"},

    # Tschechien
    {"name": "Alza CZ", "url": "https://www.alza.cz/search.htm?exps=midea%20portasplit"},
    {"name": "Heureka CZ", "url": "https://www.heureka.cz/?h%5Bfraze%5D=midea+portasplit"},
    {"name": "Mall CZ", "url": "https://www.mall.cz/hledani?query=midea%20portasplit"},
    {"name": "CZC", "url": "https://www.czc.cz/hledat?q=midea%20portasplit"},
    {"name": "Datart", "url": "https://www.datart.cz/vyhledavani.html?search=midea%20portasplit"},
    {"name": "Bazos CZ", "url": "https://www.bazos.cz/search.php?hledat=midea%20portasplit"},

    # Polen / Niederlande
    {"name": "Ceneo PL", "url": "https://www.ceneo.pl/;szukaj-midea+portasplit"},
    {"name": "Bol NL", "url": "https://www.bol.com/nl/nl/s/?searchtext=midea+portasplit"},

       # Weitere Marktplätze
    {"name": "Willhaben AT", "url": "https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz?keyword=midea%20portasplit"},
    {"name": "Ricardo CH", "url": "https://www.ricardo.ch/de/s/midea%20portasplit"},
    {"name": "Bazos CZ", "url": "https://www.bazos.cz/search.php?hledat=midea%20portasplit"},

    # Preisvergleich
    {"name": "Geizhals AT", "url": "https://geizhals.at/?fs=midea+portasplit"},
    {"name": "Heureka CZ", "url": "https://www.heureka.cz/?h%5Bfraze%5D=midea+portasplit"},
    
    # Sonstige
    {"name": "Google Shopping", "url": "https://www.google.com/search?tbm=shop&q=midea+portasplit"}
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
        "halterung",
        "abdeckung",
        "adapter",
        "leitung",
        "ersatz",
        "bedienungsanleitung",
        "manual",
        "spare",
        "cover"
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
