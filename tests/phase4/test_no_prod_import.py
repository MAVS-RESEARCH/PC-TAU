"""P4 test: audit package boundary holds (reachability sole exception)."""

import ast
from pathlib import Path


# console.log P4T01-01: test module import confirms boundary check is active.
print("[test:p4-import-ban] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
BANNED = {"semantics", "touch", "freeze", "planner", "metrics", "claims"}


def test_no_prod_import():
    """No audit module imports banned production leaves; guard present."""
    # console.log P4T01-02: boundary test entry.
    print("[test:p4-import-ban] test_no_prod_import: entry.")
    checked = 0
    for path in (REPO_ROOT / "src" / "pc_tau_audit").glob("*.py"):
        if path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[-1] not in BANNED, (path.name, alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[-1] not in BANNED, (path.name, node.module)
        checked += 1
    assert checked == 6
    guard = (REPO_ROOT / "scripts" / "run_audit.py").read_text(encoding="utf-8")
    assert "sys.modules" in guard and "enforce_boundary" in guard
    # console.log P4T01-03: boundary verified.
    print("[test:p4-import-ban] test_no_prod_import: passed modules=%d." % checked)
