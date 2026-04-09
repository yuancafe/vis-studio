---
name: brand-production-orchestrator
description: Route approved VIS outputs into the correct downstream design tool, support document/production dual modes, auto-discover local design MCP services, and orchestrate execution-ready production pipelines.
---

# Brand Production Orchestrator

## Overview

This skill sits after the core VIS workflow and packaging stage. It does not redefine strategy or visual direction. Its role is to route approved brand outputs into execution-ready downstream production.

Version 2.1 adds two run modes:

- `document`: stop at planning documents and payloads
- `production`: continue into automated execution orchestration after documentation

## Use This Skill

- Convert a production request into a normalized intent and route
- Select a primary tool and optional secondary tools
- Assemble route-specific source documents
- Generate `EXECUTION_PLAN.md`
- Generate `TOOL_EXECUTION_PAYLOAD.json`
- Render a tool-specific prompt for handoff or execution
- Discover local design MCP services from both Codex and global MCP config
- Build deterministic single-task or full-suite production pipelines
- Execute route tasks in order, with dependency input chaining between task families

## Inputs

- production goal text
- packaged outputs (`brand_pack.json`, design markdown files)
- optional execution mode (`handoff` or `execute`)
- optional tool preference or constraints
- optional run mode (`document` or `production`)
- optional production scope (`single` or `full_suite`)

## Outputs

- `EXECUTION_PLAN.md`
- `TOOL_EXECUTION_PAYLOAD.json`
- route-specific tool prompt text
- `MCP_DISCOVERY_REPORT.json` in production mode
- `RUN_MANIFEST.json`, `RUN_LOG.md`, `ARTIFACT_REGISTRY.json` in production mode

## Execution model

### 1. Detect intent

Map the request to one route:

- `vis_handbook`
- `logo_refinement`
- `visual_asset_system`
- `packaging_mockup`
- `social_template_pack`
- `landing_page_visual_system`
- `ui_screen_system`
- `open_source_vector_refinement`

### 2. Select route and tool

Use `assets/route-rules.yaml` as the route contract.

### 3. Build artifacts

Run:

- `scripts/select_route.py`
- `scripts/build_execution_plan.py`
- `scripts/build_tool_execution_payload.py`
- `scripts/render_tool_prompt.py`

### 4. Choose run mode

- `document`: produce plan + payload + prompt and stop
- `production`: produce plan + payload, then auto-discover MCP, build pipeline, and execute

## Non-negotiables

- Never override approved brand direction
- Always treat `brand_pack.json` and approved design docs as source of truth
- Keep orchestration thin: route and execute, do not reopen strategy
- Load only route-relevant documents by default
- In production mode, keep outputs organized by application-family folders
- Critical task failures should ask for `retry/skip/stop` with timeout fallback

## Resources

- `assets/execution-plan-template.md`
- `assets/tool-execution-payload.schema.json`
- `assets/route-rules.yaml`
- `assets/tool-prompt-templates/`
- `scripts/select_route.py`
- `scripts/build_execution_plan.py`
- `scripts/build_tool_execution_payload.py`
- `scripts/render_tool_prompt.py`
- `scripts/discover_mcp_servers.py`
- `scripts/build_pipeline.py`
- `scripts/run_orchestration.py`
