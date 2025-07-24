import pytest
from agi_eggs.security.token_issuance import TokenAuthority
from agi_eggs.security.token_verification import TokenVerifier
from agi_eggs.context import SystemContext
from agi_eggs.security.trust_token import TrustToken


def test_token_sign_verify():
    auth = TokenAuthority()
    device_key = auth.register_device('dev1')
    ctx = SystemContext()
    compact = auth.issue_operation_token('dev1', ['comms'], ctx)
    verifier = TokenVerifier(auth.public_certificate())
    token = verifier.verify(compact, ['comms'])
    assert token
