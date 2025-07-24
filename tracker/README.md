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
processed or manipulated by future automation.
