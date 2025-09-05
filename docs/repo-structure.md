Repository structure and canonical files
======================================

This document lists the canonical files and directories in this repository and their purpose. Use it as the single-source-of-truth when curating prompts, specs, and tooling.

Top-level layout
-----------------

- docs/ : high-level converted specs and developer docs (this file).
- spec/  : narrative templates and guidance derived from the spec.
- prompts/: canonical prompts used by Interviewer and Renderer agents.
- schema/: JSON Schema (authoritative validation artifact).
- src/: Python source for CLI and processing code.
- tests/: unit and synthetic test cases used by CI.
- eval/: evaluation artifacts and scorecards.

Canonical prompt files
----------------------

- prompts/interviewer_prompt.md — canonical interviewer prompt (human + machine instructions + JSONL audit format).
- prompts/renderer_prompt.md — canonical renderer prompt (human + machine instructions).

Notes on duplicates
-------------------

If you find other prompt files (e.g. `interviewer.md`, `renderer.md`, `*.txt`) treat them as historical copies. Keep `prompts/*_prompt.md` as the canonical files and archive or remove duplicates.

How to update prompts
---------------------

1. Edit the canonical `prompts/*_prompt.md` files.
2. Add a short note in `docs/` (this file) describing the change.
3. Add an entry to `CHANGELOG.md` under Unreleased.

Contact
-------
If you need help deciding the canonical wording for a prompt, open an issue or a PR and reference this document.
