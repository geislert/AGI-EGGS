"""Capability-based trust token."""
import time
import json
from dataclasses import dataclass, field
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from agi_eggs.context import SystemContext


class InvalidTokenError(Exception):
    pass


@dataclass
class TrustToken:
    issuer: str
    subject: str
    capabilities: list
    context: SystemContext
    issue_time: int = field(default_factory=lambda: int(time.time()))
    expiry_time: int = field(init=False)
    token_id: str = field(init=False)
    signature: bytes = field(default=None)
    TOKEN_LIFETIME = 3600
    TOKEN_VERSION = "v1"

    def __post_init__(self):
        self.expiry_time = self.issue_time + self.TOKEN_LIFETIME
        self.token_id = self._generate_token_id()

    def _generate_token_id(self):
        h = hashes.Hash(hashes.SHA256(), backend=default_backend())
        h.update(f"{self.issuer}{self.subject}{self.issue_time}".encode())
        return h.finalize().hex()

    def _payload(self):
        return json.dumps({
            "ver": self.TOKEN_VERSION,
            "iss": self.issuer,
            "sub": self.subject,
            "cap": self.capabilities,
            "ctx": self.context.snapshot(),
            "iat": self.issue_time,
            "exp": self.expiry_time,
            "tid": self.token_id,
        }, sort_keys=True).encode()

    def sign(self, private_key):
        self.signature = private_key.sign(self._payload(), ec.ECDSA(hashes.SHA256()))
        return self

    def verify(self, public_key):
        if not self.signature:
            raise InvalidTokenError("Token not signed")
        public_key.verify(self.signature, self._payload(), ec.ECDSA(hashes.SHA256()))
        return True

    def is_valid(self, now=None):
        now = now or int(time.time())
        return self.issue_time <= now <= self.expiry_time

    def to_compact(self):
        sig_hex = self.signature.hex() if self.signature else ""
        return f"{self.TOKEN_VERSION}.{self._payload().decode()}.{sig_hex}"

    @classmethod
    def from_compact(cls, data):
        parts = data.split('.', 2)
        if len(parts) != 3 or parts[0] != cls.TOKEN_VERSION:
            raise InvalidTokenError("Invalid format")
        payload = json.loads(parts[1])
        token = cls(
            issuer=payload['iss'],
            subject=payload['sub'],
            capabilities=payload['cap'],
            context=SystemContext.from_snapshot(payload['ctx'])
        )
        token.issue_time = payload['iat']
        token.expiry_time = payload['exp']
        token.token_id = payload['tid']
        if parts[2]:
            token.signature = bytes.fromhex(parts[2])
        return token

