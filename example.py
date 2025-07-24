#!/usr/bin/env python3
# Enhanced example of AGI-EGGS networking
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
from datetime import datetime

from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network
from agi_eggs.persistence import MessageStore


def main():
    pi_store = MessageStore(f"pi_messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
    egg_store = MessageStore(f"egg_messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")

    pi = PiNode('raspberry-pi', store=pi_store)
    egg = EggNode('sensor-egg', port=8766, store=egg_store)

    network_pi = Network(port=8765)
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
        await asyncio.gather(
            network_pi.start_server(pi),
            network_egg.start_server(egg)
        )

        connections = []

        print(f"[{datetime.now().isoformat()}] Connecting pi to egg...")
        writer_to_egg = await network_pi.connect('localhost', 8766)
        connections.append(writer_to_egg)
        await pi.send(writer_to_egg, {
            'key': 'greeting',
            'message': 'Hello from Raspberry Pi!'
        })

        print(f"[{datetime.now().isoformat()}] Connecting egg to pi...")
        writer_to_pi = await network_egg.connect('localhost', 8765)
        connections.append(writer_to_pi)
        await egg.send(writer_to_pi, {
            'key': 'greeting',
            'message': 'Hi from Sensor Egg!'
        })

        print(f"[{datetime.now().isoformat()}] Pi broadcasting announcement...")
        await network_pi.broadcast({
            'key': 'announce',
            'message': 'System status: ONLINE',
            'timestamp': datetime.now().isoformat()
        })

        print(f"[{datetime.now().isoformat()}] Egg broadcasting sensor data...")
        await network_egg.broadcast({
            'key': 'sensor_data',
            'temperature': 23.5,
            'humidity': 45,
            'timestamp': datetime.now().isoformat()
        })

        await asyncio.sleep(2)

        print("Closing connections...")
        for writer in connections:
            writer.close()
            await writer.wait_closed()

        await asyncio.gather(network_pi.stop(), network_egg.stop())
        print("Networks stopped")

    asyncio.run(run())


if __name__ == '__main__':
    main()
