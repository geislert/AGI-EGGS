import json
from pathlib import Path

TRACKER_FILE = Path(__file__).with_name('uulp_tasks.json')

def load_tasks():
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('tasks', [])


def print_tasks():
    tasks = sorted(load_tasks(), key=lambda t: t['priority'])
    for t in tasks:
        print(f"[{t['id']}] priority {t['priority']} - {t['status']}: {t['description']}")

if __name__ == '__main__':
    print_tasks()
