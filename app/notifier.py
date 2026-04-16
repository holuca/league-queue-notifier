import requests
from config import DISCORD_WEBHOOK_URL


def send_discord_message(message: str) -> bool:
    if not DISCORD_WEBHOOK_URL:
        print("ERROR: Discord webhook URL is not configured.")
        return False

    payload = {"content": message}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"ERROR sending Discord message: {exc}")
        return False