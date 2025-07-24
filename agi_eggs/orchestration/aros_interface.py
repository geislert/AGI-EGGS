"""Control interface for AROS."""
from __future__ import annotations

import time


class AROSInterface:
    MODES = ["automatic", "directed", "collaborative", "emergency"]

    def __init__(self) -> None:
        self.current_mode = "automatic"
        self.control_history = []

    def execute_command(self, func, *args, **kwargs):
        result = func(*args, **kwargs)
        self.control_history.append({"ts": time.time(), "cmd": func.__name__})
        return result

    def switch_mode(self, new_mode: str):
        if new_mode in self.MODES:
            self.control_history.append({"ts": time.time(), "mode": new_mode})
            self.current_mode = new_mode
