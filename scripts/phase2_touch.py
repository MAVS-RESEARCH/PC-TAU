"""Phase-2 mechanical touch derivation with validation (no manual labels)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.repairs import legal_repairs
from pc_tau.source import canonical_dumps, sha256_of_canonical
from pc_tau.touch import derive_touch


# console.log TCH10-01: script entry confirms touch pipeline start.
print("[phase2:touch] entry: parsing arguments.")


TOOL_LOCATORS = {
    "qR_fast": "calculate",
    "qE_slow": "lookup",
    "qA_close": "transfer_to_human_agents",
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log TCH10-02: argparse configuration entry.
    print("[phase2:touch] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Derive mechanical touch.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log TCH10-03: arguments parsed.
    print("[phase2:touch] parse_args: config=%s." % args.config)
    return args


def snapshots_for(domain: str) -> dict[str, dict]:
    """Return per-state governance snapshots for the template topology.

    OPEN carries no admitted facts. S1 admits the evidence fact. CLOSED
    via the representation path exposes a new certificate distinction
    without new facts. CLOSED via the authority path admits delegation
    without new world facts. Snapshots make E/R/A mechanically separable.
    """
    # console.log TCH10-04: snapshot build entry.
    print("[phase2:touch] snapshots_for: entry domain=%s." % domain)
    base_pr = [["h0_open"], ["h1_mid"], ["h2_closed"]]
    exposed_pr = [["h0_open", "h1_mid"], ["h2_closed"]]
    base_lam = sorted(["source:tool:%s" % domain, "source:user"])
    snap = {
        "OPEN": {
            "H": [],
            "P_R": base_pr,
            "Lambda": base_lam,
        },
        "S1": {
            "H": ["fact_E:%s" % domain],
            "P_R": base_pr,
            "Lambda": base_lam,
        },
        "CLOSED_R": {
            "H": [],
            "P_R": exposed_pr,
            "Lambda": base_lam,
        },
        "CLOSED_A": {
            "H": ["fact_E:%s" % domain],
            "P_R": base_pr,
            "Lambda": sorted(base_lam + ["interface:approval"]),
        },
    }
    # console.log TCH10-05: snapshots complete.
    print("[phase2:touch] snapshots_for: complete.")
    return snap


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log TCH10-06: manifest update entry.
    print("[phase2:touch] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log TCH10-07: manifest update complete.
    print("[phase2:touch] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Extract repairs and derive touch for every contract edge."""
    # console.log TCH10-08: main entry.
    print("[phase2:touch] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log TCH10-09: experiment config loaded.
    print("[phase2:touch] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    contracts: list[dict] = []
    with open(contract_dir / "task_contracts.jsonl", encoding="utf-8") as fh:
        for line in fh:
            contracts.append(json.loads(line))
    # console.log TCH10-10: contracts loaded.
    print("[phase2:touch] main: contracts=%d." % len(contracts))
    repair_rows: list[dict] = []
    touch_rows: list[dict] = []
    for contract in contracts:
        domain = contract["domain"]
        locators = {
            "qR_fast": "external_source/_upstream/src/tau2/domains/%s/tools.py" % domain,
            "qE_slow": "external_source/_upstream/src/tau2/domains/%s/tools.py" % domain,
            "qA_close": "external_source/_upstream/src/tau2/domains/%s/tools.py" % domain,
        }
        for repair in legal_repairs(contract, locators):
            repair_rows.append(repair)
        snap = snapshots_for(domain)
        edges = [
            ("OPEN", "qR_fast", "CLOSED_R"),
            ("OPEN", "qE_slow", "S1"),
            ("S1", "qA_close", "CLOSED_A"),
        ]
        meta_by_repair = {
            "qR_fast": {"repair": "qR_fast"},
            "qE_slow": {"repair": "qE_slow", "adds_fact": True},
            "qA_close": {"repair": "qA_close"},
        }
        for pre, rep, post in edges:
            touch = derive_touch(
                snap[pre]["H"],
                snap[pre]["P_R"],
                snap[pre]["Lambda"],
                snap[post]["H"],
                snap[post]["P_R"],
                snap[post]["Lambda"],
                meta_by_repair[rep],
            )
            touch_rows.append(
                {
                    "task_id": contract["task_id"],
                    "repair": rep,
                    "pre_state": pre,
                    "post_state": post,
                    "touch": sorted(touch),
                }
            )
    # console.log TCH10-11: derivation complete for all contracts.
    print(
        "[phase2:touch] main: repairs=%d touches=%d."
        % (len(repair_rows), len(touch_rows))
    )
    repairs_path = contract_dir / "repair_actions.jsonl"
    with open(repairs_path, "w", encoding="utf-8") as fh:
        for row in repair_rows:
            fh.write(canonical_dumps(row) + "\n")
    # console.log TCH10-12: repairs written.
    print("[phase2:touch] main: wrote %s." % repairs_path.as_posix())
    touch_frame = pd.DataFrame(touch_rows)
    touch_path = contract_dir / "touch_records.parquet"
    touch_frame.to_parquet(touch_path, index=False)
    # console.log TCH10-13: touch parquet written.
    print("[phase2:touch] main: wrote %s rows=%d." % (touch_path.as_posix(), len(touch_frame)))
    update_manifest(
        repo_root, run_id, "results/%s/contract/repair_actions.jsonl" % run_id, repair_rows
    )
    update_manifest(
        repo_root,
        run_id,
        "results/%s/contract/touch_records.parquet" % run_id,
        touch_rows,
    )
    # console.log TCH10-14: touch pipeline complete.
    print("[phase2:touch] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log TCH10-15: script invoked as main.
    print("[phase2:touch] __main__: invoking main.")
    raise SystemExit(main())
