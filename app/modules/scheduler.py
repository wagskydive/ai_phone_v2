import json
import os
import time
import random
from datetime import datetime
from typing import Callable


class CallScheduler:
    """Simple scheduler reading config from JSON."""

    def __init__(self, config_path: str = "app/config/schedule.json",
                 now_fn: Callable[[], datetime] | None = None) -> None:
        self.config = self._load_config(config_path)
        self.last_call = 0.0
        # allow injection of current time for tests
        self.now_fn = now_fn or datetime.now
        # determine interval with jitter for first call
        self.next_interval = self._calculate_interval()

    def _calculate_interval(self) -> float:
        """Return call interval in minutes including jitter."""
        base = self.config.get("call_interval_minutes", 30)
        jitter = self.config.get("jitter_minutes", 0)
        if jitter <= 0:
            return float(base)
        return float(base) + random.uniform(-jitter, jitter)

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
        now = self.now_fn()
        hours = self.config.get("hours", {})
        start = hours.get("start", 9)
        end = hours.get("end", 17)
        if not start <= now.hour < end:
            return False
        if time.time() - self.last_call >= self.next_interval * 60:
            self.last_call = time.time()
            # calculate next interval for subsequent calls
            self.next_interval = self._calculate_interval()
            return True
        return False
