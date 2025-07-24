# SPDX-License-Identifier: GPL-3.0-or-later
"""Simple network topology mapping."""
from typing import Dict

def map_network(peers: Dict[str, float]) -> Dict[str, float]:
    """Return peers ranked by link quality."""
    print(f"[infrastructure_mapper] mapping {len(peers)} peers")
    return {peer: quality for peer, quality in sorted(peers.items(), key=lambda x: -x[1])}
