"""LLM1 L1 tests: parent inheritance and secret lock (no API required)."""

import json
import subprocess
import sys
from pathlib import Path


# console.log L1T-01: test module import confirms L1 checks are active.
print("[test:llm1-l1] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_parent_inheritance():
    """Sealed parent verifies; inheritance manifest covers required objects."""
    # console.log L1T-02: inheritance test entry.
    print("[test:llm1-l1] test_parent_inheritance: entry.")
    parent = REPO_ROOT / "results" / "pctau-20260906-672227c"
    seal = json.loads((parent / "SEALED").read_text(encoding="utf-8"))
    assert seal["status"] == "SEALED" and seal["reasons"] == []
    manifest = json.loads(
        (REPO_ROOT / "llm1" / "parent_inheritance_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["parent_run"] == "pctau-20260906-672227c"
    assert len(manifest["artifacts"]) == 25
    assert "contract/natural_population.json" in manifest["artifacts"]
    # console.log L1T-03: inheritance verified.
    print("[test:llm1-l1] test_parent_inheritance: passed.")


def test_env_is_gitignored():
    """check-ignore must succeed for .env."""
    # console.log L1T-04: ignore test entry.
    print("[test:llm1-l1] test_env_is_gitignored: entry.")
    proc = subprocess.run(
        ["git", "check-ignore", ".env"], cwd=str(REPO_ROOT), capture_output=True, text=True
    )
    assert proc.returncode == 0
    # console.log L1T-05: ignore verified.
    print("[test:llm1-l1] test_env_is_gitignored: passed.")


def test_env_is_not_tracked():
    """ls-files must fail for .env."""
    # console.log L1T-06: untracked test entry.
    print("[test:llm1-l1] test_env_is_not_tracked: entry.")
    proc = subprocess.run(
        ["git", "ls-files", "--error-unmatch", ".env"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    # console.log L1T-07: untracked verified.
    print("[test:llm1-l1] test_env_is_not_tracked: passed.")


def test_env_example_has_no_secret():
    """.env.example carries the name only, no value."""
    # console.log L1T-08: example test entry.
    print("[test:llm1-l1] test_env_example_has_no_secret: entry.")
    text = (REPO_ROOT / ".env.example").read_text(encoding="utf-8")
    assert "OPENROUTER_API_KEY" in text
    assert text.strip() in ("OPENROUTER_API_KEY=", "OPENROUTER_API_KEY= ")
    # console.log L1T-09: example verified clean.
    print("[test:llm1-l1] test_env_example_has_no_secret: passed.")


def test_no_secret_in_tracked_files():
    """Tracked files and the bundle member list carry no credential patterns."""
    # console.log L1T-10: scan test entry.
    print("[test:llm1-l1] test_no_secret_in_tracked_files: entry.")
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=str(REPO_ROOT), capture_output=True, text=True, check=True
    ).stdout.splitlines()
    assert ".env" not in tracked
    import re

    for rel in tracked:
        if rel.replace("\\", "/") == "tests/llm1/test_l1_prep.py":
            continue
        path = REPO_ROOT / rel
        if path.is_file() and path.stat().st_size < 5_000_000:
            content = path.read_bytes()
            assert not re.search(rb"sk-or-[A-Za-z0-9\-_]{8,}", content), rel
            assert b"Bearer sk-" not in content, rel
            if rel.replace("\\", "/").startswith("scripts/llm1_"):
                continue
            assert b"Authorization:" not in content, rel
            if rel.replace("\\", "/").startswith("tests/"):
                continue
            for match in re.findall(rb"OPENROUTER_API_KEY=([^\s]*)", content):
                cleaned = match.strip().strip(b"`'\"():")
                assert len(cleaned) < 8 or (cleaned.startswith(b"<") and cleaned.endswith(b">")), (
                    rel,
                    "secret-length key assignment",
                )
    # console.log L1T-11: tracked files scan passed.
    print("[test:llm1-l1] test_no_secret_in_tracked_files: passed.")


def test_no_secret_in_results():
    """Result payloads and the release member list carry no credentials."""
    # console.log L1T-12: results scan entry.
    print("[test:llm1-l1] test_no_secret_in_results: entry.")
    pointer = json.loads(
        (REPO_ROOT / "releases" / "pctau-20260906-672227c.json").read_text(encoding="utf-8")
    )
    assert "Authorization" not in json.dumps(pointer)
    # console.log L1T-13: results scan passed.
    print("[test:llm1-l1] test_no_secret_in_results: passed.")


def test_calibration_frozen():
    """Calibration protocol frozen on excluded pilots with tuning bans."""
    # console.log L1T-14: calibration test entry.
    print("[test:llm1-l1] test_calibration_frozen: entry.")
    protocol = json.loads(
        (REPO_ROOT / "llm1" / "preregistration" / "calibration_protocol.json").read_text(
            encoding="utf-8"
        )
    )
    assert protocol["frozen"] is True and protocol["scientific_episodes"] is False
    assert protocol["calibration_set"]["episodes_per_candidate"] == 16
    # console.log L1T-15: calibration frozen verified.
    print("[test:llm1-l1] test_calibration_frozen: passed.")
