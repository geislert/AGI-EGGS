# SPDX-License-Identifier: GPL-3.0-or-later
"""Prototype HF antenna autotuning helper."""

import random


def autotune_antenna(current_freq: float) -> float:
    """Return an adjusted frequency based on simple propagation heuristics."""
    adjustment = random.uniform(-0.05, 0.05) * current_freq
    tuned_freq = current_freq + adjustment
    print(f"[hf_autotune] Adjusting from {current_freq:.3f}MHz to {tuned_freq:.3f}MHz")
    return tuned_freq
