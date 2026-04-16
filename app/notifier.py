import requests


def send_discord_message(webhook_url: str, message: str) -> bool:
    if not webhook_url:
        print("ERROR: Discord webhook URL is not configured.")
        return False

    payload = {"content": message}

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"ERROR sending Discord message: {exc}")
        return False