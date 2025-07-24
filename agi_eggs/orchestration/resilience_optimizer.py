"""Failure-resistant planning utilities."""
from __future__ import annotations

from typing import Dict, Any


class ResilienceOptimizer:
    """Add simple redundancy to allocation plans."""

    def harden_plan(self, allocation_plan: Dict[str, Any], threat_level: int) -> Dict[str, Any]:
        multiplier = 1.0
        if threat_level > 8:
            multiplier = 2.0
        elif threat_level > 5:
            multiplier = 1.5
        allocations = {k: v * multiplier for k, v in allocation_plan["allocations"].items()}
        return {"allocations": allocations}

    def handle_resource_gap(self, task) -> bool:
        return False
