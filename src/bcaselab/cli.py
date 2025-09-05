from __future__ import annotations
import json
import sys
import os
from pathlib import Path
import typer
from rich import print
from jsonschema import Draft202012Validator

app = typer.Typer(help="Business case lab CLI")

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schema" / "business_case.schema.json"


def _load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


def _load_json(path: Path):
    with open(path, "r") as f:
        return json.load(f)


def validate_impl(json_path: str):
    """Core validation logic separated so both the Typer command
    and the old direct-call shim can reuse it.
    """
    schema = _load_schema()
    data = _load_json(Path(json_path))
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: e.path)
    if errors:
        print("[red]❌ Validation failed:[/red]")
        for e in errors:
            loc = "/".join([str(x) for x in e.path])
            print(f" - [bold]{loc or '$'}[/bold]: {e.message}")
        raise typer.Exit(code=1)
    print("[green]✅ Valid[/green]")


@app.command("validate")
def _validate_cmd(json_path: str = typer.Argument(...)):
    """Validate a business case JSON against the schema (Typer CLI)."""
    validate_impl(json_path)


def validate_cmd(json_path: str | None = None):
    """Backward-compatible exported function. If `json_path` is None
    it delegates to the Typer app so that calling the console script
    without args will still run the CLI parser.
    """
    if json_path is None:
        _run_subcommand("validate")
        return
    return validate_impl(json_path)


def render_impl(json_path: str, out: str = "out/draft.md"):
    data = _load_json(Path(json_path))
    os.makedirs(Path(out).parent, exist_ok=True)

    def s(ns, key, default=""):
        return ns.get(key, default)

    md = []
    md.append(f"# {data['metadata']['title']}")
    md.append("")
    md.append(f"**SRO:** {data['metadata']['sro']}  ")
    md.append(f"**Organisation:** {data['metadata']['sponsoring_org']}  ")
    md.append(f"**Level:** {data['case_level']}  ")
    md.append("")
    sc = data["strategic_case"]
    md.append("## Strategic Case")
    md.append(f"**Problem statement**: {s(sc,'problem_statement')}")
    md.append(f"**Objectives**:")
    for o in sc.get("objectives", []):
        md.append(f"- {o}")
    md.append(f"**Strategic fit**: {s(sc,'strategic_fit')}")
    md.append(f"**Stakeholders**: {', '.join(sc.get('stakeholders', []))}")
    md.append("")
    ec = data["economic_case"]
    md.append("## Economic Case")
    md.append("**Options considered:**")
    for o in ec.get("options", []):
        md.append(f"- {o}")
    md.append(f"**Preferred option:** {s(ec,'preferred_option')}")
    md.append(f"**NPV:** {ec.get('npv')}")
    md.append(f"**Sensitivity:** {s(ec,'sensitivity')}")
    md.append("")
    cc = data["commercial_case"]
    md.append("## Commercial Case")
    md.append(f"**Delivery model:** {s(cc,'delivery_model')}")
    md.append(f"**Route to market:** {s(cc,'route_to_market')}")
    if cc.get("lock_in_mitigations"):
        md.append(f"**Lock-in mitigations:** {cc['lock_in_mitigations']}")
    if cc.get("data_ai_clauses"):
        md.append(f"**Data/AI clauses:** {cc['data_ai_clauses']}")
    md.append("")
    fc = data["financial_case"]
    md.append("## Financial Case")
    md.append(f"**CAPEX:** {fc.get('capex')}  **OPEX:** {fc.get('opex')}  **Cashable benefits:** {fc.get('cashable_benefits')}")
    md.append("**Funding profile:**")
    for fp in fc.get("funding_profile", []):
        md.append(f"- {fp['year']}: {fp['amount']}")
    if fc.get("non_cashable_benefits"):
        md.append(f"**Non-cashable benefits:** {fc['non_cashable_benefits']}")
    md.append("")
    mc = data["management_case"]
    md.append("## Management Case")
    md.append(f"**Plan:** {s(mc,'plan')}")
    md.append(f"**Governance:** {s(mc,'governance')}")
    if mc.get("assurance"):
        md.append("**Assurance gates:** " + ", ".join(mc["assurance"]))
    md.append(f"**Measurement:** {s(mc,'measurement')}")
    if mc.get("dpia_ref"): md.append(f"**DPIA:** {mc['dpia_ref']}")
    if mc.get("eqia_ref"): md.append(f"**EQIA:** {mc['eqia_ref']}")
    if mc.get("technical_feasibility"): md.append(f"**Technical feasibility:** {mc['technical_feasibility']}")

    Path(out).write_text("\n".join(md))
    print(f"[green]✅ Rendered[/green] → {out}")


@app.command("render")
def _render_cmd(json_path: str = typer.Argument(...), out: str = typer.Option("out/draft.md", "--out", help="Output path")):
    """Render a minimal draft from a validated JSON (Typer CLI)."""
    render_impl(json_path, out)


def render_cmd(json_path: str | None = None, out: str = "out/draft.md"):
    """Backward-compatible exported function for render."""
    if json_path is None:
        _run_subcommand("render")
        return
    return render_impl(json_path, out)


@app.command("eval")
def eval_cmd():
    """Run a simple evaluation over synthetic cases and write eval/scorecard.json."""
    root = Path(__file__).resolve().parents[2]
    cases_dir = root / "tests" / "synthetic"
    schema = _load_schema()
    v = Draft202012Validator(schema)
    score = {"cases": [], "summary": {"count": 0, "valid": 0}}
    for case_dir in sorted(cases_dir.glob("case_*")):
        gold_json = case_dir / "gold.json"
        if not gold_json.exists():
            continue
        data = json.loads(gold_json.read_text())
        errors = sorted(v.iter_errors(data), key=lambda e: e.path)
        case_result = {
            "case_id": case_dir.name,
            "valid": len(errors) == 0,
            "errors": [e.message for e in errors],
            "has_funding_profile": bool(data.get("financial_case", {}).get("funding_profile")),
        }
        score["cases"].append(case_result)
        score["summary"]["count"] += 1
        score["summary"]["valid"] += int(case_result["valid"])
    outp = root / "eval" / "scorecard.json"
    outp.write_text(json.dumps(score, indent=2))
    print(f"[green]✅ Evaluation complete[/green] → {outp}")
    print(json.dumps(score["summary"], indent=2))


def _run_subcommand(name: str) -> None:
    """Helper to call the Typer `app` with a subcommand name and forward argv."""
    # Prepend the subcommand so Typer sees it as the invoked command.
    args = [name] + sys.argv[1:]
    # Click/Typer supports calling the app with an args iterable
    app(args=args)


def bcl_validate() -> None:
    """Console-script wrapper for `validate` that forwards CLI args."""
    _run_subcommand("validate")


def bcl_render() -> None:
    """Console-script wrapper for `render` that forwards CLI args."""
    _run_subcommand("render")


def bcl_eval() -> None:
    """Console-script wrapper for `eval` that forwards CLI args."""
    _run_subcommand("eval")


if __name__ == "__main__":
    app()
