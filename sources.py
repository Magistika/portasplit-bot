import re
import requests
from bs4 import BeautifulSoup
from config import MAX_PRICE

SEARCH_TERMS = [
    "Midea PortaSplit 12000 BTU",
    "Midea PortaSplit 12.000 BTU",
    "Midea PortaSplit 3,5 kW",
    "Midea PortaSplit Klimaanlage",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def extract_price(text: str):
    text = text.replace(".", "").replace(",", ".")
    matches = re.findall(r"(\d+(?:\.\d{1,2})?)\s*€", text)
    prices = [float(x) for x in matches]
    return min(prices) if prices else None


def search_ebay():
    offers = []

    for term in SEARCH_TERMS:
        url = "https://www.ebay.de/sch/i.html?_nkw=" + requests.utils.quote(term)

        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            print("eBay status:", r.status_code)

            soup = BeautifulSoup(r.text, "lxml")

            for item in soup.select(".s-item"):
                title_el = item.select_one(".s-item__title")
                price_el = item.select_one(".s-item__price")
                link_el = item.select_one(".s-item__link")

                if not title_el or not price_el or not link_el:
                    continue

                title = title_el.get_text(" ", strip=True)
                price_text = price_el.get_text(" ", strip=True)
                link = link_el.get("href")

                combined = title.lower()

                if "portasplit" not in combined:
                    continue

                if "midea" not in combined:
                    continue

                price = extract_price(price_text)

                if price and price <= MAX_PRICE:
                    offers.append({
                        "id": link,
                        "title": title,
                        "price": price,
                        "url": link,
                        "source": "eBay"
                    })

        except Exception as e:
            print("eBay exception:", e)

    return offers


def search_all_sources():
    return search_ebay()
