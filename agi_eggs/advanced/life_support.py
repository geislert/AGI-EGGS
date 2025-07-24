"""Life-saving utilities for crisis response."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

SEVERE = "severe"
URGENT = "urgent"
MONITOR = "monitor"


def triage_report(report: Dict[str, str]) -> str:
    """Categorize emergencies using simple keyword matching."""
    if "cardiac_arrest" in report.get("tags", ""):
        return SEVERE
    if "structural_collapse" in report.get("tags", ""):
        return URGENT
    return MONITOR


def blood_supply_alert(blood_type: str, location: str) -> None:
    """Placeholder for notifying nearby donors."""
    print(f"[blood-alert] Need {blood_type} units near {location}")


def detect_collapsed_structure(photo: bytes) -> Dict[str, str]:
    """Pretend to analyze building images for survivable voids."""
    return {"void_spaces": 1, "hazards": "none"}


def epidemic_early_warning(symptoms: List[str]) -> Optional[str]:
    """Detect unusual symptom clusters."""
    if symptoms.count(symptoms[0]) > 3:
        return "potential_outbreak"
    return None


def emergency_procedure_guide(procedure: str) -> str:
    """Return short text guidance for first aid steps."""
    guides = {
        "cpr": "Check responsiveness, call emergency services, begin compressions.",
        "tourniquet": "Place 2-3 inches above wound, tighten until bleeding stops.",
    }
    return guides.get(procedure, "No guide available")


def reunify_refugee_family(photo: bytes) -> str:
    """Placeholder for privacy-preserving facial recognition."""
    return "match_pending"


def predictive_evacuation_model(data: Dict[str, float]) -> str:
    """Estimate best evacuation time."""
    risk = data.get("flood_risk", 0) + data.get("crowd", 0)
    if risk > 5:
        return "evacuate_now"
    return "standby"


def log_supply(item: str, qty: int, location: str, exp: str) -> None:
    """Demo supply blockchain entry."""
    print(f"LOG {item} {qty} {location} {exp}")


disaster_checklists = {
    "earthquake": ["Structural triage", "Medical"],
    "chemical": ["Wind direction", "Containment"],
    "conflict": ["Safe corridors", "Trauma care"],
}


def drone_dispatch(task: str, dest: str) -> None:
    """Placeholder for autonomous drone integration."""
    print(f"[drone] {task} to {dest}")
