#!/usr/bin/env python3
"""Generate a brand-specific wrapper skill from a brand-pack."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def slugify(value: str) -> str:
    parts = re.findall(r"[\w-]+", value.lower())
    return "-".join(parts) or "brand"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_bundle_reference(pack: dict[str, Any]) -> str:
    lines = ["# Application Bundles", ""]
    for recipe in pack.get("application_recipes", []):
        lines.append(f"## {recipe['family']}")
        lines.append(f"- default route: {recipe['default_route']}")
        lines.append(f"- template fit: {recipe['template_fit']}")
        lines.append(f"- sample items: {', '.join(recipe['sample_items'])}")
        lines.append(f"- export formats: {', '.join(recipe['export_formats'])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_optional_text(path: Path, value: str | None) -> None:
    if value:
        write_text(path, value if value.endswith("\n") else value + "\n")


def write_design_docs(skill_dir: Path, pack: dict[str, Any]) -> None:
    design_docs = pack.get("design_md_documents", {}) or {}
    write_optional_text(
        skill_dir / "references" / "reference-style-distillation.md",
        pack.get("reference_style_distillation"),
    )
    write_optional_text(
        skill_dir / "references" / "brand-foundation-design.md",
        design_docs.get("brand_foundation_design"),
    )
    write_optional_text(
        skill_dir / "references" / "ui-ux-design.md",
        design_docs.get("ui_ux_design"),
    )
    write_optional_text(
        skill_dir / "references" / "application-design.md",
        design_docs.get("application_design"),
    )
    write_optional_text(
        skill_dir / "references" / "design-index.md",
        design_docs.get("design_index"),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brand_pack", type=Path, help="Path to a final brand-pack JSON file")
    parser.add_argument("output_dir", type=Path, help="Directory to create the wrapper skill in")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    template_path = root / "assets" / "wrapper_skill_template.md"
    brand_guidelines_template_path = root / "assets" / "brand_guidelines_skill_template.md"

    pack = load_json(args.brand_pack)
    brand_name = pack.get("brand", {}).get("name", "Brand")
    brand_slug = pack.get("brand", {}).get("slug") or slugify(brand_name)
    applications_skill_name = f"{brand_slug}-brand-applications"
    applications_skill_dir = args.output_dir / applications_skill_name
    guidelines_skill_name = f"{brand_slug}-brand-guidelines"
    guidelines_skill_dir = args.output_dir / guidelines_skill_name

    template = template_path.read_text(encoding="utf-8")
    applications_skill_md = template.format(
        skill_name=applications_skill_name,
        brand_name=brand_name,
        brand_slug=brand_slug,
        pack_rel_path="assets/brand_pack.json",
        bundle_ref_rel_path="references/application-bundles.md",
    )
    guidelines_template = brand_guidelines_template_path.read_text(encoding="utf-8")
    guidelines_skill_md = guidelines_template.format(
        skill_name=guidelines_skill_name,
        brand_name=brand_name,
        brand_slug=brand_slug,
        pack_rel_path="assets/brand_pack.json",
    )

    write_text(applications_skill_dir / "SKILL.md", applications_skill_md)
    write_json(applications_skill_dir / "assets" / "brand_pack.json", pack)
    write_text(
        applications_skill_dir / "references" / "application-bundles.md",
        build_bundle_reference(pack),
    )
    write_design_docs(applications_skill_dir, pack)

    write_text(guidelines_skill_dir / "SKILL.md", guidelines_skill_md)
    write_json(guidelines_skill_dir / "assets" / "brand_pack.json", pack)
    write_design_docs(guidelines_skill_dir, pack)

    print(
        json.dumps(
            {
                "application_skill_name": applications_skill_name,
                "guidelines_skill_name": guidelines_skill_name,
                "output_dir": str(args.output_dir),
                "brand_name": brand_name,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
