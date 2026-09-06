"""P3 test: production planner on hand-solved regime graphs (Fix 7)."""

import sys
from pathlib import Path


# console.log P3T03-01: test module import confirms synthetic check is active.
print("[test:p3-synthetic] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_planner_synthetic():
    """Finite substitution, zero gap, structural and complementary cases solve as expected."""
    # console.log P3T03-02: synthetic test entry.
    print("[test:p3-synthetic] test_planner_synthetic: entry.")
    from pc_tau.freeze import lattice

    template = (
        {"OPEN": [{"repair": "qR", "to": "CLOSED"}, {"repair": "qE", "to": "S1"}], "S1": [{"repair": "qA", "to": "CLOSED"}], "CLOSED": []},
        {"qR": {"R"}, "qE": {"E"}, "qA": {"A"}},
    )
    result = lattice("syn-finite", template[0], template[1], "OPEN", "CLOSED")
    assert result["cells"]["F000"]["kappa"] == 1
    assert result["cells"]["F010"]["kappa"] == 2
    assert result["r_class"] == "FINITE_POSITIVE"
    # console.log P3T03-03: finite substitution verified.
    print("[test:p3-synthetic] finite substitution verified.")
    zero = (
        {"OPEN": [{"repair": "qE0", "to": "S1"}], "S1": [{"repair": "qA0", "to": "CLOSED"}], "CLOSED": []},
        {"qE0": {"E"}, "qA0": {"A"}},
    )
    zero_result = lattice("syn-zero", zero[0], zero[1], "OPEN", "CLOSED")
    assert zero_result["r_class"] == "ZERO" and zero_result["delta_r"] == 0
    structural = (
        {"OPEN": [{"repair": "qR1", "to": "CLOSED"}], "CLOSED": []},
        {"qR1": {"R"}},
    )
    struct_result = lattice("syn-struct", structural[0], structural[1], "OPEN", "CLOSED")
    assert struct_result["cells"]["F010"]["kappa"] == "INF" and struct_result["r_class"] == "STRUCTURAL"
    complementary = (
        {"OPEN": [{"repair": "qE", "to": "S1"}], "S1": [{"repair": "qR", "to": "CLOSED"}], "CLOSED": []},
        {"qE": {"E"}, "qR": {"R"}},
    )
    comp_result = lattice("syn-comp", complementary[0], complementary[1], "OPEN", "CLOSED")
    assert comp_result["interactions"]["er_complementary"] is True
    # console.log P3T03-04: zero, structural and complementary verified.
    print("[test:p3-synthetic] test_planner_synthetic: passed.")
