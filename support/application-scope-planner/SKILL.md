---
name: application-scope-planner
description: Normalizes brand application requests into a structured scope matrix with families, priorities, sizes, effort bands, and scope bands. Use this skill when a client names a set of applications and the list needs to become a production-ready plan.
---

# Application Scope Planner

## Overview

Turn raw application requests into a structured scope matrix that downstream skills can classify, price, batch, and produce.

## Use This Skill

- normalize 1-100+ application items
- convert vague asks into repeatable schema
- assign scope bands before production starts

## Workflow

### 1. Parse the request

Accept:

- a raw list of items
- a partial bundle choice
- a mix of item names and notes

### 2. Normalize the schema

Run `scripts/build_scope_matrix.py`.

### 3. Review the output

Confirm:

- family grouping
- priorities
- likely sizes
- export formats
- effort expectations

### 4. Pass forward

Use the resulting matrix as the input for `application-route-classifier`.

## Resources

- `references/application-families.md`
- `references/scope-band-rules.md`
- `assets/starter_bundles.json`
- `scripts/build_scope_matrix.py`
