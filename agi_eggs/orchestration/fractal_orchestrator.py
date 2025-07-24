"""Fractal orchestration engine for hierarchical node management.
This is a simplified placeholder implementing automatic parent-child
negotiation and topology tracking.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class FractalNode:
    """Basic node with capability profile and parent-child links."""

    node_id: str
    capabilities: Dict[str, float]
    location: tuple
    parent: Optional["FractalNode"] = None
    children: List["FractalNode"] = field(default_factory=list)

    def layer(self) -> int:
        score = sum(self.capabilities.values())
        return max(0, int(math.log10(score)))

    def minimum_requirements(self) -> Dict[str, float]:
        return {k: v * 0.1 for k, v in self.capabilities.items()}

    def adopt_child(self, child: "FractalNode") -> bool:
        if self._can_support(child):
            child.parent = self
            self.children.append(child)
            return True
        return False

    def _can_support(self, child: "FractalNode") -> bool:
        req = child.minimum_requirements()
        for k, v in req.items():
            if self.capabilities.get(k, 0) * 0.8 < v:
                return False
        return True


class FractalOrchestrator:
    """Manages hierarchical relationships among nodes."""

    def __init__(self) -> None:
        self.root_nodes: List[FractalNode] = []

    def join(self, node: FractalNode) -> None:
        parent = self._find_parent(node)
        if parent:
            parent.adopt_child(node)
        else:
            self.root_nodes.append(node)

    def _find_parent(self, node: FractalNode) -> Optional[FractalNode]:
        candidates = [r for r in self.root_nodes if r.layer() >= node.layer()]
        candidates.sort(key=lambda n: self._distance(n.location, node.location))
        for cand in candidates:
            if cand.adopt_child(node):
                return cand
        return None

    @staticmethod
    def _distance(a: tuple, b: tuple) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
