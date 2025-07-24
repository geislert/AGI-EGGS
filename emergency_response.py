#!/usr/bin/env python3
"""Emergency Response System built on AGI-EGGS framework.

This extends the base AGI-EGGS framework with simple life-saving applications:
- Medical emergency triage
- Disaster coordination
- Resource tracking
- Basic Architectural Conformance Agent (ACA) compliance checks
"""

import asyncio
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Tuple, Optional

from agi_eggs.node import Node, Message
from agi_eggs.network import Network
from agi_eggs.persistence import MessageStore


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class EmergencyType(Enum):
    MEDICAL = "medical"
    FIRE = "fire"
    NATURAL_DISASTER = "natural_disaster"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"


@dataclass
class EmergencyAlert:
    """Structured emergency alert message."""
    alert_id: str
    emergency_type: EmergencyType
    priority: Priority
    location: Tuple[float, float]
    description: str
    timestamp: float
    reporter: str
    status: str = "active"
    resources_needed: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.resources_needed is None:
            self.resources_needed = []


class BasicACA:
    """Minimal ACA validator for emergency responses."""

    ETHICAL_RULES = {
        "no_discrimination": "Emergency aid must be provided without discrimination",
        "medical_priority": "Medical emergencies take precedence over property damage",
        "privacy_protection": "Personal data must be protected even during emergencies",
        "transparent_logging": "All emergency decisions must be logged",
    }

    def __init__(self) -> None:
        self.violations: List[str] = []

    def validate_emergency_response(self, alert: EmergencyAlert, response: Dict) -> bool:
        violations: List[str] = []
        text = json.dumps(response, default=str).lower()
        for term in ["race", "religion", "ethnicity", "gender"]:
            if f"because of {term}" in text or f"due to {term}" in text:
                violations.append(f"Potential discrimination based on {term}")
        if alert.emergency_type == EmergencyType.MEDICAL and alert.priority != Priority.CRITICAL:
            if "delay" in text or "wait" in text:
                violations.append("Medical emergency response delayed")
        if violations:
            self.violations.extend(violations)
            return False
        return True

    def get_violation_report(self) -> List[str]:
        return self.violations.copy()


class EmergencyResponseNode(Node):
    """Node with emergency response capabilities."""

    def __init__(self, name: str, location: Tuple[float, float], node_type: str = "responder", **kwargs):
        super().__init__(name, **kwargs)
        self.location = location
        self.node_type = node_type
        self.aca = BasicACA()
        self.active_emergencies: Dict[str, EmergencyAlert] = {}
        self.resources = {
            "medical_supplies": 0,
            "personnel": 0,
            "vehicles": 0,
            "communication_range_km": 10,
        }
        self.emergency_protocols = self._load_emergency_protocols()

    def _load_emergency_protocols(self) -> Dict:
        return {
            EmergencyType.MEDICAL: {
                Priority.CRITICAL: [
                    "Assess airway, breathing, circulation",
                    "Call for immediate medical evacuation",
                    "Begin life-saving interventions",
                    "Prepare for transport",
                ],
                Priority.HIGH: [
                    "Stabilize patient",
                    "Monitor vital signs",
                    "Prepare for medical transport",
                    "Document injuries",
                ],
            },
            EmergencyType.FIRE: {
                Priority.CRITICAL: [
                    "Evacuate immediate area",
                    "Call fire services",
                    "Establish safety perimeter",
                    "Account for all personnel",
                ]
            },
            EmergencyType.NATURAL_DISASTER: {
                Priority.CRITICAL: [
                    "Issue immediate evacuation order",
                    "Activate emergency communications",
                    "Coordinate with regional authorities",
                    "Establish emergency shelters",
                ]
            },
        }

    def calculate_distance(self, other_location: Tuple[float, float]) -> float:
        lat1, lon1 = self.location
        lat2, lon2 = other_location
        lat_diff = lat1 - lat2
        lon_diff = lon1 - lon2
        return ((lat_diff * 111) ** 2 + (lon_diff * 111) ** 2) ** 0.5

    async def broadcast_emergency(self, network: Network, alert: EmergencyAlert) -> None:
        alert_dict = asdict(alert)
        alert_dict["emergency_type"] = alert.emergency_type.value
        alert_dict["priority"] = alert.priority.name
        content = {
            "key": "emergency_alert",
            "alert": alert_dict,
            "sender_location": self.location,
            "timestamp": time.time(),
        }
        if not self.aca.validate_emergency_response(alert, content):
            print(f"[{self.name}] ACA blocked emergency broadcast")
            return
        await network.broadcast(content)
        print(f"[{self.name}] Broadcast {alert.emergency_type.value} emergency")

    async def respond_to_emergency(self, alert: EmergencyAlert) -> Dict:
        distance = self.calculate_distance(alert.location)
        protocol_steps = self.emergency_protocols.get(alert.emergency_type, {}).get(alert.priority, [])
        response = {
            "responder_id": self.name,
            "distance_km": distance,
            "estimated_arrival_minutes": max(5, distance * 3),
            "available_resources": self.resources,
            "protocol_steps": protocol_steps,
            "can_respond": distance <= self.resources["communication_range_km"],
        }
        if not self.aca.validate_emergency_response(alert, response):
            response["aca_violations"] = self.aca.get_violation_report()
        return response


