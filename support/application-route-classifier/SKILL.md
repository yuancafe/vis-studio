---
name: application-route-classifier
description: Classifies normalized application items into template-auto, mockup-semi-auto, or manual-vector routes with explicit reasons. Use this skill after scope normalization and before application production starts.
---

# Application Route Classifier

## Overview

Choose the right production route for each application item so the studio does not overpromise automation or underuse templates.

## Use This Skill

- classify every normalized application item
- separate scalable template work from manual vector work
- prepare route-aware batching for production

## Workflow

### 1. Load the scope matrix

Require output from `application-scope-planner`.

### 2. Classify each item

Run `scripts/classify_routes.py`.

### 3. Review exceptions

Check any item that feels ambiguous across:

- packaging
- signage
- stationery
- environment

### 4. Pass forward

- send `template_auto` items to `application-template-factory`
- send `mockup_semi_auto` items to `application-mockup-composer`
- convert `manual_vector` items into execution briefs

## Resources

- `references/route-rules.md`
- `scripts/classify_routes.py`
