"""P4 test: bundle pointer matches the asset; tampering is detected."""

import hashlib
import json
from pathlib import Path

import yaml


# console.log P4T06-01: test module import confirms bundle check is active.
print("[test:p4-bundle] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_bundle():
    """Pointer hash equals asset bytes; a flipped byte mismatches."""
    # console.log P4T06-02: bundle test entry.
    print("[test:p4-bundle] test_bundle: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    pointer = json.loads((REPO_ROOT / "releases" / ("%s.json" % cfg["run_id"])).read_text(encoding="utf-8"))
    asset = REPO_ROOT / "releases" / pointer["bundle"]
    assert asset.exists()
    assert hashlib.sha256(asset.read_bytes()).hexdigest() == pointer["sha256"]
    tampered = bytearray(asset.read_bytes())
    tampered[100] ^= 1
    assert hashlib.sha256(bytes(tampered)).hexdigest() != pointer["sha256"]
    # console.log P4T06-03: bundle verified.
    print("[test:p4-bundle] test_bundle: passed.")
