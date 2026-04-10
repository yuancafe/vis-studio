#!/usr/bin/env python3
"""Shared helpers for VIS STUDIO production orchestration scripts."""

from __future__ import annotations

import json
import shutil
import subprocess
import re
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROUTE_RULES = ROOT / "assets" / "route-rules.json"
DEFAULT_PROMPT_TEMPLATE_DIR = ROOT / "assets" / "tool-prompt-templates"
DEFAULT_CODEX_CONFIG = Path.home() / ".codex" / "config.toml"
DEFAULT_GLOBAL_MCP_CONFIG = Path.home() / ".config" / "mcp" / "config.json"

EXECUTOR_SERVER_ALIASES = {
    "figma_mcp": ["figma", "figma-mcp", "figma_mcp"],
    "illustrator": ["illustrator", "adobe-illustrator"],
    "adobe_illustrator": ["illustrator", "adobe-illustrator"],
    "photoshop": ["photoshop", "adobe-photoshop"],
    "adobe_photoshop": ["photoshop", "adobe-photoshop"],
    "inkscape-mcp": ["inkscape-mcp", "inkscape", "inkscape_mcp"],
    "inkscape": ["inkscape-mcp", "inkscape", "inkscape_mcp"],
    "stitch": ["stitch"],
    "pencil": ["pencil"],
    "canva": ["canva"],
}

EXECUTOR_PLUGIN_FALLBACKS = {
    "figma_connector": "figma@openai-curated",
    "canva": "canva@openai-curated",
}

EXECUTOR_APP_ALIASES = {
    "figma_mcp": ["figma"],
    "figma_connector": ["figma"],
    "illustrator": ["illustrator"],
    "adobe_illustrator": ["illustrator"],
    "inkscape": ["inkscape"],
    "inkscape-mcp": ["inkscape"],
    "photoshop": ["photoshop"],
    "adobe_photoshop": ["photoshop"],
    "canva": [],
    "stitch": [],
    "pencil": [],
}

EXECUTOR_CLI_ALIASES = {
    "pencil": ["pencil"],
}

DESIGN_APP_CATALOG = {
    "figma": [
        "/Applications/Figma.app",
    ],
    "illustrator": [
        "/Applications/Adobe Illustrator 2026/Adobe Illustrator.app",
        "/Applications/Adobe Illustrator 2025/Adobe Illustrator.app",
        "/Applications/Adobe Illustrator.app",
    ],
    "inkscape": [
        "/Applications/Inkscape.app",
    ],
    "photoshop": [
        "/Applications/Adobe Photoshop 2026/Adobe Photoshop 2026.app",
        "/Applications/Adobe Photoshop 2025/Adobe Photoshop 2025.app",
        "/Applications/Adobe Photoshop.app",
    ],
}

DESIGN_CLI_CATALOG = {
    "pencil": [
        {
            "cli_id": "open-pencil",
            "probe_command": ["open-pencil", "--help"],
            "execute_command": ["open-pencil", "eval"],
        },
        {
            "cli_id": "open-pencil-bun",
            "probe_command": ["bun", "open-pencil", "--help"],
            "execute_command": ["bun", "open-pencil", "eval"],
        },
    ],
}

EXECUTOR_CAPABILITIES = {
    "figma_mcp": ["layout", "ui", "template"],
    "figma_connector": ["layout", "ui", "template"],
    "illustrator": ["vector", "logo"],
    "adobe_illustrator": ["vector", "logo"],
    "photoshop": ["mockup", "layout"],
    "adobe_photoshop": ["mockup", "layout"],
    "inkscape": ["vector", "logo"],
    "inkscape-mcp": ["vector", "logo"],
    "stitch": ["ui", "layout", "template"],
    "pencil": ["ui", "layout"],
    "canva": ["template", "layout"],
}

DEFAULT_EXECUTOR_CANDIDATES = {
    "vis_handbook": ["figma_mcp", "figma_connector", "stitch"],
    "logo_refinement": ["illustrator", "inkscape-mcp"],
    "visual_asset_system": ["figma_mcp", "illustrator", "canva"],
    "packaging_mockup": ["photoshop", "canva"],
    "social_template_pack": ["canva", "figma_connector"],
    "landing_page_visual_system": ["stitch", "figma_connector", "pencil"],
    "ui_screen_system": ["pencil", "stitch", "figma_connector"],
    "open_source_vector_refinement": ["inkscape-mcp", "illustrator"],
}

