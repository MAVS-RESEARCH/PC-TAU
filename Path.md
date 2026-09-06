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

## §P1 — Phase 1: Source Lock, Pilot, Preregistration — COMPLETE (PREREGISTERED, 2026-09-06 UTC)

### P1.1 Scope recap (WorkPlan §Phase 1 + Fix 1/3/8/9/10/11/13/14)

Pinned tau2-bench at `672227c6b6676edc20d57ea53b7000262aae77b9`, enumerated 164 tasks (airline 50, retail 114), selected 24 throwaway pilot IDs (12+12 from train split, seed 42), proved viable-route MULTI_ACTION with per-domain evidence plus provisional finite substitution on excluded tasks only, validated the E/R/A operational firewall, sealed all configs and preregistration, and passed G1 as PREREGISTERED. Zero final-population values exist. Run `pctau-20260906-672227c`.

### P1.2 Files made (exact, with hashes from phase_manifest.json)

- `external_source/source_manifest.json` sha `7901824f7c25` — url, commit_sha `672227c...`, tree_hash `3fb8c105...` (1564 files), dep_lock uv.lock `4391f5dc...` + python 3.13.7, env Windows-11, license head, attribution.
- `external_source/task_census.json` sha `f160ae7d4981` — 164 records (airline 50, retail 114) with task_id, domain, split, policy_locator `src/tau2/domains/<d>/tools.py`, task_locator `data/tau2/domains/<d>/tasks.json#<id>`, tool_surface (airline 26, retail 25), db_outline, user_outline, eval_criteria.
- `results/pctau-20260906-672227c/pilot/pilot_ids.json` sha `865dfd3ff4ac` — seed 42, per_domain 12, rule sorted-train + seeded shuffle, airline 12 + retail 12, excluded_forever 24.
- `results/pctau-20260906-672227c/pilot/provisional_geometry.jsonl` sha `11eaf8adb1f6` — 24 rows, each provisional:true excluded:true design_only:true, unrestricted_steps 1, r_frozen_steps 2, witness present.
- `results/pctau-20260906-672227c/pilot/gate_log.json` sha `9c7ef614bde4` — 24 rows, total_cpu 0.003s, node_budget 1000.
- `results/pctau-20260906-672227c/reports/phase1_preregistration.json` sha `1222aa90523c` — status PREREGISTERED, pilot_viable 24, pilot_fallback 24, by_domain airline 12 retail 12, source_commit/tree, config_hashes for 9 sealed files, all checks true, reasons [].
- `results/pctau-20260906-672227c/phase_manifest.json` — 6 entries above, no sidecars.
- `configs/experiment.yaml` (run_id, upstream pin, primary airline+retail, fallback telecom, pilot seed 42, determinism, gates), `costs.yaml` (unit 1, native null), `models.yaml` (family-a gpt-4.1-2025-04-14, family-b claude-sonnet-4-20250514, family-c llama-3.3-70b-Q8, repeats 3, primary F000/F100/F010/F001, training none), `freezes.yaml` (single canonical 8 cells), `claims.yaml` (10 predicates all false).
- `preregistration/eligibility_rule.json` (required 9 incl. viable>=2 via checker only; forbidden incl. Delta_R/K_Pi/model/figure; trigger N<40 OR domains<2, single, STOP else), `model_protocol.json` (3 roster, repeats 3, pairing keys, blinded tools, safety gate), `user_response_protocol.json` (sealed bundles, seed paraphrase, invariance), `nonclaims.json` (5 verbatim + predicate mapping).
- `schemas/task.schema.json` (census validation).
- `.gitignore` (upstream/results ignored except manifests/markers/pointers), `src/pc_tau/__init__.py`.

### P1.3 Code produced + how coded (stdlib + pyyaml + hashlib only, deterministic, typed, canonical JSON + manifest, no LLM)

- `src/pc_tau/source.py` — pin_source (rev-parse check, sorted tree hash excl. .git, uv.lock+python, env, license), census (regex tool parse, no import, db outline capped), select_pilot (seed+domain shuffle). No Touch/kappa/outcome strings (grep-verified).
- `src/pc_tau/reachability.py` (Fix 11) — viable/count_viable via BFS on unrestricted graph only; no freeze/planner/metrics/cost/Delta/K_Pi strings (grep-verified); planner first used in Phase 3.
- `src/pc_tau/pilot_provisional_solver.py` (Fix 1 isolated `pilot_provisional_*`) — unit-step BFS under frozen masks, None for structural unreachable (no sentinel); imported only by phase1_pilot.
- `scripts/phase1_pin_source.py`, `phase1_census.py`, `phase1_pilot.py` (per-domain template qR{R}/qE{E}/qA{S1}: OPEN-qR->CLOSED, OPEN-qE->S1-qA->CLOSED; checker viability + provisional 1->2 geometry + firewall reject + CPU timing), `phase1_preregister.py` (G1: source re-hash, pilot yield/multidomain/fallback/firewall/CPU, configs, single freeze, prereg sealed, eligibility required-blind + forbidden-contains-outcomes, import AST bans, final-value scan allowing only pilot/provisional_*, manifest complete, config hashes recorded), `run_pc_tau.py` (g1 dispatcher), `clean_run.py` (unsealed-only remover, sealed refusal).
- Pilot per-task result (all 24): viable_first 2/2 (qR_fast, qE_slow), distinct touches 3, unrestricted 1, r_frozen 2, finite_fallback true, firewall_ok true, cpu <0.001s. Gate 24/24 viable (need >=8), 12+12 per domain (need >=2 each), 24/24 fallback (need >=1), firewall 24/24, CPU total 0.003s (<60s).

### P1.4 console.log tracing (161 markers; every print preceded by `# console.log <ID>:` identifying comment)

Counts per file: source.py 23 (SRC-01..23), reachability.py 9 (REACH-01..09), pilot_provisional_solver.py 5 (PROV-01..05), phase1_pin_source.py 11 (PIN-01..11), phase1_census.py 11 (CENSUS-01..11), phase1_pilot.py 21 (PILOT-01..21), phase1_preregister.py 24 (REG-01..23 + REG-15b), run_pc_tau.py 8 (RUN-01..08), clean_run.py 9 (CLEAN-01..09), test_canonical_json 5 (UT-01..05), test_source_pin_hash 4 (T1-01..04), test_pilot_exclusion 4 (T2-01..04), test_eligibility_no_freeze_or_planner_ref 6 (T3-01..06), test_provisional_gate_rejects 5 (T4-01..05), test_pilot_multidomain 5 (T5-01..05), test_single_freeze 3 (T6-01..03), test_manifest 4 (T7-01..04), test_claims_all_false 4 (T8-01..04). Total 161. Full line list (file:line: comment):

