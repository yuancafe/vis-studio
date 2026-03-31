#!/usr/bin/env python3
"""Normalize brand application requests into a scope matrix."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


FAMILY_RULES = [
    ("social", ["social", "instagram", "linkedin", "xiaohongshu", "story", "post"]),
    ("deck", ["deck", "slide", "presentation", "pitch"]),
    ("stationery", ["business card", "card", "envelope", "notebook", "paper"]),
    ("document", ["proposal", "one-pager", "pdf", "doc", "letterhead"]),
    ("packaging", ["packaging", "box", "label", "bag", "cup", "wrap"]),
    ("merch", ["tote", "shirt", "merch", "uniform", "sticker"]),
    ("signage", ["sign", "signage", "storefront", "window"]),
    ("wayfinding", ["wayfinding", "navigation", "directional"]),
    ("environment", ["booth", "event", "space", "exhibition"]),
    ("web", ["website", "web", "landing", "homepage", "app"]),
    ("banner", ["banner", "hero", "cover", "header", "ad", "billboard"]),
]

EXPORT_MAP = {
    "social": ["png", "jpg"],
    "banner": ["png", "jpg", "webp"],
    "web": ["png", "svg"],
    "deck": ["png", "pptx"],
    "document": ["pdf", "png"],
    "stationery": ["pdf", "png"],
    "packaging": ["pdf", "png"],
    "merch": ["png", "pdf"],
    "signage": ["pdf", "png"],
    "wayfinding": ["pdf"],
    "environment": ["pdf", "png"],
}

TEMPLATE_FIT = {
    "social": "high",
    "banner": "high",
    "web": "high",
    "deck": "high",
    "document": "medium",
    "stationery": "medium",
    "packaging": "low",
    "merch": "medium",
    "signage": "low",
    "wayfinding": "low",
    "environment": "low",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def slugify(value: str) -> str:
    parts = re.findall(r"[\w-]+", value.lower())
    return "-".join(parts) or "item"


def infer_family(name: str) -> str:
    lowered = name.lower()
    tokens = set(re.findall(r"[\w-]+", lowered))
    for family, keywords in FAMILY_RULES:
        for keyword in keywords:
            keyword_tokens = set(re.findall(r"[\w-]+", keyword.lower()))
            if keyword_tokens and keyword_tokens <= tokens:
                return family
            if " " in keyword and keyword.lower() in lowered:
                return family
        if family == "banner" and any(keyword in tokens for keyword in {"banner", "hero", "header"}):
            return family
    return "document"


def infer_effort_band(family: str, variant_count: int) -> str:
    if family in {"packaging", "signage", "wayfinding", "environment"}:
        return "L" if variant_count <= 2 else "XL"
    if family in {"stationery", "merch"}:
        return "M" if variant_count <= 3 else "L"
    return "S" if variant_count <= 3 else "M"


def scope_band(count: int) -> str:
    if count <= 10:
        return "Core"
    if count <= 30:
        return "Growth"
    if count <= 100:
        return "System"
    return "Enterprise"


def normalize_item(item: Any) -> dict[str, Any]:
    if isinstance(item, str):
        raw = {"name": item}
    else:
        raw = dict(item)

    name = raw.get("name") or raw.get("title") or raw.get("purpose") or "Untitled item"
    family = raw.get("family") or infer_family(name)
    variants = int(raw.get("variant_count", 1))
    sizes = raw.get("sizes", [])
    if isinstance(sizes, str):
        sizes = [sizes]

    return {
        "id": raw.get("id") or slugify(name),
        "name": name,
        "family": family,
        "purpose": raw.get("purpose") or name,
        "priority": raw.get("priority") or "high",
        "sizes": sizes,
        "variant_count": variants,
        "content_source": raw.get("content_source") or "brand_pack",
        "template_fit": raw.get("template_fit") or TEMPLATE_FIT[family],
        "production_route": raw.get("production_route") or "pending_route_classification",
        "effort_band": raw.get("effort_band") or infer_effort_band(family, variants),
        "export_formats": raw.get("export_formats") or EXPORT_MAP[family],
        "owner": raw.get("owner") or "design",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path, help="Path to application request JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    request = load_json(args.request)
    starter_bundles = load_json(root / "assets" / "starter_bundles.json")

    raw_items: list[Any] = list(request.get("items", []))
    for bundle_id in request.get("bundle_ids", []):
        raw_items.extend(starter_bundles.get(bundle_id, []))

    items = [normalize_item(item) for item in raw_items]
    families = Counter(item["family"] for item in items)
    result = {
        "brand": request.get("brand", {}),
        "item_count": len(items),
        "scope_band": scope_band(len(items)),
        "bundles_used": request.get("bundle_ids", []),
        "family_summary": dict(sorted(families.items())),
        "items": items,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
