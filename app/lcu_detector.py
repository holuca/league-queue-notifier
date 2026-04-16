from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
import urllib3

urllib3.disable_warnings()


LOCKFILE_PATH = Path(r"C:\Riot Games\League of Legends\lockfile")


@dataclass
class LcuCredentials:
    port: int
    token: str
    protocol: str


class LeagueClientDetector:
    def __init__(self) -> None:
        self._credentials: Optional[LcuCredentials] = None

    def get_phase(self) -> Optional[str]:
        credentials = self._get_credentials()
        if credentials is None:
            return None

        url = f"{credentials.protocol}://127.0.0.1:{credentials.port}/lol-gameflow/v1/gameflow-phase"

        try:
            response = requests.get(
                url,
                auth=("riot", credentials.token),
                verify=False,
                timeout=3,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            print(f"DEBUG request failed: {exc}")
            self._credentials = None
            return None

    def _get_credentials(self) -> Optional[LcuCredentials]:
        if self._credentials is not None:
            return self._credentials

        if not LOCKFILE_PATH.exists():
            print(f"DEBUG lockfile not found at: {LOCKFILE_PATH}")
            return None

        try:
            content = LOCKFILE_PATH.read_text(encoding="utf-8").strip()
            # format: process_name:pid:port:token:protocol
            parts = content.split(":")
            if len(parts) != 5:
                print(f"DEBUG unexpected lockfile format: {content}")
                return None

            _, _, port, token, protocol = parts

            credentials = LcuCredentials(
                port=int(port),
                token=token,
                protocol=protocol,
            )
            self._credentials = credentials
            print(
                f"DEBUG loaded credentials: port={credentials.port}, "
                f"protocol={credentials.protocol}"
            )
            return credentials

        except Exception as exc:
            print(f"DEBUG failed reading lockfile: {exc}")
            return None