"""Quality control representative for system integrity checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Callable


@dataclass
class QualityControlRepresentative:
    """Simple quality control agent.

    It checks readiness before handing control back to the user. When
    issues are detected it notifies maintenance via a callback.
    """

    maintenance_callback: Callable[[str], None]
    concerned_parties: List[str]

    def check_readiness(self, action: str) -> bool:
        """Return True if system is ready for user."""
        print(f"[qc] verifying action '{action}' with parties: {', '.join(self.concerned_parties)}")
        ready = True  # placeholder for complex checks
        if not ready:
            self.notify_maintenance(f"Action '{action}' failed QC")
        return ready

    def notify_maintenance(self, issue: str) -> None:
        """Send issue to maintenance system."""
        self.maintenance_callback(issue)
