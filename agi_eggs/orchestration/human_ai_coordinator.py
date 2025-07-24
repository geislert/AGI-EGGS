"""Coordinate human and AI tasks."""
from __future__ import annotations

from typing import List, Dict, Any


class HumanAICoordinator:
    def __init__(self) -> None:
        self.assignments: Dict[str, List[Any]] = {}

    def assign_tasks(self, tasks, humans):
        self.assignments = {h.id: [] for h in humans}
        ai_tasks = []
        for task in tasks:
            if getattr(task, "automatable", False):
                ai_tasks.append(task)
            else:
                if humans:
                    self.assignments[humans[0].id].append(task)
        return {"ai_tasks": ai_tasks, "human_tasks": self.assignments}

    def deliver_assignments(self, human, tasks):
        pass

    def broadcast_alert(self, message):
        pass
