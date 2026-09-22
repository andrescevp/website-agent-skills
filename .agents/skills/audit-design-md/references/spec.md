# design.md Specification Reference

Source: https://github.com/google-labs-code/design.md (Apache-2.0, format version `alpha`).
Load this reference when writing complex token files, diagnosing warnings, or
when the exact schema of a DESIGN.md matters. For the authoritative current
text, run `designmd spec` (add `--format markdown` for human-readable output).

## Two layers of a DESIGN.md

| Layer | Location | Role |
|---|---|---|
| YAML frontmatter | between the top `---` fences | design tokens — **normative values** |
| Markdown body | `##` sections after frontmatter | prose context for how to apply tokens |

Consumers read tokens as truth; prose explains usage. Never change a token
value silently when only the prose needs an update.

## Top-level keys

```yaml
version: <string>          # optional; current spec version is "alpha"
name: <string>             # required: project/design-system name
description: <string>      # optional
omitted: <string[] | OmittedSection[]>  # sections intentionally NOT present
colors:
  <token-name>: <Color>
typography:
  <token-name>: <Typography>
rounded:
  <scale-level>: <Dimension>
spacing:
  <scale-level>: <Dimension | number>
components:
  <component-name>:
    <token-name>: <string | token reference>
```

Custom extension keys under top level are tolerated (silent). Keys that look
like typos of known keys (e.g. `colours:` → `colors:`) are flagged.

## Token types

| Type | Accepted format | Example |
|---|---|---|
| Color | any CSS color: hex, `rgb()`, `oklch()`, named | `"#1A1C1E"`, `"oklch(62% 0.18 250)"` |
| Dimension | number + unit (`px`, `em`, `rem`) | `48px`, `-0.02em` |
| Token Reference | `{path.to.token}` | `{colors.primary}`, `{typography.h1.fontSize}` |
| Typography | object with typographic properties | see below |

### Typography object properties

| Property | Meaning |
|---|---|
| `fontFamily` | font family name or stack |
| `fontSize` | Dimension, e.g. `1.125rem` |
| `fontWeight` | e.g. `400`, `700`, `bold` |
| `lineHeight` | e.g. `1.5`, `24px` |
| `letterSpacing` | Dimension, e.g. `-0.02em` |
| `fontFeature` | OpenType feature settings |
| `fontVariation` | variable font axes |

## Component tokens

Component tokens describe concrete UI parts and should reference core tokens.

### Valid component properties

`backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`,
`height`, `width`.

```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:   # variants are separate entries
    backgroundColor: "{colors.tertiary-hover}"
```

Unknown component property → accepted with a warning (do not delete such keys
unless the user asks).

## Canonical section order

Body sections may be omitted, but **present sections must appear in this order**
(aliases in parentheses map to the same section):

1. Overview (Brand & Style)
2. Colors
3. Typography
4. Layout (Layout & Spacing)
5. Elevation & Depth (Elevation)
6. Shapes
7. Components
8. Do's and Don'ts

Several section names are aliases for the same canonical section; pick the
canonical name when creating a file. Out-of-order sections produce a
`section-order` warning.

## Lint rules (11)

| Rule | Severity | Checks |
|---|---|---|
| `broken-ref` | error | Token refs (`{colors.primary}`) that don't resolve |
| `missing-primary` | warning | Colors exist but no `primary` — agents auto-generate one; prefer explicit `primary` |
| `contrast-ratio` | warning | Component background/text pairs below WCAG AA (4.5:1) |
| `orphaned-tokens` | warning | Colors defined but never referenced by components |
| `token-summary` | info | Token count per section |
| `missing-sections` | info | Optional sections (spacing, rounded) absent while other tokens exist |
| `missing-typography` | warning | Colors but no typography tokens — agents use default fonts |
| `section-order` | warning | Sections out of canonical order |
| `unknown-key` | warning | Top-level key looks like a typo; custom extension keys stay silent |
| `token-like-ignored` | warning | Unknown top-level key holding token-like values (hex, fonts, dimensions) |
| `omitted-rules` | info | Validates `omitted` config mapping |

## Consumer behavior for unknown content

| Situation | Behavior |
|---|---|
| Unknown section heading | preserved, no error |
| Unknown color token name | accepted if the value is a valid color |
| Unknown typography token name | accepted as valid typography |
| Unknown component property | accepted with a warning |
| Duplicate section heading | **error — file rejected** |