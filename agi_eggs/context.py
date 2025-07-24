"""Shared system context placeholder."""
from dataclasses import dataclass

@dataclass
class SystemContext:
    power_state: str = "plenary"
    location_type: str = "unknown"
    security_level: int = 0

    def snapshot(self):
        return {
            "power_state": self.power_state,
            "location_type": self.location_type,
            "security_level": self.security_level,
        }

    @classmethod
    def from_snapshot(cls, data):
        return cls(
            power_state=data.get("power_state", "plenary"),
            location_type=data.get("location_type", "unknown"),
            security_level=data.get("security_level", 0),
        )

    @classmethod
    def current(cls):
        # In real system, gather actual context.
        return cls()
