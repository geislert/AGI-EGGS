"""Authority issuing trust tokens."""
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from agi_eggs.security.trust_token import TrustToken
from agi_eggs.context import SystemContext


class TokenAuthority:
    def __init__(self):
        self.root_key = ec.generate_private_key(ec.SECP256R1())
        self.device_keys = {}
        self.tokens = {}

    def register_device(self, device_id):
        key = ec.generate_private_key(ec.SECP256R1())
        self.device_keys[device_id] = key.public_key()
        return key

    def issue_operation_token(self, device_id, capabilities, context):
        if device_id not in self.device_keys:
            raise ValueError("unregistered device")
        token = TrustToken(
            issuer="authority",
            subject=device_id,
            capabilities=capabilities,
            context=context,
        )
        token.sign(self.root_key)
        self.tokens[token.token_id] = token
        return token.to_compact()

    def public_certificate(self):
        return self.root_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
