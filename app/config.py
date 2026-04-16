import json
from pathlib import Path

APP_DIR = Path.home() / "AppData" / "Local" / "LoLQueueNotifier"
CONFIG_PATH = APP_DIR / "config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {
            "discord_webhook_url": "",
            "poll_interval": 1.0,
        }

    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {
            "discord_webhook_url": "",
            "poll_interval": 1.0,
        }


def save_config(config: dict) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8",
    )