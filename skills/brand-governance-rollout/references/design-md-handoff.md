# Design Markdown Handoff

Finalize the brand as a markdown design system pack that AI tools can consume repeatedly.

## Final File Set

- `REFERENCE_STYLE_DISTILLATION.md`
- `BRAND_FOUNDATION_DESIGN.md`
- `UI_UX_DESIGN.md` when relevant
- `APPLICATION_DESIGN.md`
- `DESIGN_INDEX.md`
- `TOOL_ADAPTER_INDEX.md`
- tool-specific adapter contracts

## What `DESIGN_INDEX.md` Should Do

Explain:

- the purpose of each file
- which file is authoritative for which decisions
- the order in which downstream agents should read them
- which files are optional by scope

## Tool Guidance

### Stitch

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `UI_UX_DESIGN.md` when interface work exists
- `TOOL_ADAPTER_INDEX.md`
- `tool-adapters/stitch.md`

### Figma MCP

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `UI_UX_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `TOOL_ADAPTER_INDEX.md`
- `tool-adapters/figma-mcp.md`

### Pencil or similar design agents

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `TOOL_ADAPTER_INDEX.md`
- `tool-adapters/pencil.md`

### Adobe Illustrator

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `tool-adapters/adobe-illustrator.md`

### Adobe Photoshop

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `tool-adapters/adobe-photoshop.md`

### Canva

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `tool-adapters/canva.md`

### Inkscape

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `tool-adapters/inkscape.md`

### Text-to-image models

Use:

- `BRAND_FOUNDATION_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `tool-adapters/image-generation-models.md`

## Governance Rule

Do not let the markdown pack drift away from the brand pack or the human-facing guideline. These must describe the same system at different levels of resolution.