DEFAULT_ROUTE_CRITICAL = {
    "vis_handbook": True,
    "logo_refinement": True,
    "visual_asset_system": False,
    "packaging_mockup": False,
    "social_template_pack": False,
    "landing_page_visual_system": False,
    "ui_screen_system": False,
    "open_source_vector_refinement": False,
}

DEFAULT_FAMILY = {
    "vis_handbook": "handbook",
    "logo_refinement": "logo",
    "visual_asset_system": "visual-assets",
    "packaging_mockup": "packaging",
    "social_template_pack": "social",
    "landing_page_visual_system": "web",
    "ui_screen_system": "ui",
    "open_source_vector_refinement": "vector",
}

DEFAULT_INPUT_ARTIFACT_TYPES = {
    "vis_handbook": ["brand_pack", "logo", "vector", "layout"],
    "logo_refinement": ["brand_pack"],
    "visual_asset_system": ["brand_pack", "logo", "vector"],
    "packaging_mockup": ["brand_pack", "vector", "layout"],
    "social_template_pack": ["brand_pack", "layout", "template"],
    "landing_page_visual_system": ["brand_pack", "layout", "ui"],
    "ui_screen_system": ["brand_pack", "ui", "layout"],
    "open_source_vector_refinement": ["brand_pack", "vector"],
}

DEFAULT_OUTPUT_ARTIFACT_TYPES = {
    "vis_handbook": ["handbook", "layout"],
    "logo_refinement": ["logo", "vector"],
    "visual_asset_system": ["asset_system", "vector"],
    "packaging_mockup": ["mockup", "layout"],
    "social_template_pack": ["template", "layout"],
    "landing_page_visual_system": ["web", "layout", "ui"],
    "ui_screen_system": ["ui", "layout"],
    "open_source_vector_refinement": ["vector"],
}

TOOL_DISPLAY_NAMES = {
    "figma_mcp": "Figma MCP",
    "adobe_illustrator": "Adobe Illustrator",
    "adobe_photoshop": "Adobe Photoshop",
    "canva": "Canva",
    "stitch": "Stitch",
    "pencil": "Pencil",
    "inkscape": "Inkscape",
    "figma_connector": "Figma Connector",
    "illustrator": "Adobe Illustrator",
    "photoshop": "Adobe Photoshop",
    "inkscape-mcp": "Inkscape MCP",
}

