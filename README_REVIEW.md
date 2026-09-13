# Anonymous Reviewer Snapshot

This branch (`anonymous`) is a sanitized reviewer snapshot prepared for double-blind review.

- Author-specific Git history was intentionally omitted. This branch is an orphan snapshot with a single root commit; it has no parent relationship to any author history. Commit author/committer are `Anonymous Authors` (UTC, non-identifying).
- Identity-bearing provenance was redacted from tracked content only: author-controlled repository URLs, organization/owner names, copyright-holder names (review copy only), local filesystem paths/usernames, and current-repository commit/object identifiers (replaced with stable `<AUTHOR_REPO_COMMIT_xxx>` aliases preserving chronology).
- Scientific results, negative evidence, failures, metrics, sample counts, freeze geometry, costs, policy semantics, theorem claims, preregistered criteria, external upstream provenance, and historical chronology were preserved exactly in meaning. No result laundering was performed.
- External scientific provenance was preserved: upstream repository URL, upstream commit SHA, source tree hash, file counts, license attribution, model/provider identifiers, and run IDs (which embed the upstream short SHA) remain byte-identical except for the single identity-bearing `repo_root` filesystem path.
- One identity redaction changed bytes authenticated by seals: `external_source/source_manifest.json` (`repo_root` absolute Windows path replaced with `<REPO>`). Consequently:
  - `results/pctau-20260906-672227c/phase_manifest.json` entry for that file was recomputed from the sanitized bytes (canonical JSON SHA-256);
  - the corresponding 12-character prefix pin in `tests/audit/test_prephase4.py` and the narrative mention in `Path.md` were updated to the review hash prefix;
  - these are REVIEW-SNAPSHOT hashes authenticating sanitized bytes, not the original experiment seals. Canonical seals remain authoritative in the canonical branch and will be restored after review.
- Two history-dependent tests (`tests/phase2/test_no_production_planner_in_phase2.py`, `tests/phase3/test_planner_first_use.py`) previously asserted `git log <Phase-2-seal-commit>` emptiness. Because history is intentionally omitted, they now explicitly skip the history assertion when the redacted commit is absent (non-zero `git log` exit) while still enforcing the file-content gates (no planner imports in Phase-2 scope; planner/checker agreement). See inline `REVIEW-SNAPSHOT` comments.
- Review integrity: `REVIEW_SHA256SUMS.txt` (SHA-256 of final reviewer bytes, excluding itself) authenticates this snapshot. `ANONYMIZATION_REPORT.json` summarizes transformations and gate results without revealing original identity values.
- Canonical identity/provenance will be restored after double-blind review. The canonical branch remains authoritative and untouched.

## Reproduction (reviewer)

Requires Python >=3.12 with `pyyaml`, `jsonschema`, `pandas`, `pyarrow`, `pytest`, `zstandard`.

A. READ-ONLY INSPECTION
Inspect existing sealed outputs and reviewer hashes. Safest first: `results/pctau-20260906-672227c/SEALED`, `results/pctau-20260906-672227c/reports/CLAIMS.md`, `results/pctau-20260906-672227c/reports/phase3_summary.json`, plus `REVIEW_SHA256SUMS.txt`. No side effects.

B. REVIEWER TEST SUITE
Expected anonymous-snapshot baseline: 66 passed, 4 failed. The four failures are environment-only checks requiring git-ignored / non-distributed upstream or release artifacts and are also present on a clean canonical checkout without those assets. See `ANONYMIZATION_REPORT.json` for the exact failure list.

```bash
pytest -q
```

C. SEALED-OUTPUT REPLAY / RESEAL VERIFICATION
Sealed-output replay / reseal verification (deterministic verification of the already-materialized sealed result state). This is distinct from full experimental regeneration and does not rerun Phases 1–3 from source. It operates on existing result material and requires the dependencies above.

```bash
python scripts/run_pc_tau.py --reproduce pctau-20260906-672227c
python scripts/run_pc_tau.py --check-gate g4 --config configs/experiment.yaml
```

D. LIVE / PROVIDER REPLICATION
No reviewer command here performs fresh provider/model inference. Ordinary review and verification do not require API keys or paid provider access.

E. LLM1
For the supporting LLM1 follow-on, see `llm1/REPRODUCE.md`. Deterministic replay uses archived raw records; fresh provider inference would be a new replication (never byte-identical exact replay) and is not required for artifact review.

The sealed bundle pointer (`releases/pctau-20260906-672227c.json`) and upstream re-clone via URL + SHA in `external_source/source_manifest.json` remain as in the canonical run. Ignored build artifacts (`external_source/_upstream/`, `releases/*.tar.zst`, etc. per `.gitignore`) are not part of this snapshot, as in the canonical tracked tree.
