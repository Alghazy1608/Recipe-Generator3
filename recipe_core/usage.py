"""A simple shared daily limit, so one public app can't use up the owner's Gemini quota."""
from __future__ import annotations

import datetime as dt
import threading


class DailyLimit:
    def __init__(self, limit: int):
        self.limit, self.day, self.used = limit, None, 0
        self._lock = threading.Lock()

    def try_use(self, today: dt.date | None = None) -> bool:
        today = today or dt.date.today()
        with self._lock:
            if today != self.day:
                self.day, self.used = today, 0
            if self.used >= self.limit:
                return False
            self.used += 1
            return True
