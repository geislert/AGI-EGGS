import json, os, time

overview_path = os.path.join(os.path.dirname(__file__), 'project_overview.json')
with open(overview_path) as f:
    data = json.load(f)

snapshot = {
    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
    'files': len([p for p in os.listdir('.') if os.path.isfile(p)]),
    'dirs': len([d for d in os.listdir('.') if os.path.isdir(d)])
}

data.setdefault('snapshots', []).append(snapshot)
with open(overview_path, 'w') as f:
    json.dump(data, f, indent=2)
print('snapshot recorded')
