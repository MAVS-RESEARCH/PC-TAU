"""Phase-1 task census: enumerate upstream tasks without importing agent logic."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, census, sha256_of_canonical


# console.log CENSUS-01: script entry confirms census pipeline start.
print("[phase1:census] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log CENSUS-02: argparse configuration entry.
    print("[phase1:census] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Enumerate upstream tasks.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log CENSUS-03: arguments parsed.
    print("[phase1:census] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log CENSUS-04: manifest update entry.
    print("[phase1:census] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log CENSUS-05: manifest update complete.
    print("[phase1:census] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Enumerate tasks and write census file."""
    # console.log CENSUS-06: main entry.
    print("[phase1:census] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log CENSUS-07: experiment config loaded.
    print("[phase1:census] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    upstream_dir = repo_root / cfg["upstream"]["dir"]
    domains = list(cfg["domains"]["primary"])
    records = census(upstream_dir, domains)
    # console.log CENSUS-08: census records assembled.
    print("[phase1:census] main: assembled %d records." % len(records))
    payload = {"run_id": run_id, "domains": domains, "records": records}
    out_path = repo_root / "external_source" / "task_census.json"
    out_path.write_text(canonical_dumps(payload) + "\n", encoding="utf-8")
    # console.log CENSUS-09: task census written.
    print("[phase1:census] main: wrote %s." % out_path.as_posix())
    update_manifest(repo_root, run_id, "external_source/task_census.json", payload)
    # console.log CENSUS-10: census pipeline complete.
    print("[phase1:census] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log CENSUS-11: script invoked as main.
    print("[phase1:census] __main__: invoking main.")
    raise SystemExit(main())