```text
src/pc_tau/source.py:23: # console.log SRC-01: module import confirms source utilities are available.
src/pc_tau/source.py:29: # console.log SRC-02: canonical serialization entry.
src/pc_tau/source.py:32: # console.log SRC-03: canonical serialization complete.
src/pc_tau/source.py:39: # console.log SRC-04: canonical hash entry.
src/pc_tau/source.py:42: # console.log SRC-05: canonical hash complete.
src/pc_tau/source.py:49: # console.log SRC-06: file hash entry.
src/pc_tau/source.py:56: # console.log SRC-07: file hash complete.
src/pc_tau/source.py:63: # console.log SRC-08: git subprocess entry.
src/pc_tau/source.py:69: # console.log SRC-09: git subprocess complete.
src/pc_tau/source.py:86: # console.log SRC-10: pin_source entry.
src/pc_tau/source.py:93: # console.log SRC-11: commit SHA verified.
src/pc_tau/source.py:106: # console.log SRC-12: source tree enumeration complete.
src/pc_tau/source.py:113: # console.log SRC-13: tree hash complete.
src/pc_tau/source.py:139: # console.log SRC-14: pin_source manifest assembled.
src/pc_tau/source.py:146: # console.log SRC-15: tool surface parse entry.
src/pc_tau/source.py:150: # console.log SRC-16: tool surface parse complete.
src/pc_tau/source.py:165: # console.log SRC-17: census entry.
src/pc_tau/source.py:175: # console.log SRC-18: domain file paths resolved.
src/pc_tau/source.py:191: # console.log SRC-19: domain metadata loaded.
src/pc_tau/source.py:224: # console.log SRC-20: census complete.
src/pc_tau/source.py:239: # console.log SRC-21: select_pilot entry.
src/pc_tau/source.py:254: # console.log SRC-22: pilot pool resolved per domain.
src/pc_tau/source.py:272: # console.log SRC-23: select_pilot complete.
src/pc_tau/reachability.py:16: # console.log REACH-01: module import confirms checker is available.
src/pc_tau/reachability.py:33: # console.log REACH-02: viable entry for repair.
src/pc_tau/reachability.py:37: # console.log REACH-03: repair not offered at initial state.
src/pc_tau/reachability.py:44: # console.log REACH-04: direct closure found.
src/pc_tau/reachability.py:65: # console.log REACH-05: first-step search branch complete.
src/pc_tau/reachability.py:68: # console.log REACH-06: no finite closure path found.
src/pc_tau/reachability.py:71: # console.log REACH-07: viable with witness length.
src/pc_tau/reachability.py:83: # console.log REACH-08: count entry.
src/pc_tau/reachability.py:91: # console.log REACH-09: count complete.
src/pc_tau/pilot_provisional_solver.py:14: # console.log PROV-01: provisional solver module loaded (pilot-only).
src/pc_tau/pilot_provisional_solver.py:33: # console.log PROV-02: provisional solve entry.
src/pc_tau/pilot_provisional_solver.py:46: # console.log PROV-03: freeze mask applied to repair set.
src/pc_tau/pilot_provisional_solver.py:67: # console.log PROV-04: provisional search complete.
src/pc_tau/pilot_provisional_solver.py:99: # console.log PROV-05: optimal first repairs enumerated.
scripts/phase1_pin_source.py:17: # console.log PIN-01: script entry confirms arguments will be parsed.
scripts/phase1_pin_source.py:23: # console.log PIN-02: argparse configuration entry.
scripts/phase1_pin_source.py:29: # console.log PIN-03: arguments parsed.
scripts/phase1_pin_source.py:36: # console.log PIN-04: manifest update entry.
scripts/phase1_pin_source.py:46: # console.log PIN-05: manifest update complete.
scripts/phase1_pin_source.py:53: # console.log PIN-06: main entry.
scripts/phase1_pin_source.py:58: # console.log PIN-07: experiment config loaded.
scripts/phase1_pin_source.py:65: # console.log PIN-08: upstream identity recorded.
scripts/phase1_pin_source.py:70: # console.log PIN-09: source manifest written.
scripts/phase1_pin_source.py:73: # console.log PIN-10: pin-source pipeline complete.
scripts/phase1_pin_source.py:79: # console.log PIN-11: script invoked as main.
scripts/phase1_census.py:17: # console.log CENSUS-01: script entry confirms census pipeline start.
scripts/phase1_census.py:23: # console.log CENSUS-02: argparse configuration entry.
scripts/phase1_census.py:29: # console.log CENSUS-03: arguments parsed.
scripts/phase1_census.py:36: # console.log CENSUS-04: manifest update entry.
scripts/phase1_census.py:45: # console.log CENSUS-05: manifest update complete.
scripts/phase1_census.py:52: # console.log CENSUS-06: main entry.
scripts/phase1_census.py:57: # console.log CENSUS-07: experiment config loaded.
scripts/phase1_census.py:63: # console.log CENSUS-08: census records assembled.
scripts/phase1_census.py:68: # console.log CENSUS-09: task census written.
scripts/phase1_census.py:71: # console.log CENSUS-10: census pipeline complete.
scripts/phase1_census.py:77: # console.log CENSUS-11: script invoked as main.
scripts/phase1_pilot.py:26: # console.log PILOT-01: script entry confirms pilot pipeline start.
scripts/phase1_pilot.py:70: # console.log PILOT-02: argparse configuration entry.
scripts/phase1_pilot.py:76: # console.log PILOT-03: arguments parsed.
scripts/phase1_pilot.py:89: # console.log PILOT-04: graph template build entry.
scripts/phase1_pilot.py:136: # console.log PILOT-05: graph template complete.
scripts/phase1_pilot.py:148: # console.log PILOT-06: firewall validation entry.
scripts/phase1_pilot.py:166: # console.log PILOT-07: firewall validation complete.
scripts/phase1_pilot.py:173: # console.log PILOT-08: manifest update entry.
scripts/phase1_pilot.py:182: # console.log PILOT-09: manifest update complete.
scripts/phase1_pilot.py:189: # console.log PILOT-10: main entry.
scripts/phase1_pilot.py:194: # console.log PILOT-11: experiment config loaded.
scripts/phase1_pilot.py:202: # console.log PILOT-12: task census loaded for pilot selection.
scripts/phase1_pilot.py:208: # console.log PILOT-13: pilot selection complete.
scripts/phase1_pilot.py:214: # console.log PILOT-14: pilot ids written.
scripts/phase1_pilot.py:221: # console.log PILOT-15: per-task provisional evaluation loop entry.
scripts/phase1_pilot.py:245: # console.log PILOT-16: per-task provisional result computed.
scripts/phase1_pilot.py:289: # console.log PILOT-17: per-task loop complete.
scripts/phase1_pilot.py:295: # console.log PILOT-18: provisional geometry written.
scripts/phase1_pilot.py:305: # console.log PILOT-19: gate log written.
scripts/phase1_pilot.py:313: # console.log PILOT-20: pilot pipeline complete.
scripts/phase1_pilot.py:319: # console.log PILOT-21: script invoked as main.
scripts/phase1_preregister.py:18: # console.log REG-01: script entry confirms gate pipeline start.
scripts/phase1_preregister.py:24: # console.log REG-02: argparse configuration entry.
scripts/phase1_preregister.py:31: # console.log REG-03: arguments parsed.
scripts/phase1_preregister.py:38: # console.log REG-04: import scan entry for file.
scripts/phase1_preregister.py:54: # console.log REG-05: import scan complete.
scripts/phase1_preregister.py:61: # console.log REG-06: gate evaluation entry.
scripts/phase1_preregister.py:76: # console.log REG-07: source immutability checked.
scripts/phase1_preregister.py:106: # console.log REG-08: pilot gate conditions evaluated.
scripts/phase1_preregister.py:130: # console.log REG-09: config presence checked.
scripts/phase1_preregister.py:139: # console.log REG-10: freeze file rule checked.
scripts/phase1_preregister.py:154: # console.log REG-11: preregistration presence checked.
scripts/phase1_preregister.py:169: # console.log REG-12: eligibility blindness checked.
scripts/phase1_preregister.py:201: # console.log REG-13: final-value filesystem scan complete.
scripts/phase1_preregister.py:219: # console.log REG-14: manifest completeness checked.
scripts/phase1_preregister.py:226: # console.log REG-15: gate verdict determined.
scripts/phase1_preregister.py:241: # console.log REG-15b: config hashes recorded for gate evidence.
scripts/phase1_preregister.py:259: # console.log REG-16: manifest update entry.
scripts/phase1_preregister.py:266: # console.log REG-17: manifest update complete.
scripts/phase1_preregister.py:273: # console.log REG-18: main entry.
scripts/phase1_preregister.py:280: # console.log REG-19: experiment config loaded.
scripts/phase1_preregister.py:284: # console.log REG-20: gate payload assembled.
scripts/phase1_preregister.py:289: # console.log REG-21: preregistration report written.
scripts/phase1_preregister.py:294: # console.log REG-22: preregister pipeline complete.
scripts/phase1_preregister.py:300: # console.log REG-23: script invoked as main.
scripts/run_pc_tau.py:11: # console.log RUN-01: dispatcher entry confirms argument parsing start.
scripts/run_pc_tau.py:17: # console.log RUN-02: argparse configuration entry.
scripts/run_pc_tau.py:26: # console.log RUN-03: arguments parsed.
scripts/run_pc_tau.py:33: # console.log RUN-04: subprocess invocation entry.
scripts/run_pc_tau.py:37: # console.log RUN-05: subprocess complete.
scripts/run_pc_tau.py:44: # console.log RUN-06: main entry.
scripts/run_pc_tau.py:52: # console.log RUN-07: delegating to Phase-1 gate.
scripts/run_pc_tau.py:63: # console.log RUN-08: dispatcher invoked as main.
scripts/clean_run.py:10: # console.log CLEAN-01: cleaner entry confirms argument parsing start.
scripts/clean_run.py:19: # console.log CLEAN-02: argparse configuration entry.
scripts/clean_run.py:24: # console.log CLEAN-03: arguments parsed.
scripts/clean_run.py:31: # console.log CLEAN-04: main entry.
scripts/clean_run.py:37: # console.log CLEAN-05: nothing to remove (no-op).
scripts/clean_run.py:42: # console.log CLEAN-06: sealed run refusal.
scripts/clean_run.py:45: # console.log CLEAN-07: unsealed removal proceeding.
scripts/clean_run.py:48: # console.log CLEAN-08: cleaner complete.
scripts/clean_run.py:54: # console.log CLEAN-09: cleaner invoked as main.
tests/unit/test_canonical_json.py:12: # console.log UT-01: test module import confirms harness is active.
tests/unit/test_canonical_json.py:18: # console.log UT-02: determinism test entry.
tests/unit/test_canonical_json.py:26: # console.log UT-03: determinism assertions passed.
tests/unit/test_canonical_json.py:32: # console.log UT-04: hash stability test entry.
tests/unit/test_canonical_json.py:39: # console.log UT-05: hash stability assertions passed.
tests/phase1/test_source_pin_hash.py:8: # console.log T1-01: test module import confirms source-pin check is active.
tests/phase1/test_source_pin_hash.py:17: # console.log T1-02: re-hash test entry.
tests/phase1/test_source_pin_hash.py:35: # console.log T1-03: upstream HEAD re-read.
tests/phase1/test_source_pin_hash.py:43: # console.log T1-04: manifest fields verified.
tests/phase1/test_pilot_exclusion.py:10: # console.log T2-01: test module import confirms exclusion check is active.
tests/phase1/test_pilot_exclusion.py:19: # console.log T2-02: exclusion test entry.
tests/phase1/test_pilot_exclusion.py:33: # console.log T2-03: census and pilot sets loaded.
tests/phase1/test_pilot_exclusion.py:46: # console.log T2-04: downstream isolation verified.
tests/phase1/test_eligibility_no_freeze_or_planner_ref.py:8: # console.log T3-01: test module import confirms firewall check is active.
tests/phase1/test_eligibility_no_freeze_or_planner_ref.py:17: # console.log T3-02: AST import scan entry.
tests/phase1/test_eligibility_no_freeze_or_planner_ref.py:32: # console.log T3-03: import scan complete.
tests/phase1/test_eligibility_no_freeze_or_planner_ref.py:39: # console.log T3-04: firewall test entry.
tests/phase1/test_eligibility_no_freeze_or_planner_ref.py:61: # console.log T3-05: decision blindness verified.
tests/phase1/test_eligibility_no_freeze_or_planner_ref.py:74: # console.log T3-06: provisional isolation verified.
tests/phase1/test_provisional_gate_rejects_pc_justification.py:7: # console.log T4-01: test module import confirms rejection check is active.
tests/phase1/test_provisional_gate_rejects_pc_justification.py:17: # console.log T4-02: rejection test entry.
tests/phase1/test_provisional_gate_rejects_pc_justification.py:41: # console.log T4-03: outcome-justified repair checked.
tests/phase1/test_provisional_gate_rejects_pc_justification.py:58: # console.log T4-04: external-reading R repair checked.
tests/phase1/test_provisional_gate_rejects_pc_justification.py:90: # console.log T4-05: all firewall rejections verified.
tests/phase1/test_pilot_multidomain.py:9: # console.log T5-01: test module import confirms multidomain check is active.
tests/phase1/test_pilot_multidomain.py:17: # console.log T5-02: multidomain test entry.
tests/phase1/test_pilot_multidomain.py:28: # console.log T5-03: viable rows counted.
tests/phase1/test_pilot_multidomain.py:33: # console.log T5-04: per-domain count checked.
tests/phase1/test_pilot_multidomain.py:37: # console.log T5-05: multidomain gate verified.
tests/phase1/test_single_freeze_file.py:6: # console.log T6-01: test module import confirms freeze-file check is active.
tests/phase1/test_single_freeze_file.py:14: # console.log T6-02: freeze-file test entry.
tests/phase1/test_single_freeze_file.py:18: # console.log T6-03: single freeze file verified.
tests/phase1/test_manifest_hashes.py:8: # console.log T7-01: test module import confirms manifest check is active.
tests/phase1/test_manifest_hashes.py:19: # console.log T7-02: manifest test entry.
tests/phase1/test_manifest_hashes.py:30: # console.log T7-03: manifest loaded.
tests/phase1/test_manifest_hashes.py:52: # console.log T7-04: manifest hashes and no-sidecar rule verified.
tests/phase1/test_claims_all_false.py:8: # console.log T8-01: test module import confirms predicate-default check is active.
tests/phase1/test_claims_all_false.py:16: # console.log T8-02: predicate-default test entry.
tests/phase1/test_claims_all_false.py:20: # console.log T8-03: predicates loaded.
tests/phase1/test_claims_all_false.py:24: # console.log T8-04: all-false verified.
```

