import json
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / 'agent_state.json'


def update_state(note: str):
    now = datetime.utcnow().isoformat()
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text())
    else:
        data = {"notes": "Codex agent state for rebuild purposes.", "recent_snapshots": []}
    data["last_update"] = now
    data.setdefault("history", []).append({"time": now, "note": note})
    STATE_FILE.write_text(json.dumps(data, indent=2))


if __name__ == '__main__':
    import sys
    note = sys.argv[1] if len(sys.argv) > 1 else 'update'
    update_state(note)
    print('agent state updated')
