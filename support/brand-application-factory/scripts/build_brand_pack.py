#!/usr/bin/env python3
"""Build a final brand-pack JSON from foundation and application outputs."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def build_application_recipes(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item.get("family", "document")].append(item)

    recipes = []
    for family, family_items in sorted(grouped.items()):
        routes = [item.get("production_route", "pending") for item in family_items]
        export_formats = sorted(
            {fmt for item in family_items for fmt in item.get("export_formats", [])}
        )
        recipes.append(
            {
                "family": family,
                "default_route": max(set(routes), key=routes.count),
                "template_fit": max(
                    set(item.get("template_fit", "medium") for item in family_items),
                    key=lambda value: ["low", "medium", "high"].index(value),
                ),
                "sample_items": [item["id"] for item in family_items[:5]],
                "export_formats": export_formats,
                "notes": "Derived from normalized application outputs",
            }
        )
    return recipes


def derive_asset_manifest(foundation: dict[str, Any], application_data: dict[str, Any]) -> dict[str, Any]:
    if "asset_manifest" in foundation:
        return foundation["asset_manifest"]

    return {
        "status": "draft",
        "source_of_truth": foundation.get("source_of_truth", "to-be-assigned"),
        "expected_export_groups": sorted(
            {
                fmt
                for item in application_data.get("items", [])
                for fmt in item.get("export_formats", [])
            }
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("foundation", type=Path, help="Path to foundation brand JSON")
    parser.add_argument("applications", type=Path, help="Path to application output JSON")
    parser.add_argument(
        "--asset-manifest",
        type=Path,
        default=None,
        help="Optional path to a separate asset manifest JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    foundation = load_json(args.foundation)
    applications = load_json(args.applications)

    asset_manifest = (
        load_json(args.asset_manifest)
        if args.asset_manifest is not None
        else derive_asset_manifest(foundation, applications)
    )

    brand_pack = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "brand": foundation.get("brand", {}),
        "brand_guideline": foundation.get("brand_guideline", {}),
        "brand_tokens": foundation.get("brand_tokens", {}),
        "logo_system": foundation.get("logo_system", {}),
        "style_playbook_selection": foundation.get("style_playbook_selection", {}),
        "reference_style_distillation": foundation.get("reference_style_distillation"),
        "design_md_documents": {
            **foundation.get("design_md_documents", {}),
            **applications.get("design_md_documents", {}),
        },
        "application_recipes": applications.get("application_recipes")
        or build_application_recipes(applications.get("items", [])),
        "asset_manifest": asset_manifest,
        "application_scope": {
            "scope_band": applications.get("scope_band"),
            "item_count": applications.get("item_count"),
            "route_counts": applications.get("route_counts", {}),
        },
        "metadata": {
            "source_files": {
                "foundation": str(args.foundation),
                "applications": str(args.applications),
            }
        },
    }
    print(json.dumps(brand_pack, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
