from notifier import send

def search():
    # Placeholder: replace with real sources later
    return [
        {
            "id": "test-1",
            "title": "Midea PortaSplit Test Offer",
            "price": 899,
            "url": "https://example.com"
        }
    ]

def run():
    offers = search()

    for o in offers:
        if o["price"] <= 900:
            send(f"🚨 Angebot gefunden!\n{o['title']}\n{o['price']}€\n{o['url']}")
            print("Sent alert")

if __name__ == "__main__":
    run()
