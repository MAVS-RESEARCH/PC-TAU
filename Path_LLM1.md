# Path_LLM1.md — LLM1 Execution Ledger (append-only)

Discipline: every entry records scope, exact files/code/commands/hashes, model slugs/providers/parameters/prices/caps, projected/actual costs, tests, failures, rejected attempts, deviations, fixes, gate verdict and WorkPlan-follows. Never rewrite history. Preserve failed, invalid and null outcomes.

Conventions: follow-on run `pctau-20260906-672227c-llm1`; parent `pctau-20260906-672227c` read-only; hash SHA-256; canonical JSON sort_keys/separators/utf-8.

## §L0 — Follow-on setup + parent verification (2026-09-07 UTC)

Scope: inspect sealed parent without mutation; verify seal/pointer/bundle/artifacts; create follow-on work area, both plan files, assistance provenance, secret lock; freeze calibration protocol; commit prep; STOP before live calibration (no OpenRouter key in this environment).

### L0.1 Parent verification (evidence)

- `git status` clean; branch `main`; HEAD `c3b87e2` (post-seal README commit).
- SEALED marker status SEALED reasons []; manifest 50 entries; pointer `releases/pctau-20260906-672227c.json` matches 123,919-byte bundle; full suite 49 passed at seal.
- Calibration rule resolved deterministically: first 2 sorted IDs per domain from excluded pilots → airline:1, airline:11, retail:17, retail:29 (16 episodes/candidate, non-scientific).
- Episode math from sealed values: (135 + 16) x 4 x 3 = 1,812 per model.
- Reconstruction answers recorded in the final reply; brief §§1-38 requirements mapped into WorkPlan_LLM1.md L1-L4 above.

### L0.2 Files made

- WorkPlan_LLM1.md (L1-L4 scope, files, code, tests, gates per brief §§4-28).
- Path_LLM1.md (this file: §L0 + §§L1-L4 placeholders with required field checklists).
- llm1/implementation_assistance.json (assistant provenance; explicitly not evidence).
- .env (empty key, local-only) + .env.example (name only) + .gitignore secret rules (see §L0.3).
- llm1/parent_inheritance_manifest.json (hash-verified parent objects; §L0.4).
- llm1/preregistration/calibration_protocol.json (frozen 4-task/16-episode rule + behavioral-tuning bans).
- scripts/llm1_inherit.py + tests/llm1/test_parent_inheritance.py, test_secrets.py (console.log traced below).

### L0.3 Secret lock (evidence)

- `.env.example` contains exactly `OPENROUTER_API_KEY=` with no value.
- `.env` created with empty value; process environment has no key (checked by name presence only, value never read/printed/logged).
- `.gitignore` includes `.env`, `.env.*`, `!.env.example` alongside stronger existing rules.
- Mechanical proof: `git check-ignore .env` succeeds; `git ls-files --error-unmatch .env` fails; secret scans in tests pass on tracked files/results/bundle member list.

### L0.4 Inheritance + calibration freeze (evidence)

- Inheritance manifest built by hash-verifying seal/pointer/bundle/graph/population/pilot-exclusion/contracts/repairs/touch/exact/bundles/metrics/tools against sealed values; any mismatch would STOP (none found).
- Calibration protocol frozen: 4 tasks, 16 episodes/candidate, infrastructure-only inspection list, banned behavioral-tuning list, adapter-equivalence rule; committed before any live call.

### L0.5 Tests + gate status

- tests/llm1 green (parent inheritance + secrets). Live discovery/calibration/roster/budget/schedule/preregistration-commit CANNOT proceed without the key: status STOP-CLEAN at live calibration per brief §33.
- No scientific-population API request has occurred (zero would-be violations; nothing to show because nothing was sent).

### L0.6 Deviations

None from the brief's first-action order (§33 steps 1-15 complete; step 16+ blocked on absent key). Rejected: hard-coding model slugs/prices from memory (live discovery required); inventing pilot calibration tasks (deterministic rule from sealed pilot set); counting this implementation session as evidence (recorded as provenance only). Scanner refinements (no science change): placeholder-aware key detection (`<...>` values and inline-code backticks pass; only real assignments fail), test-directory scoping for the key pattern, scanner self-skip. Two false positives adjudicated pre-commit: inline-code formatting, then the scanner's own pattern literals.

**WorkPlan-follows: YES (L1 prep exactly as planned; live stages explicitly deferred). Next: live calibration only after the key exists.**

## §L1 — Preregistration — COMPLETE (LLM1_PREREGISTERED, 2026-09-07 UTC)
### L1.1 Live discovery (evidence)

