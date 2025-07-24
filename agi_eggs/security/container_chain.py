"""Container identity blockchain for container provenance.
This is a simplified proof-of-work chain used to track container
registrations and permissions."""
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import List, Dict
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


@dataclass
class ContainerBlock:
    index: int
    previous_hash: str
    container_id: str
    owner_id: str
    permissions: Dict[str, int]
    timestamp: float = field(default_factory=time.time)
    nonce: int = 0
    signature: bytes = None

    def calculate_hash(self) -> str:
        payload = f"{self.index}{self.previous_hash}{self.container_id}{self.owner_id}" \
                  f"{json.dumps(self.permissions, sort_keys=True)}{self.timestamp}{self.nonce}"
        return hashlib.sha256(payload.encode()).hexdigest()


class ContainerChain:
    difficulty: int = 4

    def __init__(self):
        self.chain: List[ContainerBlock] = [self._genesis_block()]
        self.pending: List[ContainerBlock] = []

    def _genesis_block(self) -> ContainerBlock:
        return ContainerBlock(0, "0", "genesis", "system", {"all": 0})

    def register_container(self, container_id: str, owner_id: str, permissions: Dict[str, int]) -> ContainerBlock:
        block = ContainerBlock(
            index=len(self.chain) + len(self.pending),
            previous_hash=self.chain[-1].calculate_hash(),
            container_id=container_id,
            owner_id=owner_id,
            permissions=permissions,
        )
        self.pending.append(block)
        return block

    def _mine_block(self, block: ContainerBlock) -> None:
        while not block.calculate_hash().startswith('0' * self.difficulty):
            block.nonce += 1

    def mine_pending(self, signer_key) -> None:
        for block in self.pending:
            self._mine_block(block)
            payload = f"{block.index}{block.container_id}{block.timestamp}".encode()
            block.signature = signer_key.sign(
                payload,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256(),
            )
            self.chain.append(block)
        self.pending.clear()

    def verify_chain(self, get_public_key) -> bool:
        prev_hash = "0"
        for block in self.chain:
            if block.previous_hash != prev_hash:
                return False
            if not block.calculate_hash().startswith('0' * self.difficulty):
                return False
            if block.signature:
                payload = f"{block.index}{block.container_id}{block.timestamp}".encode()
                try:
                    get_public_key(block.owner_id).verify(
                        block.signature,
                        payload,
                        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                        hashes.SHA256(),
                    )
                except Exception:
                    return False
            prev_hash = block.calculate_hash()
        return True
