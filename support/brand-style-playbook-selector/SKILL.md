---
name: brand-style-playbook-selector
description: Selects the best-fit brand style playbooks from the structured VIS library and returns a scored top-3 with fit and avoid reasoning. Use this skill when narrowing concept directions after the strategy brief is approved.
---

# Brand Style Playbook Selector

## Overview

Use the structured VIS playbook library to narrow visual direction before concept exploration gets noisy.

## Use This Skill

- narrow concept directions from a strategic brief
- translate brand signals into reusable style playbooks
- produce a justified top-3 instead of vague taste language

## Workflow

### 1. Normalize the brief

Capture:

- category
- audience
- price point
- personality
- required signals
- avoid signals

### 2. Score against the library

Run `scripts/select_playbooks.py` against `assets/brand_style_playbooks.json`.

### 3. Review the top 3

Check:

- why each playbook fits
- what it would likely solve well
- what it may over-signal or under-signal

### 4. Hand the result forward

Use the recommended lead playbook as the main direction for `visual-concept-exploration`.

## Outputs

- top-3 playbooks
- scored rationale
- fit matches
- avoid conflicts
- one recommended lead playbook

## Resources

- `references/playbook-selection-heuristics.md`
- `assets/brand_style_playbooks.json`
- `scripts/select_playbooks.py`
