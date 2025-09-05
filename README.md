# business-case-lab

A vendor-neutral repository for:
- A Five Case Model business case template (schema-first)
- A guided interviewer prompt + deterministic renderer
- An automated test & evaluation harness with synthetic cases

## Quick start (preferred: module execution via uv)

This repo standardises on running the package as a module through `uv` so CLI parsing is always correct, and you avoid stale console-scripts in the venv. See `copilot-instructions.md` for the full rationale and optional console-script regeneration steps.

```bash
# create and enter the project directory
git clone <your-repo-url> business-case-lab
cd business-case-lab

# install deps (creates .venv by default)
uv sync

# validate (preferred):
uv run python -m bcaselab.cli validate tests/synthetic/case_001/gold.json

# render (preferred):
uv run python -m bcaselab.cli render tests/synthetic/case_001/gold.json --out out/case_001.md

# evaluate (preferred):
uv run python -m bcaselab.cli eval

# The older `bcl-validate` / `bcl-render` console-scripts may still exist in
# `.venv/bin` for convenience — if you prefer those, see `copilot-instructions.md`
# for how to regenerate them.
```

## Layout
```
schema/                     # JSON Schema for the business case
prompts/                    # Interviewer & renderer prompts
src/bcaselab/               # Python package: CLI, schema/renderer helpers
tests/synthetic/case_*/     # Synthetic input + Gold outputs
eval/                       # Evaluation artefacts (scorecard etc.)
out/                        # Rendered drafts
```

This is only a starter. Extend the schema, prompts, and evaluator to your needs.
