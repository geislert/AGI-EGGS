#!/usr/bin/env python3
"""Example demonstrating NotificationService with AGI-EGGS."""

import asyncio
from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network
from agi_eggs.notifications import NotificationService


def main() -> None:
    notifications = NotificationService(
        rss_path="notifications.xml",
        # Configure SMTP if available
        smtp_server=None,
        from_addr=None,
        to_addrs=[],
    )

    pi = PiNode("pi-1")
    egg = EggNode("egg-1", port=8766)

    net_pi = Network()
    net_egg = Network(port=8766)

    @pi.on("greeting")
    async def handle_pi(msg):
        print(f"[pi] received: {msg.content['message']}")
        notifications.add_event("Greeting from egg", msg.content["message"])

    @egg.on("greeting")
    async def handle_egg(msg):
        print(f"[egg] received: {msg.content['message']}")
        notifications.add_event("Greeting from pi", msg.content["message"])

    async def run():
        await net_pi.start_server(pi)
        await net_egg.start_server(egg)

        writer_to_egg = await net_pi.connect("localhost", 8766)
        writer_to_pi = await net_egg.connect("localhost", 8765)

        await pi.send(writer_to_egg, {"key": "greeting", "message": "hello from pi"})
        await egg.send(writer_to_pi, {"key": "greeting", "message": "hi from egg"})

        await asyncio.sleep(0.5)

        await net_pi.stop()
        await net_egg.stop()
        notifications.write_feed()
        print("RSS feed written to notifications.xml")

    asyncio.run(run())


if __name__ == "__main__":
    main()