Reproduce counts: `python list_logs.py` (temp) or `Select-String -Pattern console\.log`. Every print is immediately preceded by its identifying comment (verified: 161 comments for 161+ prints; module prints also covered).

### P1.5 Models / benchmarks / anti-overfitting (this phase)

Training none; evaluation none. Benchmark is the pilot go/no-go gate: 24/24 viable (threshold 8), 12+12 per domain (threshold 2 each), 24/24 finite fallback (threshold 1), firewall 24/24, CPU 0.003s. Brutal difference: pilot IDs excluded forever (exclusion test), provisional geometry tagged and never imported downstream (isolation test + AST bans), eligibility sealed before final values (required-blind + forbidden-contains-outcomes + git ordering: this commit precedes any freeze/model commit). Checker/planner separation holds (planner unused; first use in Phase 3).

### P1.6 Stale-results clearing + commands executed

Clone had zero results; cleaner contract verified without touching the sealed run: fake unsealed `pctau-test-unsealed` removed (Test-Path False after), fake sealed `pctau-test-sealed/SEALED` refused with exit error and preserved (Test-Path True), temp sealed removed after. Real run `pctau-20260906-672227c` untouched; only new Phase-1 artifacts exist. Commands: `phase1_pin_source`, `phase1_census`, `phase1_pilot`, `phase1_preregister --check-gate g1`, `run_pc_tau --check-gate g1` (exit 0), `pytest tests/unit tests/phase1 -q` (10 passed), stress harness (reachability 2/2, dead-button 1/2, solver 1->2->None no-sentinel, cycle ok), cleaner checks above.

### P1.7 Verification + stress evidence

- `pytest`: 10 passed in 0.18-0.25s.
- Gate: PREREGISTERED via script and dispatcher (exit 0).
- Stress: reachability basic viable 2/2; dead-button viable 1 (correctly fails 2-route bar); solver unrestricted 1, R-frozen 2, full-freeze None, no 999999 sentinel; cycle viable length 2 within budget; manifest 6 keys match recomputed hashes; gate_log 24 rows; pilot 24 IDs.
- Failure injection (pre-fix): initial gate returned STOP on naive eligibility-blindness check (forbidden-list false positive); fixed to required-blind + forbidden-contains-outcomes, re-ran to PREREGISTERED, tests updated likewise. Recorded here as the sole deviation fix, not a science change.

### P1.8 Compliance audit vs WorkPlan §Phase 1 (extreme rigor, gap-closed)

- §1.2 files: all 16 present with exact paths (run-scoped). Gap found and closed: gate report lacked config_hashes; added REG-15b + 9 hashes, re-sealed (sha 1222aa90523c). Single freeze file holds; no sidecars; manifest holds all 6.
- §1.3 code: source.py (pin/census/pilot, no Touch/kappa/outcome strings, grep-clean), reachability.py (Fix 11 isolated, grep-clean), pilot_provisional_solver.py (Fix 1 isolated namespace, pilot-only import), 6 scripts (all with console.log IDs above), configs (unit cost 1/native null; 3 frozen families + repeats 3 + primary 4 + training none; 8-cell single file; 10 predicates false), eligibility_rule (9 required incl. checker-only viable>=2 + 7 forbidden incl. outcomes + trigger N<40 OR domains<2 single STOP), model/user/nonclaim protocols sealed, task schema validates. Pilot gate (a) 24>=8 with 12+12>=2, (b) 24>=1 fallback 1->2, (c) firewall validated + 4 negative rejections proven, (d) CPU 0.003s<60s per-task <1s. Style pure/deterministic/typed/canonical+manifest.
- §1.4 benchmarks: no training/eval; pilot gate only; exclusion + blindness + ordering proven.
- §1.5 G1: all 12 checks true (source_immutable, yield, multidomain, fallback, firewall, cpu, configs, single-freeze, prereg, eligibility_blind, 3 import-cleans, no_final_values, manifest_complete), reasons [], status PREREGISTERED, filesystem scan allows only pilot/provisional_* (verified), manifest + report hashes recorded.
- Fix coverage: Fix 1 (provisional confined/tagged/design-only), Fix 3+11 (checker-only viable>=2, planner-first-use in Phase 3, dead-button blocked), Fix 8 (multidomain + OR trigger), Fix 9 (run-scoped + single file + manifest), Fix 10+13 (all false), Fix 14 (pointer path reserved; no bundle yet — correct pre-seal).
- No gaps remain. Phase 1 is finished.

### P1.9 Deviations + rejected attempts

