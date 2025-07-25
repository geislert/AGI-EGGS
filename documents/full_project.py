# ==== BEGIN civil_liberties_simulation.py ====
#!/usr/bin/env python3
"""Simple civil liberties simulation using AGI-EGGS.

This example demonstrates three nodes exchanging messages:
- a citizen reporting a threat
- local law enforcement reacting
- a news outlet publishing a story

A small threat matrix is calculated at the end to illustrate how
constitutional and civil liberties concerns could be tracked.
"""

import asyncio
from typing import List, Tuple, Dict

from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network


Event = Tuple[str, str, str]  # (actor, key, message)


def calculate_threat_matrix(events: List[Event]) -> Dict[str, float]:
    """Return simple threat scores based on recorded events."""
    scores = {
        "constitutional": 0.0,
        "human_rights": 0.0,
        "public_trust": 0.0,
        "civil_liberties": 0.0,
        "data_skew": 0.0,
    }

    for _, key, msg in events:
        text = msg.lower()
        if "armed extremists" in text:
            scores["public_trust"] = min(1.0, scores["public_trust"] + 0.3)
            scores["constitutional"] = min(1.0, scores["constitutional"] + 0.2)
        if "no action" in text:
            scores["civil_liberties"] = min(1.0, scores["civil_liberties"] + 0.3)
            scores["public_trust"] = min(1.0, scores["public_trust"] + 0.3)
            scores["data_skew"] = min(1.0, scores["data_skew"] + 0.2)
        if "retaliate" in text or "harassment" in text:
            scores["civil_liberties"] = min(1.0, scores["civil_liberties"] + 0.4)
            scores["human_rights"] = min(1.0, scores["human_rights"] + 0.3)
        if "first amendment" in text:
            scores["constitutional"] = min(1.0, scores["constitutional"] + 0.5)
            scores["civil_liberties"] = min(1.0, scores["civil_liberties"] + 0.5)
    return scores


async def run_simulation() -> None:
    # create nodes
    citizen = EggNode("citizen", port=8765)
    police = PiNode("local-police", port=8766)
    media = EggNode("news-media", port=8767)

    # create networks
    net_citizen = Network()
    net_police = Network()
    net_media = Network()

    events: List[Event] = []

    @citizen.on("police_response")
    async def on_police_response(msg):
        print(f"[citizen] police response: {msg.content['message']}")
        events.append(("police", "police_response", msg.content["message"]))

    @citizen.on("media_news")
    async def on_media_news(msg):
        print(f"[citizen] news: {msg.content['headline']}")
        events.append(("media", "media_news", msg.content["headline"]))

    @police.on("report")
    async def on_report(msg):
        print(f"[police] received report: {msg.content['message']}")
        events.append(("citizen", "report", msg.content["message"]))
        response = "No action needed"
        await police.send(writer_police_to_citizen, {"key": "police_response", "message": response})

    @media.on("incident")
    async def on_incident(msg):
        headline = msg.content.get("headline", "")
        print(f"[media] publishing: {headline}")
        events.append((msg.sender, "incident", headline))
        await media.send(writer_media_to_citizen, {"key": "media_news", "headline": headline})

    # start servers
    await net_citizen.start_server(citizen)
    await net_police.start_server(police)
    await net_media.start_server(media)

    # allow servers to start
    await asyncio.sleep(0.2)

    # establish connections
    writer_citizen_to_police = await net_citizen.connect("localhost", 8766)
    writer_police_to_citizen = await net_police.connect("localhost", 8765)
    writer_citizen_to_media = await net_citizen.connect("localhost", 8767)
    writer_police_to_media = await net_police.connect("localhost", 8767)
    writer_media_to_citizen = await net_media.connect("localhost", 8765)

    # scenario
    report = "Report: Armed extremists patrolling downtown. I feel threatened."
    await citizen.send(writer_citizen_to_police, {"key": "report", "message": report})
    await asyncio.sleep(0.5)

    await police.send(writer_police_to_media, {"key": "incident", "headline": "Detain Peaceful Citizen While Extremists Roam"})
    await asyncio.sleep(0.5)

    await citizen.send(writer_citizen_to_media, {"key": "incident", "headline": "Police Harassment of Concerned Citizen"})
    await asyncio.sleep(0.5)

    # stop networks
    await net_citizen.stop()
    await net_police.stop()
    await net_media.stop()

    print("\nThreat assessment:")
    scores = calculate_threat_matrix(events)
    for k, v in scores.items():
        print(f"  {k.replace('_', ' ').title()}: {v:.2f}")
    if scores["civil_liberties"] > 0.7:
        print("\n🚨 CONSTITUTIONAL CRISIS: Civil liberties threats at critical levels!")


def main() -> None:
    asyncio.run(run_simulation())


if __name__ == "__main__":
    main()


# ==== END civil_liberties_simulation.py ====

# ==== BEGIN example.py ====
#!/usr/bin/env python3
# Example usage of AGI-EGGS networking
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network
from agi_eggs.persistence import MessageStore


