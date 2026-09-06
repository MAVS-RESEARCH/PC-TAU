"""Phase-1 source pinning: record immutable upstream identity (WorkPlan 1.3)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, pin_source, sha256_of_canonical


# console.log PIN-01: script entry confirms arguments will be parsed.
print("[phase1:pin-source] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log PIN-02: argparse configuration entry.
    print("[phase1:pin-source] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Pin upstream tau2-bench source.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log PIN-03: arguments parsed.
    print("[phase1:pin-source] parse_args: config=%s run-id=%s." % (args.config, args.run_id))
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest (no sidecars, Fix 9)."""
    # console.log PIN-04: manifest update entry.
    print("[phase1:pin-source] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log PIN-05: manifest update complete.
    print("[phase1:pin-source] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Pin source and write manifest."""
    # console.log PIN-06: main entry.
    print("[phase1:pin-source] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log PIN-07: experiment config loaded.
    print("[phase1:pin-source] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    url = cfg["upstream"]["url"]
    expected_rev = cfg["upstream"]["commit_sha"]
    upstream_dir = repo_root / cfg["upstream"]["dir"]
    manifest = pin_source(url, expected_rev, upstream_dir, repo_root)
    # console.log PIN-08: upstream identity recorded.
    print("[phase1:pin-source] main: upstream identity recorded.")
    out_path = repo_root / "external_source" / "source_manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log PIN-09: source manifest written.
    print("[phase1:pin-source] main: wrote %s." % out_path.as_posix())
    update_manifest(repo_root, run_id, "external_source/source_manifest.json", manifest)
    # console.log PIN-10: pin-source pipeline complete.
    print("[phase1:pin-source] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log PIN-11: script invoked as main.
    print("[phase1:pin-source] __main__: invoking main.")
    raise SystemExit(main())
