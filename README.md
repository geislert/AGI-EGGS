# AGI-EGGS

This repository contains early experiments toward a knowledge management interface called **AGI‑EGG**. The goal is to explore how a "Unified Universal Language Protocol" (UULP) might organize and visualize incoming information.

Currently the project consists of a single HTML/JavaScript prototype (`index.html`). Opening this file in any modern browser launches a lightweight command post UI:

A minimal backend prototype (`agi_egg_backend.py`) stores ingested fragments in an SQLite database and attaches a simple 3-D timestamp (quantum/classical/cosmological). Use `python agi_egg_backend.py ingest <file>` to add data or `python agi_egg_backend.py list` to view stored entries.
- **Manual Ingest** – upload text, PDF, or CSV documents which are split into fragments and stored in memory.
- **Oversight** – view flagged content and a running audit log.
- **Visualization** – plot knowledge fragments in a radial chart based on a simple scoring heuristic.
- **Live Intelligence Feed** – pull data from several RSS feeds and highlight potentially important articles.

The prototype does not persist data or provide any backend services. It is primarily a front‑end demonstration meant to guide future development. To try it out, simply open `index.html` in your browser.

## Next Steps

1. **Persistence layer** – add a lightweight database so ingested documents are saved across sessions.
2. **Backend API** – separate data processing from the UI and expose endpoints for ingesting documents and signals.
3. **Testing & linters** – set up automated tests to ensure the UI behaves correctly as the codebase grows.

This repository uses the GNU GPL v3 license. Contributions and suggestions are welcome as we experiment with the UULP concept.
