import json
import os
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

SNAP_FILE = Path(__file__).with_name('structure.json')
HISTORY_FILE = Path(__file__).with_name('structure_history.json')


def snapshot_structure():
    structure = {
        "directories": {},
        "key_files": []
    }
    for item in BASE.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            structure["directories"][item.name] = "dir"
        elif item.is_file():
            structure["key_files"].append(item.name)
    return structure


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)


if __name__ == '__main__':
    snap = snapshot_structure()
    with open(SNAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(snap, f, indent=2)
    history = load_history()
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "snapshot": snap
    })
    save_history(history)
    print('Structure snapshot saved.')
