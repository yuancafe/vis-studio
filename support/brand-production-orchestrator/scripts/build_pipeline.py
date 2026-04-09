#!/usr/bin/env python3
"""Build order-driven production pipeline tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _orchestration_utils import (
    load_json,
    load_route_rules,
    slugify,
)


DEFAULT_MINIMUM_DELIVERABLE = "logo_core_package"
DEFAULT_MANUAL_FORMATS = ["pdf", "ai"]
SUPPORTED_MANUAL_FORMATS = {"pdf", "ai", "pptx"}

PACKAGE_ORDER = [
    "logo_core_package",
    "vector_extension_package",
    "viis_manual_package",
    "brand_prompt_pack",
    "application_assets_package",
]

FULL_SUITE_BASE_CHAIN = [
    "logo_core_package",
    "viis_manual_package",
    "brand_prompt_pack",
]

PACKAGE_DEPENDENCIES = {
    "logo_core_package": [],
    "vector_extension_package": ["logo_core_package"],
    "viis_manual_package": ["logo_core_package"],
    "brand_prompt_pack": ["viis_manual_package"],
    "application_assets_package": ["brand_prompt_pack"],
}

PACKAGE_TO_ROUTE = {
    "logo_core_package": {
        "intent": "logo_refinement",
        "family": "logo-core",
        "artifact_outputs": ["logo", "vector"],
    },
    "vector_extension_package": {
        "intent": "open_source_vector_refinement",
        "family": "vector-extension",
        "artifact_outputs": ["vector"],
    },
    "viis_manual_package": {
        "intent": "vis_handbook",
        "family": "viis-manual",
        "artifact_outputs": ["manual", "layout"],
    },
    "brand_prompt_pack": {
        "intent": "social_template_pack",
        "family": "prompt-pack",
        "artifact_outputs": ["prompt_pack"],
    },
    "application_assets_package": {
        "intent": "social_template_pack",
        "family": "application-assets",
        "artifact_outputs": ["template", "mockup"],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goal", help="Production goal text")
    parser.add_argument(
        "--intent",
        default=None,
        help="Optional explicit intent (kept for backward compatibility).",
    )
    parser.add_argument(
        "--production-scope",
        default="single",
        choices=["single", "full_suite"],
        help="Pipeline scope.",
    )
    parser.add_argument(
        "--brand-pack",
        type=Path,
        default=None,
        help="Brand pack path.",
    )
    parser.add_argument(
        "--order-file",
        type=Path,
        default=None,
        help="Order form path. If absent, default minimum order is used.",
    )
    parser.add_argument(
        "--resume-from-run-dir",
        type=Path,
        default=None,
        help="Optional previous production run directory.",
    )
    parser.add_argument(
        "--preferred-tool",
        default=None,
        help="Optional preferred tool used in route inference (kept for compatibility).",
    )
    parser.add_argument(
        "--route-rules",
        type=Path,
        default=None,
        help="Optional route-rules JSON path (default: assets/route-rules.json).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path.",
    )
    return parser.parse_args()


def _dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def _normalize_order_form(raw: dict[str, Any], resume_override: Path | None = None) -> dict[str, Any]:
    selected = raw.get("selected_deliverables", [])
    if not isinstance(selected, list):
        selected = []
    selected = [str(item).strip() for item in selected if str(item).strip() in PACKAGE_TO_ROUTE]
    if not selected:
        selected = [DEFAULT_MINIMUM_DELIVERABLE]

    manual_formats = raw.get("manual_formats", [])
    if not isinstance(manual_formats, list):
        manual_formats = []
    normalized_formats = []
    for item in manual_formats:
        fmt = str(item).strip().lower()
        if fmt in SUPPORTED_MANUAL_FORMATS:
            normalized_formats.append(fmt)
    if not normalized_formats:
        normalized_formats = DEFAULT_MANUAL_FORMATS.copy()

    auto_assets = bool(raw.get("auto_generate_application_assets", False))

    resume_from = ""
    if resume_override is not None:
        resume_from = str(resume_override)
    elif isinstance(raw.get("resume_from_run_dir"), str):
        resume_from = raw.get("resume_from_run_dir", "").strip()

    constraints = raw.get("client_constraints", {})
    if not isinstance(constraints, dict):
        constraints = {}

    return {
        "selected_deliverables": selected,
        "manual_formats": _dedupe_keep_order(normalized_formats),
        "auto_generate_application_assets": auto_assets,
        "resume_from_run_dir": resume_from,
        "client_constraints": constraints,
    }


def _load_order_form(order_file: Path | None, resume_override: Path | None) -> dict[str, Any]:
    default_order = {
        "selected_deliverables": [DEFAULT_MINIMUM_DELIVERABLE],
        "manual_formats": DEFAULT_MANUAL_FORMATS.copy(),
        "auto_generate_application_assets": False,
        "resume_from_run_dir": str(resume_override) if resume_override else "",
        "client_constraints": {},
    }
    if order_file is None or not order_file.exists():
        return default_order

    loaded = load_json(order_file)
    if not isinstance(loaded, dict):
        return default_order
    return _normalize_order_form(loaded, resume_override=resume_override)


def _load_resume_registry(resume_from_run_dir: str) -> dict[str, Any]:
    if not resume_from_run_dir:
        return {}
    run_dir = Path(resume_from_run_dir)
    registry = run_dir / "ARTIFACT_REGISTRY.json"
    if not registry.exists():
        return {}
    try:
        data = load_json(registry)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _extract_completed_packages(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not registry:
        return {}

    packages = registry.get("packages")
    if isinstance(packages, dict):
        completed: dict[str, dict[str, Any]] = {}
        for package, meta in packages.items():
            if not isinstance(meta, dict):
                continue
            status = str(meta.get("status", "")).lower()
            if status in {"success", "completed", "skipped"}:
                completed[package] = meta
        if completed:
            return completed

    completed = {}
    tasks = registry.get("tasks", {})
    if isinstance(tasks, dict):
        for task_id, task in tasks.items():
            if not isinstance(task, dict):
                continue
            package = str(task.get("package", "")).strip()
            status = str(task.get("status", "")).lower()
            if package and status in {"success", "completed", "skipped"}:
                completed[package] = {
                    "task_id": task_id,
                    "status": status,
                    "files": task.get("output_artifacts", []),
                }
    return completed


def _file_spec(name: str, artifact_type: str, editable: bool = True) -> dict[str, Any]:
    suffix = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return {
        "name": name,
        "artifact_type": artifact_type,
        "format": suffix,
        "editable": editable,
    }


def _build_delivery_contract(package: str, manual_formats: list[str]) -> dict[str, Any]:
    if package == "logo_core_package":
        files = [
            _file_spec("logo_primary.svg", "logo"),
            _file_spec("logo_secondary.svg", "logo"),
            _file_spec("logo_lockups.svg", "logo"),
            _file_spec("logo_usage_rules.md", "spec"),
        ]
    elif package == "vector_extension_package":
        files = [
            _file_spec("brand_graphics.svg", "vector"),
            _file_spec("pattern_library.svg", "vector"),
        ]
    elif package == "viis_manual_package":
        files = [_file_spec("VIIS_MASTER.md", "manual")]
        for fmt in manual_formats:
            files.append(_file_spec(f"VIIS_BASIC_SPEC.{fmt}", "manual"))
            files.append(_file_spec(f"VIIS_APPLICATION_SPEC.{fmt}", "manual"))
    elif package == "brand_prompt_pack":
        files = [
            _file_spec("PROMPTS_Doubao.md", "prompt_pack"),
            _file_spec("PROMPTS_Kling.md", "prompt_pack"),
            _file_spec("PROMPTS_Canva.md", "prompt_pack"),
            _file_spec("PROMPT_VARIABLES.json", "prompt_pack"),
        ]
    elif package == "application_assets_package":
        files = [
            _file_spec("canva_template_manifest.json", "template"),
            _file_spec("poster_sample_1080x1350.svg", "mockup"),
        ]
    else:
        files = [_file_spec(f"{package}.md", "artifact")]

    return {
        "package": package,
        "required_files": files,
        "acceptance": [
            "all-required-files-exist",
            "files-are-non-empty",
            "registry-contains-file-metadata",
        ],
    }


def _resolve_requested_packages(order_context: dict[str, Any], production_scope: str) -> list[str]:
    requested = list(order_context.get("selected_deliverables", []))
    if bool(order_context.get("auto_generate_application_assets", False)):
        requested.append("application_assets_package")
    if production_scope == "full_suite":
        requested = FULL_SUITE_BASE_CHAIN + requested

    requested = [item for item in requested if item in PACKAGE_TO_ROUTE]
    requested = _dedupe_keep_order(requested)

    # Always pull required upstream dependencies.
    selected: set[str] = set()

    def add_with_deps(package: str) -> None:
        if package in selected:
            return
        for dep in PACKAGE_DEPENDENCIES.get(package, []):
            add_with_deps(dep)
        selected.add(package)

    for package in requested:
        add_with_deps(package)

    return [item for item in PACKAGE_ORDER if item in selected]


def _build_task(
    package: str,
    route_data: dict[str, Any],
    index: int,
    order_context: dict[str, Any],
    completed_packages: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    route_meta = PACKAGE_TO_ROUTE[package]
    family_slug = slugify(route_meta["family"])
    contract = _build_delivery_contract(package, order_context["manual_formats"])
    return {
        "task_id": f"task-{index:02d}-{family_slug}",
        "package": package,
        "intent": route_meta["intent"],
        "route": route_data.get("route", route_meta["intent"]),
        "family": route_meta["family"],
        "critical": bool(route_data.get("critical", False)),
        "executor_candidates": route_data.get("executor_candidates", []),
        "input_artifact_types": route_data.get("input_artifact_types", []),
        "output_artifact_types": route_meta.get("artifact_outputs", route_data.get("output_artifact_types", [])),
        "required_documents": route_data.get("required_documents", []),
        "optional_documents": route_data.get("optional_documents", []),
        "actions": route_data.get("actions", []),
        "deliverables": route_data.get("deliverables", []),
        "delivery_contract": contract,
        "depends_on_packages": PACKAGE_DEPENDENCIES.get(package, []),
        "skip_existing": package in completed_packages,
        "resume_package": completed_packages.get(package, {}),
    }


def build_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    routes = load_route_rules(args.route_rules)
    order_context = _load_order_form(args.order_file, args.resume_from_run_dir)
    resume_registry = _load_resume_registry(order_context.get("resume_from_run_dir", ""))
    completed_packages = _extract_completed_packages(resume_registry)

    packages = _resolve_requested_packages(order_context, args.production_scope)
    tasks: list[dict[str, Any]] = []
    for idx, package in enumerate(packages, 1):
        route_meta = PACKAGE_TO_ROUTE[package]
        route_intent = route_meta["intent"]
        if route_intent not in routes:
            raise SystemExit(f"Route rules missing intent for package {package}: {route_intent}")
        tasks.append(
            _build_task(
                package=package,
                route_data=routes[route_intent],
                index=idx,
                order_context=order_context,
                completed_packages=completed_packages,
            )
        )

    task_id_by_package = {task["package"]: task["task_id"] for task in tasks}
    for task in tasks:
        deps = []
        for dep_package in task.get("depends_on_packages", []):
            dep_task_id = task_id_by_package.get(dep_package)
            if dep_task_id:
                deps.append(dep_task_id)
        task["depends_on"] = deps
        task.pop("depends_on_packages", None)

    return {
        "goal": args.goal,
        "production_scope": args.production_scope,
        "requested_intent": args.intent or "",
        "task_count": len(tasks),
        "order_context": order_context,
        "resume_from_run_dir": order_context.get("resume_from_run_dir", ""),
        "tasks": tasks,
    }


def main() -> None:
    args = parse_args()
    result = build_pipeline(args)
    serialized = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
