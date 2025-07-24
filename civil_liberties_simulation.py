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
