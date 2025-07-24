"""Placeholder distributed ledger."""

class DistributedLedger:
    def __init__(self):
        self.issued = set()

    def record_token(self, issuer, token_id):
        self.issued.add((issuer, token_id))

    def verify_token_issuance(self, issuer, token_id):
        return (issuer, token_id) in self.issued
