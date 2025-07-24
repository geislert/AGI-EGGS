#!/usr/bin/env python3
# Enhanced example of AGI-EGGS networking
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
from datetime import datetime

from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network
from agi_eggs.persistence import MessageStore
from agi_eggs import (
    ENABLED_MODULES,
    UULPEncoder,
    UULPInterpreter,
    UULPMessage,
    QuantumSecureComms,
)


def main():
    pi_store = MessageStore(
        f"pi_messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    )
    egg_store = MessageStore(
        f"egg_messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    )

    encoder = UULPEncoder() if ENABLED_MODULES.get("uulp") else None
    interpreter = UULPInterpreter() if ENABLED_MODULES.get("uulp") else None
    secure = QuantumSecureComms() if ENABLED_MODULES.get("security") else None

    pi = PiNode('raspberry-pi', store=pi_store)
    egg = EggNode('sensor-egg', port=8766, store=egg_store)

    network_pi = Network(port=8765)
    network_egg = Network(port=8766)

    @pi.on('greeting')
    async def handle_greeting(msg):
        content = msg.content['message']
        if secure and encoder and interpreter:
            try:
                content = bytes.fromhex(content)
                content = secure.decrypt_message(content).decode()
                decoded = interpreter.decode(UULPMessage(content=content, provenance=""))
                content = decoded['data']
            except Exception:
                pass
        print(f"{pi.name} received: {content}")

    @pi.on('announce')
    async def handle_announce(msg):
        content = msg.content['message']
        if secure and encoder and interpreter:
            try:
                content = bytes.fromhex(content)
                content = secure.decrypt_message(content).decode()
                decoded = interpreter.decode(UULPMessage(content=content, provenance=""))
                content = decoded['data']
            except Exception:
                pass
        print(f"{pi.name} broadcast: {content}")

    @egg.on('greeting')
    async def handle_greeting_egg(msg):
        content = msg.content['message']
        if secure and encoder and interpreter:
            try:
                content = bytes.fromhex(content)
                content = secure.decrypt_message(content).decode()
                decoded = interpreter.decode(UULPMessage(content=content, provenance=""))
                content = decoded['data']
            except Exception:
                pass
        print(f"{egg.name} received: {content}")

    @egg.on('announce')
    async def handle_announce_egg(msg):
        content = msg.content['message']
        if secure and encoder and interpreter:
            try:
                content = bytes.fromhex(content)
                content = secure.decrypt_message(content).decode()
                decoded = interpreter.decode(UULPMessage(content=content, provenance=""))
                content = decoded['data']
            except Exception:
                pass
        print(f"{egg.name} broadcast: {content}")

    async def run():
        await asyncio.gather(
            network_pi.start_server(pi),
            network_egg.start_server(egg)
        )

        connections = []

        print(f"[{datetime.now().isoformat()}] Connecting pi to egg...")
        writer_to_egg = await network_pi.connect('localhost', 8766)
        connections.append(writer_to_egg)
        message = {
            'key': 'greeting',
            'message': 'Hello from Raspberry Pi!'
        }
        if encoder:
            encoded = encoder.encode(message, 'text').content
            if secure:
                encoded = secure.encrypt_message(encoded.encode()).hex()
            message = {'key': 'greeting', 'message': encoded}
        await pi.send(writer_to_egg, message)

        print(f"[{datetime.now().isoformat()}] Connecting egg to pi...")
        writer_to_pi = await network_egg.connect('localhost', 8765)
        connections.append(writer_to_pi)
        message = {
            'key': 'greeting',
            'message': 'Hi from Sensor Egg!'
        }
        if encoder:
            encoded = encoder.encode(message, 'text').content
            if secure:
                encoded = secure.encrypt_message(encoded.encode()).hex()
            message = {'key': 'greeting', 'message': encoded}
        await egg.send(writer_to_pi, message)

        print(f"[{datetime.now().isoformat()}] Pi broadcasting announcement...")
        broadcast = {
            'key': 'announce',
            'message': 'System status: ONLINE',
            'timestamp': datetime.now().isoformat(),
        }
        if encoder:
            encoded = encoder.encode(broadcast, 'json').content
            if secure:
                encoded = secure.encrypt_message(encoded.encode()).hex()
            broadcast = {'key': 'announce', 'message': encoded}
        await network_pi.broadcast(broadcast)

        print(f"[{datetime.now().isoformat()}] Egg broadcasting sensor data...")
        sdata = {
            'key': 'sensor_data',
            'temperature': 23.5,
            'humidity': 45,
            'timestamp': datetime.now().isoformat(),
        }
        if encoder:
            encoded = encoder.encode(sdata, 'json').content
            if secure:
                encoded = secure.encrypt_message(encoded.encode()).hex()
            sdata = {'key': 'sensor_data', 'data': encoded}
        await network_egg.broadcast(sdata)

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
