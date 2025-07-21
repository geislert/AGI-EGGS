# AGI-EGGS node abstraction
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import json
from dataclasses import dataclass, field
from typing import Callable, Dict, Any


@dataclass
class Message:
    """Simple message container for inter-node communication."""
    sender: str
    content: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({'sender': self.sender, 'content': self.content})

    @staticmethod
    def from_json(data: str) -> 'Message':
        payload = json.loads(data)
        return Message(sender=payload['sender'], content=payload['content'])


class Node:
    """Base class for network-connected nodes."""
    def __init__(self, name: str, host: str = 'localhost', port: int = 8765):
        self.name = name
        self.host = host
        self.port = port
        self.handlers: Dict[str, Callable[[Message], None]] = {}

    def on(self, key: str):
        """Decorator to register a handler for a message key."""
        def decorator(handler: Callable[[Message], None]):
            self.handlers[key] = handler
            return handler

        return decorator

    async def handle_message(self, message: Message):
        key = message.content.get('key')
        if key in self.handlers:
            await asyncio.create_task(self.handlers[key](message))

    async def send(self, writer: asyncio.StreamWriter, content: Dict[str, Any]):
        msg = Message(sender=self.name, content=content)
        data = msg.to_json().encode() + b'\n'
        writer.write(data)
        await writer.drain()


class PiNode(Node):
    """Raspberry Pi device."""
    pass


class EggNode(Node):
    """AGI Egg device."""
    pass
