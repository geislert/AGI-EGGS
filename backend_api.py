"""
Simple Flask backend API for AGI-EGG
Provides endpoints to ingest text or files and list stored fragments.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sqlite3
from werkzeug.utils import secure_filename
from agi_egg_backend import init_db, ingest_file, list_fragments, apply_3d_timestamp, Fragment, compute_spin_score

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

init_db()

@app.route('/api/ingest', methods=['POST'])
def api_ingest():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400
    txt = data['text']
    source = data.get('source', 'api')
    source_type = data.get('source_type', 'user_upload')
    domain = data.get('domain', 'default')
    path = os.path.join(UPLOAD_DIR, f"temp_{int(app.config.get('COUNTER',0))}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(txt)
    count = ingest_file(path, source_type, domain)
    os.remove(path)
    return jsonify({'ingested': count})

@app.route('/api/ingest_file', methods=['POST'])
def api_ingest_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    source_type = request.form.get('source_type', 'user_upload')
    domain = request.form.get('domain', 'default')
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_DIR, filename)
    file.save(path)
    count = ingest_file(path, source_type, domain)
    os.remove(path)
    return jsonify({'ingested': count})

@app.route('/api/fragments')
def api_fragments():
    limit = int(request.args.get('limit', 10))
    conn = sqlite3.connect('agi_egg_data.db')
    c = conn.cursor()
    c.execute('SELECT id, content, source, source_type, ts_classical, spin_score FROM fragments ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    frags = []
    for r in rows:
        frags.append({
            'id': r[0],
            'content': r[1],
            'source': r[2],
            'source_type': r[3],
            'timestamp': r[4],
            'spin_score': r[5]
        })
    return jsonify({'fragments': frags})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
