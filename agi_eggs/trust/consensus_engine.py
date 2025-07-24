import random

class ConsensusEngine:
    def __init__(self):
        self.validator_nodes = list(range(1, 6))

    def seek_approval(self, change_package, impact_report, min_approval=0.7):
        votes = [self._vote() for _ in self.validator_nodes]
        ratio = sum(votes)/len(votes)
        return ratio >= min_approval

    def _vote(self):
        return 1 if random.random() > 0.2 else 0
