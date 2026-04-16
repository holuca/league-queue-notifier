import requests
from config import DISCORD_WEBHOOK_URL


def send_discord_message(message: str) -> bool:
    if not DISCORD_WEBHOOK_URL:
        print("ERROR: DISCORD_WEBHOOK_URL is not set in .env")
        return False

    payload = {
        "content": message
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"ERROR sending Discord message: {e}")
        return False