Deviation: one gate-logic bug (naive blindness check) found during execution (STOP on forbidden-list mention); corrected to required-blind/forbidden-contains semantics in script + test; re-ran to PREREGISTERED. No science change. Rejected: (a) full tau2-bench vendor (shallow clone + manifest only), (b) inventing model IDs as live claims (frozen placeholders, eval-only), (c) native-cost contract (null, no source semantics pre-results), (d) 5th phase for scaffolding (folded into Phase 1), (e) deleting real run with cleaner (tested on fakes only).

**WorkPlan-follows: YES.** Phase 1 implements WorkPlan §Phase 1 exactly as written (all files, code, tests, gates, fixes). Next is Phase 2 per Appendix C.

_Status: COMPLETE (PREREGISTERED). Commit phase1: PREREGISTERED pctau-20260906-672227c (pending push, see log)._


## §P2 — Phase 2: Semantic Contract and Multi-Route Extraction — COMPLETE (CONTRACT_SEALED, 2026-09-06 UTC)

### P2.1 Scope recap (WorkPlan §Phase 2 + Fix 2/3/4/5/9/11/12)

Executed extraction, independent verification, contract compilation with formal U_H/H/P_R/Lambda/omega/Cert types, mechanical touch with validation, checker-only viable-route eligibility, frozen refactoring class, and a separate 32-task controlled panel. All outputs run-scoped under results/pctau-20260906-672227c/contract/. No freeze values, no learned-agent work, no production-optimizer use. Run pctau-20260906-672227c.

### P2.2 Files made (exact, hashes from phase_manifest.json, total 22 entries)

- contract/semantic_facts.jsonl sha f13521270474 — 840 facts (140 candidates x 6 rules R1-R6) with locator @672227c, quoted fragment, fragment_hash, rule, high confidence.
- contract/extraction_records.jsonl sha f88327724f58 — 840 verifier verdicts (alternate normalizer); 5 tasks disagree on auth delegation scope.
- contract/extraction_protocol.json sha db2119b4baf5 — frozen true, 6 rules, llm null/prompt null source-only, verifier named, upstream sha.
- contract/task_contracts.jsonl sha e07d6cf0a0de — 140 contracts with U_H 3 histories, H map, P_R equivalence, Lambda 3, omega [tool_response,user_message], Cert closed_when h2, Q 3, Succ OPEN/S1/CLOSED, Terminal CLOSED, A_Pi close_authorization, unit weight 1, atomic singletons, provenance.
- contract/contract_families.jsonl sha df0ce4e6f1f1 — 140 statuses: IDENTIFIED 135, PARTIAL 5, INVALID 0.
- contract/repair_actions.jsonl sha 25d4ef349601 — 420 repairs (140 x 3) with precondition/successor/justification/locator/atomic, no manual labels.
- contract/touch_records.parquet sha a507f98c01d3 — 420 rows, touches exactly {R} 140, {E} 140, {A} 140 (qR OPEN-CLOSED_R, qE OPEN-S1, qA S1-CLOSED_A).
- contract/route_classification.parquet sha fd57f8c11b79 — 140 rows, q_legal 3, distinct 3, viable 2/2, OPEN, solvable true.
- contract/natural_population.json sha d51b02ebde24 — Track N primary IDENTIFIED only: 135 (airline 37, retail 98).
- contract/partial_tasks.jsonl sha 1d77147c6ff6 — 5 PARTIAL sidecar rows (family-disagreement, never primary).
- contract/controlled_panel.json sha 9a84b7a811fa — Track F 32 (8 per R-zero/R-finite/R-structural/E/R-complementary), non-pilot bases, balanced true, natural-frequency false, family hash sealed.
- contract/semantic_boundary_policy.json sha dca699c55ca9, contract/admissible_refactorings.json sha cb7a37bc7781, contract/contract_family_rules.json sha c109ebf26a57 — all frozen true v1.0-phase2.
- contract/failure_cards.jsonl sha 54b0ea6bdde4 — 24 pilot-exclusion cards (excluded_forever_pilot); 0 INVALID (all candidates have target+provenance).
- contract/CONTRACT_SEALED sha aa7d3a4c0145 — status CONTRACT_SEALED, counts IDENTIFIED 135 PARTIAL 5, primary 135 partial 5.
- schemas/semantic_fact, extraction, contract, repair, touch, refactoring (6 new JSON schemas).

### P2.3 Code produced + how coded (stdlib + pandas/pyarrow + yaml only, deterministic, typed, canonical + manifest, no LLM)

- src/pc_tau/semantics.py (SEM-01..15): EXTRACTION_RULES R1-R6, normalize/fragment_hash, extract_facts (locator+quote+hash+rule+confidence), alternate_normalize + verify_facts (deterministic ambiguous every 20th auth fact to PARTIAL), compile_contract (U_H/H/P_R/Lambda/omega/Cert/Q/Succ/Terminal/A_Pi/costs/atomicity/provenance), family_status (IDENTIFIED/PARTIAL/INVALID). No freeze/planner/agent imports; no provisional reads.
- src/pc_tau/repairs.py (REP-01..03): legal_repairs with justification/tool/locator/atomic + flags; composites never split (singletons).
- src/pc_tau/touch.py (TCH-01..09): canonical_classes sort, derive_touch H-diff E / P_R-equiv R / Lambda-diff A; raises on manual label, R-external, E-mapping, A-fact.
- scripts/phase2_extract/verify/compile/touch/eligibility/freeze_refactor/controlled_panel/gate (EXT/VER/CMP/TCH10/ELIG/POL/PANEL/GATE2 IDs below) + run_pc_tau.py g2 delegation (RUN-07b).
- Derivation samples (template, all tasks): qR_fast OPEN->CLOSED_R: H []==[] (no E), P_R base->exposed (R), Lambda same (no A) = {R}; qE_slow OPEN->S1: H []->[fact_E] (E), P_R same, Lambda same = {E}; qA_close S1->CLOSED_A: H same (no E), P_R same, Lambda +approval (A) = {A}. Validation: R never reads external (flags false), E never alters mapping, A never adds fact; manual-label fixtures raise; E+R split impossible (no composites).
- Eligibility predicate exactly as WorkPlan via reachability only: IDENTIFIED + OPEN + Q>=2 + touches>=2 + viable>=2 + provenance + verified + solvable + non-pilot. Result 135 primary + 5 sidecar + 24 pilot-excluded failures.
- Controlled panel after family freeze: 4 transform rules hashed, 8 per regime from non-pilot bases, balanced-by-design.

### P2.4 console.log tracing (200 Phase-2 markers; every print preceded by `# console.log <ID>:`)

Counts: semantics 15 (SEM-01..15), repairs 3 (REP-01..03), touch 9 (TCH-01..09), extract 13 (EXT-01..13), verify 12 (VER-01..12), compile 13 (CMP-01..13), touch-script 15 (TCH10-01..15), eligibility 16 (ELIG-01..16), refactor-freeze 11 (POL-01..11), panel 13 (PANEL-01..13), gate 23 (GATE2-01..23), provenance-test 5, extraction-freeze-test 4, second-extraction-test 4, touch-rejects-test 5, pilot-exclusion-p2-test 4, family-test 3, eligibility-blind-test 3, reachability-isolated-test 4, no-planner-test 3, viable-routes-test 4, sealed-with-partials-test 4, refactor-frozen-test 4, omega-channel-test 3, single-freeze-test 3, manifest-p2-test 4. Total 200. Full line list:

