import requests
from config import DISCORD_WEBHOOK_URL


def send_discord_message(message: str, mention_user_id: str = "") -> bool:
    if not DISCORD_WEBHOOK_URL:
        print("ERROR: Discord webhook URL is not configured.")
        return False

    mention_user_id = mention_user_id.strip()
    content = f"<@{mention_user_id}> {message}" if mention_user_id else message

    payload = {
        "content": content,
        "allowed_mentions": {"users": [mention_user_id]} if mention_user_id else {}
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"ERROR sending Discord message: {exc}")
        return False