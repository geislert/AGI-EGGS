"""Simple CRDT-based environment state engine."""
import time
import threading
from typing import Dict, Any


class CRDTMap:
    def __init__(self):
        self.data = {}
        self.timestamps = {}
        self.lock = threading.Lock()

    def update(self, key: str, value: Any, node_id: str):
        with self.lock:
            ts = time.time_ns()
            if key not in self.timestamps or ts > self.timestamps[key][0]:
                self.data[key] = value
                self.timestamps[key] = (ts, node_id)
                return True
            return False

    def merge(self, remote: Dict[str, tuple]):
        with self.lock:
            for k, (rts, rnode, rval) in remote.items():
                lts, lnode = self.timestamps.get(k, (0, ""))
                if rts > lts or (rts == lts and rnode > lnode):
                    self.data[k] = rval
                    self.timestamps[k] = (rts, rnode)

    def get_state(self, node_id: str) -> Dict[str, tuple]:
        return {k: (ts, node_id, self.data[k]) for k, (ts, _) in self.timestamps.items()}

    def __getitem__(self, key):
        return self.data.get(key)


class EnvironmentState:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.lighting = CRDTMap()
        self.temperature = CRDTMap()
        self.media = CRDTMap()
        self.accessibility = CRDTMap()

    def apply_prefs(self, prefs: Dict[str, Any]):
        if 'lighting' in prefs:
            self.lighting.update('main', prefs['lighting'], self.node_id)
        if 'temp' in prefs:
            self.temperature.update('room', prefs['temp'], self.node_id)
        if 'volume' in prefs:
            self.media.update('audio', prefs['volume'], self.node_id)
        if prefs.get('high_contrast'):
            self.accessibility.update('ui_mode', 'high_contrast', self.node_id)

    def sync(self, neighbor_state: Dict[str, Dict]):
        self.lighting.merge(neighbor_state['lighting'])
        self.temperature.merge(neighbor_state['temperature'])
        self.media.merge(neighbor_state['media'])
        self.accessibility.merge(neighbor_state['accessibility'])

    def snapshot(self):
        return {
            'lighting': self.lighting.get_state(self.node_id),
            'temperature': self.temperature.get_state(self.node_id),
            'media': self.media.get_state(self.node_id),
            'accessibility': self.accessibility.get_state(self.node_id)
        }
