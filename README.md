# AGI-EGGS

This repository contains early experiments toward a knowledge management interface called **AGI‑EGG**. The goal is to explore how a "Unified Universal Language Protocol" (UULP) might organize and visualize incoming information.

The project provides:

- `index.html` – a browser-based command post with manual ingest, oversight tools and a radial knowledge visualization.
- `agi_egg_backend.py` – utilities for splitting text into fragments, applying a simple 3‑D timestamp and storing data in SQLite.
- `backend_api.py` – a small Flask service exposing HTTP endpoints so the front-end can ingest data and list stored fragments.

## Usage

1. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```
2. Start the backend API:
   ```bash
   python backend_api.py
   ```
3. Open `index.html` in a browser. Ingested files or signals will be sent to the backend and stored in `agi_egg_data.db`.

## Notes

This is still an early prototype. The HTML front-end currently keeps additional state in memory. Persistence and richer APIs are planned for future versions.

This repository uses the GNU GPL v3 license. Contributions and suggestions are welcome as we experiment with the UULP concept.
