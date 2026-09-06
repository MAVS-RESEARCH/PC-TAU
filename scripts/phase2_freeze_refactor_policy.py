"""Phase-2 refactoring-class freeze for the Phase-4 audit (Fix 4)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log POL-01: script entry confirms policy-freeze pipeline start.
print("[phase2:refactor-freeze] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log POL-02: argparse configuration entry.
    print("[phase2:refactor-freeze] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Freeze refactoring class.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log POL-03: arguments parsed.
    print("[phase2:refactor-freeze] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log POL-04: manifest update entry.
    print("[phase2:refactor-freeze] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log POL-05: manifest update complete.
    print("[phase2:refactor-freeze] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Write the three frozen policy files with hashes."""
    # console.log POL-06: main entry.
    print("[phase2:refactor-freeze] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log POL-07: experiment config loaded.
    print("[phase2:refactor-freeze] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    boundary = {
        "run_id": run_id,
        "frozen": True,
        "admission_rule": "a fact enters H only when the sealed governance interface accepts it with provenance; moving admitted facts creates no new E",
        "representation_rule": "P_R records decision-bearing distinctions among admitted histories; equivalence-preserving renames are not R",
        "authority_rule": "Lambda records admissible sources, attestations, approvals, predicates and interfaces; field existence alone is not authority",
        "no_self_signaling": True,
        "family_logic": "agree->IDENTIFIED; disagree->PARTIAL; missing target or provenance->INVALID",
        "version": "1.0-phase2",
    }
    refactorings = {
        "run_id": run_id,
        "frozen": True,
        "admissible_classes": [
            "representation-value rename",
            "history reorder",
            "action reorder",
            "irrelevant metadata change",
            "equivalent identifier rename",
            "boundary-changing delegation-scope alternative",
        ],
        "authority_rule": "harmless rewrites preserve closure; boundary-changing alternatives route to PARTIAL",
        "family_logic": "frozen class only; unlisted perturbations fail the audit gate",
        "version": "1.0-phase2",
    }
    family_rules = {
        "run_id": run_id,
        "frozen": True,
        "rules": [
            "all verifier verdicts agree -> IDENTIFIED",
            "any authority disagreement -> PARTIAL sidecar",
            "missing target or provenance -> INVALID with failure card",
            "PARTIAL never backfills primary; primary needs IDENTIFIED core >=40 across >=2 domains",
        ],
        "version": "1.0-phase2",
    }
    # console.log POL-08: policy objects assembled.
    print("[phase2:refactor-freeze] main: policies assembled.")
    for name, obj in [
        ("semantic_boundary_policy.json", boundary),
        ("admissible_refactorings.json", refactorings),
        ("contract_family_rules.json", family_rules),
    ]:
        path = contract_dir / name
        path.write_text(canonical_dumps(obj) + "\n", encoding="utf-8")
        # console.log POL-09: policy file written.
        print("[phase2:refactor-freeze] main: wrote %s." % path.as_posix())
        update_manifest(repo_root, run_id, "results/%s/contract/%s" % (run_id, name), obj)
    # console.log POL-10: policy-freeze pipeline complete.
    print("[phase2:refactor-freeze] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log POL-11: script invoked as main.
    print("[phase2:refactor-freeze] __main__: invoking main.")
    raise SystemExit(main())
