from agi_eggs.security.network_sentinel import NodeGuardian


def test_authorize_shutdown():
    alerts = []
    g = NodeGuardian("node1", criticality=9, on_alert=alerts.append)
    allowed = g.authorize_shutdown(False, "test")
    assert not allowed
    assert any("denied" in a for a in alerts)