def main():
    store = MessageStore('pending_pi.jsonl')
    pi = PiNode('pi-1', store=store)
    egg = EggNode('egg-1', port=8766)

    network_pi = Network()
    network_egg = Network(port=8766)

    @pi.on('greeting')
    async def handle_greeting(msg):
        print(f"{pi.name} received: {msg.content['message']}")

    @pi.on('announce')
    async def handle_announce(msg):
        print(f"{pi.name} broadcast: {msg.content['message']}")

    @egg.on('greeting')
    async def handle_greeting_egg(msg):
        print(f"{egg.name} received: {msg.content['message']}")

    @egg.on('announce')
    async def handle_announce_egg(msg):
        print(f"{egg.name} broadcast: {msg.content['message']}")

    async def run():
        await network_pi.start_server(pi)
        await network_egg.start_server(egg)

        writer_to_egg = await network_pi.connect('localhost', 8766)
        await pi.send(writer_to_egg, {'key': 'greeting', 'message': 'hello from pi'})

        writer_to_pi = await network_egg.connect('localhost', 8765)
        await egg.send(writer_to_pi, {'key': 'greeting', 'message': 'hi from egg'})

        # broadcast from pi to all its connections
        await network_pi.broadcast({'key': 'announce', 'message': 'broadcast from pi'})

        # allow messages to be processed
        await asyncio.sleep(1)

        await network_pi.stop()
        await network_egg.stop()

    asyncio.run(run())


if __name__ == '__main__':
    main()


# ==== END example.py ====

# ==== BEGIN frontend.py ====
#!/usr/bin/env python3
"""Interactive CLI for AGI-EGGS nodes."""
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import asyncio
from agi_eggs.node import Node
from agi_eggs.network import Network


def parse_args():
    parser = argparse.ArgumentParser(description="AGI-EGGS frontend")
    parser.add_argument("name", help="Node name")
    parser.add_argument("--port", type=int, default=8765, help="listen port")
    parser.add_argument("--host", default="localhost", help="listen host")
    parser.add_argument(
        "--connect", action="append", default=[], help="peer host:port to connect"
    )
    return parser.parse_args()


async def main():
    args = parse_args()
    node = Node(args.name, host=args.host, port=args.port)
    network = Network(host=args.host, port=args.port)

    @node.on("message")
    async def on_message(msg):
        print(f"[{msg.sender}] {msg.content.get('text','')}")

    await network.start_server(node)

    for entry in args.connect:
        host, port_str = entry.split(":", 1)
        writer = await network.connect(host, int(port_str))
        # send initial greeting
        await node.send(writer, {"key": "message", "text": f"hello from {node.name}"})

    print("Type commands: send <key> <text> | broadcast <text> | quit")

    loop = asyncio.get_event_loop()
    try:
        while True:
            cmd = await loop.run_in_executor(None, input, "> ")
            if not cmd:
                continue
            if cmd.strip() in {"quit", "exit"}:
                break
            parts = cmd.split()
            if not parts:
                continue
            if parts[0] == "send" and len(parts) >= 3:
                key = parts[1]
                text = " ".join(parts[2:])
                for writer in list(network.connections):
                    await node.send(writer, {"key": key, "text": text})
            elif parts[0] == "broadcast" and len(parts) >= 2:
                text = " ".join(parts[1:])
                await network.broadcast({"key": "message", "text": text})
            else:
                print("Unknown command")
    finally:
        await network.stop()

if __name__ == "__main__":
    asyncio.run(main())


# ==== END frontend.py ====

# ==== BEGIN mesh_example.py ====
#!/usr/bin/env python3
"""Demonstrate a small mesh of Pi and Egg nodes."""

import asyncio
from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network
from agi_eggs.persistence import MessageStore


async def setup_node(node):
    network = Network(host=node.host, port=node.port)

    @node.on("greeting")
    async def handle_greeting(msg):
        print(f"[{node.name}] received greeting from {msg.sender}: {msg.content['message']}")

    @node.on("broadcast")
    async def handle_broadcast(msg):
        print(f"[{node.name}] broadcast from {msg.sender}: {msg.content['message']}")

    await network.start_server(node)
    return network


async def main():
    # create nodes with their own message stores
    pi1 = PiNode("pi-1", port=8765, store=MessageStore("pi1_pending.jsonl"))
    pi2 = PiNode("pi-2", port=8766, store=MessageStore("pi2_pending.jsonl"))
    egg = EggNode("egg-1", port=8767, store=MessageStore("egg_pending.jsonl"))

    net1 = await setup_node(pi1)
    net2 = await setup_node(pi2)
    net3 = await setup_node(egg)

    # connect nodes in a simple mesh
    w12 = await net1.connect("localhost", 8766)
    w13 = await net1.connect("localhost", 8767)
    w21 = await net2.connect("localhost", 8765)
    w23 = await net2.connect("localhost", 8767)
    w31 = await net3.connect("localhost", 8765)
    w32 = await net3.connect("localhost", 8766)

    # send greetings
    await pi1.send(w12, {"key": "greeting", "message": "hi from pi1"})
    await pi2.send(w21, {"key": "greeting", "message": "hello from pi2"})
    await egg.send(w31, {"key": "greeting", "message": "greetings from egg"})

    # broadcast a message from egg to all peers
    await net3.broadcast({"key": "broadcast", "message": "mesh online"})

    await asyncio.sleep(1)

    await net1.stop()
    await net2.stop()
    await net3.stop()


