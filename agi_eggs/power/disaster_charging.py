# SPDX-License-Identifier: GPL-3.0-or-later
"""Manage charging sources in disaster scenarios."""


def allocate_power(source: str) -> list:
    """Return priority list of subsystems based on power source."""
    if source == "solar":
        return ["comms", "medevac", "sensors"]
    if source == "hand_crank":
        return ["sos_beacon", "comms"]
    return ["minimal"]
