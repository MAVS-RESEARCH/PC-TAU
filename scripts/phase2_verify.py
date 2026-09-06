"""Phase-2 independent verification: second-path fact checking (Fix 2)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.semantics import verify_facts
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log VER-01: script entry confirms verification pipeline start.
print("[phase2:verify] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log VER-02: argparse configuration entry.
    print("[phase2:verify] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Verify Pass-A facts.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log VER-03: arguments parsed.
    print("[phase2:verify] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log VER-04: manifest update entry.
    print("[phase2:verify] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log VER-05: manifest update complete.
    print("[phase2:verify] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Verify facts per task with the independent second path."""
    # console.log VER-06: main entry.
    print("[phase2:verify] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log VER-07: experiment config loaded.
    print("[phase2:verify] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    by_task: dict[str, list[dict]] = {}
    with open(contract_dir / "semantic_facts.jsonl", encoding="utf-8") as fh:
        for line in fh:
            fact = json.loads(line)
            by_task.setdefault(fact["task_id"], []).append(fact)
    # console.log VER-08: facts grouped per task.
    print("[phase2:verify] main: grouped tasks=%d." % len(by_task))
    records: list[dict] = []
    for task_id in sorted(by_task):
        numeric = int(task_id.split(":")[1])
        task_records, _ = verify_facts(by_task[task_id], task_id, numeric)
        records.extend(task_records)
    # console.log VER-09: verification complete.
    print("[phase2:verify] main: verified records=%d." % len(records))
    out_path = contract_dir / "extraction_records.jsonl"
    with open(out_path, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(canonical_dumps(rec) + "\n")
    # console.log VER-10: extraction records written.
    print("[phase2:verify] main: wrote %s." % out_path.as_posix())
    update_manifest(
        repo_root, run_id, "results/%s/contract/extraction_records.jsonl" % run_id, records
    )
    # console.log VER-11: verification pipeline complete.
    print("[phase2:verify] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log VER-12: script invoked as main.
    print("[phase2:verify] __main__: invoking main.")
    raise SystemExit(main())
