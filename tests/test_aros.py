from agi_eggs.orchestration.aros_core import AROSCore


def test_aros_cycle():
    aros = AROSCore()
    aros.add_task(lambda: None)
    result = aros.execute_cycle()
    assert result["queue_length"] == 0
