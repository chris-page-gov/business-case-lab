Repository copilot instructions — standardise on `uv`

Scope
- Use `uv` as the primary developer runtime/command runner in this repository.
- Prefer running the package as a module (python -m ...) through `uv run` to avoid relying on stale console_scripts in the virtualenv.

Why
- Editable installs or previously-generated console scripts can point at old callables (we saw `bcl-validate` invoking `validate_cmd()` directly). Running the package as a module avoids that, and is reproducible inside CI and dev shells.

Recommended workflows (zsh)
- Run validation (preferred, avoids console-script issues):

```bash
uv run python -m bcaselab.cli validate tests/synthetic/case_001/gold.json
```

- Render (preferred):

```bash
uv run python -m bcaselab.cli render tests/synthetic/case_001/gold.json --out out/case_001.md
```

- Run eval (preferred):

```bash
uv run python -m bcaselab.cli eval
```

Optional: regenerate console scripts
- If you do want the `bcl-validate` / `bcl-render` / `bcl-eval` scripts in `.venv/bin` to be updated to the new wrapper functions, reinstall the package in editable mode from within the workspace venv. This is optional — the preferred approach above removes the need for this.

```bash
# optional: from repo root
uv run python -m pip install -e .
```

Notes about why this fixes the earlier problem
- The root problem was console-scripts that referenced the old exported callables. When those scripts call the functions directly (e.g. `validate_cmd()`), arguments can be dropped. Running `python -m bcaselab.cli` executes the module and lets Typer parse the full argv correctly. The console-script regeneration step above will replace old scripts so they call the new wrapper functions instead.

Changelog & documentation best-practice (enforced by copilot instructions)
- Always update `CHANGELOG.md` for any user-visible change. Use the Keep a Changelog format (Unreleased / Added / Changed / Fixed / Removed). Example top of file:

```md
# Changelog

## [Unreleased]
- Added: ...
```

- Documentation: keep high-level requirements and converted artifacts under `docs/`. When updating behavior, add a short note in `docs/` and a reference in the changelog.
 - Documentation: keep high-level requirements and converted artifacts under `docs/`. When updating behavior, add a short note in `docs/` and a reference in the changelog.

Canonical prompts
-----------------

The canonical prompt files are:

- `prompts/interviewer_prompt.md`
- `prompts/renderer_prompt.md`

Other prompt files (e.g. `interviewer.md`, `*.txt`) are historical; the repository has been cleaned to keep only the canonical `_prompt.md` files.

- Pull requests must include:
  - Short summary of change
  - Link to any edited docs
  - Entry in `CHANGELOG.md` (Unreleased)

Testing and quick checks
- After changes to CLI code, run the preferred commands above. If you prefer to test without reinstalling, the `python -m` approach will reflect code edits immediately.

If you'd like, I can:
- Add a small `Makefile` or `uv` task that wraps the three preferred commands above.
- Create a `CHANGELOG.md` starter and update `README.md` with the uv workflow.
