# Repository copilot instructions — standardise on `uv`

## Scope

- Use `uv` as the primary developer runtime / command runner in this repository.

- Prefer running the package as a module (python -m ...) through `uv run` to avoid relying on stale console-scripts in the virtualenv.

## Why

Editable installs or previously-generated console scripts can point at old callables (for example, `bcl-validate` could invoke `validate_cmd()` directly). Running the package as a module avoids that, and is reproducible inside CI and developer shells.

## Recommended workflows (zsh)

Run validation (preferred, avoids console-script issues):

```bash
uv run python -m bcaselab.cli validate tests/synthetic/case_001/gold.json
```

Render (preferred):

```bash
uv run python -m bcaselab.cli render tests/synthetic/case_001/gold.json --out out/case_001.md
```

Run eval (preferred):

```bash
uv run python -m bcaselab.cli eval
```

## Optional: regenerate console scripts

If you do want the `bcl-validate` / `bcl-render` / `bcl-eval` scripts in `.venv/bin` to be updated to the new wrapper functions, reinstall the package in editable mode from within the workspace venv. This is optional — the preferred approach above removes the need for this.

```bash
# optional: from repo root
uv run python -m pip install -e .
```

## Notes about why this fixes the earlier problem

The root problem was console-scripts that referenced the old exported callables. When those scripts call the functions directly (for example `validate_cmd()`), arguments can be dropped. Running `python -m bcaselab.cli` executes the module and lets Typer parse the full argv correctly. The console-script regeneration step above will replace old scripts so they call the new wrapper functions instead.

## Changelog & documentation best-practice

- Always update `CHANGELOG.md` for any user-visible change. Use the Keep a Changelog format (Unreleased / Added / Changed / Fixed / Removed). Example top of file:

```md
# Changelog

## [Unreleased]
- Added: ...
```

- Documentation: keep high-level requirements and converted artifacts under `docs/`. When updating behaviour, add a short note in `docs/` and a reference in the changelog.

## Canonical prompts

The canonical prompt files are:

- `prompts/interviewer_prompt.md`
- `prompts/renderer_prompt.md`

Other prompt files (for example `interviewer.md` or `*.txt`) are historical. The repository keeps the canonical `_prompt.md` files.

## Pull request checklist

Pull requests must include:

- Short summary of change
- Link to any edited docs
- Entry in `CHANGELOG.md` (Unreleased)

## Testing and quick checks

After changes to CLI code, run the preferred commands above. If you prefer to test without reinstalling, the `python -m` approach will reflect code edits immediately.

## Offer

If you'd like, I can:

- Add a small `Makefile` or `uv` task that wraps the three preferred commands above.
- Create a `CHANGELOG.md` starter and update `README.md` with the uv workflow.

## Copilot: Markdown output rules

When asking Copilot (or any automated assistant) to produce Markdown for this repository, require it to follow strict Markdown rules to avoid lint warnings and formatting regressions.

Rules (mandatory):

- Use CommonMark / GitHub-flavoured Markdown only; avoid inline raw HTML unless absolutely necessary and explain why.
- Surround lists with blank lines above and below (avoids MD032).
- Surround fenced code blocks with blank lines and include a language identifier (```bash, ```md, etc.).
- Use ATX headings (##) and include a blank line after headings.
- Use backticks for filenames and code symbols (e.g. `pyproject.toml`, `uv run`).
- Avoid trailing whitespace; keep line length reasonable (the repo uses a 100 char guide for code, but Markdown can wrap naturally).
- Use consistent bullet style (hyphen `-`) for lists in this repo.
- When producing lists of files or commands, ensure each list item is on its own line and indented correctly.

Prompt template for Copilot/assistant:

"When you generate Markdown, follow these rules exactly:
- Use CommonMark/GFM only, no inline HTML.
- Put a blank line above and below every list and fenced code block.
- Use fenced code blocks with a language tag.
- Use backticks for filenames and code symbols.
- Do not include trailing whitespace.
- Keep lists and headings separated by blank lines.
Return only the raw Markdown content, nothing else."

Recommended automation (enforce in CI / pre-commit):

- Add `markdownlint` (or `remark-lint`) to the dev toolchain. Example rules to enable: MD032 (blanks around lists), MD046 (code fence style), MD013 (line length) as needed.
- Add a lightweight GitHub Actions workflow to run `markdownlint` on changed Markdown files, or add a `pre-commit` hook running `markdownlint-cli`.

If you want, I can add a small `markdownlint` config and a GitHub Action or `pre-commit` hook to enforce these rules automatically. Would you like me to add that now?"
