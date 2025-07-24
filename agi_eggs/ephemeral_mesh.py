# SPDX-License-Identifier: GPL-3.0-or-later
"""Ephemeral mesh networking module with adaptive contraction.

This implementation provides dynamic shrinking and expansion based on
available power and environmental context. It is a simplified version of
the longer design provided in the specification and can be extended in
future iterations.
"""

from __future__ import annotations

import json
import time
import zlib
from enum import Enum
from typing import Dict, Any, List


class PowerState(Enum):
    """Power availability levels."""
    PLENARY = 0
    CONSERVATION = 1
    ECHO_SEED = 2
    CRYPTOBIOSIS = 3


PROTOCOL_POWER_MAP = {
    "LoRaWAN": PowerState.CONSERVATION,
    "WiFiDirect": PowerState.PLENARY,
    "HF_Burst": PowerState.ECHO_SEED,
    "Acoustic": PowerState.CRYPTOBIOSIS,
}

EPHEMERAL_RETENTION = {
    PowerState.PLENARY: 3600,
    PowerState.CONSERVATION: 28800,
    PowerState.ECHO_SEED: 86400,
    PowerState.CRYPTOBIOSIS: 604800,
}


class HardwareProfile:
    """Detect available hardware and energy input."""

    def __init__(self) -> None:
        self.capabilities = self.detect_hardware()

    def detect_hardware(self) -> Dict[str, Any]:
        return {
            "power_source": "battery",
            "comms": ["LoRaWAN", "BLE"],
            "sensors": ["accelerometer", "thermometer"],
            "harvesters": ["solar"],
        }

    def energy_balance(self) -> Dict[str, int]:
        return {"input": 15, "output": 8, "reserves": 3600}


class SystemContext:
    """Track environment and compute reduced profiles."""

    def __init__(self) -> None:
        self.hardware = HardwareProfile()
        self._power_state = self.calculate_power_state()
        self._emergency_context = "normal"

    def calculate_power_state(self) -> PowerState:
        energy = self.hardware.energy_balance()
        if energy["reserves"] > 7200:
            return PowerState.PLENARY
        if energy["reserves"] > 1800:
            return PowerState.CONSERVATION
        if energy["reserves"] > 300:
            return PowerState.ECHO_SEED
        return PowerState.CRYPTOBIOSIS

    def contract_profile(self) -> Dict[str, List[str]]:
        profile = {
            "comms": ["HF_Burst"],
            "sensors": ["thermometer"],
            "functions": ["sos", "location_broadcast"],
        }
        if self._emergency_context == "flood":
            profile["sensors"].append("water_sensor")
        return profile

    def expand_profile(self) -> Dict[str, List[str]]:
        return {
            "comms": list(PROTOCOL_POWER_MAP.keys()),
            "sensors": self.hardware.capabilities["sensors"],
            "functions": ["sos", "location_broadcast", "status"]
        }


class LZ4CompressedCache:
    """Simplified message cache using zlib for now."""

    def __init__(self, max_size_kb: int = 10) -> None:
        self.cache: List[bytes] = []
        self.max_size = max_size_kb * 1024

    def append(self, message: Dict[str, Any]) -> None:
        data = json.dumps(message).encode()
        compressed = zlib.compress(data, 9)
        self.cache.append(compressed)
        self._trim()

    def _trim(self) -> None:
        size = sum(len(c) for c in self.cache)
        while size > self.max_size and self.cache:
            removed = self.cache.pop(0)
            size -= len(removed)


class EphemeralMeshNode:
    """Node that can contract capabilities when power is low."""

    def __init__(self, node_id: str, context: SystemContext) -> None:
        self.node_id = node_id
        self.context = context
        self.operational_profile = context.contract_profile()
        self.message_cache = LZ4CompressedCache(max_size_kb=5)
        self.current_protocol = self.select_protocol()

    def select_protocol(self) -> str:
        for proto in self.operational_profile["comms"]:
            if PROTOCOL_POWER_MAP[proto].value <= self.context._power_state.value:
                return proto
        return "HF_Burst"

    def dynamic_contraction(self) -> None:
        if self.context._power_state in (PowerState.ECHO_SEED, PowerState.CRYPTOBIOSIS):
            self.operational_profile = self.context.contract_profile()
            self.compress_knowledge()

    def compress_knowledge(self) -> None:
        combined = b"".join(self.message_cache.cache)
        self.message_cache.cache = [zlib.compress(combined, 9)]

    def expand_capabilities(self, energy_available: int) -> None:
        if energy_available > 1000:
            self.operational_profile = self.context.expand_profile()

    def send_ephemeral_message(self, content: str, msg_type: str = "vital") -> None:
        package = {
            "src": self.node_id,
            "type": msg_type,
            "ts": int(time.time()),
            "data": content,
        }
        self.message_cache.append(package)
        # Actual transmission would go here

