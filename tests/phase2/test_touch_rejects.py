"""P2 test: mechanical touch rejects with 6+ adversarial cases."""

import sys
from pathlib import Path

import pytest


# console.log P2T04-01: test module import confirms touch-reject check is active.
print("[test:p2-touch-rejects] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_touch_rejects():
    """Manual labels, firewall violations and atomicity splits must raise."""
    # console.log P2T04-02: rejection test entry.
    print("[test:p2-touch-rejects] test_touch_rejects: entry.")
    from pc_tau.touch import derive_touch

    base_pr = [["h0"], ["h1"]]
    with pytest.raises(ValueError):
        derive_touch([], base_pr, ["l"], ["f"], base_pr, ["l"], {"repair": "x", "resource_label": ["E"]})
    # console.log P2T04-03: manual label rejected.
    print("[test:p2-touch-rejects] manual label rejected.")
    with pytest.raises(ValueError):
        derive_touch([], base_pr, ["l"], [], [["h0", "h1"]], ["l"], {"repair": "r", "reads_external": True})
    with pytest.raises(ValueError):
        derive_touch([], base_pr, ["l"], ["f"], base_pr, ["l"], {"repair": "e", "alters_mapping": True})
    with pytest.raises(ValueError):
        derive_touch(["f"], base_pr, ["l"], ["f"], base_pr, ["l", "m"], {"repair": "a", "adds_fact": True})
    # console.log P2T04-04: firewall violations rejected.
    print("[test:p2-touch-rejects] firewall violations rejected.")
    assert derive_touch([], base_pr, ["l"], ["f"], base_pr, ["l"], {"repair": "e"}) == {"E"}
    assert derive_touch([], base_pr, ["l"], [], [["h0", "h1"]], ["l"], {"repair": "r"}) == {"R"}
    assert derive_touch(["f"], base_pr, ["l"], ["f"], base_pr, ["l", "m"], {"repair": "a"}) == {"A"}
    assert derive_touch([], base_pr, ["l"], [], base_pr, ["l"], {"repair": "n"}) == set()
    # console.log P2T04-05: positive derivations verified.
    print("[test:p2-touch-rejects] test_touch_rejects: passed.")
