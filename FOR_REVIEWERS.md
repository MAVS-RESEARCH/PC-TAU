# For Reviewers

> **Start here.** This is a short map of the artifact: what it supports, where the final result is, and where to look if you want more detail.

## What this artifact is

This is a constructed multi-route benchmark over pinned tau-family customer-service tasks. It supports the paper's fixed-contract freezing claim: how exact resource freezes change repair geometry when authorization is open.

The main experiment is deterministic and exact. A separately preregistered `llm1` follow-on tests real trained models against the same frozen geometry and is supporting evidence only.

## `WorkPlan.md` and `Path.md`

**`WorkPlan.md` = what was supposed to happen.**

It is the design specification: planned phases, gates, requirements, and acceptance criteria.

**`Path.md` = what actually happened.**

It is the execution ledger: implementation steps, tests, failures, deviations, and gate outcomes.

`WorkPlan_LLM1.md` and `Path_LLM1.md` play the same roles for the supporting `llm1` experiment. You do not need to read any of these front-to-back; they are there if you want protocol or history detail.

## Main result

Authoritative result is the sealed run `pctau-20260906-672227c` (status `SEALED`, no open reasons).

- Track N (135 primary IDENTIFIED tasks): 135/135 `FINITE_POSITIVE`, `K=[1,1,2,1,INF,1,INF,INF]`, `delta_R=1`.
- Track F (32 controlled tasks, balanced by design): `ZERO` 8, `FINITE` 8, `STRUCTURAL` 16.
- Main-artifact probes (deterministic scripted stand-ins, 5,436 paired episodes): 0 unsafe attempts; governance and regret differ by family and freeze (see phase summary).
- Sealed claims (3 only): finite substitution in constructed contracts; controlled-regime reproduction; typing invariance under the frozen refactoring class.
- Explicitly disabled: learned-agent claims, native multi-route realization, natural PARTIAL ambiguity, and all prevalence, superiority, or safety claims.

The matching 5,436 count in `llm1` refers to a separate provider-backed schedule, not these probe episodes; do not equate them.

## Where to look

1. `results/pctau-20260906-672227c/reports/CLAIMS.md` — the 3 sealed claims and their evidence pointers
2. `results/pctau-20260906-672227c/SEALED` — authoritative gate status for the main run
3. `results/pctau-20260906-672227c/reports/phase3_summary.json` — Track N/F numbers and probe metrics
4. `results/pctau-20260906-672227c/audit_prephase4/POST_MEASUREMENT_AUDIT.md` — what was disabled and why
5. `llm1/REPRODUCE.md` — supporting follow-on: archived-raw replay versus fresh replication
6. `WorkPlan.md`, `Path.md` — original protocol and execution history (deeper provenance)

## Quick verification

Safest first (read-only, no side effects): open the `SEALED` marker, `CLAIMS.md`, and `phase3_summary.json` above.

Optional reviewer test-suite check:

```bash
pytest -q
```

Expected anonymous-snapshot baseline: 66 passed, 4 failed. The four failures are environment-only checks requiring git-ignored / non-distributed upstream or release artifacts and are also present on a clean canonical checkout without those assets. See `ANONYMIZATION_REPORT.json` for the exact failure list.

Sealed-output replay / reseal verification (not a full from-source rerun):

```bash
python scripts/run_pc_tau.py --reproduce pctau-20260906-672227c
```

This deterministically verifies the already-materialized sealed result state (downstream tables, bundle, seal marker). It does not regenerate Phases 1–3 from source. Requires the Python dependencies and existing result material (see `README_REVIEW.md`).

For the supporting LLM1 follow-on, see `llm1/REPRODUCE.md`. Deterministic replay uses archived raw records; fresh provider inference would be a new replication and is not required for artifact review.

## Scope / important interpretation

Probes in the main run are scripted deterministic stand-ins, not learned-model evidence. Do not read probe performance as proof about trained agents. Learned-agent evidence, if considered at all, comes only from the separate `llm1` supporting experiment and does not establish universality or prevalence.

`llm1/reports/LLM1_CLAIMS.md` preserves the sealed experiment's historical predicate terminology. The submitted manuscript adopts the narrower interpretation of descriptive fallback realizability: because F000 and F010 resolve on different subsets, it does not treat the observed marginal differences as a paired causal freeze-effect estimate, and it makes no prevalence, universal-safety, or architecture-superiority claim.

## Reviewer snapshot

This is an anonymous reviewer snapshot with history omitted by design. See `README_REVIEW.md` for reproduction and `ANONYMIZATION_REPORT.json` for reviewer-safe integrity information.
