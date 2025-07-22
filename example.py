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
