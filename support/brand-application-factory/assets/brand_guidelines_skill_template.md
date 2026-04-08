---
name: {skill_name}
description: Uses the approved {brand_name} brand pack and design markdown files to restate style, constraints, and prompt-ready design instructions for new brand work. Use this skill when creating or directing posters, campaign assets, collateral, landing pages, social graphics, or other on-brand design outputs for {brand_name}.
---

# {brand_name} Brand Guidelines

## Overview

Use the bundled brand pack at `{pack_rel_path}` and the bundled design markdown files as the single source of truth for new design work.

## What this skill is for

- restating the brand's visual language
- directing AI design tools with approved style and constraint rules
- keeping posters, key visuals, pages, and collateral on-system
- identifying when a request is actually a brand-change request rather than an application request

## Read order

1. `references/design-index.md`
2. `assets/brand_pack.json`
3. the specific design markdown file matched to the task

## Task routing

### 1. Foundation-level direction

For broad style direction, read:

- `references/brand-foundation-design.md`

### 2. UI and digital tasks

For sites, product UI, landing pages, or dashboards, read:

- `references/ui-ux-design.md`

### 3. Application and collateral tasks

For posters, social media, decks, print, signage, banners, packaging, and other touchpoints, read:

- `references/application-design.md`

### 4. Reference-origin reasoning

When asked why the system looks the way it does, read:

- `references/reference-style-distillation.md`

## Operating rules

- Prefer the bundled files over memory or improvised taste
- Restate the style in concrete, prompt-ready terms
- Keep the work inside the approved identity system
- Flag any request that changes the logo, color architecture, or core visual posture
- When a request is underspecified, derive from the most specific matching design markdown file
