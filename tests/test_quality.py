from agi_eggs.advanced.quality_control import QualityControlRepresentative


def test_quality_control_notify():
    log = []
    qc = QualityControlRepresentative(log.append, ["dev", "ops"])
    qc.notify_maintenance("fail")
    assert log == ["fail"]
    assert qc.check_readiness("deploy") is True
