"""P2 test: production optimizer absent from the Phase-2 path (Fix 11)."""

import ast
from pathlib import Path


# console.log P2T09-01: test module import confirms absence check is active.
print("[test:p2-no-planner] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_no_production_planner_in_phase2():
    """Optimizer first appears in Phase 3 history; no Phase-2 file imports it."""
    # console.log P2T09-02: absence test entry.
    print("[test:p2-no-planner] test_no_production_planner_in_phase2: entry.")
    import subprocess

    log = subprocess.run(
        ["git", "log", "--oneline", "eff5ba5", "--", "src/pc_tau/planner.py", "src/pc_tau/freeze.py"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    # console.log P2T09-02b: Phase-2 history checked for optimizer files.
    print("[test:p2-no-planner] planner history at Phase-2 seal empty=%s." % (log.stdout.strip() == ""))
    assert log.stdout.strip() == ""
    checked = 0
    phase2_scope = [
        REPO_ROOT / "src" / "pc_tau" / name
        for name in ["source.py", "reachability.py", "semantics.py", "repairs.py", "touch.py"]
    ] + list((REPO_ROOT / "scripts").glob("phase1_*.py")) + list(
        (REPO_ROOT / "scripts").glob("phase2_*.py")
    )
    for path in phase2_scope:
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
