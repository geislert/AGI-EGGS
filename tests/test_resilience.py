import pytest
from agi_eggs.advanced.resilience import emergency_webhook


def test_emergency_webhook(capsys):
    emergency_webhook("33139")
    captured = capsys.readouterr().out
    assert "URGENT" in captured
    assert "33139" in captured

