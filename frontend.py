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
