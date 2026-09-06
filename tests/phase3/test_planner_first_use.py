"""P3 test: planner first use in Phase 3 with checker agreement (Fix 11)."""

import ast
import subprocess
import sys
from pathlib import Path

import yaml


# console.log P3T04-01: test module import confirms first-use check is active.
print("[test:p3-first-use] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_planner_first_use():
    """Planner absent from history and Phase-1/2 code; agrees with checker on viability."""
    # console.log P3T04-02: first-use test entry.
    print("[test:p3-first-use] test_planner_first_use: entry.")
    log = subprocess.run(
        ["git", "log", "--oneline", "--", "src/pc_tau/planner.py", "src/pc_tau/freeze.py"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    # console.log P3T04-03: git history checked.
    print("[test:p3-first-use] planner history empty=%s." % (log.stdout.strip() == ""))
    assert log.stdout.strip() == ""
    for rel in [
        "src/pc_tau/source.py",
        "src/pc_tau/reachability.py",
        "src/pc_tau/semantics.py",
        "src/pc_tau/repairs.py",
        "src/pc_tau/touch.py",
        "scripts/phase2_eligibility.py",
    ]:
        tree = ast.parse((REPO_ROOT / rel).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[-1] != "planner", rel
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[-1] != "planner", rel
    from pc_tau.planner import solve
    from pc_tau.reachability import count_viable_first_repairs

    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    import json

    contracts = [
        json.loads(line)
        for line in open(
            REPO_ROOT / "results" / cfg["run_id"] / "contract" / "task_contracts.jsonl",
            encoding="utf-8",
        )
    ]
    # console.log P3T04-04: agreement sampled on sealed contracts.
    print("[test:p3-first-use] contracts=%d." % len(contracts))
    for contract in contracts[:5]:
        n_viable, _ = count_viable_first_repairs("OPEN", contract["Succ"], contract["Terminal"])
        solved = solve(contract["Succ"], "OPEN", contract["Terminal"])
        assert n_viable >= 2
        assert solved["kappa"] == 1
    # console.log P3T04-05: first use and agreement verified.
    print("[test:p3-first-use] test_planner_first_use: passed.")