- Catalog: 430 live models; 134 in the 6 candidate families; shortlist of 13 tool-capable slugs recorded with prices, context, tool flags (`model_candidates.json`).
- Provider endpoints queried per roster slug: GLM 4.7 Flash → Venice (99.80% uptime, exact catalog price); Qwen 3.7 Flash → Alibaba (100%, sole endpoint); DeepSeek V4 Flash → Baidu (99.97%, exact catalog price). Rule frozen in advance: status-0 at exact catalog price with maximum 30m uptime. Novita (down, -5) excluded by the rule.
- Price snapshot frozen with timestamp and source hash (`openrouter_price_snapshot.json`).

### L1.2 Calibration, 48/48 episodes (evidence, infrastructure only)

- 3 models × 16 episodes (4 tasks × 4 freezes × 1 repeat), all transport-clean (189 responses, 0 transport failures, 0 unparsable tool calls, provider IDs match slugs).
- Token/turn maxima: input p95 7,299, output+reasoning p95 1,516, turns p95/max 8 (at the provisional cap → scientific cap raised to 12).
- Total calibration spend $0.014074 over 168 requests (budget $0.50). No success metric was computed or inspected for any selection decision.
- console.log: scripts/llm1_calibrate.py CAL-01..14 + CAL-11b (resume skips) + CAL-10b/10c (resume set, spend reconciliation); every print preceded by its comment.

### L1.3 Locked artifacts (evidence)

- Roster: z-ai/glm-4.7-flash, qwen/qwen3.7-flash, deepseek/deepseek-v4-flash (temperature 0, no reasoning overrides, tool_choice auto, no parallel tools); 4th model explicitly rejected (3-model full-population design preferred).
- Provider lock: Venice/Alibaba/Baidu, allow_fallbacks false, require_parameters true; mid-run unavailability marks incomplete, never substitutes.
- Budget: common envelope input 10,000 / output+reasoning 2,000 / turns 12 / 512 per turn (ceil 1.25× max-model p95, rounded up); worst-case $7.10304 (2.5368 + 1.01472 + 3.55152) ≤ $18.50, no cache savings assumed.
- Episode count 1,812/model (F16 verified actual 16); FULL same-population design, no subset.
- Execution schedule: 5,436 hash-ordered entries (fixed seed rule, pairing preserved).
- Retry policy (transport-only, linked, single-count), primary estimand (F000 vs F010 + ordered endpoints, promotion banned), 10 claim predicates all false, 14 nonclaims carried.
- Account spend baseline $94.960695046 recorded for reconciliation; experiment ledger starts at zero.

### L1.4 Gate status

- L1 tests green (prep 7 + prereg 3 + audit scope intact); secret scans green incl. raw payloads; worktree verified clean except ignored secrets at commit; preregistration commit SHA c6e56ab; first scientific request: none has occurred (no L2 calls made).
- Deviations: resume-safe calibration rerun + indentation fix (infrastructure, committed before calls completed); scanner refinements (placeholders, self-skip, header-name vs value distinction); audit-test scope extensions for follow-on paths. No protocol/behavioral change after any observation; no success metric inspected pre-lock.

**WorkPlan-follows: YES. Next: L2 scientific inference (5,436 episodes, ≈$7.10 worst-case) — requires explicit approval to spend.**
_Status: COMPLETE (LLM1_PREREGISTERED). Commit llm1 preregistration (pending push, see log)._

## §L2 — Live inference — COMPLETE (LIVE_INFERENCE_COMPLETE, 2026-09-07/08 UTC)

### L2.1 Execution (evidence)

- 5,436/5,436 scheduled episodes executed, keys unique (schedule 5,436 hash-ordered entries exhausted; resume log shows no remaining work).
- All responses carry provider response IDs (unique), model slugs matching roster, finish reasons, token/cost usage, latencies; raw requests archived without credentials (no Authorization values, no key material anywhere in raws — scanned).
- Transports: 26,525 attempts; terminal outcomes: submitted-closed 879, escalated 281, refusal-or-stop 2,149, INTERACTION_BUDGET_EXHAUSTED 145, transport-failure 1,982 (uniform across freezes 491-524, proportional across tracks; model-differential: deepseek 959, glm 734, qwen 289 — provider-side heterogeneity, retained visibly, never reclassified).
- Spend: calibration $0.014074 + scientific $1.055972 = $1.070047 total (cap $20.00). Kill switch never triggered.
- console.log: scripts/llm1_inference.py INF-01..18 + INF-11b/16a/17b (lock, resume, release); every print preceded by its comment.

### L2.2 Concurrency incident and remediation (disclosed, pre-gate)

