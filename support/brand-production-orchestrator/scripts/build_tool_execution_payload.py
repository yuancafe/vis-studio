#!/usr/bin/env python3
"""Build TOOL_EXECUTION_PAYLOAD.json for a production route."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _orchestration_utils import (
    choose_executor_for_intent,
    discover_design_services,
    load_route_rules,
    infer_intent,
    render_tool_prompt,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goal", help="Production goal text")
    parser.add_argument(
        "--intent",
        default=None,
        help="Optional explicit intent; if omitted, inferred from goal",
    )
    parser.add_argument(
        "--execution-mode",
        default="handoff",
        choices=["handoff", "execute"],
        help="Execution mode",
    )
    parser.add_argument(
        "--run-mode",
        default="document",
        choices=["document", "production"],
        help="Run mode. production mode forces execute behavior downstream.",
    )
    parser.add_argument(
        "--production-scope",
        default="single",
        choices=["single", "full_suite"],
        help="Production scope for orchestration context.",
    )
    parser.add_argument(
        "--execution-gateway-mode",
        default="hybrid",
        choices=["direct", "swarm", "hybrid"],
        help="Gateway mode for executor routing.",
    )
    parser.add_argument(
        "--decision-timeout-seconds",
        type=int,
        default=15,
        help="Timeout used when critical-step user decision is required.",
    )
    parser.add_argument(
        "--fallback-figma-connector",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Allow figma connector fallback when local figma MCP is unavailable.",
    )
    parser.add_argument(
        "--route-rules",
        type=Path,
        default=None,
        help="Optional route-rules JSON path (default: assets/route-rules.json)",
    )
    parser.add_argument(
        "--preferred-tool",
        default=None,
        help="Optional preferred tool for route inference",
    )
    parser.add_argument(
        "--template-dir",
        type=Path,
        default=None,
        help="Optional prompt template directory override",
    )
    parser.add_argument(
        "--target-file",
        default=None,
        help="Optional target file/link for MCP execution",
    )
    parser.add_argument(
        "--target-selection",
        default=None,
        help="Optional target selection identifier for MCP execution",
    )
    parser.add_argument(
        "--selected-executor",
        default=None,
        help="Optional selected executor override",
    )
    parser.add_argument(
        "--output-family-dir",
        default="",
        help="Optional family output directory for production artifacts.",
    )
    parser.add_argument(
        "--dependency-inputs-file",
        type=Path,
        default=None,
        help="Optional JSON file describing dependency inputs.",
    )
    parser.add_argument(
        "--fallback-trace-file",
        type=Path,
        default=None,
        help="Optional JSON file describing fallback trace.",
    )
    parser.add_argument(
        "--order-context-file",
        type=Path,
        default=None,
        help="Optional JSON file describing normalized order context.",
    )
    parser.add_argument(
        "--gateway-trace-file",
        type=Path,
        default=None,
        help="Optional JSON file describing gateway routing attempts.",
    )
    parser.add_argument(
        "--delivery-contract-file",
        type=Path,
        default=None,
        help="Optional JSON file describing task-level delivery contract.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional payload output path",
    )
    return parser.parse_args()


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    routes = load_route_rules(args.route_rules)
    intent = args.intent
    if not intent:
        intent, _ = infer_intent(args.goal, routes, args.preferred_tool)
    if intent not in routes:
        raise SystemExit(f"Unknown intent: {intent}")

    route_data = routes[intent]
    required_docs = route_data.get("required_documents", [])
    prompt = render_tool_prompt(
        intent=intent,
        goal=args.goal,
        required_documents=required_docs,
        template_dir=args.template_dir,
    )

    if args.run_mode == "production":
        execution_mode = "execute"
    else:
        execution_mode = args.execution_mode

    mcp_supported = bool(route_data.get("mcp_supported", False))
    discovery = discover_design_services(routes)
    auto_selected_executor, route_candidates, selected_reason = choose_executor_for_intent(
        intent, discovery
    )
    selected_executor = args.selected_executor or auto_selected_executor

    dependency_inputs: list[dict[str, Any]] = []
    if args.dependency_inputs_file is not None and args.dependency_inputs_file.exists():
        loaded = json.loads(args.dependency_inputs_file.read_text(encoding="utf-8"))
        if isinstance(loaded, list):
            dependency_inputs = loaded

    fallback_trace: list[dict[str, Any]] = []
    if args.fallback_trace_file is not None and args.fallback_trace_file.exists():
        loaded = json.loads(args.fallback_trace_file.read_text(encoding="utf-8"))
        if isinstance(loaded, list):
            fallback_trace = loaded

    mcp_block = {
        "supported": mcp_supported,
        "tool_name": route_data.get("primary_tool"),
        "target_file": args.target_file or "",
        "target_selection": args.target_selection or "",
        "notes": (
            "Provide a concrete target file or selection before direct MCP execution."
            if mcp_supported
            else "Route currently runs in handoff-oriented mode."
        ),
    }

    order_context: dict[str, Any] = {}
    if args.order_context_file is not None and args.order_context_file.exists():
        loaded = json.loads(args.order_context_file.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            order_context = loaded

    gateway_trace: list[dict[str, Any]] = []
    if args.gateway_trace_file is not None and args.gateway_trace_file.exists():
        loaded = json.loads(args.gateway_trace_file.read_text(encoding="utf-8"))
        if isinstance(loaded, list):
            gateway_trace = loaded

    delivery_contract: dict[str, Any] = {}
    if args.delivery_contract_file is not None and args.delivery_contract_file.exists():
        loaded = json.loads(args.delivery_contract_file.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            delivery_contract = loaded

    return {
        "goal": args.goal,
        "intent": intent,
        "route": route_data.get("route", intent),
        "primary_tool": route_data.get("primary_tool"),
        "secondary_tools": route_data.get("secondary_tools", []),
        "required_documents": required_docs,
        "optional_documents": route_data.get("optional_documents", []),
        "run_mode": args.run_mode,
        "production_scope": args.production_scope,
        "execution_gateway_mode": args.execution_gateway_mode,
        "execution_mode": execution_mode,
        "fallback_policy": {
            "figma_connector": bool(args.fallback_figma_connector),
        },
        "executor_candidates": route_data.get("executor_candidates", []),
        "selected_executor": selected_executor,
        "dependency_inputs": dependency_inputs,
        "output_family_dir": args.output_family_dir or "",
        "decision_timeout_seconds": max(1, args.decision_timeout_seconds),
        "fallback_trace": fallback_trace,
        "order_context": order_context,
        "gateway_trace": gateway_trace,
        "delivery_contract": delivery_contract,
        "actions": route_data.get("actions", []),
        "deliverables": route_data.get("deliverables", []),
        "tool_prompt": prompt,
        "mcp": mcp_block,
        "selection_reason": selected_reason,
        "route_critical": bool(route_data.get("critical", False)),
        "input_artifact_types": route_data.get("input_artifact_types", []),
        "output_artifact_types": route_data.get("output_artifact_types", []),
    }


def main() -> None:
    args = parse_args()
    payload = build_payload(args)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
