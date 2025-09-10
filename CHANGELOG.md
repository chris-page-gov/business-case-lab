# Changelog

## [Unreleased]

- Added: minimal `[build-system]` to `pyproject.toml` to enable editable installs (`pip install -e .`).
- Changed: recommend using `uv sync` and `uv run` as the canonical developer workflow. Tests validated after the change.

## [0.1.0] - 2025-09-05

- Initial public release.
- Standardise on `uv` runtime and module execution for CLI (see `copilot-instructions.md`).
