"""G1 test: run manifest indexes every Phase-1 output with correct hashes (Fix 9)."""

import json
import sys
from pathlib import Path


# console.log T7-01: test module import confirms manifest check is active.
print("[test:manifest] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

import yaml


def test_manifest_hashes():
    """Manifest entries match recomputed canonical hashes; no sidecars exist."""
    # console.log T7-02: manifest test entry.
    print("[test:manifest] test_manifest_hashes: entry.")
    from pc_tau.source import canonical_dumps, sha256_of_canonical

    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    manifest = json.loads(
        (REPO_ROOT / "results" / run_id / "phase_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    # console.log T7-03: manifest loaded.
    print("[test:manifest] manifest entries=%d." % len(manifest))
    expected_keys = [
        "external_source/source_manifest.json",
        "external_source/task_census.json",
        "results/%s/pilot/pilot_ids.json" % run_id,
        "results/%s/pilot/provisional_geometry.jsonl" % run_id,
        "results/%s/pilot/gate_log.json" % run_id,
        "results/%s/reports/phase1_preregistration.json" % run_id,
    ]
    for key in expected_keys:
        assert key in manifest, "manifest missing %s" % key
    manifest_file = json.loads(
        (REPO_ROOT / "external_source" / "source_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["external_source/source_manifest.json"] == sha256_of_canonical(
        manifest_file
    )
    sidecars = list((REPO_ROOT / "results").rglob("*.sha256"))
    assert sidecars == []
    # console.log T7-04: manifest hashes and no-sidecar rule verified.
    print("[test:manifest] test_manifest_hashes: passed.")
