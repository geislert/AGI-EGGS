"""AGI-EGGS framework."""
# SPDX-License-Identifier: GPL-3.0-or-later

from .node import Node, PiNode, EggNode, Message
from .network import Network
from .persistence import MessageStore
from .config import ENABLED_MODULES
from .ephemeral_mesh import EphemeralMeshNode, SystemContext, PowerState
from .power_manager import apply_power_constraints
from .structures.survival_graph import SurvivalGraph
from .security.container_chain import ContainerChain
from .state.crdt import EnvironmentState
from .privacy.gateway import PrivacyEngine
from .trust.adaptive_trust import AdaptiveTrustSystem
from .orchestration.aros_core import AROSCore
from .security.network_sentinel import NodeGuardian
from .security.protection_gateway import CognitiveGuardian
from .security.token_integration import TrustTokenSystem
from .orchestration.resource_mapper import ResourceMapper
from .orchestration.dynamic_allocator import DynamicAllocator
from .orchestration.resilience_optimizer import ResilienceOptimizer
from .orchestration.human_ai_coordinator import HumanAICoordinator
from .orchestration.aros_interface import AROSInterface
from .orchestration.fractal_orchestrator import FractalOrchestrator, FractalNode
from .orchestration.entropy_scheduler import EntropyAwareScheduler, EntropyTask
from .radio.spectrum_ai import SpectrumAI, BandInfo
from .radio.hf_autotune import autotune_antenna
from .radio.signal_processing import denoise
from .security.identity_rotation import rotate_identity
from .power.disaster_charging import allocate_power
from .netutils.infrastructure_mapper import map_network
from .ai.model_swap import select_model
from .maintenance.nightwatch import (
    DrDiagnostician,
    MacGyver,
    Vigilance,
    vote,
    quarantine_agent,
    generate_daily_report,
)

# Advanced modules (optional)
try:
    from .advanced.ethics import ArchitecturalConformanceAgent
    from .advanced.uulp import UULPEncoder, UULPMessage
    from .advanced.uulp_interpreter import UULPInterpreter
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
        emergency_webhook,
        human_like_search,
        moral_weight_score,
        triage_by_zip,
        visualize_threat,
    )
    from .advanced.life_support import (
        SEVERE,
        URGENT,
        MONITOR,
        blood_supply_alert,
        detect_collapsed_structure,
        disaster_checklists,
        drone_dispatch,
        emergency_procedure_guide,
        epidemic_early_warning,
        log_supply,
        predictive_evacuation_model,
        reunify_refugee_family,
        triage_report,
    )
    from .advanced.quality_control import QualityControlRepresentative
    ADVANCED_AVAILABLE = True
except Exception:  # pragma: no cover - optional deps may be missing
    ADVANCED_AVAILABLE = False

__all__ = [
    'Node', 'PiNode', 'EggNode', 'Message',
    'Network', 'MessageStore', 'ENABLED_MODULES',
    'EphemeralMeshNode', 'SystemContext', 'PowerState',
    'apply_power_constraints', 'SurvivalGraph',
    'ContainerChain', 'EnvironmentState', 'PrivacyEngine',
    'AdaptiveTrustSystem',
    "TrustTokenSystem",
    'AROSCore', 'ResourceMapper', 'DynamicAllocator',
    'ResilienceOptimizer', 'HumanAICoordinator', 'AROSInterface',
    'FractalOrchestrator', 'EntropyAwareScheduler',
    'SpectrumAI', 'BandInfo', 'select_model',
    "allocate_power", "map_network",
    "DrDiagnostician", "MacGyver", "Vigilance", "vote", "quarantine_agent",
    "generate_daily_report", "NodeGuardian", "CognitiveGuardian"
]

if ADVANCED_AVAILABLE:
    __all__ += [
        'ArchitecturalConformanceAgent', 'UULPEncoder', 'UULPMessage', 'UULPInterpreter',
        'QuantumSecureComms', 'ConstitutionalLLaMA', 'TraumaDetector',
        'RuggedEdgeNode', 'HumanitarianDataGovernance',
        'triage_by_zip', 'visualize_threat', 'DataProvenanceManager',
        'human_like_search', 'SelfUpdater', 'MeshSync', 'MultimodalCortex',
        'moral_weight_score', 'JournalistVerifier', 'ZipDataPod',
        'emergency_webhook',
        'SEVERE', 'URGENT', 'MONITOR',
        'triage_report', 'blood_supply_alert',
        'detect_collapsed_structure', 'epidemic_early_warning',
        'emergency_procedure_guide', 'reunify_refugee_family',
        'predictive_evacuation_model', 'log_supply', 'disaster_checklists',
        'drone_dispatch', 'QualityControlRepresentative',
    ]