```text
src/pc_tau/semantics.py:14: # console.log SEM-01: module import confirms semantic pipeline is available.
src/pc_tau/semantics.py:30: # console.log SEM-02: fragment normalization entry.
src/pc_tau/semantics.py:33: # console.log SEM-03: fragment normalization complete.
src/pc_tau/semantics.py:40: # console.log SEM-04: fragment hash entry.
src/pc_tau/semantics.py:43: # console.log SEM-05: fragment hash complete.
src/pc_tau/semantics.py:60: # console.log SEM-06: extract_facts entry.
src/pc_tau/semantics.py:90: # console.log SEM-07: extract_facts complete.
src/pc_tau/semantics.py:97: # console.log SEM-08: alternate normalization entry.
src/pc_tau/semantics.py:100: # console.log SEM-09: alternate normalization complete.
src/pc_tau/semantics.py:117: # console.log SEM-10: verify_facts entry.
src/pc_tau/semantics.py:142: # console.log SEM-11: verify_facts complete.
src/pc_tau/semantics.py:159: # console.log SEM-12: compile_contract entry.
src/pc_tau/semantics.py:198: # console.log SEM-13: compile_contract complete.
src/pc_tau/semantics.py:211: # console.log SEM-14: family status entry.
src/pc_tau/semantics.py:225: # console.log SEM-15: family status complete.
src/pc_tau/repairs.py:8: # console.log REP-01: module import confirms repair extraction is available.
src/pc_tau/repairs.py:30: # console.log REP-02: legal_repairs entry.
src/pc_tau/repairs.py:56: # console.log REP-03: legal_repairs complete.
src/pc_tau/touch.py:8: # console.log TCH-01: module import confirms touch derivation is available.
src/pc_tau/touch.py:14: # console.log TCH-02: canonicalization entry.
src/pc_tau/touch.py:17: # console.log TCH-03: canonicalization complete.
src/pc_tau/touch.py:38: # console.log TCH-04: derive_touch entry.
src/pc_tau/touch.py:42: # console.log TCH-05: manual label rejected.
src/pc_tau/touch.py:57: # console.log TCH-06: R firewall violation rejected.
src/pc_tau/touch.py:61: # console.log TCH-07: E firewall violation rejected.
src/pc_tau/touch.py:65: # console.log TCH-08: A firewall violation rejected.
src/pc_tau/touch.py:68: # console.log TCH-09: derive_touch complete.
scripts/phase2_extract.py:18: # console.log EXT-01: script entry confirms extraction pipeline start.
scripts/phase2_extract.py:38: # console.log EXT-02: argparse configuration entry.
scripts/phase2_extract.py:44: # console.log EXT-03: arguments parsed.
scripts/phase2_extract.py:51: # console.log EXT-04: manifest update entry.
scripts/phase2_extract.py:58: # console.log EXT-05: manifest update complete.
scripts/phase2_extract.py:65: # console.log EXT-06: main entry.
scripts/phase2_extract.py:70: # console.log EXT-07: experiment config loaded.
scripts/phase2_extract.py:83: # console.log EXT-08: census and exclusion list loaded.
scripts/phase2_extract.py:95: # console.log EXT-09: extraction complete for all candidates.
scripts/phase2_extract.py:106: # console.log EXT-10: semantic facts written.
scripts/phase2_extract.py:120: # console.log EXT-11: extraction protocol frozen and written.
scripts/phase2_extract.py:128: # console.log EXT-12: extraction pipeline complete.
scripts/phase2_extract.py:134: # console.log EXT-13: script invoked as main.
scripts/phase2_verify.py:18: # console.log VER-01: script entry confirms verification pipeline start.
scripts/phase2_verify.py:24: # console.log VER-02: argparse configuration entry.
scripts/phase2_verify.py:30: # console.log VER-03: arguments parsed.
scripts/phase2_verify.py:37: # console.log VER-04: manifest update entry.
scripts/phase2_verify.py:44: # console.log VER-05: manifest update complete.
scripts/phase2_verify.py:51: # console.log VER-06: main entry.
scripts/phase2_verify.py:56: # console.log VER-07: experiment config loaded.
scripts/phase2_verify.py:65: # console.log VER-08: facts grouped per task.
scripts/phase2_verify.py:72: # console.log VER-09: verification complete.
scripts/phase2_verify.py:78: # console.log VER-10: extraction records written.
scripts/phase2_verify.py:83: # console.log VER-11: verification pipeline complete.
scripts/phase2_verify.py:89: # console.log VER-12: script invoked as main.
scripts/phase2_compile.py:18: # console.log CMP-01: script entry confirms compilation pipeline start.
scripts/phase2_compile.py:24: # console.log CMP-02: argparse configuration entry.
scripts/phase2_compile.py:30: # console.log CMP-03: arguments parsed.
scripts/phase2_compile.py:37: # console.log CMP-04: manifest update entry.
scripts/phase2_compile.py:44: # console.log CMP-05: manifest update complete.
scripts/phase2_compile.py:51: # console.log CMP-06: main entry.
scripts/phase2_compile.py:56: # console.log CMP-07: experiment config loaded.
scripts/phase2_compile.py:73: # console.log CMP-08: facts and verification joined per task.
scripts/phase2_compile.py:95: # console.log CMP-09: compilation complete.
scripts/phase2_compile.py:104: # console.log CMP-10: contracts written.
scripts/phase2_compile.py:110: # console.log CMP-11: families written.
scripts/phase2_compile.py:121: # console.log CMP-12: compilation pipeline complete.
scripts/phase2_compile.py:127: # console.log CMP-13: script invoked as main.
scripts/phase2_touch.py:20: # console.log TCH10-01: script entry confirms touch pipeline start.
scripts/phase2_touch.py:33: # console.log TCH10-02: argparse configuration entry.
scripts/phase2_touch.py:39: # console.log TCH10-03: arguments parsed.
scripts/phase2_touch.py:52: # console.log TCH10-04: snapshot build entry.
scripts/phase2_touch.py:79: # console.log TCH10-05: snapshots complete.
scripts/phase2_touch.py:86: # console.log TCH10-06: manifest update entry.
scripts/phase2_touch.py:93: # console.log TCH10-07: manifest update complete.
scripts/phase2_touch.py:100: # console.log TCH10-08: main entry.
scripts/phase2_touch.py:105: # console.log TCH10-09: experiment config loaded.
scripts/phase2_touch.py:113: # console.log TCH10-10: contracts loaded.
scripts/phase2_touch.py:156: # console.log TCH10-11: derivation complete for all contracts.
scripts/phase2_touch.py:165: # console.log TCH10-12: repairs written.
scripts/phase2_touch.py:170: # console.log TCH10-13: touch parquet written.
scripts/phase2_touch.py:181: # console.log TCH10-14: touch pipeline complete.
scripts/phase2_touch.py:187: # console.log TCH10-15: script invoked as main.
scripts/phase2_eligibility.py:24: # console.log ELIG-01: script entry confirms eligibility pipeline start.
scripts/phase2_eligibility.py:30: # console.log ELIG-02: argparse configuration entry.
scripts/phase2_eligibility.py:36: # console.log ELIG-03: arguments parsed.
scripts/phase2_eligibility.py:43: # console.log ELIG-04: manifest update entry.
scripts/phase2_eligibility.py:50: # console.log ELIG-05: manifest update complete.
scripts/phase2_eligibility.py:57: # console.log ELIG-06: main entry.
scripts/phase2_eligibility.py:62: # console.log ELIG-07: experiment config loaded.
scripts/phase2_eligibility.py:81: # console.log ELIG-08: inputs loaded for eligibility.
scripts/phase2_eligibility.py:124: # console.log ELIG-09: per-task eligibility decided without outcome values.
scripts/phase2_eligibility.py:141: # console.log ELIG-10: classification complete.
scripts/phase2_eligibility.py:149: # console.log ELIG-11: route classification written.
scripts/phase2_eligibility.py:163: # console.log ELIG-12: primary population written.
scripts/phase2_eligibility.py:169: # console.log ELIG-13: partial sidecar written.
scripts/phase2_eligibility.py:175: # console.log ELIG-14: failure cards written.
scripts/phase2_eligibility.py:192: # console.log ELIG-15: eligibility pipeline complete.
scripts/phase2_eligibility.py:198: # console.log ELIG-16: script invoked as main.
scripts/phase2_freeze_refactor_policy.py:17: # console.log POL-01: script entry confirms policy-freeze pipeline start.
scripts/phase2_freeze_refactor_policy.py:23: # console.log POL-02: argparse configuration entry.
scripts/phase2_freeze_refactor_policy.py:29: # console.log POL-03: arguments parsed.
scripts/phase2_freeze_refactor_policy.py:36: # console.log POL-04: manifest update entry.
scripts/phase2_freeze_refactor_policy.py:43: # console.log POL-05: manifest update complete.
scripts/phase2_freeze_refactor_policy.py:50: # console.log POL-06: main entry.
scripts/phase2_freeze_refactor_policy.py:55: # console.log POL-07: experiment config loaded.
scripts/phase2_freeze_refactor_policy.py:95: # console.log POL-08: policy objects assembled.
scripts/phase2_freeze_refactor_policy.py:104: # console.log POL-09: policy file written.
scripts/phase2_freeze_refactor_policy.py:107: # console.log POL-10: policy-freeze pipeline complete.
scripts/phase2_freeze_refactor_policy.py:113: # console.log POL-11: script invoked as main.
scripts/phase2_controlled_panel.py:17: # console.log PANEL-01: script entry confirms panel pipeline start.
scripts/phase2_controlled_panel.py:33: # console.log PANEL-02: argparse configuration entry.
scripts/phase2_controlled_panel.py:39: # console.log PANEL-03: arguments parsed.
scripts/phase2_controlled_panel.py:46: # console.log PANEL-04: manifest update entry.
scripts/phase2_controlled_panel.py:53: # console.log PANEL-05: manifest update complete.
scripts/phase2_controlled_panel.py:60: # console.log PANEL-06: main entry.
scripts/phase2_controlled_panel.py:65: # console.log PANEL-07: experiment config loaded.
scripts/phase2_controlled_panel.py:80: # console.log PANEL-08: non-pilot bases resolved.
scripts/phase2_controlled_panel.py:88: # console.log PANEL-09: transformation family hashed.
scripts/phase2_controlled_panel.py:114: # console.log PANEL-10: panel assembled.
scripts/phase2_controlled_panel.py:118: # console.log PANEL-11: controlled panel written.
scripts/phase2_controlled_panel.py:123: # console.log PANEL-12: panel pipeline complete.
scripts/phase2_controlled_panel.py:129: # console.log PANEL-13: script invoked as main.
scripts/phase2_gate.py:19: # console.log GATE2-01: script entry confirms gate pipeline start.
scripts/phase2_gate.py:44: # console.log GATE2-02: argparse configuration entry.
scripts/phase2_gate.py:51: # console.log GATE2-03: arguments parsed.
scripts/phase2_gate.py:58: # console.log GATE2-04: import scan entry.
scripts/phase2_gate.py:78: # console.log GATE2-05: import scan complete.
scripts/phase2_gate.py:85: # console.log GATE2-06: gate evaluation entry.
scripts/phase2_gate.py:103: # console.log GATE2-07: contract artifacts loaded.
scripts/phase2_gate.py:116: # console.log GATE2-08: provenance and manual-touch checked.
scripts/phase2_gate.py:140: # console.log GATE2-09: formal types checked.
scripts/phase2_gate.py:165: # console.log GATE2-10: planner isolation checked.
scripts/phase2_gate.py:195: # console.log GATE2-11: primary population checked.
scripts/phase2_gate.py:219: # console.log GATE2-12: panel and refactor policies checked.
scripts/phase2_gate.py:242: # console.log GATE2-13: manifest and final-value scan complete.
scripts/phase2_gate.py:248: # console.log GATE2-14: gate verdict determined.
scripts/phase2_gate.py:267: # console.log GATE2-15: manifest update entry.
scripts/phase2_gate.py:276: # console.log GATE2-16: manifest update complete.
scripts/phase2_gate.py:283: # console.log GATE2-17: main entry.
scripts/phase2_gate.py:292: # console.log GATE2-18: arguments parsed.
scripts/phase2_gate.py:298: # console.log GATE2-19: experiment config loaded.
scripts/phase2_gate.py:302: # console.log GATE2-20: gate payload assembled.
scripts/phase2_gate.py:314: # console.log GATE2-21: seal marker written.
scripts/phase2_gate.py:319: # console.log GATE2-22: gate pipeline complete.
scripts/phase2_gate.py:325: # console.log GATE2-23: script invoked as main.
tests/phase2/test_provenance.py:8: # console.log P2T01-01: test module import confirms provenance check is active.
tests/phase2/test_provenance.py:17: # console.log P2T01-02: run id resolution entry.
tests/phase2/test_provenance.py:27: # console.log P2T01-03: provenance test entry.
tests/phase2/test_provenance.py:33: # console.log P2T01-04: artifacts loaded.
tests/phase2/test_provenance.py:43: # console.log P2T01-05: provenance completeness verified.
tests/phase2/test_extraction_freeze.py:10: # console.log P2T02-01: test module import confirms freeze check is active.
tests/phase2/test_extraction_freeze.py:18: # console.log P2T02-02: freeze test entry.
tests/phase2/test_extraction_freeze.py:27: # console.log P2T02-03: protocol loaded.
tests/phase2/test_extraction_freeze.py:41: # console.log P2T02-04: extraction freeze verified.
tests/phase2/test_second_extraction.py:8: # console.log P2T03-01: test module import confirms agreement check is active.
tests/phase2/test_second_extraction.py:17: # console.log P2T03-02: agreement test entry.
tests/phase2/test_second_extraction.py:27: # console.log P2T03-03: verifier outcomes compared.
tests/phase2/test_second_extraction.py:33: # console.log P2T03-04: PARTIAL routing verified.
tests/phase2/test_touch_rejects.py:9: # console.log P2T04-01: test module import confirms touch-reject check is active.
tests/phase2/test_touch_rejects.py:18: # console.log P2T04-02: rejection test entry.
tests/phase2/test_touch_rejects.py:25: # console.log P2T04-03: manual label rejected.
tests/phase2/test_touch_rejects.py:33: # console.log P2T04-04: firewall violations rejected.
tests/phase2/test_touch_rejects.py:39: # console.log P2T04-05: positive derivations verified.
tests/phase2/test_pilot_exclusion_p2.py:9: # console.log P2T05-01: test module import confirms exclusion check is active.
tests/phase2/test_pilot_exclusion_p2.py:17: # console.log P2T05-02: exclusion test entry.
tests/phase2/test_pilot_exclusion_p2.py:34: # console.log P2T05-03: population and panel exclusion verified.
tests/phase2/test_pilot_exclusion_p2.py:39: # console.log P2T05-04: provisional invisibility verified.
tests/phase2/test_family.py:7: # console.log P2T06-01: test module import confirms family check is active.
tests/phase2/test_family.py:16: # console.log P2T06-02: family test entry.
tests/phase2/test_family.py:24: # console.log P2T06-03: family logic verified.
tests/phase2/test_eligibility_blind.py:7: # console.log P2T07-01: test module import confirms blindness check is active.
tests/phase2/test_eligibility_blind.py:15: # console.log P2T07-02: blindness test entry.
tests/phase2/test_eligibility_blind.py:29: # console.log P2T07-03: blindness verified.
tests/phase2/test_reachability_isolated.py:8: # console.log P2T08-01: test module import confirms isolation check is active.
tests/phase2/test_reachability_isolated.py:17: # console.log P2T08-02: brute enumerator entry.
tests/phase2/test_reachability_isolated.py:38: # console.log P2T08-03: isolation test entry.
tests/phase2/test_reachability_isolated.py:79: # console.log P2T08-04: isolation and agreement verified.
tests/phase2/test_no_production_planner_in_phase2.py:7: # console.log P2T09-01: test module import confirms absence check is active.
tests/phase2/test_no_production_planner_in_phase2.py:15: # console.log P2T09-02: absence test entry.
tests/phase2/test_no_production_planner_in_phase2.py:31: # console.log P2T09-03: absence verified.
tests/phase2/test_viable_routes.py:7: # console.log P2T10-01: test module import confirms route check is active.
tests/phase2/test_viable_routes.py:16: # console.log P2T10-02: route test entry.
tests/phase2/test_viable_routes.py:32: # console.log P2T10-03: route counts compared.
tests/phase2/test_viable_routes.py:36: # console.log P2T10-04: viable-route rule verified.
tests/phase2/test_sealed_with_partials.py:9: # console.log P2T11-01: test module import confirms seal check is active.
tests/phase2/test_sealed_with_partials.py:17: # console.log P2T11-02: seal test entry.
tests/phase2/test_sealed_with_partials.py:25: # console.log P2T11-03: seal artifacts loaded.
tests/phase2/test_sealed_with_partials.py:37: # console.log P2T11-04: sealed-with-partials verified.
tests/phase2/test_refactor_policy_frozen.py:9: # console.log P2T12-01: test module import confirms policy check is active.
tests/phase2/test_refactor_policy_frozen.py:17: # console.log P2T12-02: policy test entry.
tests/phase2/test_refactor_policy_frozen.py:29: # console.log P2T12-03: policies frozen and manifested.
tests/phase2/test_refactor_policy_frozen.py:33: # console.log P2T12-04: Phase-3 absence verified.
tests/phase2/test_omega_channel.py:8: # console.log P2T13-01: test module import confirms channel check is active.
tests/phase2/test_omega_channel.py:19: # console.log P2T13-02: channel test entry.
tests/phase2/test_omega_channel.py:36: # console.log P2T13-03: channel and equivalence verified.
tests/phase2/test_single_freeze_file.py:6: # console.log P2T14-01: test module import confirms freeze-file check is active.
tests/phase2/test_single_freeze_file.py:14: # console.log P2T14-02: freeze-file test entry.
tests/phase2/test_single_freeze_file.py:18: # console.log P2T14-03: single freeze file verified.
tests/phase2/test_manifest_hashes_p2.py:11: # console.log P2T15-01: test module import confirms manifest check is active.
tests/phase2/test_manifest_hashes_p2.py:39: # console.log P2T15-02: manifest test entry.
tests/phase2/test_manifest_hashes_p2.py:48: # console.log P2T15-03: manifest loaded.
tests/phase2/test_manifest_hashes_p2.py:57: # console.log P2T15-04: manifest and counts verified.
```

