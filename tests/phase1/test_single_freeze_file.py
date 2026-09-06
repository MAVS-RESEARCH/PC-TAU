"""G1 test: exactly one canonical freeze file exists (Fix 9)."""

from pathlib import Path


# console.log T6-01: test module import confirms freeze-file check is active.
print("[test:single-freeze] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_single_freeze_file():
    """configs/freezes.yaml exists; freeze_lattice.yaml must not exist."""
    # console.log T6-02: freeze-file test entry.
    print("[test:single-freeze] test_single_freeze_file: entry.")
    assert (REPO_ROOT / "configs" / "freezes.yaml").exists()
    assert not (REPO_ROOT / "configs" / "freeze_lattice.yaml").exists()
    # console.log T6-03: single freeze file verified.
    print("[test:single-freeze] test_single_freeze_file: passed.")
