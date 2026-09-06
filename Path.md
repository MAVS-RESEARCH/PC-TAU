# Path.md — PC-TAU Execution Ledger (append-only)

**Discipline (spec §4.2):** every completed phase records exact files, commands, hashes, run IDs, tests, deviations, rejected attempts, and whether the implementation follows WorkPlan.md. Planning observations, development pilots, sealed scientific results, and later paper transformations remain visibly distinct. **Never rewrite an entry; append corrections as new dated entries.** Timestamps live here and in logs, never inside scientific hashes (spec §4.3).

**Companion plan:** `WorkPlan.md` (4 phases mirroring spec §§Phase 1–4; §0.2 justifies why 4, not 5–6). Each entry below ends with `WorkPlan-follows: YES/NO + detail`, in the same depth as WorkPlan.md (scope, files made, code produced + how coded, model/benchmark specifics, anti-overfitting evidence).

**Conventions:** `run-id` = `pctau-<yyyymmdd>-<shortsha>` per sealed attempt. Hash = sha256. Canonical JSON = `sort_keys=True, separators=(",",":"), ensure_ascii=False, utf-8`. Gate checks = `python scripts/run_pc_tau.py --check-gate g<N>` (before scripts exist, verification is manual + `pytest -q` once harness lands).

---

## §0 — Planning setup (2026-09-06, UTC)

### 0.1 Scope

Study both input documents deeply (PDF-text extraction + 15 page-image set; verified identical: Implementation Specification v0.1, §§1–6.3), inspect the repo, verify external references, and create the `WorkPlan.md` + `Path.md` setup. No scientific code, no freeze values, no model runs in this entry.

### 0.2 What was done (commands + evidence)

- `git clone https://github.com/MAVS-RESEARCH/PC-TAU PC-TAU` → `573c701 Initial commit`, branch `main`, `origin/main` in sync. Listing showed only `LICENSE` (MIT, ©2026 MAVS-RESEARCH); `git show --stat HEAD` confirmed 1 file, 21 lines.
- Read `LICENSE` in full (21 lines, MIT, no result artifacts).
- Verified upstream source target exists: `https://github.com/sierra-research/tau2-bench` (τ-Bench/τ²/τ³; domains `mock/airline/retail/telecom/banking_knowledge`; text half-duplex + voice full-duplex; `uv sync`, Python `>=3.12,<3.14`; 199 commits on `main`; 2.0k stars / 496 forks at fetch time). Confirms spec §6.2 reference is actionable; exact commit pin deferred to Phase 1 per firewall (no pin invented during planning).
- Cross-checked the two input docs: cover mission, design-property table (6 rows), §§1–1.3 (estimand K_Pi, 6-step loop, E/R/A firewalls, Touch derivation, nondegeneracy + desired finite-substitution geometry), §2 (N vs F tracks, scale 24/60–96 min 40/32-panel/2160-episode table, 4 regimes, 4 baselines), §3 (4-phase firewall), Phase 1 (P1.1 pilot 12+12 + GO/STOP, P1.2 pin, P1.3 eligibility + telecom fallback-once, P1.4 costs/models/repeats/bundles/freezes/nonclaims, P1 outputs + gate), Phase 2 (P2.1 two-pass, P2.2 boundaries + no self-signaling, P2.3 IDENTIFIED/PARTIAL/INVALID, P2.4 mechanical touch + 4 rejects + atomicity, P2.5 eligibility predicate, P2.6 32-panel, outputs + gate), Phase 3 (P3.1 8-cell AND-OR minimax + structural infinity + crosscheck + same-instance, P3.2 6 quantities, P3.3 6-row agent protocol, P3.4 frozen bundles, P3.5 7 metrics, P3.6 stats, outputs + gate), Phase 4 (P4.1 6-layer audit boundary, P4.2 8 corruption families, P4.3 refactoring audit, P4.4 5 allowed claims, P4.5 5 nonclaims, P4.6 release outputs, exit gate), §4 (repo tree, 9+6 module responsibilities, ledger + runtime discipline), §5 (7 hard stops, 4 gates, DoD incl. null-result-is-success), §6 (D32 4-leg table, high-value pattern kappa=1→2, refs, "do not scale first" 6-line principle). No section left unmapped — see WorkPlan.md Appendix B traceability.

