#!/usr/bin/env python3
# Example usage of AGI-EGGS networking
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network


def main():
    pi = PiNode('pi-1')
    egg = EggNode('egg-1', port=8766)

    network_pi = Network()
    network_egg = Network(port=8766)

    @pi.on('greeting')
    async def handle_greeting(msg):
        print(f"{pi.name} received: {msg.content['message']}")

    @egg.on('greeting')
    async def handle_greeting_egg(msg):
        print(f"{egg.name} received: {msg.content['message']}")

    async def run():
        await network_pi.start_server(pi)
        await network_egg.start_server(egg)

        writer_to_egg = await network_pi.connect('localhost', 8766)
        await pi.send(writer_to_egg, {'key': 'greeting', 'message': 'hello from pi'})

        writer_to_pi = await network_egg.connect('localhost', 8765)
        await egg.send(writer_to_pi, {'key': 'greeting', 'message': 'hi from egg'})

        # allow messages to be processed
        await asyncio.sleep(1)

    asyncio.run(run())


if __name__ == '__main__':
    main()
