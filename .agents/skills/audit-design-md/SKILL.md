---
name: audit-design-md
description: >
  Use this skill when creating, updating, or validating DESIGN.md files in a
  project — the design.md format specification that gives coding agents a
  structured, persistent understanding of a project's visual identity (colors,
  typography, spacing, components, and usage rules). Use when the user asks to
  "create a DESIGN.md", "validate/lint the DESIGN.md", "update design tokens",
  "export tokens to Tailwind", or whenever UI work should follow a documented
  design system. Requires the official @google/design.md CLI and uses it
  directly — never reimplements the validator.
license: Apache-2.0
compatibility: opencode
allowed-tools: bash, read, write, edit
metadata:
  audience: coding agents and developers maintaining design systems
  workflow: design-system documentation and validation
---

# audit-design-md

## What I do

- **Create** a `DESIGN.md` from a design brief, style guide, or legacy project.
- **Update** tokens and prose while keeping the file valid and regression-free.
- **Validate** the file with the official `@google/design.md` CLI and report
  findings (errors/warnings/infos) in an actionable form.

## When to use me

- A project has no `DESIGN.md` and needs one.
- The user asks to lint/validate/check an existing `DESIGN.md`.
- Design tokens change (colors, typography, spacing, components) and the file
  must stay in sync.
- UI output should conform to the documented design system.

## Prerequisite: official validator (mandatory)

This skill uses the official `@google/design.md` CLI. The CLI **must be
installed and invoked directly**. Never write a reimplementation of the
validator, and never fabricate lint results — run the real tool.

Check availability:

```bash
designmd --version
# or, without a global install:
npx -p @google/design.md designmd --version
```

Install (one-time):

```bash
npm install -g @google/design.md
```

If the CLI is missing, install it before proceeding (ask before networked
actions if required by policy).

## DESIGN.md quick facts

- Default location: project root `DESIGN.md` (confirm if ambiguous).
- Two layers:
  - **YAML frontmatter** = design tokens (normative values).
  - **Markdown body** (`##` sections) = prose context on how to apply them.
- Tokens: `colors`, `typography`, `rounded`, `spacing`, `components`.
- Colors: any CSS color (`#hex`, `rgb()`, `oklch()`, named).
- Dimensions: number + unit (`12px`, `0.5rem`, `-0.02em`).
- Token references: `{path.to.token}` — e.g. `{colors.primary}`.
- Canonical body section order (present sections must follow it):
  Overview → Colors → Typography → Layout (aka Layout & Spacing) →
  Elevation & Depth (aka Elevation) → Shapes → Components → Do's and Don'ts.
- Omit sections deliberately with the `omitted:` key rather than silently
  deleting them.
- Duplicate section headings are a hard validation error.

## Workflows

### 1. Validate

1. Run `designmd lint DESIGN.md` (use `--format json` when scripting).
2. Fix **all errors** (exit code 1 on errors); fix warnings; read infos.
3. Report the summary to the user: N errors, N warnings, N infos.

### 2. Create

1. Resolve the target path (default: project root `DESIGN.md`).
2. Gather context: design brief, style guide, existing CSS/UI tokens. If none
   exists, ask the user for palette, fonts, spacing scale, and corner radii.
3. Scaffold frontmatter: `version: alpha`, `name`, optional `description`,
   `colors` (include `primary` — otherwise the linter warns and agents
   auto-generate one), `typography`, `spacing`, `rounded`, `components`.
4. Write body sections in canonical order; prose explains how to apply tokens
   in practice.
5. Components must reference tokens: `backgroundColor: "{colors.primary}"` —
   never hardcode values that already exist as tokens.
6. Run the Validate workflow; iterate until 0 errors and no avoidable warnings.

### 3. Update

1. Baseline: run `designmd lint DESIGN.md` and record current findings.
2. Keep a previous copy (e.g. `cp DESIGN.md /tmp/DESIGN-prev.md`) for diffing.
3. Apply the changes with `edit`; preserve canonical section order and reuse
   existing tokens where possible.
4. Regression check: `designmd diff /tmp/DESIGN-prev.md DESIGN.md` — exit 1
   means regressions; fix them.
5. Re-lint: confirm errors are resolved and no new warnings were introduced.

### 4. Export tokens (optional)

```bash
designmd export --format json-tailwind   # Tailwind v3 theme.extend
designmd export --format css-tailwind    # Tailwind v4 @theme {}
designmd export --format dtcg            # W3C Design Tokens Format Module
```

## Rules and gotchas

- **Tokens are normative; prose is context.** Never change token values silently
  when only copy needs updating.
- Do not delete unknown/extension keys — the linter tolerates custom keys by
  design; only remove them if the user asks.
- Watch for typo keys that look like tokens (e.g. `colours:` instead of
  `colors:`) — the linter flags them; fix the spelling.
- `contrast-ratio` warnings matter: component background/text pairs must reach
  WCAG AA (4.5:1).
- Use `designmd spec` to inject the exact current spec (optionally with
  `--rules`) into an agent prompt when uncertain about formats.

## References — load when needed

- `references/spec.md` — full token schema, component property list, the 11
  lint rules with severities, and consumer behavior for unknown content. Load
  when writing complex token files or diagnosing warnings.
- `references/cli.md` — CLI installation, every command with flags, JSON output
  shape, and exit codes; plus troubleshooting (`ENOVERSIONS`). Load when
  scripting, debugging the CLI, or using `diff`/`export` in depth.

## Validation checklist

- [ ] Official CLI installed and used directly; no reimplemented validator.
- [ ] `designmd lint DESIGN.md` passes with 0 errors (exit code 0).
- [ ] Body sections appear in canonical order; no duplicate headings.
- [ ] Component tokens use `{...}` references that resolve to defined tokens.
- [ ] Token key names spelled correctly (colors, typography, rounded, spacing,
      components).
- [ ] A `primary` color exists when colors are defined.
- [ ] Findings summarized to the user (errors → warnings → infos).