# SPDX-License-Identifier: GPL-3.0-or-later
"""Minimal emergency handshake protocol."""

from __future__ import annotations

import struct
import xxhash


PROTOCOL_INDEX = {
    "LoRaWAN": 0,
    "WiFiDirect": 1,
    "HF_Burst": 2,
    "Acoustic": 3,
}


def establish_emergency_link(sender, receiver) -> bytes:
    """Return a compact handshake packet."""
    cap_bits = sum(2 ** PROTOCOL_INDEX[p] for p in sender.operational_profile["comms"])
    context_hash = xxhash.xxh32(f"{sender.context._emergency_context}{sender.context._group_size}").intdigest() & 0xFFFF
    time_diff = (receiver.current_time - sender.current_time) & 0xFFFF
    return struct.pack('>HHH', cap_bits, context_hash, time_diff)

