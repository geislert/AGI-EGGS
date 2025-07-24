"""Simple token rotation manager."""
import time
from agi_eggs.security.token_issuance import TokenAuthority
from agi_eggs.security.trust_token import TrustToken
from agi_eggs.context import SystemContext


class TokenRotationEngine:
    def __init__(self, device_id, authority: TokenAuthority):
        self.device_id = device_id
        self.authority = authority
        self.current_token = None
        self.expiry_margin = 60

    def initialize(self):
        ctx = SystemContext.current()
        self.current_token = TrustToken.from_compact(
            self.authority.issue_operation_token(self.device_id, ["comms"], ctx))
        return self.current_token

    def get_active_token(self):
        if not self.current_token or not self.current_token.is_valid(
                time.time() + self.expiry_margin):
            self.initialize()
        return self.current_token
