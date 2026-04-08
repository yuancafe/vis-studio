# Tool Adapter Index

Use this index when the brand has already been defined and the next step is to execute design work through a specific tool, MCP, or image model.

## Core rule

Always read the brand source files first:

1. `REFERENCE_STYLE_DISTILLATION.md`
2. `BRAND_FOUNDATION_DESIGN.md`
3. `UI_UX_DESIGN.md` when digital scope exists
4. `APPLICATION_DESIGN.md`
5. `DESIGN_INDEX.md`

Then read the matching adapter:

- `tool-adapters/figma-mcp.md`
- `tool-adapters/stitch.md`
- `tool-adapters/pencil.md`
- `tool-adapters/adobe-illustrator.md`
- `tool-adapters/adobe-photoshop.md`
- `tool-adapters/canva.md`
- `tool-adapters/inkscape.md`
- `tool-adapters/image-generation-models.md`

## Why adapters exist

The same brand should not be described the same way to every tool.

- Figma MCP wants structure, components, layout, and tokens.
- Stitch wants a dense AI-readable design brief for digital surfaces.
- Illustrator and Inkscape need vector and construction guidance.
- Photoshop needs composition, imagery, and mockup direction.
- Canva needs template-safe layout logic.
- Text-to-image models need visual prompts plus explicit guardrails.

## Output rule

Use the same brand source files across all tools, but translate them through the correct adapter instead of writing one generic prompt.