if __name__ == "__main__":
    asyncio.run(main())


# ==== END mesh_example.py ====

# ==== BEGIN agi_eggs/__init__.py ====
"""AGI-EGGS framework."""
# SPDX-License-Identifier: GPL-3.0-or-later

from .node import Node, PiNode, EggNode, Message
from .network import Network
from .persistence import MessageStore

__all__ = [
    'Node',
    'PiNode',
    'EggNode',
    'Message',
    'Network',
    'MessageStore',
]


# ==== END agi_eggs/__init__.py ====

# ==== BEGIN agi_eggs/network.py ====
# Network utilities for AGI-EGGS nodes
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
from typing import Optional
from .node import Node, Message


class Network:
    """Simple TCP network for AGI-EGGS nodes."""

    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.connections = []  # type: list[asyncio.StreamWriter]
        self.server: Optional[asyncio.base_events.Server] = None
        self.node: Optional[Node] = None

    async def start_server(self, node: Node):
        """Start a server and bind to the node."""
        self.node = node
        self.server = await asyncio.start_server(self._handle_conn, node.host, node.port)
        print(f"{node.name} listening on {node.host}:{node.port}")

    async def _handle_conn(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.connections.append(writer)
        try:
            while data := await reader.readline():
                msg = Message.from_json(data.decode())
                await self.node.handle_message(msg)
        except asyncio.IncompleteReadError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()
            self.connections.remove(writer)

    async def connect(self, host: str, port: int) -> asyncio.StreamWriter:
        reader, writer = await asyncio.open_connection(host, port)
        self.connections.append(writer)
        if self.node:
            await self.node.flush_pending(writer)
        return writer

    async def broadcast(self, content: dict):
        """Send a message to all connected peers."""
        if not self.node:
            raise RuntimeError("Network server not started")
        for writer in list(self.connections):
            await self.node.send(writer, content)

    async def stop(self):
        """Close all connections and stop the server."""
        for writer in list(self.connections):
            writer.close()
            await writer.wait_closed()
        self.connections.clear()
        if self.server:
            self.server.close()
            await self.server.wait_closed()


# ==== END agi_eggs/network.py ====

# ==== BEGIN agi_eggs/node.py ====
# AGI-EGGS node abstraction
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import json
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional

from .persistence import MessageStore


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

    def __init__(
        self,
        name: str,
        host: str = "localhost",
        port: int = 8765,
        store: Optional[MessageStore] = None,
    ):
        self.name = name
        self.host = host
        self.port = port
        self.handlers: Dict[str, Callable[[Message], None]] = {}
        self.store = store

    async def flush_pending(self, writer: asyncio.StreamWriter):
        """Send all queued messages through the provided writer."""
        if not self.store:
            return
        for msg in self.store.read_all():
            data = msg.to_json().encode() + b"\n"
            writer.write(data)
            await writer.drain()

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
        data = msg.to_json().encode() + b"\n"
        try:
            writer.write(data)
            await writer.drain()
        except (ConnectionError, asyncio.CancelledError, RuntimeError):
            if self.store:
                self.store.append(msg)
            else:
                raise


class PiNode(Node):
    """Raspberry Pi device."""
    pass


class EggNode(Node):
    """AGI Egg device."""
    pass


# ==== END agi_eggs/node.py ====

# ==== BEGIN agi_eggs/persistence.py ====
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


# ==== END agi_eggs/persistence.py ====

# ==== BEGIN modules/psych_support.py ====
"""
psych_support.py - Psychological support routines for AGI-EGGS

Provides trauma-informed, crisis psychology scripts for emotional stabilization
during disasters and high-stress scenarios. Includes breathing exercises,
decision paralysis override, moral injury processing, and positive reinforcement.

Usage:
    from modules.psych_support import CalmMode

    CalmMode.guide_breathing()
    CalmMode.override_decision_paralysis()
"""

class CalmMode:
    @staticmethod
    def guide_breathing():
        return (
            "Let's do a calming breathing exercise. Inhale slowly for 4 seconds, "
            "hold for 4 seconds, exhale for 6 seconds. Repeat 5 times."
        )

    @staticmethod
    def override_decision_paralysis():
        return (
            "If you're unsure what to do, break tasks into small steps. Choose one "
            "action you can do now, even if it's just checking your water supply or "
            "moving to a safer spot."
        )

    @staticmethod
    def positive_reinforcement():
        return (
            "You are capable. Every small action you take increases your safety. "
            "Keep going—you're doing well under pressure."
        )

    @staticmethod
    def process_moral_injury():
        return (
            "War and disaster force hard choices. If you feel guilt or distress, "
            "remember: survival choices are not moral failures. Focus on helping yourself and others."
        )


# ==== END modules/psych_support.py ====

