import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
PROGRESS_FILE = BASE / 'progress_history.json'
REPO_ROOT = BASE.parent


def current_commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True, cwd=REPO_ROOT).strip()
    except Exception:
        return 'unknown'


def repo_stats():
    file_count = 0
    dir_count = 0
    for root, dirs, files in os.walk(REPO_ROOT):
        dir_count += len(dirs)
        file_count += len(files)
    return {'files': file_count, 'dirs': dir_count}


def load_history():
    if PROGRESS_FILE.exists():
        if PROGRESS_FILE.stat().st_size > 0:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        else:
            return []
    return []


def save_history(history):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)


if __name__ == '__main__':
    history = load_history()
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'commit': current_commit(),
    }
    entry.update(repo_stats())
    history.append(entry)
    save_history(history)
    print('Progress logged.')
