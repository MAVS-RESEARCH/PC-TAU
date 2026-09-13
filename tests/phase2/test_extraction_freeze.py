"""P2 test: extraction protocol frozen before compilation (Fix 2)."""

import ast
import json
from pathlib import Path

import yaml


# console.log P2T02-01: test module import confirms freeze check is active.
print("[test:p2-extraction-freeze] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_extraction_freeze():
    """Protocol sealed with rules and source-only method; extractor isolated."""
    # console.log P2T02-02: freeze test entry.
    print("[test:p2-extraction-freeze] test_extraction_freeze: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    protocol = json.loads(
        (REPO_ROOT / "results" / run_id / "contract" / "extraction_protocol.json").read_text(
            encoding="utf-8"
        )
    )
    # console.log P2T02-03: protocol loaded.
    print("[test:p2-extraction-freeze] protocol frozen=%s." % protocol.get("frozen"))
    assert protocol.get("frozen") is True
    assert len(protocol.get("rules", [])) == 6
    assert protocol.get("llm_extractor") is None
    for rel in ["src/pc_tau/semantics.py", "scripts/phase2_extract.py"]:
        tree = ast.parse((REPO_ROOT / rel).read_text(encoding="utf-8"))
        roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        assert not (roots & {"freeze", "planner", "metrics"}), "%s imports %s" % (rel, roots)
    # console.log P2T02-04: extraction freeze verified.
    print("[test:p2-extraction-freeze] test_extraction_freeze: passed.")
