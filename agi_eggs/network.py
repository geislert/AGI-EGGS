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
