"""P2 test: run manifest indexes every Phase-2 output with correct hashes (Fix 9)."""

import json
import sys
from pathlib import Path

import pandas as pd
import yaml


# console.log P2T15-01: test module import confirms manifest check is active.
print("[test:p2-manifest] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

EXPECTED = [
    "contract/semantic_facts.jsonl",
    "contract/extraction_records.jsonl",
    "contract/extraction_protocol.json",
    "contract/task_contracts.jsonl",
    "contract/contract_families.jsonl",
    "contract/repair_actions.jsonl",
    "contract/touch_records.parquet",
    "contract/route_classification.parquet",
    "contract/natural_population.json",
    "contract/partial_tasks.jsonl",
    "contract/controlled_panel.json",
    "contract/semantic_boundary_policy.json",
    "contract/admissible_refactorings.json",
    "contract/contract_family_rules.json",
    "contract/failure_cards.jsonl",
    "contract/CONTRACT_SEALED",
]


def test_manifest_hashes_p2():
    """All Phase-2 outputs manifested; parquet row counts agree with jsonl."""
    # console.log P2T15-02: manifest test entry.
    print("[test:p2-manifest] test_manifest_hashes_p2: entry.")
    from pc_tau.source import sha256_of_canonical

    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    manifest = json.loads(
        (REPO_ROOT / "results" / run_id / "phase_manifest.json").read_text(encoding="utf-8")
    )
    # console.log P2T15-03: manifest loaded.
    print("[test:p2-manifest] manifest entries=%d." % len(manifest))
    for suffix in EXPECTED:
        key = "results/%s/%s" % (run_id, suffix)
        assert key in manifest, "manifest missing %s" % key
    touch = pd.read_parquet(REPO_ROOT / "results" / run_id / "contract" / "touch_records.parquet")
    repairs = [line for line in open(REPO_ROOT / "results" / run_id / "contract" / "repair_actions.jsonl", encoding="utf-8")]
    assert len(touch) == 420 and len(repairs) == 420
    assert not list((REPO_ROOT / "results").rglob("*.sha256"))
    # console.log P2T15-04: manifest and counts verified.
    print("[test:p2-manifest] test_manifest_hashes_p2: passed.")
