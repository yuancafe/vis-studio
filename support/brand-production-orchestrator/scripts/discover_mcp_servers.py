#!/usr/bin/env python3
"""Discover local design MCP services from Codex and global MCP configs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _orchestration_utils import discover_design_services, load_route_rules


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--route-rules",
        type=Path,
        default=None,
        help="Optional route-rules JSON path (default: assets/route-rules.json)",
    )
    parser.add_argument(
        "--codex-config",
        type=Path,
        default=None,
        help="Optional Codex config path (default: ~/.codex/config.toml)",
    )
    parser.add_argument(
        "--global-mcp-config",
        type=Path,
        default=None,
        help="Optional global MCP config path (default: ~/.config/mcp/config.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    routes = load_route_rules(args.route_rules)
    report = discover_design_services(
        route_rules=routes,
        codex_config_path=args.codex_config,
        global_mcp_config_path=args.global_mcp_config,
    )
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
