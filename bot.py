from notifier import send
from sources import search_all_sources


def run():
    offers = search_all_sources()

   if not offers:
    print("Keine passenden Angebote gefunden.")
    send("✅ PortaSplit Bot läuft. Aktuell keine Angebote ≤ 900 € gefunden.")
    return 

    for offer in offers:
        message = (
            "🚨 PortaSplit Angebot gefunden!\n\n"
            f"Quelle: {offer['source']}\n"
            f"Titel: {offer['title']}\n"
            f"Preis: {offer['price']:.2f} €\n"
            f"Link: {offer['url']}"
        )
        send(message)
        print("Sent alert:", offer["title"])


if __name__ == "__main__":
    run()
