#!/usr/bin/env python3
"""Select the most likely production route for a VIS STUDIO goal."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _orchestration_utils import load_route_rules, infer_intent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goal", help="Production goal text")
    parser.add_argument(
        "--route-rules",
        type=Path,
        default=None,
        help="Optional route-rules JSON path (default: assets/route-rules.json)",
    )
    parser.add_argument(
        "--preferred-tool",
        default=None,
        help="Optional preferred primary tool (for example: figma_mcp, canva, inkscape)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write selected route JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    routes = load_route_rules(args.route_rules)
    intent, reason = infer_intent(args.goal, routes, args.preferred_tool)
    route_data = routes[intent]

    result = {
        "goal": args.goal,
        "intent": intent,
        "route": route_data.get("route", intent),
        "primary_tool": route_data.get("primary_tool"),
        "secondary_tools": route_data.get("secondary_tools", []),
        "critical": bool(route_data.get("critical", False)),
        "default_family": route_data.get("default_family", intent.replace("_", "-")),
        "executor_candidates": route_data.get("executor_candidates", []),
        "input_artifact_types": route_data.get("input_artifact_types", []),
        "output_artifact_types": route_data.get("output_artifact_types", []),
        "reason": reason,
        "required_documents": route_data.get("required_documents", []),
        "optional_documents": route_data.get("optional_documents", []),
        "actions": route_data.get("actions", []),
        "deliverables": route_data.get("deliverables", []),
        "mcp_supported": bool(route_data.get("mcp_supported", False)),
    }

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
