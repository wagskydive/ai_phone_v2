import json
import os
import time
from datetime import datetime


class CallScheduler:
    """Simple scheduler reading config from JSON."""

    def __init__(self, config_path: str = "app/config/schedule.json") -> None:
        self.config = self._load_config(config_path)
        self.last_call = 0.0

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def should_call_now(self) -> bool:
        """Return True if a call should be initiated."""
        if not self.config.get("enabled", False):
            return False
        now = datetime.now()
        hours = self.config.get("hours", {})
        start = hours.get("start", 9)
        end = hours.get("end", 17)
        if not start <= now.hour < end:
            return False
        interval = self.config.get("call_interval_minutes", 30)
        if time.time() - self.last_call >= interval * 60:
            self.last_call = time.time()
            return True
        return False
