from agi_eggs import EphemeralMeshNode, SystemContext, PowerState


def test_contraction_and_expansion():
    ctx = SystemContext()
    node = EphemeralMeshNode('n1', ctx)
    # force low power
    ctx._power_state = PowerState.ECHO_SEED
    node.dynamic_contraction()
    assert 'HF_Burst' in node.operational_profile['comms']
    # simulate power recovery
    node.expand_capabilities(2000)
    assert 'WiFiDirect' in node.operational_profile['comms']
