---
name: brand-application-factory
description: Builds the reusable automation layer for a finished identity system by publishing the brand pack and generating a brand-specific applications wrapper skill. Use this skill after the core identity and application recipes are approved.
---

# Brand Application Factory

## Overview

Turn the finished design system into a reusable automation surface. This skill publishes the machine-readable `brand-pack`, preserves the AI-readable design documents, and generates two lightweight wrapper skills that future sessions can call directly.

## Use This Skill

- finalize a reusable `brand-pack`
- generate `<brand-slug>-brand-applications`
- rebuild a wrapper skill after a guideline update

## Workflow

### 1. Build the final brand pack

Run `scripts/build_brand_pack.py` against the approved foundation and application outputs.

### 2. Validate the pack

Check that all required sections exist:

- `brand-guideline`
- `brand-tokens`
- `logo-system`
- `style-playbook-selection`
- `application-recipes`
- `asset-manifest`

Check for recommended design-doc payloads:

- `reference_style_distillation`
- `design_md_documents.brand_foundation_design`
- `design_md_documents.ui_ux_design` when digital scope exists
- `design_md_documents.application_design`
- `design_md_documents.design_index`

### 3. Generate the wrapper skills

Run `scripts/generate_wrapper_skill.py` with the published pack and output directory.

### 4. Hand off

Use the generated wrapper skills in future sessions to:

- use `<brand-slug>-brand-applications` to list bundles, generate application work, and produce manual briefs
- use `<brand-slug>-brand-guidelines` to restate the visual language and direct on-brand design work across tools
- reuse the design-md files as AI-readable design instructions for Stitch, Figma MCP, Pencil, and similar tooling

## Resources

- `references/brand-pack-schema.md`
- `references/wrapper-skill-contract.md`
- `assets/wrapper_skill_template.md`
- `scripts/build_brand_pack.py`
- `scripts/generate_wrapper_skill.py`
