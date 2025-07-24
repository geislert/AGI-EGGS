import json
import time
from pathlib import Path


class Agent:
    def __init__(self, name):
        self.name = name
        self.health = 1.0

    def review_change(self, change):
        """Return APPROVE, REJECT, or VETO"""
        return 'APPROVE'


class DrDiagnostician(Agent):
    def review_change(self, change):
        if 'error' in change.get('description', '').lower():
            return 'REJECT'
        return 'APPROVE'


class MacGyver(Agent):
    def review_change(self, change):
        if change.get('experimental'):
            return 'APPROVE'
        return 'APPROVE'


class Vigilance(Agent):
    def review_change(self, change):
        if change.get('risk', 0) > 0.7:
            return 'VETO'
        return 'APPROVE'


def vote(change, agents):
    results = {a.name: a.review_change(change) for a in agents}
    approve = sum(1 for r in results.values() if r == 'APPROVE')
    if 'VETO' in results.values():
        outcome = 'REJECTED'
    elif approve >= 2:
        outcome = 'APPROVED'
    else:
        outcome = 'REJECTED'
    results['outcome'] = outcome
    return results


def quarantine_agent(agent: Agent, log_path: Path):
    log = {'agent': agent.name, 'time': time.time(), 'action': 'quarantined'}
    if log_path.exists():
        data = json.loads(log_path.read_text())
    else:
        data = []
    data.append(log)
    log_path.write_text(json.dumps(data, indent=2))




def generate_daily_report(votes, path: Path):
    """Append a human-readable maintenance report."""
    with path.open('a') as f:
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{ts}] Maintenance vote results:\n")
        for agent, decision in votes.items():
            if agent != 'outcome':
                f.write(f"- {agent}: {decision}\n")
        f.write(f"Outcome: {votes.get('outcome')}\n\n")
