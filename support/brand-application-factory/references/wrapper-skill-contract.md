# Wrapper Skill Contract

The generated wrapper skill set should produce two thin skills:

1. `<brand-slug>-brand-applications`
2. `<brand-slug>-brand-guidelines`

## Applications wrapper intents

The applications wrapper must support four intents:

1. list supported application bundles
2. restate brand constraints from the pack
3. generate automation-friendly application work
4. produce manual briefs for `manual_vector` items

## Brand-guidelines wrapper intents

The brand-guidelines wrapper should support:

1. restate the brand's visual style and non-negotiables
2. guide new design work such as posters, campaign assets, pages, and collateral
3. route tasks to the right design-doc source file
4. warn when a request would change the identity system rather than apply it

## Thin-wrapper rule

Both wrappers should stay thin:

- do not duplicate the full suite
- read the bundled `brand_pack.json`
- read the bundled design markdown files when present
- route to the common factory logic when needed
