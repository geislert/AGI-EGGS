"""Physical and power protection utilities."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable


@dataclass
class NodeGuardian:
    node_id: str
    criticality: int = 5
    protection_mode: str = "standard"  # standard|alert|lockdown
    active_services: int = 0
    on_alert: Callable[[str], None] | None = None

    def monitor_power(self, remaining_minutes: Callable[[], int]):
        """Monitor power and warn if it runs low."""
        while True:
            mins = remaining_minutes()
            if mins < 30:
                self._broadcast(
                    f"CRITICAL: node {self.node_id} power {mins}m left for"
                    f" {self.active_services} services"
                )
                if mins < 10:
                    self.protection_mode = "alert"
            time.sleep(60)

    def authorize_shutdown(self, allowed: bool, reason: str) -> bool:
        """Return True if shutdown allowed."""
        if not allowed and self.criticality >= 8:
            self._broadcast(
                f"Shutdown denied for {self.node_id}: critical services running"
            )
            return False
        self._broadcast(f"Shutdown for {self.node_id}: {reason}")
        return True

    def _broadcast(self, msg: str) -> None:
        if self.on_alert:
            self.on_alert(msg)
        else:
            print(f"[guardian] {msg}")

