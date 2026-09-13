"""Safe run cleaner: remove only an explicitly named unsealed run (WorkPlan 0.6)."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


# console.log CLEAN-01: cleaner entry confirms argument parsing start.
print("[clean:run] entry: parsing arguments.")


SEAL_MARKERS = ("CONTRACT_SEALED", "PHASE3_COMPLETE", "SEALED", "INVALID")


def parse_args() -> argparse.Namespace:
    """Parse cleaner arguments."""
    # console.log CLEAN-02: argparse configuration entry.
    print("[clean:run] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Remove one unsealed run directory.")
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    # console.log CLEAN-03: arguments parsed.
    print("[clean:run] parse_args: run-id=%s." % args.run_id)
    return args


def main() -> int:
    """Remove results/<run-id> iff no seal marker is present."""
    # console.log CLEAN-04: main entry.
    print("[clean:run] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / "results" / args.run_id
    if not target.exists():
        # console.log CLEAN-05: nothing to remove (no-op).
        print("[clean:run] main: no-op, directory absent.")
        return 0
    for marker in SEAL_MARKERS:
        if (target / marker).exists() or list(target.rglob(marker)):
            # console.log CLEAN-06: sealed run refusal.
            print("[clean:run] main: refusal, sealed marker %s present." % marker)
            raise SystemExit("refusal: %s is sealed (%s present)" % (args.run_id, marker))
    # console.log CLEAN-07: unsealed removal proceeding.
    print("[clean:run] main: removing unsealed %s." % target.as_posix())
    shutil.rmtree(target)
    # console.log CLEAN-08: cleaner complete.
    print("[clean:run] main: complete.")
    return 0


if __name__ == "__main__":
    # console.log CLEAN-09: cleaner invoked as main.
    print("[clean:run] __main__: invoking main.")
    raise SystemExit(main())
