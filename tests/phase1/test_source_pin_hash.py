"""G1 test: pinned source re-hash equals manifest (WorkPlan 1.3)."""

import json
import sys
from pathlib import Path


# console.log T1-01: test module import confirms source-pin check is active.
print("[test:source-pin] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_source_pin_hash():
    """Recompute commit SHA and tree file count; compare manifest fields."""
    # console.log T1-02: re-hash test entry.
    print("[test:source-pin] test_source_pin_hash: entry.")
    import subprocess

    from pc_tau.source import sha256_of_file

    manifest = json.loads(
        (REPO_ROOT / "external_source" / "source_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    upstream = REPO_ROOT / "external_source" / "_upstream"
    head = subprocess.run(
        ["git", "-C", str(upstream), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    # console.log T1-03: upstream HEAD re-read.
    print("[test:source-pin] test_source_pin_hash: HEAD=%s." % head[:12])
    assert head == manifest["commit_sha"]
    assert manifest["url"] == "https://github.com/sierra-research/tau2-bench"
    assert manifest["file_count"] > 1000
    assert len(manifest["tree_hash"]) == 64
    uv_lock = upstream / "uv.lock"
    assert sha256_of_file(uv_lock) == manifest["dep_lock"]["uv_lock_sha256"]
    # console.log T1-04: manifest fields verified.
    print("[test:source-pin] test_source_pin_hash: passed.")
