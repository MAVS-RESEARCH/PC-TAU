"""P4 test: exact replay from the bundle is byte-identical."""

import importlib.util
import json
from pathlib import Path

import yaml


# console.log P4T07-01: test module import confirms replay check is active.
print("[test:p4-replay] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_exact_replay():
    """Bundle extract plus sample recomputation matches the sealed outputs."""
    # console.log P4T07-02: replay test entry.
    print("[test:p4-replay] test_exact_replay: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    pointer = json.loads((REPO_ROOT / "releases" / ("%s.json" % run_id)).read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location(
        "phase4_seal", str(REPO_ROOT / "scripts" / "phase4_seal.py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    bundle_path = REPO_ROOT / "releases" / pointer["bundle"]
    assert module.exact_replay_check(REPO_ROOT, run_id, bundle_path, pointer["sha256"]) is True
    # console.log P4T07-03: replay verified identical.
    print("[test:p4-replay] test_exact_replay: passed.")
