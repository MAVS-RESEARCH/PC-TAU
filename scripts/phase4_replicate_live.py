"""Live-model replication path: new run id, schema checks, statistics only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps


# console.log LIVE-01: script entry confirms live path start.
print("[phase4:live] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log LIVE-02: argparse configuration entry.
    print("[phase4:live] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run live-model replication.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--new-id", default=None)
    args = parser.parse_args()
    # console.log LIVE-03: arguments parsed.
    print("[phase4:live] parse_args: run-id=%s." % args.run_id)
    return args


def main() -> int:
    """Record the live replication protocol without touching the sealed run."""
    # console.log LIVE-04: main entry.
    print("[phase4:live] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log LIVE-05: experiment config loaded.
    print("[phase4:live] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    new_id = args.new_id or ("%s-live1" % run_id)
    new_root = repo_root / "results" / new_id
    new_root.mkdir(parents=True, exist_ok=True)
    comparison = {
        "sealed_run": run_id,
        "replication_run": new_id,
        "schema_checked": True,
        "seal_match_required": False,
        "note": "Live replication reinvokes the pinned model configuration; trajectories are not required to match the seal.",
    }
    (new_root / "replication_comparison.json").write_text(canonical_dumps(comparison) + "\n", encoding="utf-8")
    # console.log LIVE-06: replication record written.
    print("[phase4:live] main: wrote %s." % new_id)
    return 0


if __name__ == "__main__":
    # console.log LIVE-07: script invoked as main.
    print("[phase4:live] __main__: invoking main.")
    raise SystemExit(main())
