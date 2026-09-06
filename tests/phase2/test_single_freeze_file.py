"""P2 test: exactly one canonical freeze file exists (Fix 9)."""

from pathlib import Path


# console.log P2T14-01: test module import confirms freeze-file check is active.
print("[test:p2-single-freeze] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_single_freeze_file():
    """configs/freezes.yaml exists; freeze_lattice.yaml must not exist."""
    # console.log P2T14-02: freeze-file test entry.
    print("[test:p2-single-freeze] test_single_freeze_file: entry.")
    assert (REPO_ROOT / "configs" / "freezes.yaml").exists()
    assert not (REPO_ROOT / "configs" / "freeze_lattice.yaml").exists()
    # console.log P2T14-03: single freeze file verified.
    print("[test:p2-single-freeze] test_single_freeze_file: passed.")
