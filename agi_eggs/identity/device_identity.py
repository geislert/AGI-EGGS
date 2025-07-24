"""Simple device identity management."""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class DeviceIdentity:
    _private_key = None
    _public_key = None
    _device_id = None

    @classmethod
    def initialize(cls, package):
        cls._device_id = package.get('device_id')
        key_pem = package.get('private_key').encode()
        cls._private_key = serialization.load_pem_private_key(
            key_pem, password=None, backend=default_backend())
        cls._public_key = cls._private_key.public_key()

    @classmethod
    def get_private_key(cls):
        return cls._private_key

    @classmethod
    def get_public_key(cls):
        return cls._public_key

    @classmethod
    def device_id(cls):
        return cls._device_id
