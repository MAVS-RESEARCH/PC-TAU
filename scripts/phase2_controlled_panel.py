"""Phase-2 controlled factorial panel: 32 balanced-by-design tasks (Track F)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log PANEL-01: script entry confirms panel pipeline start.
print("[phase2:panel] entry: parsing arguments.")


REGIMES = ["R-zero", "R-finite", "R-structural", "E/R-complementary"]

TRANSFORMS = {
    "R-zero": "optimal closure avoids the representation path; representation restriction preserves optimal length",
    "R-finite": "representation restriction raises optimal length finitely via the evidence-authority fallback",
    "R-structural": "every closure path uses the representation path; representation restriction destroys closure",
    "E/R-complementary": "closure needs one evidence step plus one representation step; either single restriction destroys closure",
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log PANEL-02: argparse configuration entry.
    print("[phase2:panel] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Build controlled panel.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log PANEL-03: arguments parsed.
    print("[phase2:panel] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log PANEL-04: manifest update entry.
    print("[phase2:panel] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log PANEL-05: manifest update complete.
    print("[phase2:panel] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Synthesize 8 tasks per regime from non-pilot bases."""
    # console.log PANEL-06: main entry.
    print("[phase2:panel] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log PANEL-07: experiment config loaded.
    print("[phase2:panel] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    census = json.loads(
        (repo_root / "external_source" / "task_census.json").read_text(encoding="utf-8")
    )
    pilot = json.loads(
        (repo_root / "results" / run_id / "pilot" / "pilot_ids.json").read_text(
            encoding="utf-8"
        )
    )
    excluded = set(pilot["pilot_ids"])
    bases = sorted(
        r["task_id"] for r in census["records"] if r["task_id"] not in excluded
    )
    # console.log PANEL-08: non-pilot bases resolved.
    print("[phase2:panel] main: non-pilot bases=%d." % len(bases))
    transform_family = {
        "run_id": run_id,
        "frozen": True,
        "templates": TRANSFORMS,
    }
    family_hash = sha256_of_canonical(transform_family)
    # console.log PANEL-09: transformation family hashed.
    print("[phase2:panel] main: transform family hash=%s." % family_hash[:12])
    tasks: list[dict] = []
    for r, regime in enumerate(REGIMES):
        for i in range(8):
            base = bases[(r * 8 + i) % len(bases)]
            tasks.append(
                {
                    "controlled_id": "controlled:%s:%d" % (regime, i),
                    "regime": regime,
                    "base_task_id": base,
                    "transformation_rule_id": "T-%s" % regime,
                    "transformation": TRANSFORMS[regime],
                    "non_pilot_base": True,
                }
            )
    panel = {
        "run_id": run_id,
        "track": "F-controlled",
        "balanced_by_design": True,
        "estimates_natural_frequency": False,
        "transform_family_hash": family_hash,
        "count": len(tasks),
        "per_regime": 8,
        "tasks": tasks,
    }
    # console.log PANEL-10: panel assembled.
    print("[phase2:panel] main: assembled tasks=%d." % len(tasks))
    out_path = repo_root / "results" / run_id / "contract" / "controlled_panel.json"
    out_path.write_text(canonical_dumps(panel) + "\n", encoding="utf-8")
    # console.log PANEL-11: controlled panel written.
    print("[phase2:panel] main: wrote %s." % out_path.as_posix())
    update_manifest(
        repo_root, run_id, "results/%s/contract/controlled_panel.json" % run_id, panel
    )
    # console.log PANEL-12: panel pipeline complete.
    print("[phase2:panel] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log PANEL-13: script invoked as main.
    print("[phase2:panel] __main__: invoking main.")
    raise SystemExit(main())
