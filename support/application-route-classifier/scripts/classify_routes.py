#!/usr/bin/env python3
"""Classify application items into production routes."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MANUAL_FAMILIES = {"packaging", "signage", "wayfinding", "environment"}
TEMPLATE_FAMILIES = {"social", "banner", "web", "deck", "document"}
MOCKUP_KEYWORDS = {
    "business card",
    "notebook",
    "tote",
    "cup",
    "bag",
    "shirt",
    "merch",
    "sticker",
}
MANUAL_KEYWORDS = {
    "dieline",
    "wayfinding",
    "vehicle",
    "livery",
    "exhibition",
    "signage system",
    "packaging line",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def classify(item: dict[str, Any]) -> tuple[str, str]:
    text = " ".join(
        str(part)
        for part in (item.get("name", ""), item.get("purpose", ""), item.get("family", ""))
    ).lower()
    family = item.get("family", "")

    if family in MANUAL_FAMILIES or any(keyword in text for keyword in MANUAL_KEYWORDS):
        return "manual_vector", "requires precise vector or engineering detail"
    if family in TEMPLATE_FAMILIES:
        return "template_auto", "stable layout family suited to template reuse"
    if any(keyword in text for keyword in MOCKUP_KEYWORDS):
        return "mockup_semi_auto", "best expressed through product or scene mockups"
    return "mockup_semi_auto", "physical or contextual application benefits from mockup treatment"


def build_batches(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for item in items:
        grouped[item["family"]].append(item["id"])

    batches = []
    for family, ids in sorted(grouped.items()):
        batches.append({"family": family, "item_ids": ids[:25]})
    return batches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scope_matrix", type=Path, help="Path to normalized scope matrix JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    matrix = load_json(args.scope_matrix)

    items = []
    for item in matrix.get("items", []):
        route, reason = classify(item)
        next_item = dict(item)
        next_item["production_route"] = route
        next_item["route_reason"] = reason
        items.append(next_item)

    route_counts = Counter(item["production_route"] for item in items)
    result = dict(matrix)
    result["items"] = items
    result["route_counts"] = dict(sorted(route_counts.items()))
    if matrix.get("scope_band") == "Enterprise":
        result["batch_recommendations"] = build_batches(items)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
