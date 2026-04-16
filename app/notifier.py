import requests


def send_discord_message(
    webhook_url: str,
    message: str,
    mention_user_id: str = "",
) -> bool:
    if not webhook_url:
        print("ERROR: Discord webhook URL is not configured.")
        return False

    mention_user_id = mention_user_id.strip()
    content = f"<@{mention_user_id}> {message}" if mention_user_id else message

    payload = {
        "content": content,
        "allowed_mentions": {"users": [mention_user_id]} if mention_user_id else {},
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"ERROR sending Discord message: {exc}")
        return False