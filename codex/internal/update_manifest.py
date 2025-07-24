import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CODEX_DIR = BASE / 'codex'
TRACKER_DIR = BASE / 'tracker'

MANIFEST_FILE = Path(__file__).with_name('manifest_history.json')

TRACKER_FILES = [
    TRACKER_DIR / 'uulp_tasks.json',
    TRACKER_DIR / 'perf_tasks.json',
    CODEX_DIR / 'tasks.json',
    CODEX_DIR / 'self_tasks.json',
]

STRUCTURE_FILE = CODEX_DIR / 'structure.json'


def load_tasks():
    tasks = []
    for file in TRACKER_FILES:
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            tasks.extend(data.get('tasks', []))
    return tasks


def load_structure():
    if STRUCTURE_FILE.exists():
        with open(STRUCTURE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def update_manifest():
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'structure': load_structure(),
        'tasks': load_tasks(),
    }
    history = []
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    history.append(entry)
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)
    print('Manifest updated')


if __name__ == '__main__':
    update_manifest()
