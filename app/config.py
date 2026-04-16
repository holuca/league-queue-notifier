import json
from pathlib import Path

APP_DIR = Path.home() / "AppData" / "Local" / "LoLQueueNotifier"
CONFIG_PATH = APP_DIR / "config.json"


def default_config() -> dict:
    return {
        "discord_webhook_url": "",
        "mention_user_id": "",
        "custom_message": "RUN BACK YOU FOOL",
        "poll_interval": 1.0,
    }


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return default_config()

    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        merged = default_config()
        merged.update(data)
        return merged
    except Exception:
        return default_config()


def save_config(config: dict) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8",
    )