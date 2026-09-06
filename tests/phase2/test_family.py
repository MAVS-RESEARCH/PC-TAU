"""P2 test: contract-family status logic (IDENTIFIED, PARTIAL, INVALID)."""

import sys
from pathlib import Path


# console.log P2T06-01: test module import confirms family check is active.
print("[test:p2-family] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_family_status():
    """Agree gives IDENTIFIED, disagree gives PARTIAL, missing gives INVALID."""
    # console.log P2T06-02: family test entry.
    print("[test:p2-family] test_family_status: entry.")
    from pc_tau.semantics import family_status

    assert family_status("a", True, True, False, [])["status"] == "IDENTIFIED"
    assert family_status("b", True, True, True, ["auth:x"])["status"] == "PARTIAL"
    assert family_status("c", False, True, False, [])["status"] == "INVALID"
    assert family_status("d", True, False, False, [])["status"] == "INVALID"
    # console.log P2T06-03: family logic verified.
    print("[test:p2-family] test_family_status: passed.")
