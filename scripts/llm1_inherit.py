"""LLM1 inheritance: hash-verify the sealed parent and record the manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps


# console.log INH-01: script entry confirms inheritance pipeline start.
print("[llm1:inherit] entry: parsing arguments.")


PARENT_RUN = "pctau-20260906-672227c"

INHERITED = [
    "contract/natural_population.json",
    "contract/partial_tasks.jsonl",
    "contract/task_contracts.jsonl",
    "contract/contract_families.jsonl",
    "contract/repair_actions.jsonl",
    "contract/touch_records.parquet",
    "contract/route_classification.parquet",
    "contract/controlled_panel.json",
    "contract/semantic_boundary_policy.json",
    "contract/admissible_refactorings.json",
    "contract/contract_family_rules.json",
    "contract/failure_cards.jsonl",
    "contract/CONTRACT_SEALED",
    "exact/freeze_results.parquet",
    "exact/k_pi_signatures.parquet",
    "pilot/pilot_ids.json",
    "reports/phase3_summary.json",
    "PHASE3_COMPLETE",
    "SEALED",
    "configs/freezes.yaml",
    "configs/costs.yaml",
    "configs/models.yaml",
    "preregistration/model_protocol.json",
    "preregistration/user_response_protocol.json",
    "preregistration/nonclaims.json",
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log INH-02: argparse configuration entry.
    print("[llm1:inherit] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Verify parent inheritance.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    args = parser.parse_args()
    # console.log INH-03: arguments parsed.
    print("[llm1:inherit] parse_args: config=%s." % args.config)
    return args


def main() -> int:
    """Verify sealed parent objects and write the inheritance manifest."""
    # console.log INH-04: main entry.
    print("[llm1:inherit] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    parent_root = repo_root / "results" / PARENT_RUN
    seal = json.loads((parent_root / "SEALED").read_text(encoding="utf-8"))
    assert seal["status"] == "SEALED" and seal["reasons"] == [], "parent not sealed"
    # console.log INH-05: parent seal verified.
    print("[llm1:inherit] main: parent SEALED with empty reasons.")
    pointer = json.loads((repo_root / "releases" / ("%s.json" % PARENT_RUN)).read_text(encoding="utf-8"))
    bundle = repo_root / "releases" / pointer["bundle"]
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() == pointer["sha256"], "bundle mismatch"
    # console.log INH-06: release pointer and bundle verified.
    print("[llm1:inherit] main: bundle verified.")
    entries: dict[str, str] = {}
    for rel in INHERITED:
        if rel.startswith(("configs/", "preregistration/")):
            path = repo_root / rel
        else:
            path = parent_root / rel
        assert path.exists(), "missing inherited object %s" % rel
        entries[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    # console.log INH-07: inherited objects hashed.
    print("[llm1:inherit] main: hashed=%d." % len(entries))
    manifest = {"parent_run": PARENT_RUN, "followon_run": "%s-llm1" % PARENT_RUN, "artifacts": entries}
    out = repo_root / "llm1" / "parent_inheritance_manifest.json"
    out.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log INH-08: inheritance manifest written.
    print("[llm1:inherit] main: wrote %s." % out.as_posix())
    return 0


if __name__ == "__main__":
    # console.log INH-09: script invoked as main.
    print("[llm1:inherit] __main__: invoking main.")
    raise SystemExit(main())
