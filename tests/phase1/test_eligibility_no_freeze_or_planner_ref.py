"""G1 test: eligibility and viability never depend on freezes, optimizer or outcomes (Fix 11)."""

import ast
import json
from pathlib import Path


# console.log T3-01: test module import confirms firewall check is active.
print("[test:eligibility-firewall] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
BANNED_IMPORTS = {"freeze", "planner", "metrics"}


def _imports(path: Path) -> set[str]:
    """Collect top-level import roots plus pc_tau leaf names."""
    # console.log T3-02: AST import scan entry.
    print("[test:eligibility-firewall] _imports: scanning %s." % path.name)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
                if alias.name.startswith("pc_tau."):
                    roots.add(alias.name.split(".")[-1])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                roots.add(node.module.split(".")[0])
                if node.module.startswith("pc_tau."):
                    roots.add(node.module.split(".")[-1])
    # console.log T3-03: import scan complete.
    print("[test:eligibility-firewall] _imports: %s -> %s." % (path.name, sorted(roots)))
    return roots


def test_eligibility_no_freeze_or_planner_ref():
    """Decision modules import nothing forbidden; rule references no outcome values."""
    # console.log T3-04: firewall test entry.
    print("[test:eligibility-firewall] test_eligibility_no_freeze_or_planner_ref: entry.")
    for rel in ["src/pc_tau/source.py", "src/pc_tau/reachability.py"]:
        roots = _imports(REPO_ROOT / rel)
        assert not (roots & BANNED_IMPORTS), "%s imports %s" % (rel, roots & BANNED_IMPORTS)
    rule_payload = json.loads(
        (REPO_ROOT / "preregistration" / "eligibility_rule.json").read_text(
            encoding="utf-8"
        )
    )
    required_text = json.dumps(rule_payload.get("required", []))
    forbidden_text = json.dumps(rule_payload.get("forbidden", []))
    assert "Delta_R" not in required_text
    assert "K_Pi" not in required_text
    assert "Delta_R" in forbidden_text and "K_Pi" in forbidden_text
    reach_text = (REPO_ROOT / "src" / "pc_tau" / "reachability.py").read_text(
        encoding="utf-8"
    )
    for token in ["Delta", "K_Pi", "freeze", "planner", "metrics"]:
        assert token not in reach_text, "reachability references %s" % token
    source_text = (REPO_ROOT / "src" / "pc_tau" / "source.py").read_text(encoding="utf-8")
    assert "Delta_R" not in source_text and "K_Pi" not in source_text
    # console.log T3-05: decision blindness verified.
    print("[test:eligibility-firewall] decision modules are blind to outcomes.")
    importers = []
    for path in (REPO_ROOT / "src" / "pc_tau").glob("*.py"):
        if path.name.startswith("pilot_provisional"):
            continue
        if "pilot_provisional" in path.read_text(encoding="utf-8"):
            importers.append(path.name)
    assert importers == ["__init__.py"] or importers == [], (
        "provisional solver imported outside pilot: %s" % importers
    )
    pilot_text = (REPO_ROOT / "scripts" / "phase1_pilot.py").read_text(encoding="utf-8")
    assert "pilot_provisional_solve" in pilot_text
    # console.log T3-06: provisional isolation verified.
    print("[test:eligibility-firewall] test_eligibility_no_freeze_or_planner_ref: passed.")
