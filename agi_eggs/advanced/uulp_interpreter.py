"""Basic UULP interpreter for decoding and routing messages."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Dict

from .uulp import UULPMessage


@dataclass
class UULPInterpreter:
    """Decode :class:`UULPMessage` objects for internal routing."""

    def decode(self, message: UULPMessage) -> Dict[str, Any]:
        """Convert message content back to structured data."""
        if ":" not in message.content:
            return {"modality": "unknown", "data": message.content}
        modality, payload = message.content.split(":", 1)
        try:
            data = ast.literal_eval(payload)
        except Exception:
            data = payload
        return {"modality": modality, "data": data, "provenance": message.provenance}

    def route(self, message: UULPMessage) -> None:
        """Simple router example printing the decoded payload."""
        decoded = self.decode(message)
        print(f"[uulp-route] {decoded}")
