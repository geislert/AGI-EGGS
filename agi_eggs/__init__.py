"""AGI-EGGS framework."""
# SPDX-License-Identifier: GPL-3.0-or-later

from .node import Node, PiNode, EggNode, Message
from .network import Network
from .persistence import MessageStore
from .config import ENABLED_MODULES

# Advanced modules (optional)
from .advanced.ethics import ArchitecturalConformanceAgent
from .advanced.uulp import UULPEncoder, UULPMessage
from .advanced.security import QuantumSecureComms
from .advanced.ai_integration import ConstitutionalLLaMA, TraumaDetector
from .advanced.edge import RuggedEdgeNode
from .advanced.governance import HumanitarianDataGovernance
from .advanced.resilience import (
    DataProvenanceManager,
    JournalistVerifier,
    MeshSync,
    MultimodalCortex,
    SelfUpdater,
    ZipDataPod,
    human_like_search,
    moral_weight_score,
    triage_by_zip,
    visualize_threat,
)

__all__ = [
    'Node', 'PiNode', 'EggNode', 'Message',
    'Network', 'MessageStore',
    'ENABLED_MODULES',
    'ArchitecturalConformanceAgent', 'UULPEncoder', 'UULPMessage',
    'QuantumSecureComms', 'ConstitutionalLLaMA', 'TraumaDetector',
    'RuggedEdgeNode', 'HumanitarianDataGovernance',
    'triage_by_zip', 'visualize_threat', 'DataProvenanceManager',
    'human_like_search', 'SelfUpdater', 'MeshSync', 'MultimodalCortex',
    'moral_weight_score', 'JournalistVerifier', 'ZipDataPod',
]
