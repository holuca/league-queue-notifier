import threading
import time
import tkinter as tk
from tkinter import ttk

from config import load_config, save_config
from lcu_detector import LeagueClientDetector
from notifier import send_discord_message


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("LoL Queue Notifier")
        self.root.geometry("430x430")
        self.root.resizable(False, False)

        self.detector = LeagueClientDetector()

        self.monitoring_enabled = False
        self.notification_sent = False
        self.worker_thread = None
        self.stop_event = threading.Event()

        config = load_config()

        self.webhook_var = tk.StringVar(value=config.get("discord_webhook_url", ""))
        self.mention_user_id_var = tk.StringVar(value=config.get("mention_user_id", ""))
        self.custom_message_var = tk.StringVar(
            value=config.get("custom_message", "RUN BACK YOU FOOL — MATCH IS FOUND")
        )
        self.status_var = tk.StringVar(value="Idle")
        self.phase_var = tk.StringVar(value="Phase: -")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="League Queue Notifier",
            font=("Arial", 14, "bold"),
        ).pack(pady=(0, 12))

        ttk.Label(frame, text="Discord Webhook URL").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.webhook_var).pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Discord User ID for ping (optional)").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.mention_user_id_var).pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Custom message").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.custom_message_var).pack(fill="x", pady=(0, 12))

        ttk.Label(frame, textvariable=self.status_var).pack(pady=(0, 4))
        ttk.Label(frame, textvariable=self.phase_var).pack(pady=(0, 12))

        ttk.Button(frame, text="Save settings", command=self.save_settings).pack(fill="x", pady=(0, 8))
        ttk.Button(frame, text="Test Discord", command=self.test_discord).pack(fill="x", pady=(0, 8))

        self.toggle_button = ttk.Button(
            frame,
            text="Notify me please",
            command=self.toggle_monitoring,
        )
        self.toggle_button.pack(fill="x", pady=(0, 8))

        ttk.Button(frame, text="Quit", command=self.on_close).pack(fill="x")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_current_config(self) -> dict:
        return {
            "discord_webhook_url": self.webhook_var.get().strip(),
            "mention_user_id": self.mention_user_id_var.get().strip(),
            "custom_message": self.custom_message_var.get().strip() or "🚨 RUN BACK — MATCH FOUND",
            "poll_interval": 1.0,
        }

    def save_settings(self) -> None:
        config = self.get_current_config()
        save_config(config)
        self.status_var.set("Settings saved")

    def test_discord(self) -> None:
        config = self.get_current_config()
        success = send_discord_message(
            webhook_url=config["discord_webhook_url"],
            message=config["custom_message"],
            mention_user_id=config["mention_user_id"],
        )

        if success:
            self.status_var.set("Test notification sent")
        else:
            self.status_var.set("Test notification failed")

    def toggle_monitoring(self) -> None:
        if not self.monitoring_enabled:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def start_monitoring(self) -> None:
        config = self.get_current_config()

        if not config["discord_webhook_url"]:
            self.status_var.set("Please enter a Discord webhook URL")
            return

        save_config(config)

        self.monitoring_enabled = True
        self.notification_sent = False
        self.stop_event.clear()

        self.status_var.set("Monitoring queue")
        self.toggle_button.config(text="Stop notifying me")

        self.worker_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.worker_thread.start()

    def stop_monitoring(self) -> None:
        self.monitoring_enabled = False
        self.stop_event.set()
        self.status_var.set("Idle")
        self.phase_var.set("Phase: -")
        self.toggle_button.config(text="Notify me please")

    def monitor_loop(self) -> None:
        last_phase = None

        while not self.stop_event.is_set():
            try:
                phase = self.detector.get_phase()

                if phase != last_phase:
                    self.root.after(0, self.phase_var.set, f"Phase: {phase or '-'}")
                    last_phase = phase

                if phase is None:
                    self.root.after(0, self.status_var.set, "League client not found")
                    self.notification_sent = False

                elif phase == "ReadyCheck":
                    self.root.after(0, self.status_var.set, "Match found")

                    if not self.notification_sent:
                        config = load_config()

                        success = send_discord_message(
                            webhook_url=config.get("discord_webhook_url", ""),
                            message=config.get("custom_message", "RUN YOU FOOL"),
                            mention_user_id=config.get("mention_user_id", ""),
                        )

                        if success:
                            self.notification_sent = True
                            self.root.after(0, self.status_var.set, "Notification sent")
                        else:
                            self.root.after(0, self.status_var.set, "Failed to send notification")

                else:
                    self.root.after(0, self.status_var.set, "Monitoring queue")
                    self.notification_sent = False

            except Exception as exc:
                self.root.after(0, self.status_var.set, f"Error: {exc}")
                self.notification_sent = False

            time.sleep(1.0)

    def on_close(self) -> None:
        self.stop_monitoring()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()