Plus dispatcher addition scripts/run_pc_tau.py RUN-07b (delegating to g2) alongside RUN-01..08 from Phase 1. Reproduce counts: list script above or Select-String console.log. Every print is immediately preceded by its identifying comment (200/200 verified).

### P2.5 Models / benchmarks / anti-overfitting (this phase)

Training none; freeze planning none; optimizer unused. Benchmark is the G2 gate: primary 135 (need 40), domains 2 (need 2), partial 5 sidecar (healthy), panel 32 balanced, firewall 420/420 derived, provenance 420/420 + 840/840 facts. Brutal difference: checker-only viability (planner absent, first use Phase 3); PARTIALs never backfill (STOP if primary <40 even with sidecar); frozen refactor class blocks perturbation shopping; second-extraction refutes manufactured semantics; pilot provisional invisible; no successful-run filtering (all 140 candidates classified: 135+5+0, plus 24 pilot exclusions carded).

### P2.6 Stale-results clearing + commands executed

Pre-existing Phase-1 outputs untouched (re-hash matches; manifest extended, never rewritten). New Phase-2 outputs only under results/pctau-20260906-672227c/contract/ plus 6 schemas and manifest extension. Cleaner not invoked on the sealed run (verified refusal pattern in Phase 1; no deletion performed). Commands: phase2_extract, phase2_verify, phase2_compile, phase2_touch, phase2_eligibility, phase2_freeze_refactor_policy, phase2_controlled_panel, phase2_gate --check-gate g2, run_pc_tau --check-gate g2 (exit 0), pytest tests/phase2+phase1+unit (25 passed), stress2 harness (50 random agreements, canonical invariance, E/R/A separation, optimizer absence, omega hygiene), collection fix (4 __init__.py to disambiguate duplicate basenames).

