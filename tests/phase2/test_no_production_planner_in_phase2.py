"""P2 test: production optimizer absent from the Phase-2 path (Fix 11)."""

import ast
from pathlib import Path


# console.log P2T09-01: test module import confirms absence check is active.
print("[test:p2-no-planner] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_no_production_planner_in_phase2():
    """planner.py must not exist; no Phase-2 file may import it."""
    # console.log P2T09-02: absence test entry.
    print("[test:p2-no-planner] test_no_production_planner_in_phase2: entry.")
    assert not (REPO_ROOT / "src" / "pc_tau" / "planner.py").exists()
    assert not (REPO_ROOT / "src" / "pc_tau" / "freeze.py").exists()
    checked = 0
    for path in list((REPO_ROOT / "src" / "pc_tau").glob("*.py")) + list(
        (REPO_ROOT / "scripts").glob("phase2_*.py")
    ):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[-1] != "planner", path.name
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[-1] != "planner", path.name
        checked += 1
    # console.log P2T09-03: absence verified.
    print("[test:p2-no-planner] checked=%d passed." % checked)
