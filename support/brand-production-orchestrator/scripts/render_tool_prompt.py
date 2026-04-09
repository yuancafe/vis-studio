#!/usr/bin/env python3
"""Render a route-specific tool prompt from prompt templates."""

from __future__ import annotations

import argparse
from pathlib import Path

from _orchestration_utils import load_route_rules, infer_intent, render_tool_prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goal", help="Production goal text")
    parser.add_argument(
        "--intent",
        default=None,
        help="Optional explicit intent; if omitted, inferred from goal",
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
        help="Optional template directory override",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write the rendered prompt",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    routes = load_route_rules(args.route_rules)
    intent = args.intent
    if not intent:
        intent, _ = infer_intent(args.goal, routes, args.preferred_tool)
    if intent not in routes:
        raise SystemExit(f"Unknown intent: {intent}")

    required_documents = routes[intent].get("required_documents", [])
    prompt = render_tool_prompt(
        intent=intent,
        goal=args.goal,
        required_documents=required_documents,
        template_dir=args.template_dir,
    )

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(prompt if prompt.endswith("\n") else prompt + "\n", encoding="utf-8")
    print(prompt)


if __name__ == "__main__":
    main()
