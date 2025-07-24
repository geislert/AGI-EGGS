import numpy as np
from agi_eggs import autotune_antenna, denoise


def test_autotune_antenna():
    freq = 7.0
    tuned = autotune_antenna(freq)
    assert 6.5 <= tuned <= 7.5


def test_denoise():
    samples = np.array([0.0, 1.0, 0.0])
    out = denoise(samples)
    assert len(out) == 3