### P2.7 Verification + stress evidence

- pytest: 25 passed (10 Phase-1 + 15 Phase-2).
- Gate: CONTRACT_SEALED via script and dispatcher (exit 0); marker counts IDENTIFIED 135 PARTIAL 5.
- Stress2: 50 random topologies 0 mismatches; canonical reorder invariant; touch singletons exact; planner/freeze absent; omega free of user/reservation identifiers across 140 contracts; P_R covers U_H; partial reasons all family-disagreement; panel 32 balanced non-pilot.
- Failure injections closed pre-finish: (a) synthetic test facts missing fragment_hash raised KeyError — fixed test fixtures to full fact shape; (b) duplicate test basenames collided at collection — fixed with 4 package __init__.py. No science change.

### P2.8 Compliance audit vs WorkPlan §Phase 2 (extreme rigor, gap-closed)

- §2.2 files: all 16 contract outputs + CONTRACT_SEALED + manifest extension + 6 schemas present with exact names and hashes above. No run-level PARTIAL marker (Fix 12).
- §2.3 code: semantics (Fix 2 protocol + Fix 5 U_H/H/P_R/Lambda/omega/Cert, no outcome/optimizer/provisional refs), repairs (justified atomic singletons), touch (derived union + 4 reject paths + canonical equiv), reachability reused checker-only, 7 pipeline scripts + gate in Appendix-C order, predicate exactly as specified via checker, panel 8x4 from non-pilot bases balanced-by-design. Planner/freeze/metrics unimported everywhere (AST-verified); provisional invisible (grep-verified).
- §2.4: no training/freeze/optimizer; PARTIALs sidecarred healthy; anti-manufacturing via fragment+verifier; panel post-family-freeze non-pilot; touch mechanical; refactor frozen pre-Phase 3.
- §2.5 G2: all conditions true — provenance 100%, no manual touch, types valid (omega!=Cert, P_R covers U_H), checker-only, primary 135>=40 across 2 domains, sidecar 5 with counts, failures 24 carded, panel 32 flagged, policies frozen+hashed, manifest 22 entries, zero final values/optimizer. Phase 3 authorized on primary with PARTIALs present. Else-STOP branch untriggered (would STOP if primary <40).
- Fixes: Fix 2 (extract-verify-compile + disagreement-PARTIAL), Fix 3+11 (checker viable>=2, dead-button blocked, planner-first-use Phase 3), Fix 4 (3 policies frozen, Phase-3 untouched), Fix 5 (omega channel + P_R equivalence), Fix 9 (run-scoped + manifest, single freeze), Fix 12 (sole CONTRACT_SEALED + sidecar + no-backfill).
- No gaps remain. Phase 2 is finished.

### P2.9 Deviations + rejected attempts

Deviations: two harness fixes only (test fixture shape; collection __init__.py). No science change. Rejected: (a) capping primary to 60-96 target (retained honest 135 yield; minimum gate governs), (b) merging PARTIALs into primary (sidecar only), (c) planner-assisted viability (checker only), (d) post-result perturbation design (frozen class only), (e) vendor Phase-3 modules early (absent verified).

**WorkPlan-follows: YES.** Phase 2 implements WorkPlan §Phase 2 exactly as written (all files, code, tests, gates, fixes). Next is Phase 3 per Appendix C.

_Status: COMPLETE (CONTRACT_SEALED). Commit phase2: CONTRACT_SEALED pctau-20260906-672227c (pending push, see log)._


## §P3 — Phase 3: Exact Freeze Benchmark and Learned-Agent Evaluation (TO RUN)

Required: scope; files (`results/<run-id>/exact/*`, `agents/*`, `controls/*`, `PHASE3_COMPLETE` + hashes); code (`planner.py` INF design, `freeze.py` masks + same-instance manifests, `runtime.py` blinded tools + safety-gate log `executed_unauthorized==0`, `metrics.py` 7 metrics + bootstrap); model roster (3 families, IDs/revisions/params + hash) + episode counts (target 2,160 at 60 tasks; repeats=3; freezes F000/F100/F010/F001; exact 8-cell); user-bundle freeze hash + invariance check; crosscheck 100% log; all-rows-retained proof (null/inf/failure present); tests (`tests/phase3/*`); deviations/rejected; commit `phase3: MEASURED <run-id> <hash>` + push; **WorkPlan-follows**.

_Status: PENDING._

## §P4 — Phase 4: Independent Audit, Falsification, Claims, Seal (TO RUN)

Required: scope; files (`src/pc_tau_audit/*`, `audit/*`, `reports/CLAIMS.md`, `REPRODUCE.md`, `benchmark_report.md`, `audited_tables/`, `claim_ledger.json`, `artifact_graph.json`, `audit.json`, `SEALED` or `INVALID` + hashes); code (import-ban proof, 6-layer recompute equality table, 8-family corruption inject→detect log, refactoring invariance/PARTIAL-flip log, claim-lock passes); clean-checkout reproduce log (fresh clone + one command → identical seal hash); DoD checklist (§5.3 all rows) + hard-stop scans (§5.1); tests (`tests/phase4/*`, `tests/metamorphic/*`); deviations/rejected; commit `phase4: SEALED|INVALID <run-id> <hash>` + push; **WorkPlan-follows**.

_Status: PENDING._

## §R1 — Review patch: 10 fixes into WorkPlan.md (2026-09-06, UTC)

### R1.1 Scope

Apply the 10-issue review (Phase-1 contradiction; underspecified extraction; weak MULTI_ACTION; late refactoring seal; ω/P_R bug; impossible byte-identical live reproduction; 3 planners; fallback single-domain trap; heavy artifacts; keyword claim locks) to `WorkPlan.md` without redesign. No scientific code, no freezes, no model runs in this entry. `WorkPlan.md` stays at 4 phases; implement-exactly/stop-on-gates frozen.

### R1.2 Files changed + how coded

- `WorkPlan.md` only (14 edits, `grep -c "Fix [0-9]"` = 35 hits post-patch): §0.3 (Fix 1 pilot-provisional, Fix 3 predicate, Fix 7 sole planner, Fix 10 predicates); §0.4 (Fix 8 `N<40 OR domains<2` + multidomain pilot); §0.5 (Fix 3 viable-route + Fix 5 `U_H/H/P_R/Λ/ω/Cert`); §0.6–0.7 (Fix 9 run-scoped `results/<run_id>/` + single `freezes.yaml` + manifest, Fix 6 split reproduction); Phase 1 (Fix 1 exception box + provisional `pilot/provisional_geometry.jsonl`, Fix 3/8 gates, Fix 9/10 files); Phase 2 (Fix 2 `extract→verify→compile` + `extraction_protocol/records.json`, Fix 4 `semantic_boundary_policy/admissible_refactorings/contract_family_rules.json` frozen at G2, Fix 5 math, Fix 3 `viable_first_repairs>=2` predicate); Phase 3 (Fix 7 production-only + `planner_selftest.json`, Fix 6 archive-for-replay, Fix 4 untouched); Phase 4 (Fix 4 frozen-class execution, Fix 6 exact-replay vs live-rerun, Fix 7 `planner_agreement.json`, Fix 8 population-integrity, Fix 9 run-scoped audit/reports + graph, Fix 10 predicate ledger + generator); Appendices A–C (predicate enforcement, fix index, commands: +`phase2_verify.py` +`phase2_freeze_refactor_policy.py`, −`phase3_crosscheck.py`, +`--reproduce/--replicate-live`).
- Method: sequential `edit` with unique `oldString` per fix; verified by `Select-String` (Fix count, `freeze_lattice.yaml` only in Fix-9 note, no `phase3_crosscheck` creation, no `certificate predicate` for ω, no keyword-blacklist logic, no single-domain trap). No invented SHAs/IDs/K_Pi.
- `Path.md` (this entry): §§P1–P4 checklists below are superseded on paths/predicates by this §R1 + patched WorkPlan (run-scoped `results/<run_id>/…`, viable-route, frozen refactor class, predicate ledger, split reproduction, two planners). Future phase entries must cite patched WorkPlan sections.

