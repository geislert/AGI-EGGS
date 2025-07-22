from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Message


class MessageStore:
    """Simple on-disk store for queued messages."""

    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, message: "Message") -> None:
        with self.path.open("a", encoding="utf-8") as f:
            json.dump(asdict(message), f)
            f.write("\n")

    def read_all(self) -> List["Message"]:
        from .node import Message

        messages: List[Message] = []
        if not self.path.exists():
            return messages
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                payload = json.loads(line)
                messages.append(Message(**payload))
        self.path.unlink()
        return messages
