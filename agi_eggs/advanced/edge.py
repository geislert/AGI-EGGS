"""Rugged edge node for off-grid deployments."""

from dataclasses import dataclass


@dataclass
class RuggedEdgeNode:
    location: str

    def __post_init__(self):
        self.hardware = {
            "solar_panels": "3kW foldable",
            "compute": "Raspberry Pi CMS",
            "comms": "LoRa/UAV-relay",
            "security": "EMP-hardened casing",
        }
        self.operational_mode = self.determine_operational_mode()

    def determine_operational_mode(self) -> str:
        if self.location:
            return "island" if "remote" in self.location else "grid"
        return "unknown"

    def island_mode_operation(self) -> str:
        return "maintaining operations via FractalEmergenceEngine"
