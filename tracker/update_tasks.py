import json
from pathlib import Path

TRACKER_FILES = [
    Path(__file__).with_name('uulp_tasks.json'),
    Path(__file__).with_name('perf_tasks.json'),
    Path(__file__).parent.parent / 'codex' / 'tasks.json',
]

def load_tasks():
    tasks = []
    for file in TRACKER_FILES:
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            tasks.extend(data.get('tasks', []))
    return tasks


def print_tasks():
    tasks = sorted(load_tasks(), key=lambda t: t['priority'])
    for t in tasks:
        print(f"[{t['id']}] priority {t['priority']} - {t['status']}: {t['description']}")

if __name__ == '__main__':
    print_tasks()
