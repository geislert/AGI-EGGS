# SPDX-License-Identifier: GPL-3.0-or-later
"""Neighbor tracking with automatic score decay."""

from __future__ import annotations


class SurvivalGraph:
    def __init__(self, decay_rate: float = 0.95) -> None:
        self.graph = {}
        self.decay_rate = decay_rate

    def update_neighbor(self, node_id: str, capabilities) -> None:
        if node_id not in self.graph:
            self.graph[node_id] = {"score": 1.0, "caps": capabilities}
        else:
            self.graph[node_id]["score"] = min(1.0, self.graph[node_id]["score"] * 0.5 + 0.5)

    def decay_scores(self) -> None:
        to_del = []
        for node, data in self.graph.items():
            data["score"] *= self.decay_rate
            if data["score"] < 0.01:
                to_del.append(node)
        for node in to_del:
            del self.graph[node]

    def rank_by_capability(self, emergency_type: str):
        def score(data):
            caps = data["caps"]
            if emergency_type == "fire" and "thermometer" in caps:
                return data["score"] + 1
            if emergency_type == "flood" and "water_sensor" in caps:
                return data["score"] + 1
            return data["score"]

        return sorted(self.graph.keys(), key=lambda n: score(self.graph[n]), reverse=True)

