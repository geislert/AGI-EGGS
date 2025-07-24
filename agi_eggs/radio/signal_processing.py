# SPDX-License-Identifier: GPL-3.0-or-later
"""Simplified AI-enhanced signal processing helpers."""

import numpy as np


def denoise(samples: np.ndarray) -> np.ndarray:
    """Apply a trivial moving average filter to noisy samples."""
    if len(samples) < 3:
        return samples
    kernel = np.ones(3) / 3
    return np.convolve(samples, kernel, mode="same")
