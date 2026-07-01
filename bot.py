from notifier import send
from sources import search_all_sources
from database import already_sent, mark_sent


def run():
    offers = search_all_sources()

    if not offers:
        print("Keine passenden Angebote gefunden.")
        return

    for offer in offers:
        if already_sent(offer["id"]):
            print("Bereits gemeldet:", offer["source"])
            continue

        message = (
            f"🚨 Midea PortaSplit gefunden!\n\n"
            f"Quelle: {offer['source']}\n"
            f"Preis: {offer['price']} €\n"
            f"Link:\n{offer['url']}"
        )

        send(message)
        mark_sent(offer["id"])

        print("Sent alert:", offer["source"])


if __name__ == "__main__":
    run()
