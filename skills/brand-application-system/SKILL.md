---
name: brand-application-system
description: Converts an approved identity system into scoped application bundles, production routes, reusable templates, mockup outputs, and automation-ready application recipes. Use after identity approval when the work shifts from core system design into touchpoint production.
---

# Brand Application System

## Overview

Handle the explicit application-production phase. Turn the approved identity system into real collateral, touchpoint bundles, and reusable application recipes without confusing this work with either core identity engineering or governance packaging.

## Why This Skill Exists

Studio practice usually separates foundational identity work from application work. The identity system defines the rules. This phase applies those rules across real touchpoints in a controlled, scoped, and route-aware way.

## Entry Requirement

Begin only after approved output exists from `identity-system-production`.

Require the draft `brand-pack` foundation before starting.

## Workflow

### 1. Normalize the application scope

Use `application-scope-planner` to convert the requested application list into the standard schema:

- `id`
- `family`
- `purpose`
- `priority`
- `sizes`
- `variant_count`
- `content_source`
- `template_fit`
- `production_route`
- `effort_band`
- `export_formats`
- `owner`

### 2. Assign scope bands

Classify the engagement as:

- `Core` = 1-10 items
- `Growth` = 11-30 items
- `System` = 31-100 items
- `Enterprise` = 100+ items

Batch and prioritize when the list exceeds `System`.

### 3. Classify production routes

Use `application-route-classifier` on every item:

- `template_auto`
- `mockup_semi_auto`
- `manual_vector`

### 4. Produce route-appropriate outputs

Use:

- `application-template-factory` for Canva-friendly template work
- `application-mockup-composer` for Photoshop-friendly mockup or image work
- manual briefs for Illustrator-heavy vector production

### 5. Build reusable application recipes

For each family, create recipes that describe:

- input requirements
- layout logic
- size logic
- brand constraints
- route choice
- export expectations

### 6. Enrich the brand pack

Add:

- `application-recipes`
- scope matrix
- bundle presets
- route metadata

## Outputs

- normalized application scope matrix
- prioritized application bundles
- route-aware production plan
- reusable application recipes
- enriched brand pack

## Non-Negotiables

- Never let a 100-item request flatten into one undifferentiated batch
- Never pretend `manual_vector` work is fully automated
- Never bury production-route decisions inside vague presentation language
- Never produce large application libraries before priorities are clear

## Hand Off

After approval, continue with `brand-governance-rollout`.

## Resources

- `references/application-system-workflow.md`
- `references/scope-bands.md`
- `references/production-routes.md`
