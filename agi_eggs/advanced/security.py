"""Quantum-resistant security utilities."""

from typing import Tuple

try:
    from pqcrypto.kem import kyber512 as kyber
except Exception:  # pragma: no cover - optional dependency
    kyber = None
    from cryptography.fernet import Fernet  # type: ignore


class QuantumSecureComms:
    def __init__(self):
        if kyber:
            self.public_key, self.private_key = kyber.generate_keypair()
        else:
            self._fernet_key = Fernet.generate_key()
            self._fernet = Fernet(self._fernet_key)

    def encrypt_message(self, message: bytes) -> bytes:
        if kyber:
            ciphertext, _ = kyber.encrypt(message, self.public_key)
            return ciphertext
        return self._fernet.encrypt(message)

    def decrypt_message(self, ciphertext: bytes) -> bytes:
        if kyber:
            return kyber.decrypt(ciphertext, self.private_key)
        return self._fernet.decrypt(ciphertext)
