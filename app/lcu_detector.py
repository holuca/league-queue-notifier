from typing import Optional

import requests
import urllib3

urllib3.disable_warnings()


class LeagueClientDetector:
    def __init__(self) -> None:
        self.port: Optional[int] = None
        self.token: Optional[str] = None

    def configure(self, port: int, token: str) -> None:
        self.port = port
        self.token = token

    def get_phase(self) -> Optional[str]:
        if self.port is None or self.token is None:
            return None

        url = f"https://127.0.0.1:{self.port}/lol-gameflow/v1/gameflow-phase"

        try:
            response = requests.get(
                url,
                auth=("riot", self.token),
                verify=False,
                timeout=3,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None