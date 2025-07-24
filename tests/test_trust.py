from agi_eggs.trust.adaptive_trust import AdaptiveTrustSystem

def test_simple_verification():
    ats = AdaptiveTrustSystem()
    assert ats.verify_component("comp", "normal")

def test_propose_modification():
    ats = AdaptiveTrustSystem()
    change = {"originator": "comp", "target": "mod", "code": b'print()'}
    result = ats.propose_self_modification(change)
    assert isinstance(result, bool)
