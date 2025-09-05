Contributing
============

Thank you for your interest in contributing.

Guidelines
- Fork the repository and open a pull request.
- Update `CHANGELOG.md` under Unreleased with a short note about the change.
- Include tests for functional changes and run `pytest`.
- Keep PRs small and focused.

Development
- Use `uv run python -m bcaselab.cli` for the CLI while developing to avoid stale console scripts.
- To regenerate console scripts (optional):

```bash
uv run python -m pip install -e .
```
