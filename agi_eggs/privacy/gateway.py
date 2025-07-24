"""Privacy gateway with layered encryption."""
from jose import jwt
from phe import paillier
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import base64
import os


class PrivacyEngine:
    def __init__(self, consent_level: int = 3):
        self.consent_level = consent_level
        self.paillier_priv, self.paillier_pub = paillier.generate_paillier_keypair()
        self.aes_keys = {}

    def process(self, data: dict, owner_id: str) -> dict:
        if not self._allowed(owner_id, data.get('category', 'default')):
            raise PermissionError('Consent insufficient')
        dtype = data['type']
        if dtype == 'biometric':
            return self._encrypt_biometric(data['value'])
        if dtype == 'environment':
            return self._homomorphic(data['value'])
        if dtype == 'media':
            return self._tokenize(data['value'])
        return data

    def _encrypt_biometric(self, blob: bytes) -> dict:
        session = os.urandom(16).hex()
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_GCM)
        ct, tag = cipher.encrypt_and_digest(blob)
        self.aes_keys[session] = key
        return {
            'alg': 'A256GCM',
            'session': session,
            'iv': base64.b64encode(cipher.nonce).decode(),
            'tag': base64.b64encode(tag).decode(),
            'data': base64.b64encode(ct).decode(),
        }

    def _homomorphic(self, values):
        return {
            'alg': 'Paillier',
            'key': self.paillier_pub.n,
            'data': [str(self.paillier_pub.encrypt(int(v))) for v in values],
        }

    def _tokenize(self, text: str) -> str:
        return jwt.encode({'t': text, 'aud': 'authorized'}, os.environ.get('JWT_SECRET', 'secret'), algorithm='HS256')

    def _allowed(self, owner_id: str, category: str) -> bool:
        rules = self._fetch_rules(owner_id)
        return rules.get(category, 0) >= self.consent_level

    def _fetch_rules(self, owner_id: str):
        # placeholder; in real system query blockchain or DB
        return {'default': 3, 'biometric': 3, 'environment': 2, 'media': 4}
