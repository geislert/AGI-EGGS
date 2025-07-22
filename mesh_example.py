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
