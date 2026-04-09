#!/usr/bin/env python3
"""Build EXECUTION_PLAN.md for a VIS STUDIO production route."""

from __future__ import annotations

import argparse
from pathlib import Path

from _orchestration_utils import (
    ROOT,
    as_bullets,
    as_numbered_steps,
    infer_intent,
    load_route_rules,
    mode_reason,
    next_action_for,
    render_tool_prompt,
    to_tool_display_name,
    tool_reason,
)


DEFAULT_PLAN_TEMPLATE = ROOT / "assets" / "execution-plan-template.md"


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
        "--template-file",
        type=Path,
        default=None,
        help="Optional execution plan template override",
    )
    parser.add_argument(
        "--prompt-template-dir",
        type=Path,
        default=None,
        help="Optional tool prompt template directory override",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path for EXECUTION_PLAN.md",
    )
    return parser.parse_args()


def build_plan(args: argparse.Namespace) -> str:
    routes = load_route_rules(args.route_rules)
    route_reason = "Route explicitly set by caller."
    intent = args.intent

    if not intent:
        intent, route_reason = infer_intent(args.goal, routes, args.preferred_tool)
    if intent not in routes:
        raise SystemExit(f"Unknown intent: {intent}")

    route_data = routes[intent]
    required_documents = route_data.get("required_documents", [])
    optional_documents = route_data.get("optional_documents", [])
    actions = route_data.get("actions", [])
    deliverables = route_data.get("deliverables", [])
    primary_tool_id = route_data.get("primary_tool", "")
    primary_tool = to_tool_display_name(primary_tool_id)
    secondary_tools = [
        f"{to_tool_display_name(tool_id)} ({tool_id})"
        for tool_id in route_data.get("secondary_tools", [])
    ]
    tool_prompt = render_tool_prompt(
        intent=intent,
        goal=args.goal,
        required_documents=required_documents,
        template_dir=args.prompt_template_dir,
    )
    execution_mode = args.execution_mode
    mcp_supported = bool(route_data.get("mcp_supported", False))
    template_path = args.template_file or DEFAULT_PLAN_TEMPLATE
    template = template_path.read_text(encoding="utf-8")

    return template.format(
        goal=args.goal,
        intent=intent,
        route=route_data.get("route", intent),
        route_reason=route_reason,
        primary_tool=primary_tool,
        tool_reason=tool_reason(intent, primary_tool_id),
        secondary_tools=as_bullets(secondary_tools),
        required_documents=as_bullets(required_documents),
        optional_documents=as_bullets(optional_documents),
        execution_mode=execution_mode,
        mode_reason=mode_reason(execution_mode, mcp_supported),
        execution_steps=as_numbered_steps(actions),
        tool_prompt=tool_prompt,
        deliverables=as_bullets(deliverables),
        next_action=next_action_for(intent, execution_mode),
    )


def main() -> None:
    args = parse_args()
    content = build_plan(args)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            content if content.endswith("\n") else content + "\n",
            encoding="utf-8",
        )
    print(content)


if __name__ == "__main__":
    main()
