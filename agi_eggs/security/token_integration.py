from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
"""Integration utilities for trust tokens."""
from agi_eggs.security.token_verification import TokenVerifier
from agi_eggs.security.token_rotation import TokenRotationEngine
from agi_eggs.security.token_issuance import TokenAuthority
from agi_eggs.identity.device_identity import DeviceIdentity


class TrustTokenSystem:
    def __init__(self, device_id):
        self.authority = TokenAuthority()
        self.device_key = self.authority.register_device(device_id)
        self.rotation = TokenRotationEngine(device_id, self.authority)
        self.verifier = TokenVerifier(self.authority.public_certificate())
        self.identity_package = {
            'device_id': device_id,
            'private_key': self.device_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()
        }
        DeviceIdentity.initialize(self.identity_package)
        self.rotation.initialize()

    def sign_message(self, text):
        token = self.rotation.get_active_token()
        priv = DeviceIdentity.get_private_key()
        signature = priv.sign(text.encode(), ec.ECDSA(hashes.SHA256()))
        return {
            'headers': {'trust_token': token.to_compact(), 'device_id': DeviceIdentity.device_id()},
            'body': text,
            'signature': signature,
        }

    def verify_message(self, msg):
        token = self.verifier.verify(msg['headers']['trust_token'], ['comms'])
        if not token:
            return False
        pub = self.authority.device_keys.get(token.subject)
        try:
            pub.verify(msg['signature'], msg['body'].encode(), ec.ECDSA(hashes.SHA256()))
            return True
        except Exception:
            return False
