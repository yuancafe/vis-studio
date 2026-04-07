# Design Markdown Sources

This package's design-markdown approach is informed by two upstream references:

- VoltAgent `awesome-design-md`
  - https://github.com/VoltAgent/awesome-design-md
- Google Stitch `DESIGN.md` documentation
  - https://stitch.withgoogle.com/docs/design-md/overview/

## What We Borrowed

- the idea that markdown design files should be written for AI consumption, not just human review
- explicit sections instead of vague stylistic prose
- prompt-friendly instructions that downstream tools can execute with less drift

## What We Changed for VIS

- added logo-system logic
- added imagery and graphic-system rules
- added reference-style distillation before concept selection
- split outputs into foundation, UI/UX, and applications instead of one UI-only file
- connected the design docs to the machine-readable `brand-pack`
