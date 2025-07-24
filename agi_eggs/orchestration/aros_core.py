"""Adaptive Resource Orchestration System core."""
from __future__ import annotations

import time
from collections import deque
from typing import Any, Dict

from ..ephemeral_mesh import SystemContext, PowerState


class AROSCore:
    """Simplified orchestration engine."""

    def __init__(self) -> None:
        self.context = SystemContext()
        self.operation_queue: deque = deque()
        self.adaptation_history = []

    def execute_cycle(self) -> Dict[str, Any]:
        """Run a single orchestration cycle."""
        self._check_environment()
        self._process_queue()
        return {"timestamp": time.time(), "queue_length": len(self.operation_queue)}

    def _check_environment(self) -> None:
        """Adapt when power state changes."""
        state = self.context.calculate_power_state()
        if state != self.context._power_state:
            self.context._power_state = state
            self.adaptation_history.append({"ts": time.time(), "state": state.name})

    def _process_queue(self) -> None:
        if not self.operation_queue:
            return
        task = self.operation_queue.popleft()
        task()

    def add_task(self, func) -> None:
        self.operation_queue.append(func)
