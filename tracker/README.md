# Tracker

This directory stores the condensed task list using a simple JSON format. The
structure mirrors the hypothetical "Universal Unified Language Protocol" (UULP),
where each task has an `id`, `priority`, `status` and `description`. Tools can
parse this file to generate human-readable reports or update task status.

Example entry:

```json
{
  "id": "T001",
  "priority": 1,
  "status": "open",
  "description": "Fix and expand README"
}
```

The goal is to keep tasks concise and machine-friendly so they can be easily
processed or manipulated by future automation. In addition to `uulp_tasks.json`
there is a secondary file `perf_tasks.json` tracking optimization-related
improvements. A separate file `../codex/self_tasks.json` records Codex-specific
tasks so the agent can rebuild context if needed. Repository layout snapshots
are stored in `../codex/structure_history.json` and updated via
`../codex/update_structure.py`.

Maintenance actions are logged in `MAINTENANCE_LOG.md`. Both automated agents
and human contributors can append entries to record recurring issues or repairs.