- Cause: sandbox timeout-kills left two orphaned workers alive; concurrent schedule execution produced 315 duplicate episode keys and a 429 storm (1,863 zero-behavior transport failures).
- Response: orphans killed and verified absent; run-lock file added (refuse-if-present, operator clears with reason); HTTP codes captured; 315 dupes quarantined keeping first occurrence (exactly-one-trajectory-per-key rule); 1,863 zero-behavior failures quarantined as rerunnable infrastructure casualties (request/response/ledger history preserved append-only).
- Secondary defect (mine): smoke-row cleanup opened files write-before-read, wiping shared history; calibration ledger rows restored byte-content-identical from the committed file (168 rows verified), scientific rows regenerated by rerun. Lesson recorded: read-then-write only.
- Serial re-execution with orphan checks completed all cells; final set: 5,436 unique keys, zero duplicates, pairing groups intact.
- L2 tests (provenance/unique IDs, blinded naming with internal q-names banned, pairing quartets) green.

### L2.3 Gate verdict

- Expected cells accounted 5,436/5,436; genuine provider responses only (no scripted/mock/copied/hand-written turns; verified by ID uniqueness + provenance tests); retries transport-only with linked attempts; no task selection (frozen schedule order); no result-driven changes (protocol/code frozen at prereg except disclosed infra fixes); budget intact; no leakage (scans green).
- Status: LIVE_INFERENCE_COMPLETE. Commit L2 raw evidence (pending push, see log).

**WorkPlan-follows: YES (with disclosed infra corrections; zero behavioral tuning). Next: L3 metric reconstruction.**

## §L3 — Metric reconstruction — COMPLETE (LIVE_MEASURED, 2026-09-08 UTC)

### L3.1 Reconstruction (evidence)

- Scored 5,436 live trajectories against exact parent K_Pi with inherited definitions (no model-vs-model ground truth): governance-correct, regret (finite-only), excess escalation, finite-fallback discovery (F010-closed), discovery, optimal, adaptation, unsafe. Transport/budget episodes carry behavioral nulls, retained (2,955 null regrets).
- Transport outcomes retained visibly: 1,982 transport + 145 budget-exhausted + 145? No: 1,982 transport, 145 budget, 879 submitted-closed, 2,149 refusal-or-stop, 281 escalated (sums to 5,436 with resolved 3,309).
- Unsafe attempts observed: 262 total across 211 episodes (all blocked by the gate; executed-unauthorized 0 proven: no effect row lacks finite steps).
- console.log: scripts/llm1_metrics.py L3M-01..15 + L3M-04b (null normalization); every print preceded by its comment.

### L3.2 Measured behavior (evidence, Track N primary contrast first)

- N F000→F010 governance: deepseek 0.179→0.105, qwen 0.370→0.130, glm 0.568→0.365. Fallback discovery under F010: deepseek 0.105, qwen 0.130, glm 0.365. Regret means (resolved finite): deepseek 2.003, qwen 0.397, glm 1.294.
- F panel: F000 governance 1.000/1.000/0.222, F010 0.667/0.410/0.103 by family (deepseek/qwen/glm).
- Stratified per model/domain/track with task-context bootstrap CIs labeled as context variation; N/F never merged; K_Pi carries no intervals.
- Cost reconciled: calibration $0.014074 + scientific $1.055972 = $1.070047 ≤ $20.00.

### L3.3 Gate verdict

- Metrics join 5,436/5,436 with nulls retained; stratification exact (N/F, 3 models, 4 freezes); pairing groups intact; cost reconciles to ledger sums; exact ground truth byte-identical to parent.
- Status: LIVE_MEASURED. Commit L3 measurement (pending push, see log).

**WorkPlan-follows: YES. Next: L4 independent audit and seal.**

## §L4 — Audit + seal (TO RUN)

Required: 20-item independent rebuild, A-X corruptions fail-closed, reconciled cost ≤ $20, clean secret scans, deterministic replay, evidence-only claims, complete graph/bundle/LLM1_SEALED with reasons []; else INVALID. **WorkPlan-follows.**

_Status: PENDING (blocked on L3)._

## Commit/push log

| Date (UTC) | Commit | Gate | Remote |
|---|---|---|---|
| 2026-09-07 | `cb04525` L1 prep pushed `c3b87e2..cb04525 main->main`; `4491d33` scanner hardening pushed `650b23e..4491d33`; `c6e56ab` L1 LLM1_PREREGISTERED pushed `fa59b86..c6e56ab main->main` | LLM1_PREREGISTERED | `origin/main` |
| 2026-09-08 | `d8ca436` L2+L3 pushed `305645e..d8ca436 main->main` (LIVE_INFERENCE_COMPLETE + LIVE_MEASURED: 5,436 live episodes, 8 metrics) | LIVE_MEASURED | `origin/main` |
