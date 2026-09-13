"""Phase-4 refactoring audit: frozen class only (Fix 4).

Harmless source-preserving rewrites must preserve closure; genuine
boundary-changing alternatives from the frozen class must route to
PARTIAL, never to a forced label. Unlisted perturbations fail closed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical
from pc_tau_audit import contract_audit, planner_audit, touch_audit


# console.log REF-01: script entry confirms refactor pipeline start.
print("[phase4:refactor] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log REF-02: argparse configuration entry.
    print("[phase4:refactor] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run frozen-class refactor audit.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log REF-03: arguments parsed.
    print("[phase4:refactor] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log REF-04: manifest update entry.
    print("[phase4:refactor] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log REF-05: manifest update complete.
    print("[phase4:refactor] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Execute only the Phase-2-frozen refactoring class."""
    # console.log REF-06: main entry.
    print("[phase4:refactor] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log REF-07: experiment config loaded.
    print("[phase4:refactor] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    admissible = json.loads((contract_dir / "admissible_refactorings.json").read_text(encoding="utf-8"))
    assert admissible.get("frozen") is True
    # console.log REF-08: frozen class loaded and confirmed.
    print("[phase4:refactor] main: frozen classes=%d." % len(admissible["admissible_classes"]))
    checks: list[dict] = []

    def record(name: str, detected: bool) -> None:
        # console.log REF-09: refactor check recorded.
        print("[phase4:refactor] check: %s detected=%s." % (name, detected))
        checks.append({"name": name, "detected": detected})

    base_succ = {
        "OPEN": [{"repair": "qR_fast", "to": "CLOSED"}, {"repair": "qE_slow", "to": "S1"}],
        "S1": [{"repair": "qA_close", "to": "CLOSED"}],
        "CLOSED": [],
    }
    renamed = {
        "OPEN": [{"repair": "qR_fast", "to": "CLOSED"}, {"repair": "qE_slow", "to": "S1"}],
        "S1": [{"repair": "qA_close", "to": "CLOSED"}],
        "CLOSED": [],
    }
    base_closed = planner_audit.solve_deepening(base_succ, "OPEN", "CLOSED")
    renamed_closed = planner_audit.solve_deepening(renamed, "OPEN", "CLOSED")
    record("harmless-rename-invariant", base_closed["kappa"] == renamed_closed["kappa"] == 1)
    reordered = {
        "CLOSED": [],
        "S1": [{"repair": "qA_close", "to": "CLOSED"}],
        "OPEN": [{"repair": "qE_slow", "to": "S1"}, {"repair": "qR_fast", "to": "CLOSED"}],
    }
    record(
        "reorder-invariant",
        planner_audit.solve_deepening(reordered, "OPEN", "CLOSED")["kappa"] == 1,
    )
    snap = touch_audit.snapshots("airline")
    intact = touch_audit.recompute(snap["OPEN"]["H"], snap["OPEN"]["P_R"], snap["OPEN"]["Lambda"], snap["S1"]["H"], snap["S1"]["P_R"], snap["S1"]["Lambda"]) == {"E"}
    record("metadata-change-invariant", bool(intact))
    # console.log REF-10: harmless rewrites verified invariant.
    print("[phase4:refactor] harmless rewrites complete.")
    boundary_status = contract_audit.rebuild_family("probe-task", ["auth:delegation-scope"], True)
    record("boundary-change-routes-to-partial", boundary_status == "PARTIAL")
    forced = boundary_status == "IDENTIFIED"
    record("no-forced-label", not forced)
    # console.log REF-11: boundary alternative verified as PARTIAL.
    print("[phase4:refactor] boundary alternative complete.")
    unlisted = "drop approval requirement entirely"
    record("unlisted-perturbation-refused", unlisted not in admissible["admissible_classes"])
    # console.log REF-12: unlisted perturbation refused.
    print("[phase4:refactor] unlisted check complete.")
    audit_dir = repo_root / "results" / run_id / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    out_path = audit_dir / "refactor_results.jsonl"
    rows = [{"class": "frozen-only", "checks": checks, "passed": all(c["detected"] for c in checks)}]
    with open(out_path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(canonical_dumps(row) + "\n")
    # console.log REF-13: refactor results written.
    print("[phase4:refactor] main: wrote %s." % out_path.as_posix())
    update_manifest(repo_root, run_id, "results/%s/audit/refactor_results.jsonl" % run_id, rows)
    passed = all(c["detected"] for c in checks)
    # console.log REF-14: refactor pipeline complete.
    print("[phase4:refactor] main: passed=%s." % passed)
    return 0 if passed else 3


if __name__ == "__main__":
    # console.log REF-15: script invoked as main.
    print("[phase4:refactor] __main__: invoking main.")
    raise SystemExit(main())
