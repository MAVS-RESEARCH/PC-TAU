"""P2 test: eligibility reads only the unrestricted graph (Fix 11)."""

import ast
from pathlib import Path


# console.log P2T07-01: test module import confirms blindness check is active.
print("[test:p2-eligibility-blind] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_eligibility_blind():
    """Eligibility and viability avoid outcome, mask, weight and optimizer references."""
    # console.log P2T07-02: blindness test entry.
    print("[test:p2-eligibility-blind] test_eligibility_blind: entry.")
    for rel in ["scripts/phase2_eligibility.py", "src/pc_tau/reachability.py"]:
        tree = ast.parse((REPO_ROOT / rel).read_text(encoding="utf-8"))
        roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        assert not (roots & {"freeze", "planner", "metrics"}), "%s imports %s" % (rel, roots)
    text = (REPO_ROOT / "scripts" / "phase2_eligibility.py").read_text(encoding="utf-8")
    assert "reachability" in text
    assert "Delta_R" not in text and "K_Pi" not in text
    # console.log P2T07-03: blindness verified.
    print("[test:p2-eligibility-blind] test_eligibility_blind: passed.")
