import json
from pathlib import Path

from bcaselab.cli import validate_impl, render_impl


def test_validate_sample():
    p = Path(__file__).resolve().parents[1] / "synthetic" / "case_001" / "gold.json"
    # should not raise
    validate_impl(str(p))


def test_render_sample(tmp_path):
    p = Path(__file__).resolve().parents[1] / "synthetic" / "case_001" / "gold.json"
    outp = tmp_path / "out.md"
    render_impl(str(p), str(outp))
    assert outp.exists()
    text = outp.read_text()
    assert "#" in text
