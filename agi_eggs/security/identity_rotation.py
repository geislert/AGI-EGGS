# SPDX-License-Identifier: GPL-3.0-or-later
"""Cryptographic identity rotation utility."""

import os
from .token_rotation import TokenRotationEngine
from .token_issuance import TokenAuthority
from agi_eggs.context import SystemContext


def rotate_identity(engine: TokenRotationEngine, authority: TokenAuthority) -> None:
    """Rotate the device identity keys in response to surveillance detection."""
    print("[identity_rotation] rotating device identity")
    context = engine.authority.get_context() if hasattr(engine.authority, 'get_context') else SystemContext()
    engine.current_token = engine.authority.issue_operation_token(engine.device_id, ['comms'], context)
    # In real use we'd regenerate key pair, here just note action
    new_id = os.urandom(4).hex()
    print(f"[identity_rotation] new temporary id {new_id}")
