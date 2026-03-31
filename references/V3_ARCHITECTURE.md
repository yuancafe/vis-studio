# V3 Architecture

This is the recommended architecture for the VIS suite after integrating NotebookLM process guidance, the Feishu discovery questionnaire, and the studio requirement that application work be treated as a distinct production layer.

## Canonical public skills

1. `brand-discovery-strategy`
2. `visual-concept-exploration`
3. `identity-system-production`
4. `brand-application-system`
5. `brand-governance-rollout`

## Why V3 replaces V2

V2 improved the original split by keeping discovery, audit, and strategy together. It still under-modeled two realities of studio practice:

- application work is a real phase, not a footnote inside rollout
- the identity system should become a reusable machine-readable base for later application generation

NotebookLM already separated "core visual identity design" from "visual ecosystem development". V3 maps that ecosystem phase explicitly to `brand-application-system`.

## Internal worker layer

Public skills stay client-facing and phase-based. Repetitive or deterministic sub-work moves into worker skills:

- `brand-style-playbook-selector`
- `application-scope-planner`
- `application-route-classifier`
- `application-template-factory`
- `application-mockup-composer`
- `brand-application-factory`

## Factory and wrapper model

V3 treats application work as both:

- a service phase in the engagement
- a reusable automation surface after the engagement

The common `brand-application-factory` consumes a completed `brand-pack` and generates a lightweight wrapper skill named `<brand-slug>-brand-applications`.

That wrapper skill lets future sessions reuse the finished identity system without re-running the full strategy and concept pipeline.
