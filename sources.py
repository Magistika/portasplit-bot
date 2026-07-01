import re
import requests
from bs4 import BeautifulSoup
from config import MAX_PRICE

SEARCH_TERMS = [
    "Midea PortaSplit 12000 BTU unter 900",
    "Midea PortaSplit 12.000 BTU 899",
    "Midea PortaSplit 3,5 kW kaufen",
    "Midea PortaSplit Klimaanlage Angebot",
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_price(text: str):
    text = text.replace(".", "").replace(",", ".")
    matches = re.findall(r"(\d+(?:\.\d{1,2})?)\s*€", text)
    prices = [float(x) for x in matches]
    return min(prices) if prices else None

def search_duckduckgo():
    offers = []

    for term in SEARCH_TERMS:
        url = "https://html.duckduckgo.com/html/?q=" + requests.utils.quote(term)

        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            print("DuckDuckGo status:", r.status_code)

            soup = BeautifulSoup(r.text, "lxml")

            for result in soup.select(".result"):
                title_el = result.select_one(".result__title")
                link_el = result.select_one(".result__a")
                snippet_el = result.select_one(".result__snippet")

                if not title_el or not link_el:
                    continue

                title = title_el.get_text(" ", strip=True)
                link = link_el.get("href", "")
                snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""

                combined = f"{title} {snippet}".lower()

                if "midea" not in combined or "portasplit" not in combined:
                    continue

                price = extract_price(combined)
                if price and price <= MAX_PRICE:
                    offers.append({
                        "id": link,
                        "title": title,
                        "price": price,
                        "url": link,
                        "source": "DuckDuckGo"
                    })

        except Exception as e:
            print("DuckDuckGo exception:", e)

    return offers

def search_all_sources():
    return search_duckduckgo()
