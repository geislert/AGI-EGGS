from agi_eggs.security.identity_rotation import rotate_identity
from agi_eggs.security.token_rotation import TokenRotationEngine
from agi_eggs.security.token_issuance import TokenAuthority

class DummyEngine(TokenRotationEngine):
    def __init__(self):
        self.device_id = 'dev'
        self.authority = TokenAuthority()
        self.current_token = None

    def register(self):
        self.authority.register_device(self.device_id)

def test_rotate_identity():
    engine = DummyEngine()
    engine.register()
    rotate_identity(engine, engine.authority)
    assert engine.current_token is not None