### 0.3 Files made

- `WorkPlan.md` (this repo root): 4 phases (§§Phase 1–4) + §§0.1–0.7 global (mission, 4-phase justification, no-training/anti-overfitting policy with 7 mechanisms, scale, regimes/baselines, repo layout, traceability, canonical commands) + Appendices A (D32), B (spec→plan map), C (commands). Each phase lists scope, exact files, code + how-to-code (functions, firewalls, tests), model/benchmark specifics, brutal-disjoint-benchmark mapping, exit gate.
- `Path.md` (this file): ledger setup + §0 entry + §§P1–P4 placeholders with required field checklists.

### 0.4 Code produced + how coded

No production code yet (correct per firewall: code lands in its phase). Planning method: manual doc diff (text vs images) + live fetch of tau2-bench + `git` inspection; no LLM inference on benchmark tasks; no invented commit SHAs, model IDs, or K_Pi values anywhere in WorkPlan/Path (prevents pre-registration contamination).

### 0.5 Models / benchmarks / anti-overfitting (this entry)

Training: none; evaluation-only framing recorded in WorkPlan §0.3. Benchmarks produced in this entry: none (planning only). Anti-overfitting evidence: (a) zero pilot IDs created or consumed; (b) zero freeze/model artifacts created — filesystem still contains only `LICENSE + WorkPlan.md + Path.md` after this entry (verified by listing before commit); (c) upstream commit deliberately **not** pinned in planning (pin is Phase 1 work with hashing); (d) model families named only as placeholders in WorkPlan (`family-a/b/c` pattern) with exact IDs deferred to `configs/models.yaml` pre-Phase 3.

### 0.6 Stale-results clearing (user requirement)

Clone contained **zero** result artifacts (`results/`, `contract/`, `audit/`, `reports/` absent; only `LICENSE`). Nothing to delete; cleaner contract recorded for future: `scripts/clean_run.py --run-id <unsealed>` is the sole deleter and refuses sealed IDs; seal markers (`CONTRACT_SEALED`, `PHASE3_COMPLETE`, `SEALED`) + git-ignored run dirs ensure only new post-change results are present after each phase. This entry's no-op clearing verified by `Get-ChildItem -Force` + `git status` (clean except the two new docs).

### 0.7 Verification

- [x] Both docs read end-to-end (15 spec pages incl. all tables/code blocks).
- [x] Repo empty-except-LICENSE confirmed via listing + `git log/show`.
- [x] tau2-bench URL live + domains match spec scope (airline/retail primary, telecom fallback).
- [x] WorkPlan.md covers every spec section (Appendix B checklist; reviewer can `grep` each `§/P` header).
- [x] Path.md setup correct (append-only rule, conventions, phase placeholders below).
- [x] No K_Pi / trajectory / freeze artifact exists (nothing to seal yet).

### 0.8 Deviations + rejected attempts

Deviations: none. Rejected: (a) creating a 5th/6th WorkPlan phase for scaffolding — rejected per WorkPlan §0.2 (would dilute gates; scaffolding folded into Phase 1); (b) inventing a tau2-bench commit SHA or model IDs during planning — rejected as firewall violation; (c) vendoring upstream data now — rejected (Phase 1 only, with license + attribution).

**WorkPlan-follows: YES.** This entry implements exactly WorkPlan §§0.6–0.7 planning prerequisites; no phase gate claimed; next is Phase 1 per WorkPlan §Phase 1 + Appendix C commands.

---

## §P1 — Phase 1: Source Lock, Pilot, Preregistration (TO RUN)

