"""Voice-based command gateway with risk assessment."""

from __future__ import annotations

from .network_sentinel import NodeGuardian
from dataclasses import dataclass
from typing import Callable


@dataclass
class CognitiveGuardian:
    guardian: NodeGuardian
    risk_check: Callable[[str], float] | None = None

    def process_command(self, command: str) -> bool:
        """Evaluate and execute a command if allowed."""
        risk = self.risk_check(command) if self.risk_check else 0.0
        if risk > 8.0:
            self.guardian._broadcast(
                f"Command '{command}' blocked due to high risk ({risk})"
            )
            return False
        if risk > 5.0:
            self.guardian._broadcast(f"Confirm command '{command}' (risk {risk})")
            # In real system require confirmation
        self.guardian._broadcast(f"Executing {command}")
        return True

