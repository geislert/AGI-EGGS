"""Token verification."""
import time
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from agi_eggs.security.trust_token import TrustToken, InvalidTokenError


class TokenVerifier:
    def __init__(self, root_cert_pem):
        self.root_cert = serialization.load_pem_public_key(root_cert_pem)
        self.revoked = set()

    def verify(self, compact_token, required_caps=None):
        try:
            token = TrustToken.from_compact(compact_token)
        except InvalidTokenError:
            return None
        try:
            token.verify(self.root_cert)
        except InvalidSignature:
            return None
        if not token.is_valid():
            return None
        if token.token_id in self.revoked:
            return None
        if required_caps and not all(c in token.capabilities for c in required_caps):
            return None
        return token

    def revoke(self, token_id):
        self.revoked.add(token_id)
