"""LLM1 calibration: excluded-pilot episodes only, infrastructure metrics only."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps


# console.log CAL-01: script entry confirms calibration start.
print("[llm1:calibrate] entry: parsing arguments.")

MASKS = {"F000": set(), "F100": {"E"}, "F010": {"R"}, "F001": {"A"}}
TOUCHES = {"lookup_details": {"E"}, "compile_record": {"R"}, "request_approval": {"A"}}
REPAIR_OF = {"lookup_details": "qE_slow", "compile_record": "qR_fast", "request_approval": "qA_close"}
HARD_CAP = 20.0


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log CAL-02: argparse configuration entry.
    print("[llm1:calibrate] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run excluded-pilot calibration.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--models", nargs="+", required=True)
    args = parser.parse_args()
    # console.log CAL-03: arguments parsed.
    print("[llm1:calibrate] parse_args: models=%s." % args.models)
    return args


def load_key() -> str:
    """Read the key from local .env without ever exposing it."""
    # console.log CAL-04: key load entry (presence only).
    print("[llm1:calibrate] load_key: checking local .env.")
    for line in open(".env", encoding="utf-8"):
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    return ""


def post_chat(key: str, payload: dict) -> tuple[int, dict]:
    """POST one chat request; return HTTP status and parsed body."""
    # console.log CAL-05: request submission entry.
    print("[llm1:calibrate] post_chat: submitting model=%s." % payload.get("model"))
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except Exception as error:
        # console.log CAL-06: transport failure recorded.
        print("[llm1:calibrate] post_chat: transport failure %s." % type(error).__name__)
        return 0, {"transport_error": type(error).__name__}


def build_tools(protocol: dict, frozen: set[str]) -> list[dict]:
    """Expose only mask-legal tools plus terminal actions."""
    # console.log CAL-07: tool surface build entry.
    print("[llm1:calibrate] build_tools: frozen=%s." % sorted(frozen))
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
                    "parameters": {
                        "type": "object",
                        "properties": schemas[name].get("properties", {}),
                    },
                },
            }
        )
    # console.log CAL-08: tool surface complete.
    print("[llm1:calibrate] build_tools: tools=%d." % len(tools))
    return tools


def main() -> int:
    """Run 16 calibration episodes per candidate with full raw archives."""
    # console.log CAL-09: main entry.
    print("[llm1:calibrate] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    key = load_key()
    if not key:
        print("[llm1:calibrate] no key; STOP.")
        return 2
    protocol = json.loads((repo_root / "llm1" / "preregistration" / "live_protocol.json").read_text(encoding="utf-8"))
    calibration = json.loads((repo_root / "llm1" / "preregistration" / "calibration_protocol.json").read_text(encoding="utf-8"))
    census = {
        r["task_id"]: r
        for r in json.loads((repo_root / "external_source" / "task_census.json").read_text(encoding="utf-8"))["records"]
    }
    # console.log CAL-10: protocol and census loaded.
    print("[llm1:calibrate] main: protocol frozen=%s." % protocol["frozen"])
    tasks = calibration["calibration_set"]["airline"] + calibration["calibration_set"]["retail"]
    raw_dir = repo_root / "llm1" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    spend = 0.0
    episodes = 0
    # console.log CAL-11: episode loop entry.
    print("[llm1:calibrate] main: tasks=%d models=%d." % (len(tasks), len(args.models)))
    with open(raw_dir / "calibration_requests.jsonl", "a", encoding="utf-8") as req_log, open(
        raw_dir / "calibration_responses.jsonl", "a", encoding="utf-8"
    ) as res_log, open(raw_dir / "calibration_episodes.jsonl", "a", encoding="utf-8") as ep_log, open(
        raw_dir / "cost_ledger.jsonl", "a", encoding="utf-8"
    ) as ledger:
        for model in args.models:
            for task_id in tasks:
                for cell, frozen in MASKS.items():
                    turn_count = 0
                    messages = [
                        {"role": "system", "content": protocol["system_prompt"]},
                        {
                            "role": "user",
                            "content": "Resolve this request: %s Known case reference: %s."
                            % (census[task_id].get("user_outline", "")[:400], task_id),
                        },
                    ]
                    tools = build_tools(protocol, frozen)
                    terminal: str | None = None
                    usage_total = {"prompt": 0, "completion": 0, "reasoning": 0, "cost": 0.0}
                    turns = 0
                    # console.log CAL-12: episode entry.
                    print("[llm1:calibrate] episode: model=%s task=%s cell=%s." % (model, task_id, cell))
                    while terminal is None and turns < protocol["max_turns"]:
                        logical_key = "calib|%s|%s|%s|r0|t%d" % (model, task_id, cell, turns)
                        payload = {
                            "model": model,
                            "messages": messages,
                            "tools": tools,
                            "tool_choice": "auto",
                            "temperature": 0,
                            "max_tokens": protocol["budget_provisional_calibration_only"]["max_completion_tokens_per_turn"],
                        }
                        req_log.write(canonical_dumps({"key": logical_key, "model": model, "params": {"temperature": 0}}) + "\n")
                        submitted = time.time()
                        status, body = post_chat(key, payload)
                        resolved = time.time()
                        if status != 200:
                            terminal = "transport-failure status=%s" % status
                            break
                        choice = (body.get("choices") or [{}])[0]
                        usage = body.get("usage", {})
                        prompt_tokens = int(usage.get("prompt_tokens", 0))
                        completion_tokens = int(usage.get("completion_tokens", 0))
                        reasoning_tokens = int(usage.get("reasoning_tokens", usage.get("completion_details", {}).get("reasoning_tokens", 0) or 0) or 0)
                        cost = float(usage.get("cost", 0.0))
                        spend += cost
                        usage_total["prompt"] += prompt_tokens
                        usage_total["completion"] += completion_tokens
                        usage_total["reasoning"] += reasoning_tokens
                        usage_total["cost"] += cost
                        if spend > HARD_CAP:
                            print("[llm1:calibrate] BUDGET_GUARD_STOP.")
                            return 5
                        message = choice.get("message", {})
                        res_log.write(
                            canonical_dumps(
                                {
                                    "key": logical_key,
                                    "response_id": body.get("id"),
                                    "model": body.get("model"),
                                    "finish_reason": choice.get("finish_reason"),
                                    "content": message.get("content"),
                                    "tool_calls": message.get("tool_calls"),
                                    "usage": usage,
                                    "latency_s": round(resolved - submitted, 3),
                                }
                            )
                            + "\n"
                        )
                        ledger.write(
                            canonical_dumps(
                                {
                                    "key": logical_key,
                                    "model": model,
                                    "prompt_tokens": prompt_tokens,
                                    "completion_tokens": completion_tokens,
                                    "reasoning_tokens": reasoning_tokens,
                                    "reported_cost": cost,
                                    "cumulative_calibration": round(spend, 6),
                                    "kind": "calibration",
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
                            messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": "ok: received %s" % name})
                            if name in ("submit_resolution", "escalate"):
                                terminal = "terminal-action %s" % name
                        turns += 1
                    turn_count = turns
                    ep_log.write(
                        canonical_dumps(
                            {
                                "key": "calib|%s|%s|%s|r0" % (model, task_id, cell),
                                "model": model,
                                "task_id": task_id,
                                "cell": cell,
                                "turns": turn_count,
                                "terminal": terminal,
                                "usage": usage_total,
                            }
                        )
                        + "\n"
                    )
                    episodes += 1
    # console.log CAL-13: calibration complete.
    print("[llm1:calibrate] main: episodes=%d spend=%.6f." % (episodes, spend))
    return 0


if __name__ == "__main__":
    # console.log CAL-14: script invoked as main.
    print("[llm1:calibrate] __main__: invoking main.")
    raise SystemExit(main())
