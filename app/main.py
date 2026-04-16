import threading
import time
import tkinter as tk
from tkinter import ttk

from lcu_detector import LeagueClientDetector
from notifier import send_discord_message


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("LoL Queue Notifier")
        self.root.geometry("320x180")
        self.root.resizable(False, False)

        self.detector = LeagueClientDetector()

        self.monitoring_enabled = False
        self.notification_sent = False
        self.worker_thread = None
        self.stop_event = threading.Event()

        self.status_var = tk.StringVar(value="Idle")
        self.phase_var = tk.StringVar(value="Phase: -")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="League Queue Notifier", font=("Arial", 14, "bold"))
        title.pack(pady=(0, 12))

        self.status_label = ttk.Label(frame, textvariable=self.status_var)
        self.status_label.pack(pady=(0, 6))

        self.phase_label = ttk.Label(frame, textvariable=self.phase_var)
        self.phase_label.pack(pady=(0, 12))

        self.toggle_button = ttk.Button(frame, text="Notify me please", command=self.toggle_monitoring)
        self.toggle_button.pack(fill="x", pady=(0, 8))

        quit_button = ttk.Button(frame, text="Quit", command=self.on_close)
        quit_button.pack(fill="x")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_monitoring(self) -> None:
        if not self.monitoring_enabled:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def start_monitoring(self) -> None:
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
                        success = send_discord_message("🚨 RUN BACK — MATCH FOUND")
                        if success:
                            self.notification_sent = True
                            self.root.after(0, self.status_var.set, "Notification sent")
                        else:
                            self.root.after(0, self.status_var.set, "Failed to send notification")

                else:
                    self.root.after(0, self.status_var.set, f"Monitoring queue")
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
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()