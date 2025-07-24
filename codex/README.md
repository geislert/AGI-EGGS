# Codex Tracker

This directory stores Codex-specific task tracking files and temporary data.
It is separated from the main `tracker/` folder to keep agent-specific
information distinct.

Files here are considered ephemeral but should allow the agent to rebuild
context if needed.

Current file layout:
- `tasks.json` – JSON task list used by `tracker/update_tasks.py`
- `notes.md` – short repository summaries and temporary notes
- `self_tasks.json` – machine-readable list of Codex's own tasks
- `structure.json` – condensed map of repository directories and key files
- `structure_history.json` – snapshot log tracking repository growth
- `update_structure.py` – helper script to refresh structure files