INTENT_TO_TEMPLATE = {
    "vis_handbook": "figma_vis_handbook.md",
    "logo_refinement": "illustrator_logo_refinement.md",
    "visual_asset_system": "figma_visual_asset_system.md",
    "packaging_mockup": "photoshop_mockup.md",
    "social_template_pack": "canva_template_pack.md",
    "landing_page_visual_system": "stitch_ui_system.md",
    "ui_screen_system": "pencil_ui_system.md",
    "open_source_vector_refinement": "inkscape_vector_refinement.md",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_route_rules(route_rules_path: Path | None = None) -> dict[str, Any]:
    path = route_rules_path or DEFAULT_ROUTE_RULES
    data = load_json(path)
    routes = data.get("routes")
    if not isinstance(routes, dict) or not routes:
        raise ValueError(f"Invalid route rules file: {path}")
    normalized: dict[str, Any] = {}
    for intent, route_data in routes.items():
        item = dict(route_data)
        item["secondary_tools"] = item.get("secondary_tools", [])
        item["optional_documents"] = item.get("optional_documents", [])
        item["actions"] = item.get("actions", [])
        item["deliverables"] = item.get("deliverables", [])
        item["executor_candidates"] = item.get(
            "executor_candidates", DEFAULT_EXECUTOR_CANDIDATES.get(intent, [])
        )
        item["critical"] = bool(item.get("critical", DEFAULT_ROUTE_CRITICAL.get(intent, False)))
        item["default_family"] = item.get("default_family", DEFAULT_FAMILY.get(intent, "deliverable"))
        item["input_artifact_types"] = item.get(
            "input_artifact_types", DEFAULT_INPUT_ARTIFACT_TYPES.get(intent, [])
        )
        item["output_artifact_types"] = item.get(
            "output_artifact_types", DEFAULT_OUTPUT_ARTIFACT_TYPES.get(intent, [])
        )
        normalized[intent] = item
    return normalized


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def infer_intent(
    goal: str,
    routes: dict[str, Any],
    preferred_tool: str | None = None,
) -> tuple[str, str]:
    normalized_goal = normalize_text(goal)
    best_intent = "vis_handbook"
    best_score = -1
    best_reason = "Fallback route selected because no strong keyword match was found."

    if preferred_tool:
        normalized_tool = preferred_tool.strip().lower()
        if normalized_tool in {"inkscape", "open-source", "open source"}:
            return (
                "open_source_vector_refinement",
                "Route selected from explicit open-source vector preference.",
            )
        for intent, route_data in routes.items():
            if route_data.get("primary_tool", "").lower() == normalized_tool:
                return intent, f"Route selected from explicit tool preference: {preferred_tool}."

    for intent, route_data in routes.items():
        keywords = route_data.get("keywords", [])
        score = 0
        matched: list[str] = []
        for kw in keywords:
            keyword = normalize_text(str(kw))
            if keyword and keyword in normalized_goal:
                score += max(2, len(keyword.split()))
                matched.append(keyword)
        if score > best_score:
            best_score = score
            best_intent = intent
            if matched:
                best_reason = (
                    f"Route selected from keyword match: {', '.join(matched[:3])}."
                )
            else:
                best_reason = "Fallback route selected because no strong keyword match was found."

    return best_intent, best_reason


def to_tool_display_name(tool_id: str) -> str:
    return TOOL_DISPLAY_NAMES.get(tool_id, tool_id)


def slugify(value: str) -> str:
    parts = re.findall(r"[\w-]+", value.lower())
    return "-".join(parts) or "artifact"


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_codex_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or DEFAULT_CODEX_CONFIG
    if not config_path.exists():
        return {}
    with config_path.open("rb") as fh:
        return tomllib.load(fh)


def load_global_mcp_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or DEFAULT_GLOBAL_MCP_CONFIG
    if not config_path.exists():
        return {}
    return load_json(config_path)


def _command_health(command: str | None) -> tuple[bool, str]:
    if not command:
        return False, "missing-command"
    if command.startswith("/") or command.startswith("./"):
        cmd_path = Path(command).expanduser()
        if cmd_path.exists():
            return True, "command-found"
        return False, "command-not-found"
    if shutil.which(command):
        return True, "command-found"
    return False, "command-not-found"


def _guess_capabilities_from_name(name: str) -> list[str]:
    normalized = name.lower()
    caps: list[str] = []
    if any(word in normalized for word in ("illustrator", "inkscape", "vector")):
        caps.extend(["vector", "logo"])
    if "photoshop" in normalized:
        caps.extend(["mockup", "layout"])
    if any(word in normalized for word in ("figma", "stitch", "pencil")):
        caps.extend(["ui", "layout"])
    if "canva" in normalized:
        caps.extend(["template", "layout"])
    deduped = list(dict.fromkeys(caps))
    return deduped


def _is_design_service(name: str, capabilities: list[str]) -> bool:
    if capabilities:
        return True
    normalized = name.lower()
    keywords = (
        "figma",
        "illustrator",
        "photoshop",
        "inkscape",
        "stitch",
        "canva",
        "pencil",
    )
    return any(keyword in normalized for keyword in keywords)


def _extract_plugins(codex_config: dict[str, Any]) -> dict[str, bool]:
    plugins = codex_config.get("plugins", {})
    result: dict[str, bool] = {}
    for name, value in plugins.items():
        enabled = bool(value.get("enabled")) if isinstance(value, dict) else bool(value)
        result[str(name)] = enabled
    return result


def _plugin_enabled(plugin_flags: dict[str, bool], plugin_id: str) -> bool:
    if plugin_flags.get(plugin_id):
        return True
    prefix = f"{plugin_id.split('@')[0]}@"
    for name, enabled in plugin_flags.items():
        if name.startswith(prefix) and enabled:
            return True
    return False


def detect_installed_design_apps() -> dict[str, dict[str, Any]]:
    apps: dict[str, dict[str, Any]] = {}
    for app_id, paths in DESIGN_APP_CATALOG.items():
        resolved = ""
        for path in paths:
            if Path(path).exists():
                resolved = path
                break
        apps[app_id] = {
            "app_id": app_id,
            "installed": bool(resolved),
            "path": resolved,
        }
    return apps


def _probe_cli_command(command: list[str], timeout: int = 20) -> tuple[bool, int, str, str]:
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError:
        return False, 127, "", "command-not-found"
    except subprocess.TimeoutExpired:
        return False, 124, "", "probe-timeout"
    except Exception as exc:  # defensive: probe should never crash discovery
        return False, 1, "", f"probe-error:{exc}"
    return proc.returncode == 0, proc.returncode, proc.stdout or "", proc.stderr or ""


def detect_installed_design_clis() -> dict[str, dict[str, Any]]:
    installed: dict[str, dict[str, Any]] = {}
    for cli_family, probes in DESIGN_CLI_CATALOG.items():
        hits: list[dict[str, Any]] = []
        for probe in probes:
            probe_command = [str(item) for item in probe.get("probe_command", []) if str(item).strip()]
            if not probe_command:
                continue
            ok, return_code, stdout, stderr = _probe_cli_command(probe_command)
            if not ok:
                continue
            binary_name = probe_command[0]
            resolved_path = shutil.which(binary_name) or ""
            hits.append(
                {
                    "cli_id": str(probe.get("cli_id", cli_family)),
                    "probe_command": probe_command,
                    "execute_command": [str(item) for item in probe.get("execute_command", []) if str(item).strip()],
                    "path": resolved_path,
                    "return_code": return_code,
                    "stdout_preview": (stdout or "")[:240],
                    "stderr_preview": (stderr or "")[:240],
                }
            )
        installed[cli_family] = {
            "cli_family": cli_family,
            "available": bool(hits),
            "hits": hits,
        }
    return installed


def _run_mcporter_list() -> dict[str, Any]:
    if not shutil.which("mcporter"):
        return {
            "available": False,
            "reason": "mcporter-not-installed",
            "return_code": 127,
            "stdout": "",
            "stderr": "mcporter not found",
            "servers": [],
        }

    proc = subprocess.run(
        ["mcporter", "list", "--output", "json"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    servers: list[str] = []
    reason = "ok" if proc.returncode == 0 else "mcporter-list-failed"
    if proc.returncode == 0:
        try:
            parsed = json.loads(proc.stdout or "{}")
            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict):
                        servers.append(str(item.get("name") or item.get("server_id") or ""))
                    elif isinstance(item, str):
                        servers.append(item)
            elif isinstance(parsed, dict):
                if isinstance(parsed.get("servers"), list):
                    for item in parsed["servers"]:
                        if isinstance(item, dict):
                            servers.append(str(item.get("name") or item.get("server_id") or ""))
                        elif isinstance(item, str):
                            servers.append(item)
                elif parsed:
                    for key in parsed:
                        servers.append(str(key))
        except json.JSONDecodeError:
            reason = "mcporter-json-parse-failed"
    return {
        "available": proc.returncode == 0,
        "reason": reason,
        "return_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "servers": [item for item in servers if item],
    }


def discover_design_services(
    route_rules: dict[str, Any],
    codex_config_path: Path | None = None,
    global_mcp_config_path: Path | None = None,
) -> dict[str, Any]:
    codex_config = load_codex_config(codex_config_path)
    global_mcp = load_global_mcp_config(global_mcp_config_path)
    plugin_flags = _extract_plugins(codex_config)
    app_catalog = detect_installed_design_apps()
    cli_catalog = detect_installed_design_clis()
    mcporter_state = _run_mcporter_list()
    swarm_detected = any("swarm" in item.lower() for item in mcporter_state.get("servers", []))

    server_records: dict[str, dict[str, Any]] = {}

    codex_servers = codex_config.get("mcp_servers", {})
    for name, meta in codex_servers.items():
        if not isinstance(meta, dict):
            continue
        command = meta.get("command")
        url = meta.get("url")
        available, health = _command_health(command) if command else (
            bool(url),
            "url-configured" if url else "unknown",
        )
        capabilities = _guess_capabilities_from_name(name)
        if not _is_design_service(name, capabilities):
            continue
        server_records[name] = {
            "server_id": name,
            "source": "codex",
            "command": command or "",
            "url": url or "",
            "available": available,
            "health": health,
            "capabilities": capabilities,
        }

    global_servers = global_mcp.get("mcpServers", {})
    for name, meta in global_servers.items():
        if not isinstance(meta, dict):
            continue
        command = meta.get("command")
        url = meta.get("url")
        available, health = _command_health(command) if command else (
            bool(url),
            "url-configured" if url else "unknown",
        )
        capabilities = _guess_capabilities_from_name(name)
        if not _is_design_service(name, capabilities):
            continue
        key = name
        if key in server_records:
            key = f"{name}@global"
        server_records[key] = {
            "server_id": name,
            "source": "global_mcp",
            "command": command or "",
            "url": url or "",
            "available": available,
            "health": health,
            "capabilities": capabilities,
        }

    def resolve_executor(executor: str) -> dict[str, Any]:
        aliases = EXECUTOR_SERVER_ALIASES.get(executor, [executor])
        alias_set = {alias.lower() for alias in aliases}
        matches = []
        for item in server_records.values():
            server_name = str(item.get("server_id", "")).lower()
            if server_name in alias_set:
                matches.append(item)

        plugin_id = EXECUTOR_PLUGIN_FALLBACKS.get(executor, "")
        plugin_ok = _plugin_enabled(plugin_flags, plugin_id) if plugin_id else False

        app_targets = EXECUTOR_APP_ALIASES.get(executor, [])
        app_hits = [app_catalog[item] for item in app_targets if app_catalog.get(item, {}).get("installed")]
        cli_targets = EXECUTOR_CLI_ALIASES.get(executor, [])
        cli_hits: list[dict[str, Any]] = []
        for cli_target in cli_targets:
            cli_entry = cli_catalog.get(cli_target, {})
            if cli_entry.get("available"):
                for hit in cli_entry.get("hits", []):
                    if isinstance(hit, dict):
                        cli_hits.append(hit)

        direct_available = any(match.get("available") for match in matches)
        swarm_available = bool(swarm_detected and mcporter_state.get("available"))
        app_cli_available = bool(app_hits or cli_hits)
        plugin_available = bool(plugin_ok)

        available = direct_available or swarm_available or app_cli_available or plugin_available
        preferred_gateway = (
            "direct"
            if direct_available
            else "swarm"
            if swarm_available
            else "app-cli"
            if app_cli_available
            else "plugin"
            if plugin_available
            else "unavailable"
        )
        reason = (
            "direct-configured"
            if direct_available
            else "swarm-detected"
            if swarm_available
            else "cli-installed"
            if cli_hits
            else "app-installed"
            if app_cli_available
            else f"plugin-enabled:{plugin_id}"
            if plugin_available
            else "no-available-server"
        )

        return {
            "executor": executor,
            "display_name": to_tool_display_name(executor),
            "available": available,
            "reason": reason,
            "preferred_gateway": preferred_gateway,
            "direct_available": direct_available,
            "swarm_available": swarm_available,
            "app_cli_available": app_cli_available,
            "plugin_available": plugin_available,
            "matched_servers": matches,
            "app_cli_hits": app_hits,
            "cli_hits": cli_hits,
            "capabilities": EXECUTOR_CAPABILITIES.get(executor, _guess_capabilities_from_name(executor)),
        }

    route_executor_matrix: dict[str, Any] = {}
    missing_critical: list[dict[str, Any]] = []
    for intent, route_data in route_rules.items():
        candidates = [resolve_executor(item) for item in route_data.get("executor_candidates", [])]
        selected = next((item for item in candidates if item.get("available")), None)
        route_executor_matrix[intent] = {
            "candidates": candidates,
            "selected_executor": selected.get("executor") if selected else "",
            "selected_reason": selected.get("reason") if selected else "no-candidate-available",
            "selected_gateway": selected.get("preferred_gateway") if selected else "unavailable",
            "critical": bool(route_data.get("critical", False)),
        }
        if route_data.get("critical") and not selected:
            missing_critical.append(
                {
                    "intent": intent,
                    "executor_candidates": route_data.get("executor_candidates", []),
                    "required_capabilities": route_data.get("input_artifact_types", []),
                }
            )

    suggestions = []
    for item in missing_critical:
        first = (item.get("executor_candidates") or ["unknown"])[0]
        snippet = ""
        if first in {"figma_mcp", "figma_connector"}:
            snippet = "[mcp_servers.figma]\ncommand = \"<figma-mcp-command>\"\nargs = [\"<args>\"]"
        elif first in {"illustrator", "adobe_illustrator"}:
            snippet = (
                "[mcp_servers.illustrator]\ncommand = \"<python-or-npx>\"\nargs = "
                "[\"<illustrator-mcp-entry>\"]"
            )
        elif first in {"inkscape-mcp", "inkscape"}:
            snippet = "[mcp_servers.inkscape-mcp]\ncommand = \"<inkscape-mcp-binary>\""
        elif first in {"photoshop", "adobe_photoshop"}:
            snippet = "[mcp_servers.photoshop]\ncommand = \"npx\"\nargs = [\"-y\", \"@alisaitteke/photoshop-mcp\"]"
        elif first == "stitch":
            snippet = "[mcp_servers.stitch]\nurl = \"https://stitch.googleapis.com/mcp\""
        elif first == "canva":
            snippet = "Enable Canva connector/plugin in Codex plugins."
        elif first == "pencil":
            snippet = (
                "Install Open Pencil CLI and ensure `open-pencil` is available in PATH.\n"
                "Example:\n"
                "git clone git@github.com:open-pencil/open-pencil.git\n"
                "cd open-pencil && <install steps> && open-pencil --help"
            )
        suggestions.append(
            {
                "intent": item["intent"],
                "recommended_executor": first,
                "suggested_config": snippet,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "codex_config": str(codex_config_path or DEFAULT_CODEX_CONFIG),
            "global_mcp_config": str(global_mcp_config_path or DEFAULT_GLOBAL_MCP_CONFIG),
        },
        "gateway_environment": {
            "swarm_detected": swarm_detected,
            "mcporter_available": bool(mcporter_state.get("available")),
            "mcporter_reason": mcporter_state.get("reason", ""),
            "mcporter_servers": mcporter_state.get("servers", []),
        },
        "plugin_flags": plugin_flags,
        "installed_apps": app_catalog,
        "installed_clis": cli_catalog,
        "design_servers": sorted(server_records.values(), key=lambda x: (x["source"], x["server_id"])),
        "route_executor_matrix": route_executor_matrix,
        "missing_critical": missing_critical,
        "suggestions": suggestions,
    }


def choose_executor_for_intent(intent: str, discovery_report: dict[str, Any]) -> tuple[str, list[dict[str, Any]], str]:
    matrix = discovery_report.get("route_executor_matrix", {}).get(intent, {})
    candidates = matrix.get("candidates", [])
    selected = matrix.get("selected_executor", "")
    reason = matrix.get("selected_reason", "")
    return selected, candidates, reason


def run_cmd(cmd: list[str], timeout: int = 30) -> tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def map_executor_to_server(executor: str, discovery_report: dict[str, Any]) -> str:
    aliases = [alias.lower() for alias in EXECUTOR_SERVER_ALIASES.get(executor, [executor])]
    for server in discovery_report.get("design_servers", []):
        sid = str(server.get("server_id", "")).lower()
        if sid in aliases and server.get("available"):
            return str(server.get("server_id", ""))
    return ""


def render_tool_prompt(
    intent: str,
    goal: str,
    required_documents: list[str],
    template_dir: Path | None = None,
) -> str:
    base_dir = template_dir or DEFAULT_PROMPT_TEMPLATE_DIR
    template_name = INTENT_TO_TEMPLATE.get(intent)
    if not template_name:
        return (
            "Use approved brand outputs as source of truth.\n"
            f"Objective: {goal}\n"
            f"Required documents: {', '.join(required_documents)}"
        )

    template_path = base_dir / template_name
    if not template_path.exists():
        return (
            "Use approved brand outputs as source of truth.\n"
            f"Objective: {goal}\n"
            f"Required documents: {', '.join(required_documents)}"
        )

    template = template_path.read_text(encoding="utf-8")
    required_docs_block = "\n".join(f"- {doc}" for doc in required_documents)
    return template.format(
        goal=goal,
        required_documents=required_docs_block,
    )


def as_bullets(items: list[str], empty_line: str = "- none") -> str:
    if not items:
        return empty_line
    return "\n".join(f"- {item}" for item in items)


def as_numbered_steps(items: list[str]) -> str:
    if not items:
        return "1. Confirm route and source documents."
    return "\n".join(f"{idx}. {item.replace('_', ' ')}" for idx, item in enumerate(items, 1))


def next_action_for(intent: str, execution_mode: str) -> str:
    if execution_mode == "execute":
        return (
            f"Run the `{intent}` route in execute mode and review route outputs against "
            "approved brand constraints before final delivery."
        )
    return (
        f"Use the `{intent}` handoff artifacts to start production in the selected tool, "
        "then review fidelity against the packaged brand system."
    )


def mode_reason(execution_mode: str, mcp_supported: bool) -> str:
    if execution_mode == "execute":
        if mcp_supported:
            return "Direct execution requested and route supports MCP-compatible execution."
        return "Direct execution requested, but route is primarily handoff-oriented in current tooling."
    if mcp_supported:
        return "Handoff chosen to keep manual control even though MCP execution is possible."
    return "Handoff chosen because direct MCP execution is unavailable for this route."


def tool_reason(intent: str, primary_tool: str) -> str:
    custom = {
        "vis_handbook": "Best suited for structured handbook pages, reusable variables, and scalable section layout.",
        "logo_refinement": "Best suited for precision vector construction and export-safe logo rules.",
        "visual_asset_system": "Best suited for reusable asset library construction and system-level organization.",
        "packaging_mockup": "Best suited for realism-heavy scene compositing and material presentation.",
        "social_template_pack": "Best suited for editable templates and non-designer reuse.",
        "landing_page_visual_system": "Best suited for rapid web visual system and screen-family generation.",
        "ui_screen_system": "Best suited for product screen-system ideation and structured UI output.",
        "open_source_vector_refinement": "Best suited for open-source vector refinement workflows.",
    }
    return custom.get(intent, f"Primary tool selected by route rules: {to_tool_display_name(primary_tool)}.")


def infer_intent_from_application_recipe(recipe: dict[str, Any]) -> str:
    family = normalize_text(str(recipe.get("family", "")))
    default_route = normalize_text(str(recipe.get("default_route", "")))

    if any(word in family for word in ("logo", "wordmark", "lockup")):
        return "logo_refinement"
    if any(word in family for word in ("handbook", "guideline", "manual")):
        return "vis_handbook"
    if any(word in family for word in ("web", "landing", "site", "campaign")):
        return "landing_page_visual_system"
    if any(word in family for word in ("ui", "app", "screen", "product")):
        return "ui_screen_system"
    if any(word in family for word in ("asset", "icon", "pattern", "illustration")):
        return "visual_asset_system"
    if any(word in family for word in ("package", "packaging", "mockup")):
        return "packaging_mockup"
    if any(word in family for word in ("social", "template", "post", "content")):
        return "social_template_pack"

    if default_route == "template-auto":
        return "social_template_pack"
    if default_route == "mockup-semi-auto":
        return "packaging_mockup"
    if default_route == "manual-vector":
        return "logo_refinement"
    return "visual_asset_system"


def resolve_dependencies(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    artifact_sources: dict[str, list[str]] = {}
    resolved: list[dict[str, Any]] = []
    for task in tasks:
        deps = []
        needed_types = task.get("input_artifact_types", [])
        for artifact_type in needed_types:
            source_task_ids = artifact_sources.get(artifact_type, [])
            for source_id in source_task_ids:
                if source_id not in deps and source_id != task["task_id"]:
                    deps.append(source_id)
        next_task = dict(task)
        next_task["depends_on"] = deps
        resolved.append(next_task)

        for output_type in task.get("output_artifact_types", []):
            artifact_sources.setdefault(output_type, []).append(task["task_id"])

    return resolved