class MedicalTriageNode(EmergencyResponseNode):
    """Specialized node for medical triage."""

    def __init__(self, name: str, location: Tuple[float, float], **kwargs):
        super().__init__(name, location, node_type="medical", **kwargs)
        self.resources.update({
            "medical_supplies": 100,
            "trained_medics": 2,
            "ambulances": 1,
            "medical_protocols": True,
        })

    def assess_medical_severity(self, symptoms: List[str], vital_signs: Optional[Dict] = None) -> Priority:
        if vital_signs is None:
            vital_signs = {}
        critical = [
            "unconscious", "not breathing", "no pulse", "severe bleeding",
            "chest pain", "difficulty breathing", "cardiac arrest",
        ]
        high = [
            "broken bone", "severe pain", "head injury", "burns",
            "allergic reaction", "poisoning",
        ]
        if vital_signs:
            hr = vital_signs.get("heart_rate", 70)
            bp = vital_signs.get("bp_systolic", 120)
            if hr > 120 or hr < 50:
                return Priority.CRITICAL
            if bp > 180 or bp < 90:
                return Priority.HIGH
        combined = " ".join(symptoms).lower()
        if any(c in combined for c in critical):
            return Priority.CRITICAL
        if any(h in combined for h in high):
            return Priority.HIGH
        return Priority.MEDIUM


async def setup_emergency_network() -> Tuple[EmergencyResponseNode, Network, MedicalTriageNode, Network, EmergencyResponseNode, Network]:
    coordinator = EmergencyResponseNode(
        "EmergencyCoordinator",
        location=(34.0522, -118.2437),
        port=8765,
        store=MessageStore("coordinator_pending.jsonl"),
    )
    medical_unit = MedicalTriageNode(
        "MedicalUnit_01",
        location=(34.0622, -118.2337),
        port=8766,
        store=MessageStore("medical_pending.jsonl"),
    )
    fire_unit = EmergencyResponseNode(
        "FireUnit_01",
        location=(34.0422, -118.2537),
        port=8767,
        store=MessageStore("fire_pending.jsonl"),
    )

    coord_net = Network(host="localhost", port=8765)
    med_net = Network(host="localhost", port=8766)
    fire_net = Network(host="localhost", port=8767)

    @coordinator.on("emergency_alert")
    async def coord_handle_emergency(msg: Message):
        alert = EmergencyAlert(**msg.content["alert"])
        coordinator.active_emergencies[alert.alert_id] = alert
        print(f"[COORDINATOR] {alert.emergency_type.value} emergency at {alert.location}")
        await coord_net.broadcast({
            "key": "coordinate_response",
            "alert_id": alert.alert_id,
            "instruction": "All available units respond",
        })

    @medical_unit.on("emergency_alert")
    async def med_handle_emergency(msg: Message):
        alert = EmergencyAlert(**msg.content["alert"])
        if alert.emergency_type == EmergencyType.MEDICAL:
            response = await medical_unit.respond_to_emergency(alert)
            step = response["protocol_steps"][0] if response["protocol_steps"] else "n/a"
            print(f"[MEDICAL] ETA {response['estimated_arrival_minutes']} min, step: {step}")

    @fire_unit.on("emergency_alert")
    async def fire_handle_emergency(msg: Message):
        alert = EmergencyAlert(**msg.content["alert"])
        if alert.emergency_type in {EmergencyType.FIRE, EmergencyType.NATURAL_DISASTER}:
            response = await fire_unit.respond_to_emergency(alert)
            print(f"[FIRE] responding, distance {response['distance_km']:.1f} km")

    await coord_net.start_server(coordinator)
    await med_net.start_server(medical_unit)
    await fire_net.start_server(fire_unit)

    await coord_net.connect("localhost", 8766)
    await coord_net.connect("localhost", 8767)
    await med_net.connect("localhost", 8765)
    await fire_net.connect("localhost", 8765)

    return coordinator, coord_net, medical_unit, med_net, fire_unit, fire_net


async def simulate_medical_emergency() -> None:
    print("=== MEDICAL EMERGENCY SIMULATION ===\n")
    coordinator, coord_net, medical_unit, med_net, fire_unit, fire_net = await setup_emergency_network()
    await asyncio.sleep(0.5)
    emergency = EmergencyAlert(
        alert_id="MED_001",
        emergency_type=EmergencyType.MEDICAL,
        priority=Priority.CRITICAL,
        location=(34.0522, -118.2437),
        description="Cardiac arrest - 65-year-old male, unconscious",
        timestamp=time.time(),
        reporter="Citizen_001",
        resources_needed=["ambulance", "defibrillator"],
    )
    await coordinator.broadcast_emergency(coord_net, emergency)
    await asyncio.sleep(2)
    print("\n=== ACA COMPLIANCE REPORT ===")
    violations = coordinator.aca.get_violation_report()
    if violations:
        for v in violations:
            print(f"- {v}")
    else:
        print("No ethical violations detected")
    for net in (coord_net, med_net, fire_net):
        await net.stop()


def calculate_network_value(nodes: int, avg_lives_saved_per_node: int = 2) -> int:
    communication_value = nodes ** 2
    life_value = nodes * avg_lives_saved_per_node * 1000
    resilience = (nodes - 1) * 100 if nodes > 1 else 0
    return communication_value + life_value + resilience


def demonstrate_network_effects() -> None:
    print("\n=== NETWORK EFFECTS DEMONSTRATION ===\n")
    for n in [1, 3, 10, 50, 100]:
        value = calculate_network_value(n)
        print(f"{n:3d} nodes -> ${value:,}")


async def main() -> None:
    await simulate_medical_emergency()
    demonstrate_network_effects()


if __name__ == "__main__":
    asyncio.run(main())
