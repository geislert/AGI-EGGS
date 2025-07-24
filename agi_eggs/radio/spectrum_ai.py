"""Adaptive Spectrum Intelligence utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class BandInfo:
    freq: float
    snr: float
    stability: float
    emergency_priority: int = 0

class SpectrumAI:
    def __init__(self, bands: List[BandInfo]):
        self.bands = bands

    def select_band(self, emergency_level: int = 0) -> BandInfo:
        """Return the optimal band based on SNR, stability and emergency level."""
        candidates = sorted(self.bands, key=lambda b: (b.emergency_priority if emergency_level else 0, b.snr, b.stability), reverse=True)
        return candidates[0] if candidates else BandInfo(freq=0, snr=0, stability=0)

    def activate_military_bands(self, location: str) -> BandInfo:
        """Placeholder for switching to special bands in crisis."""
        return BandInfo(freq=30.0, snr=20.0, stability=0.9, emergency_priority=10)
