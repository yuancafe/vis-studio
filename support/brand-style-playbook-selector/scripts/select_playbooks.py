#!/usr/bin/env python3
"""Score brand style playbooks against a structured brief."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def tokens_from_value(value: Any) -> set[str]:
    tokens: set[str] = set()
    if isinstance(value, dict):
        for nested in value.values():
            tokens |= tokens_from_value(nested)
    elif isinstance(value, list):
        for nested in value:
            tokens |= tokens_from_value(nested)
    elif isinstance(value, str):
        tokens |= {token.lower() for token in re.findall(r"[\w-]+", value)}
    return tokens


def build_brief_tokens(brief: dict[str, Any]) -> tuple[set[str], set[str]]:
    avoid_tokens = tokens_from_value(brief.get("avoid_signals", []))
    positive_source = {
        key: value
        for key, value in brief.items()
        if key not in {"avoid_signals", "notes", "raw"}
    }
    positive_tokens = tokens_from_value(positive_source)
    return positive_tokens, avoid_tokens


def score_playbook(
    playbook: dict[str, Any], positive_tokens: set[str], avoid_tokens: set[str]
) -> dict[str, Any]:
    fit_tokens = tokens_from_value(playbook.get("fit_signals", []))
    avoid_playbook_tokens = tokens_from_value(playbook.get("avoid_signals", []))
    match_tokens = sorted(positive_tokens & fit_tokens)
    positive_conflicts = sorted(positive_tokens & avoid_playbook_tokens)
    avoid_alignment = sorted(avoid_tokens & avoid_playbook_tokens)
    score = len(match_tokens) * 3 + len(avoid_alignment) * 2 - len(positive_conflicts) * 4

    positioning_tokens = tokens_from_value(playbook.get("positioning_match", ""))
    positioning_overlap = sorted(positive_tokens & positioning_tokens)
    score += len(positioning_overlap)

    rationale_parts: list[str] = []
    if match_tokens:
        rationale_parts.append("fit matches: " + ", ".join(match_tokens[:8]))
    if positioning_overlap:
        rationale_parts.append(
            "positioning overlap: " + ", ".join(positioning_overlap[:6])
        )
    if avoid_alignment:
        rationale_parts.append("avoid alignment: " + ", ".join(avoid_alignment[:8]))
    if positive_conflicts:
        rationale_parts.append(
            "signal conflicts: " + ", ".join(positive_conflicts[:8])
        )
    if not rationale_parts:
        rationale_parts.append("limited direct overlap; review manually")

    return {
        "id": playbook["id"],
        "name": playbook["name"],
        "score": score,
        "fit_matches": match_tokens,
        "avoid_alignment": avoid_alignment,
        "signal_conflicts": positive_conflicts,
        "rationale": "; ".join(rationale_parts),
        "playbook": playbook,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="Path to a structured brand brief JSON file")
    parser.add_argument("--top", type=int, default=3, help="Number of top playbooks to return")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    brief = load_json(args.brief)
    playbooks = load_json(root / "assets" / "brand_style_playbooks.json")

    positive_tokens, avoid_tokens = build_brief_tokens(brief)
    scored = [
        score_playbook(playbook, positive_tokens, avoid_tokens) for playbook in playbooks
    ]
    scored.sort(key=lambda item: item["score"], reverse=True)

    result = {
        "brief_summary": {
            "brand_name": brief.get("brand_name"),
            "category": brief.get("category"),
            "audience": brief.get("audience"),
            "price_point": brief.get("price_point"),
            "personality": brief.get("personality"),
            "required_signals": brief.get("required_signals", []),
            "avoid_signals": brief.get("avoid_signals", []),
        },
        "selected_playbooks": scored[: args.top],
        "positive_tokens": sorted(positive_tokens),
        "avoid_tokens": sorted(avoid_tokens),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
