"""Utility for switching models based on available resources."""

import psutil

MODELS = {
    'high': 'phi3-mini',
    'medium': 'distilbert',
    'low': 'tinylstm'
}

def select_model() -> str:
    """Return the model name appropriate for current system memory."""
    mem = psutil.virtual_memory().total / (1024**2)  # MB
    if mem > 2000:
        return MODELS['high']
    if mem > 512:
        return MODELS['medium']
    return MODELS['low']
