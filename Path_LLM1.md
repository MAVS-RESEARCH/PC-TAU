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

## §L1 — Preregistration (TO RUN: discovery → calibration → roster → budget → schedule → commit LLM1_PREREGISTERED)

Required: live catalog rows, price snapshot, token calibration, episode_count.json (1,812/model), worst-case projection ≤ $18.50, frozen roster/provider/prompts/tools/budget/population/schedule/retry/estimand/all-false claims, prereg commit SHA + timing proof (first scientific request after), full L1 tests green; else STOP. **WorkPlan-follows.**

_Status: BLOCKED (no key; see §L0.5)._

## §L2 — Live inference (TO RUN)

Required: 1,812 accounted episodes/model from real provider responses with raw-first archives, linked retries, frozen protocol, kill-switch log, no secret leakage; else INVALID. **WorkPlan-follows.**

_Status: PENDING (blocked on L1)._

## §L3 — Metrics + analysis (TO RUN)

Required: 8 reconstructed metrics, F000/F010 primary with F100/F001 matched, per-model/per-domain/N/F stratification, nulls retained, parent ground truth byte-identical; else INVALID. **WorkPlan-follows.**

_Status: PENDING (blocked on L2)._

## §L4 — Audit + seal (TO RUN)

Required: 20-item independent rebuild, A-X corruptions fail-closed, reconciled cost ≤ $20, clean secret scans, deterministic replay, evidence-only claims, complete graph/bundle/LLM1_SEALED with reasons []; else INVALID. **WorkPlan-follows.**

_Status: PENDING (blocked on L3)._

## Commit/push log

| Date (UTC) | Commit | Gate | Remote |
|---|---|---|---|
| 2026-09-07 | `cb04525` L1 prep pushed `c3b87e2..cb04525 main->main`; `4491d33` scanner hardening pushed `650b23e..4491d33` | prep (no gate) | `origin/main` |