Required fields on completion: scope recap; files made (P1 outputs list + hashes); code produced + how coded (`source.py`, `phase1_*.py`, `run_pc_tau.py`, `clean_run.py`, configs with SHAs); pilot table (24 IDs, per-task MULTI_ACTION y/n, finite-fallback evidence, firewall + CPU verdicts); GO/STOP + `reports/phase1_preregistration.json` hash; tests (`tests/phase1/*`, `pytest -q` output); deviations/rejected; stale-results cleaner log; commit `phase1: PREREGISTERED <run-id> <hash>` + push URL; **WorkPlan-follows: YES/NO + detail**. Must assert zero final K_Pi / trajectories exist (filesystem scan log).

_Status: PENDING._

## §P2 — Phase 2: Semantic Contract and Multi-Route Extraction (TO RUN)

Required: scope; files (`contract/*` + hashes, `CONTRACT_SEALED`); code (`semantics.py`, `repairs.py`, `touch.py`, `phase2_*.py`) + derivation samples (H/P_R/Lambda diffs for ≥2 repairs); family counts (IDENTIFIED/PARTIAL/INVALID) + failure_cards; eligibility counts (Track N ≥40/≥2 domains, no pilots; Track F 32 balanced-by-design); tests (`tests/phase2/*` incl. import-ban + firewall rejects); zero-freeze-result scan; deviations/rejected; commit `phase2: CONTRACT_SEALED <run-id> <hash>` + push; **WorkPlan-follows**.

_Status: PENDING._

## §P3 — Phase 3: Exact Freeze Benchmark and Learned-Agent Evaluation (TO RUN)

Required: scope; files (`results/<run-id>/exact/*`, `agents/*`, `controls/*`, `PHASE3_COMPLETE` + hashes); code (`planner.py` INF design, `freeze.py` masks + same-instance manifests, `runtime.py` blinded tools + safety-gate log `executed_unauthorized==0`, `metrics.py` 7 metrics + bootstrap); model roster (3 families, IDs/revisions/params + hash) + episode counts (target 2,160 at 60 tasks; repeats=3; freezes F000/F100/F010/F001; exact 8-cell); user-bundle freeze hash + invariance check; crosscheck 100% log; all-rows-retained proof (null/inf/failure present); tests (`tests/phase3/*`); deviations/rejected; commit `phase3: MEASURED <run-id> <hash>` + push; **WorkPlan-follows**.

_Status: PENDING._

## §P4 — Phase 4: Independent Audit, Falsification, Claims, Seal (TO RUN)

Required: scope; files (`src/pc_tau_audit/*`, `audit/*`, `reports/CLAIMS.md`, `REPRODUCE.md`, `benchmark_report.md`, `audited_tables/`, `claim_ledger.json`, `artifact_graph.json`, `audit.json`, `SEALED` or `INVALID` + hashes); code (import-ban proof, 6-layer recompute equality table, 8-family corruption inject→detect log, refactoring invariance/PARTIAL-flip log, claim-lock passes); clean-checkout reproduce log (fresh clone + one command → identical seal hash); DoD checklist (§5.3 all rows) + hard-stop scans (§5.1); tests (`tests/phase4/*`, `tests/metamorphic/*`); deviations/rejected; commit `phase4: SEALED|INVALID <run-id> <hash>` + push; **WorkPlan-follows**.

_Status: PENDING._

---

## Commit/push log (user requirement: push after each phase without being asked)

| Date (UTC) | Commit | Gate | Remote |
|---|---|---|---|
| 2026-09-06 | `docs: WorkPlan.md + Path.md setup` (pending push, see §0.6) | planning (no gate) | `origin/main` |
| — | Phase 1 commit (pending) | PREREGISTERED/STOP | — |
| — | Phase 2 commit (pending) | CONTRACT_SEALED/PARTIAL/STOP | — |
| — | Phase 3 commit (pending) | MEASURED | — |
| — | Phase 4 commit (pending) | SEALED/INVALID | — |
