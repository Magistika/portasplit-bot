import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send(msg: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    r = requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg
        },
        timeout=30
    )

    print("Telegram Status:", r.status_code)
    print("Telegram Response:", r.text)