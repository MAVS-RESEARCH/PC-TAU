"""Phase-3 controls: reject-on-open, evidence-only and untyped-generic baselines."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.runtime import baseline_evidence_only, baseline_reject_on_open, baseline_untyped_generic
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log CTL-01: script entry confirms controls pipeline start.
print("[phase3:controls] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log CTL-02: argparse configuration entry.
    print("[phase3:controls] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run control baselines.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log CTL-03: arguments parsed.
    print("[phase3:controls] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log CTL-04: manifest update entry.
    print("[phase3:controls] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log CTL-05: manifest update complete.
    print("[phase3:controls] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Run the three baselines over the primary core unrestricted cell."""
    # console.log CTL-06: main entry.
    print("[phase3:controls] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log CTL-07: experiment config loaded.
    print("[phase3:controls] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    rows: list[dict] = []
    for task_id in sorted(population["task_ids"]):
        reject = baseline_reject_on_open()
        rows.append({"task_id": task_id, "baseline": "reject_on_open", **reject})
        evidence = baseline_evidence_only(["qE_slow", "qR_fast", "qA_close"])
        rows.append({"task_id": task_id, "baseline": "evidence_only", **evidence})
        generic = baseline_untyped_generic(["qR_fast"])
        rows.append({"task_id": task_id, "baseline": "untyped_generic", **generic})
    # console.log CTL-08: baselines complete.
    print("[phase3:controls] main: rows=%d." % len(rows))
    controls_dir = repo_root / "results" / run_id / "controls"
    controls_dir.mkdir(parents=True, exist_ok=True)
    out_path = controls_dir / "control_results.jsonl"
    with open(out_path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(canonical_dumps(row) + "\n")
    # console.log CTL-09: controls written.
    print("[phase3:controls] main: wrote %s." % out_path.as_posix())
    update_manifest(repo_root, run_id, "results/%s/controls/control_results.jsonl" % run_id, rows)
    # console.log CTL-10: controls pipeline complete.
    print("[phase3:controls] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log CTL-11: script invoked as main.
    print("[phase3:controls] __main__: invoking main.")
    raise SystemExit(main())
