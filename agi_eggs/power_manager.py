# SPDX-License-Identifier: GPL-3.0-or-later
"""Power-aware reconfiguration helpers."""

import time
from .ephemeral_mesh import EphemeralMeshNode, PowerState


def apply_power_constraints(node: EphemeralMeshNode) -> None:
    energy = node.context.hardware.energy_balance()

    if energy["reserves"] < 300:
        node.context._power_state = PowerState.CRYPTOBIOSIS
        node.dynamic_contraction()
    elif energy["input"] < energy["output"]:
        node.context._power_state = PowerState.ECHO_SEED
        node.dynamic_contraction()

    if int(time.time()) % 3600 == 0:
        node.expand_capabilities(energy["input"])

