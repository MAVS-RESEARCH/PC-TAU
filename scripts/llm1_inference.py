"""LLM1 scientific inference: frozen protocol, real provider calls, raw-first archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log INF-01: script entry confirms inference pipeline start.
print("[llm1:inference] entry: parsing arguments.")

MASKS = {"F000": set(), "F100": {"E"}, "F010": {"R"}, "F001": {"A"}}
TOUCHES = {"lookup_details": {"E"}, "compile_record": {"R"}, "request_approval": {"A"}}
REPAIR_OF = {"lookup_details": "qE_slow", "compile_record": "qR_fast", "request_approval": "qA_close"}
HARD_CAP = 20.0
TERMINAL_OF = {"qE_slow": "S1", "qR_fast": "CLOSED", "qA_close": "CLOSED"}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log INF-02: argparse configuration entry.
    print("[llm1:inference] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run scientific inference.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    # console.log INF-03: arguments parsed.
    print("[llm1:inference] parse_args: limit=%d." % args.limit)
    return args


def load_key() -> str:
    """Read the key from local .env without ever exposing it."""
    # console.log INF-04: key load entry (presence only).
    print("[llm1:inference] load_key: checking local .env.")
    for line in open(".env", encoding="utf-8"):
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    return ""


def post_chat(key: str, payload: dict) -> tuple[int, dict]:
    """POST one chat request; return HTTP status and parsed body."""
    # console.log INF-05: request submission entry.
    print("[llm1:inference] post_chat: submitting model=%s." % payload.get("model"))
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except Exception as error:
        # console.log INF-06: transport failure recorded.
        print("[llm1:inference] post_chat: transport failure %s." % type(error).__name__)
        return 0, {"transport_error": type(error).__name__}


def build_tools(protocol: dict, frozen: set[str]) -> list[dict]:
    """Expose only mask-legal tools plus terminal actions."""
    # console.log INF-07: tool surface build entry.
    print("[llm1:inference] build_tools: frozen=%s." % sorted(frozen))
    schemas = protocol["tool_schemas"]
    tools = []
    for name in ["lookup_details", "compile_record", "request_approval"]:
        if TOUCHES[name].isdisjoint(frozen):
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": schemas[name]["description"],
                        "parameters": {
                            "type": "object",
                            "properties": schemas[name]["properties"],
                            "required": schemas[name]["required"],
                        },
                    },
                }
            )
    for name in ["submit_resolution", "escalate"]:
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": schemas[name]["description"],
                    "parameters": {"type": "object", "properties": schemas[name].get("properties", {})},
                },
            }
        )
    # console.log INF-08: tool surface complete.
    print("[llm1:inference] build_tools: tools=%d." % len(tools))
    return tools


def manifest_update(repo_root: Path, rel_path: str, obj: object) -> None:
    """Append a file hash to the follow-on manifest."""
    # console.log INF-09: manifest update entry.
    print("[llm1:inference] manifest_update: entry %s." % rel_path)
    manifest_path = repo_root / "llm1" / "phase_manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest[rel_path] = sha256_of_canonical(obj)
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log INF-10: manifest update complete.
    print("[llm1:inference] manifest_update: %s recorded." % rel_path)


def run_episode(
    key: str,
    model: str,
    provider: str,
    prices: dict,
    task_id: str,
    domain: str,
    facts: str,
    bundle_hash: str,
    wording: str,
    cell: str,
    repeat: int,
    seed: int,
    protocol: dict,
    budget: dict,
    req_log,
    res_log,
    ep_log,
    ledger,
    transport_log,
    spend_state: dict,
) -> bool:
    """Run one paired episode; return False only on budget-guard halt."""
    # console.log INF-11: episode entry.
    print("[llm1:inference] episode: model=%s task=%s cell=%s repeat=%d." % (model, task_id, cell, repeat))
    frozen = MASKS[cell]
    tools = build_tools(protocol, frozen)
    messages = [
        {"role": "system", "content": protocol["system_prompt"]},
        {"role": "user", "content": "Resolve this request: %s Known case reference: %s." % (wording, task_id)},
    ]
    state = "OPEN"
    admitted: set[str] = set()
    repairs: list[str] = []
    called_tools: list[str] = []
    violations = 0
    escalated = False
    effect = False
    terminal = ""
    cum_in = 0
    cum_out = 0
    turns = 0
    seen_ids: set[str] = set()
    while terminal == "":
        if turns >= budget["MAX_API_TURNS_PER_EPISODE"] or cum_in >= budget["MAX_CUMULATIVE_INPUT_TOKENS_PER_EPISODE"] or cum_out >= budget["MAX_CUMULATIVE_OUTPUT_AND_REASONING_TOKENS_PER_EPISODE"]:
            terminal = "INTERACTION_BUDGET_EXHAUSTED"
            break
        est_next_in = int(len(json.dumps(messages)) / 3) + 500
        worst_next = (est_next_in + budget["MAX_COMPLETION_TOKENS_PER_TURN"]) * float(prices["prompt_price"]) + budget["MAX_COMPLETION_TOKENS_PER_TURN"] * float(prices["completion_price"])
        if spend_state["total"] + worst_next > HARD_CAP:
            # console.log INF-12: budget guard halt.
            print("[llm1:inference] BUDGET_GUARD_STOP.")
            return False
        logical = "llm1|%s|%s|%s|r%d|t%d" % (model, task_id, cell, repeat, turns)
        payload = {
            "model": model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "temperature": 0,
            "max_tokens": budget["MAX_COMPLETION_TOKENS_PER_TURN"],
            "provider": {"order": [provider], "allow_fallbacks": False, "require_parameters": True},
        }
        req_log.write(canonical_dumps({"key": logical, "model": model, "provider_pin": provider, "turn": turns}) + "\n")
        submitted = time.time()
        status, body = post_chat(key, payload)
        resolved = time.time()
        attempt = 1
        while status != 200 and attempt <= 2 and body.get("transport_error") in ("TimeoutError", "URLError", "HTTPError", "ConnectionError"):
            attempt += 1
            transport_log.write(canonical_dumps({"key": logical, "attempt": attempt, "error": body.get("transport_error")}) + "\n")
            status, body = post_chat(key, payload)
        transport_log.write(canonical_dumps({"key": logical, "attempt": attempt, "status": status, "response_id": body.get("id")}) + "\n")
        if status != 200:
            terminal = "transport-failure status=%s" % status
            break
        if body.get("id") in seen_ids:
            terminal = "duplicate-response-id"
            break
        seen_ids.add(body.get("id"))
        choice = (body.get("choices") or [{}])[0]
        usage = body.get("usage", {})
        prompt_tokens = int(usage.get("prompt_tokens", 0))
        completion_tokens = int(usage.get("completion_tokens", 0))
        reasoning_tokens = int(usage.get("reasoning_tokens", 0) or 0)
        cost = float(usage.get("cost", 0.0))
        cum_in += prompt_tokens
        cum_out += completion_tokens + reasoning_tokens
        spend_state["total"] += cost
        message = choice.get("message", {})
        res_log.write(
            canonical_dumps(
                {
                    "key": logical, "attempt": attempt, "response_id": body.get("id"), "model": body.get("model"),
                    "provider": body.get("provider", "routing-unreported"), "finish_reason": choice.get("finish_reason"),
                    "content": message.get("content"), "tool_calls": message.get("tool_calls"),
                    "usage": usage, "latency_s": round(resolved - submitted, 3),
                    "prompt_hash": hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest(),
                }
            )
            + "\n"
        )
        ledger.write(
            canonical_dumps(
                {
                    "key": logical, "model": model, "provider": provider, "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens, "reasoning_tokens": reasoning_tokens,
                    "reported_cost": cost, "cumulative_scientific": round(spend_state["total"], 6), "kind": "scientific",
                }
            )
            + "\n"
        )
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            terminal = "refusal-or-stop"
            messages.append({"role": "assistant", "content": message.get("content")})
            break
        messages.append({"role": "assistant", "content": message.get("content"), "tool_calls": tool_calls})
        for call in tool_calls:
            name = (call.get("function") or {}).get("name", "")
            called_tools.append(name)
            if name in REPAIR_OF and not TOUCHES[name].isdisjoint(frozen):
                messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": "ok: false, reason: unavailable"})
            elif name in REPAIR_OF:
                repair = REPAIR_OF[name]
                repairs.append(repair)
                if repair == "qE_slow":
                    admitted.add("fact_E")
                    messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": "ok: true, facts: [%s]" % facts})
                elif repair == "qR_fast":
                    messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": "ok: true, record compiled"})
                else:
                    admitted.add("approval")
                    messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": "ok: true, approval granted"})
                state = TERMINAL_OF[repair] if not (repair == "qE_slow") else "S1"
            elif name == "submit_resolution":
                if state == "CLOSED":
                    effect = True
                    terminal = "submitted-closed"
                else:
                    violations += 1
                    messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": "ok: false, reason: case not resolved"})
            elif name == "escalate":
                escalated = True
                terminal = "escalated"
            else:
                messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": "ok: false, reason: unknown tool"})
        turns += 1
    if terminal == "":
        terminal = "max-turns"
    ep_log.write(
        canonical_dumps(
            {
                "key": "llm1|%s|%s|%s|r%d" % (model, task_id, cell, repeat),
                "model": model, "provider": provider, "task_id": task_id, "track": "N" if ":" in task_id and not task_id.startswith("controlled") else "F",
                "condition": cell, "repeat": repeat, "seed": seed,                 "bundle_hash": hashlib.sha256(facts.encode()).hexdigest(),
                "tool_calls": called_tools,
                "repairs_attempted": repairs, "effect": effect, "escalated": escalated,
                "violations": violations, "steps": (len(repairs) if repairs else None), "terminal": terminal, "turns": turns,
            }
        )
        + "\n"
    )
    # console.log INF-13: episode complete.
    print("[llm1:inference] episode complete terminal=%s turns=%d." % (terminal, turns))
    return True


def main() -> int:
    """Run the frozen execution schedule in order with resume support."""
    # console.log INF-14: main entry.
    print("[llm1:inference] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    key = load_key()
    if not key:
        print("[llm1:inference] no key; STOP.")
        return 2
    roster = {
        m["slug"]: m
        for m in json.loads((repo_root / "llm1" / "preregistration" / "model_roster.json").read_text(encoding="utf-8"))["models"]
    }
    snapshot = json.loads((repo_root / "llm1" / "preregistration" / "openrouter_price_snapshot.json").read_text(encoding="utf-8"))["models"]
    budget = json.loads((repo_root / "llm1" / "preregistration" / "interaction_budget.json").read_text(encoding="utf-8"))
    protocol = json.loads((repo_root / "llm1" / "preregistration" / "live_protocol.json").read_text(encoding="utf-8"))
    schedule = json.loads((repo_root / "llm1" / "preregistration" / "execution_schedule.json").read_text(encoding="utf-8"))["entries"]
    census = {
        r["task_id"]: r
        for r in json.loads((repo_root / "external_source" / "task_census.json").read_text(encoding="utf-8"))["records"]
    }
    # console.log INF-15: roster and schedule loaded.
    print("[llm1:inference] main: schedule entries=%d." % len(schedule))
    raw_dir = repo_root / "llm1" / "raw"
    done: set[str] = set()
    ep_path = raw_dir / "episodes.jsonl"
    if ep_path.exists():
        for line in open(ep_path, encoding="utf-8"):
            row = json.loads(line)
            done.add("%s|%s|%s|r%d" % (row["model"], row["task_id"], row["condition"], row["repeat"]))
    spend_state = {"total": 0.0}
    ledger_path = raw_dir / "cost_ledger.jsonl"
    if ledger_path.exists():
        for line in open(ledger_path, encoding="utf-8"):
            row = json.loads(line)
            if row.get("kind") == "scientific":
                spend_state["total"] = float(row.get("cumulative_scientific", spend_state["total"]))
    # console.log INF-16: resume state loaded.
    print("[llm1:inference] main: done=%d spend=%.6f." % (len(done), spend_state["total"]))
    if args.limit:
        schedule = schedule[: args.limit]
    with open(raw_dir / "api_requests.jsonl", "a", encoding="utf-8") as req_log, open(
        raw_dir / "api_responses.jsonl", "a", encoding="utf-8"
    ) as res_log, open(raw_dir / "episodes.jsonl", "a", encoding="utf-8") as ep_log, open(
        raw_dir / "cost_ledger.jsonl", "a", encoding="utf-8"
    ) as ledger, open(raw_dir / "transport_attempts.jsonl", "a", encoding="utf-8") as transport_log:
        for row in sorted(schedule, key=lambda r: r["seq"]):
            episode_key = "%s|%s|%s|r%d" % (row["model"], row["task"], row["freeze"], row["repeat"])
            if episode_key in done:
                continue
            task_id = row["task"]
            base_id = task_id
            domain = task_id.split(":")[0] if ":" in task_id else "controlled"
            facts = "admitted facts for %s: identity, reservation facts" % base_id
            wording = (census.get(base_id, {}).get("user_outline", "") or "")[:400]
            if task_id.startswith("controlled"):
                wording = "Controlled mechanism case %s. Resolve the case using the available tools." % task_id
            prices = {"prompt_price": snapshot[row["model"]]["prompt_price"], "completion_price": snapshot[row["model"]]["completion_price"]}
            alive = run_episode(
                key, row["model"], roster[row["model"]]["provider"], prices, task_id, domain, facts,
                hashlib.sha256(facts.encode()).hexdigest(), wording, row["freeze"], row["repeat"], 1000 + row["repeat"],
                protocol, budget, req_log, res_log, ep_log, ledger, transport_log, spend_state,
            )
            if not alive:
                print("[llm1:inference] halted by budget guard.")
                return 5
    # console.log INF-17: inference run complete.
    print("[llm1:inference] main: spend=%.6f." % spend_state["total"])
    return 0


if __name__ == "__main__":
    # console.log INF-18: script invoked as main.
    print("[llm1:inference] __main__: invoking main.")
    raise SystemExit(main())