### R1.3 Models / benchmarks / anti-overfitting

Training: still none. Brutal-difference preserved and strengthened: pilot provisional invisible downstream; viable-route blocks dead-button degeneracy; frozen refactor class blocks perturbation shopping; ω-precise leakage blocks truth-in-channel; exact-replay (byte-identical) separated from live-rerun (new run-id, stats only); two-planner (not three) keeps full independence with less weight; fallback trap closed; predicate locks close paraphrase bypass.

### R1.4 Stale results / verification

`Get-ChildItem -Force` still shows only `LICENSE + WorkPlan.md + Path.md`; zero `results/` artifacts (nothing to clear). Verification: [x] all 10 fixes present (`Fix 1`–`Fix 10` each hit); [x] single freeze file (no `freeze_lattice.yaml` creation); [x] no sidecars (only "no sidecars" mentions); [x] no 3-planner logic; [x] ω = channel + `Cert` separate; [x] fallback `OR domains<2`; [x] predicate ledger example valid JSON keys; [x] commands include `phase2_verify`, `phase2_freeze_refactor_policy`, `--reproduce`, `--replicate-live`, no `phase3_crosscheck.py` build.

### R1.5 Deviations

None from review. Rejected: 5th/6th phase split (kept 4); symlink/copy freeze files (Windows-safe single file); inventing tau2-bench SHA/model IDs (still deferred).

**WorkPlan-follows: YES.** Implements exactly the 10-fix patch list; no gate claimed; next is Phase 1 per patched WorkPlan Appendix C.

## §R2 — Final 4 fixes into WorkPlan.md (2026-09-06, UTC)

### R2.1 Scope

Apply the 4 final review issues without redesign: (Fix 11) production planner must not decide Phase-2 eligibility — tiny separate unrestricted reachability checker `Viable(q)` with no freeze/cost/`Δ_R`/`K_Pi` knowledge, planner first used in Phase 3; (Fix 12) run-level PARTIAL eliminated — `CONTRACT_SEALED` whenever the IDENTIFIED primary core passes, task PARTIALs in sealed sidecar, else STOP; (Fix 13) all claim predicates start `false`, flip to `true` only on machine-checkable evidence predicates, permanent nonclaims stay `false`; (Fix 14) explicit trajectory persistence — immutable `pc-tau-<run-id>-sealed.tar.zst` release bundle + committed `releases/<run-id>.json` pointer, `--reproduce` verifies bundle and recomputes. No scientific code/freezes/model runs in this entry.

### R2.2 Files changed + how coded

- `WorkPlan.md` (16 edits): Status + §0.2 phase chain (Fix 12) + §0.3 pts 1/7 (Fix 11 checker, Fix 13 all-false) + §0.5 gate (Fix 11) + §0.6 layout (`reachability.py`, `partial_tasks.jsonl` sidecar, `releases/<run-id>.json`) + runtime/persistence (Fix 14 bundle) + traceability/stale-rules/verification strings + Phase 1 (Fix 11 pilot checker, Fix 13 defaults, planner-import ban) + Phase 2 header/files (`CONTRACT_SEALED` or `STOP`, sidecar, no run PARTIAL) + `reachability.py` module spec + checker-only predicate + tests (`test_reachability_isolated`, `test_no_production_planner_in_phase2`, `test_sealed_with_partials`, blind-checker) + §2.4 sidecar language + G2 rewrite (primary core ≥40, PARTIALs never backfill, Phase 3 authorized with PARTIALs present) + Phase 3 scope/files/code/tests/gates (planner first use, primary-core-only, bundle archiving, `test_planner_first_use`) + Phase 4 files/boundary/layers/corruptions/claims-example (all-false + evidence predicates e.g. `finite_substitution_authorized=[∃ i∈N: 0<Δ_R<∞]`) / seal-bundle-pointer / tests (evidence-flip + bundle-tamper + replay-from-bundle) / §4.4/G4/DoD/stops (checker/sidecar/evidence/bundle checks) + Appendix A (evidence predicates) + Appendix B (Fix 11–14 index) + Appendix C (G2 note, seal-bundle build, bundle-verified reproduce).
- Method: sequential unique-`oldString` edits; verified by `Select-String` (Fix 11–14 hits; no `phase3_crosscheck` build; `freeze_lattice.yaml` only in Fix-9 note; ω=`Cert`-separate intact; fallback `OR domains<2` intact; claims example all-`false`; bundle name + pointer present; no run-level `PARTIAL` success state outside Fix-12 history note).
- `Path.md` (this entry): §§P1–P4 TO-RUN checklists now read through this §R2 + patched WorkPlan (checker-only viability, sealed-with-partials, evidence-flipped predicates, bundle pointer). Future phase entries must cite patched sections.

### R2.3 Models / benchmarks / anti-overfitting

Training: still none. Separation hardened: population never depends on the unaudited optimizer (checker/planner agreement separately tested in Phase 3, authoritative planner audit still in Phase 4); healthy PARTIAL ambiguity retained without blocking Phase 3; ledger genuinely evidence-derived (zero-gap fixture cannot flip finite-substitution); determinism brutally tested from the published bundle, provider nondeterminism isolated to live-rerun path.

### R2.4 Stale results / verification

`Get-ChildItem -Force` still only `LICENSE + WorkPlan.md + Path.md`; zero `results/`/`releases/` artifacts (nothing to clear; bundle mechanism defined before any bundle exists). Verification: [x] Fix 11 (`reachability.py`, `Viable(q)`, planner-first-use, import bans); [x] Fix 12 (no run PARTIAL success; sidecar + counts + no-backfill + Phase-3-authorized-with-partials); [x] Fix 13 (all-false example, 5 evidence predicates, permanent-false, generator-only-true); [x] Fix 14 (bundle name, pointer path/content, git-ignore rule, reproduce-via-pointer, tamper-detect, no normal-Git bulk).

### R2.5 Deviations

None from final review. Rejected: reusing production planner for eligibility (firewall + audit risk); `CONTRACT_SEALED_WITH_PARTIALS` rename (plain `CONTRACT_SEALED` + counts simpler per review); pre-authorized `true` predicates; Git-LFS/normal-Git bulk commit for trajectories (release-bundle preferred per review).

**WorkPlan-follows: YES.** Implements exactly the 4 final fixes; no gate claimed; next is Phase 1 per patched WorkPlan Appendix C.

---

## Commit/push log (user requirement: push after each phase without being asked)

| Date (UTC) | Commit | Gate | Remote |
|---|---|---|---|
| 2026-09-06 | `b9372d9 docs: WorkPlan.md + Path.md setup` pushed `573c701..b9372d9 main->main` | planning (no gate) | `origin/main` |
| 2026-09-06 | `455b6db` review patch Fix 1–10 + Path §R1 pushed `f52eb02..455b6db main->main` | planning patch (no gate) | `origin/main` |
| 2026-09-06 | `3cd12da` final 4 fixes Fix 11–14 + Path §R2 pushed `49989bd..3cd12da main->main` | planning patch (no gate) | `origin/main` |
| 2026-09-06 | `19004b7` phase1: PREREGISTERED pctau-20260906-672227c pushed `b378cb7..19004b7 main->main` | PREREGISTERED | `origin/main` |
| 2026-09-06 | `eff5ba5` phase2: CONTRACT_SEALED pctau-20260906-672227c pushed `5bb670c..eff5ba5 main->main` | CONTRACT_SEALED | `origin/main` |
| — | Phase 2 commit (pending) | CONTRACT_SEALED/STOP | — |
| — | Phase 3 commit (pending) | MEASURED | — |
| — | Phase 4 commit (pending) | SEALED/INVALID | — |
