#!/usr/bin/env python3
"""Demo using EchoSeed HALO mesh config with AGI-EGGS."""

import asyncio
import yaml
from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network

CONFIG_PATH = "EchoSeed_HALO_RESTORED/aether/os/init/mesh_network_config.yaml"


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_nodes(roles):
    nodes = {}
    for i, role in enumerate(roles, start=1):
        if role in {"sentinel", "coord", "hub"}:
            node = PiNode(f"{role}-{i}", port=8764 + i)
        else:
            node = EggNode(f"{role}-{i}", port=8764 + i)
        nodes[role] = node
    return nodes


def setup_handlers(node):
    @node.on("status")
    async def handle_status(msg):
        print(f"[{node.name}] got status from {msg.sender}: {msg.content['msg']}")


async def main():
    cfg = load_config(CONFIG_PATH)
    nodes = create_nodes(cfg.get("roles", []))
    nets = {}
    for role, node in nodes.items():
        net = Network(host=node.host, port=node.port)
        setup_handlers(node)
        await net.start_server(node)
        nets[role] = net
    node_list = list(nodes.values())
    # connect each node to every other node
    for src in node_list:
        for dst in node_list:
            if src is not dst:
                await nets[src.name.split("-")[0]].connect(dst.host, dst.port)
    # send greeting from first role
    if node_list:
        sender = node_list[0]
        net = nets[sender.name.split("-")[0]]
        for dst in node_list[1:]:
            writer = await net.connect(dst.host, dst.port)
            await sender.send(writer, {"key": "status", "msg": f"hello from {sender.name}"})
    await asyncio.sleep(1)
    for net in nets.values():
        await net.stop()

if __name__ == "__main__":
    asyncio.run(main())
