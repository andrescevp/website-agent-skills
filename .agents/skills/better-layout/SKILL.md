---
name: better-layout
description: >
  Use this skill when improving grouping, alignment, reading order and other
  details that make a great layout in your project — progressive disclosure,
  spacing, breakpoints and RTL. Use when the user asks to "improve the
  layout", "fix alignment", "reflow at 320px", or when spacing, order, or
  breakpoints look off.
license: MIT
compatibility: opencode
allowed-tools: bash, read, write, edit, chrome-devtools
metadata:
  audience: agents improving layout
  workflow: layout structure and adaptivity
---

# Layout

Position, spacing and alignment carry hierarchy before a word is read. This skill builds that structure and stress-tests it: resize it, translate it, mirror it for RTL.

Write every fix in the project's styling system. The numbers below are starting points for interfaces with no established density system, and where one applies, use it as written rather than a familiar-looking substitute. Keep deliberate platform chrome, compact professional tools and project tokens where they still pass the stress tests.

Hit areas and focus behavior belong to `better-accessibility`. Radius, shadows and animation belong to `better-ui`. Line length and text spacing belong to `better-typography`.

## Group with space, not lines

Space groups first, background shapes second, separator lines last and only where space alone can't carry the structure. The gap between groups must be at least 2× the gap within one (`8px` intra-group to `16px`+ inter-group), or the grouping reads as noise. Alignment edges and importance ordering are in [grouping-and-alignment.md](references/grouping-and-alignment.md).

## Keep controls distinct from content

Give every interactive element a background shape, a border, or a consistent placement zone. A control styled like the static text beside it does not read as a control.

## Align to shared edges

Pick alignment edges and stick to them; every stray edge reads as noise. Use one project spacing step per level of subordination, where `16px` is a useful default.

Use logical properties for direction-dependent layout: `padding-inline-start`, `margin-inline-end`. Reserve physical left and right for genuinely physical geometry.

## Order by importance

The most important content sits near the top and the leading edge. Reading order flows top-to-bottom, leading-to-trailing. Think in leading and trailing, not left and right.

## Hint at hidden content

Progressive disclosure needs a visible affordance. Use the project's established cue, or let the next item peek `16–32px` past the scroll edge, or show a disclosure control. Content hidden with zero cue may as well not exist.

## Breathing room between targets

Without an established density system, start with `12px` between adjacent bordered or filled controls and `24px` around borderless text- and icon-only ones. Compact layouts may use less, as long as `better-accessibility` hit areas don't overlap and the controls stay distinct. Layout margins and breakpoint recipes are in [spacing-and-adaptivity.md](references/spacing-and-adaptivity.md).

## Inset buttons from the edges

In content layouts, keep full-width buttons inside the layout margins with a visible radius, starting near `16px` inline on mobile. Edge-to-edge actions work when they follow established platform chrome, account for safe areas and stay distinguishable from system UI.

## Content bleeds, controls float

Backgrounds and media extend to the viewport edges. Controls and text stay inside the layout margins and safe areas (`env(safe-area-inset-*)`). Sticky chrome floats above the content layer rather than blocking it.

## Hold structure until it breaks

Breakpoints come from the content, not device presets. Keep the expanded layout as long as it genuinely fits and collapse late. Prefer container queries for component-level adaptation, and test the smallest and largest sizes first.

## Plan for growth and clipping

Translated strings grow, and short ones grow proportionally more, so a one-word button label is the riskiest thing on the screen. Put no fixed width or height on a text container, and let rows wrap. Test with pseudo-localization and one representative locale rather than budgeting a percentage.

Never park a critical action where resizing or scrolling clips it. Keep it in the normal flow, or in stable chrome suited to the product.

## Metrics: Lighthouse

- `performance_start_trace` (reload, mobile viewport via `emulate`) → CLS ≤ 0.1 at every supported width; a shift at 320px or on resize confirms a structure failure.
- `lighthouse_audit` (mobile) → "Content wider than screen" and tap-target diagnostics.
- Metrics only corroborate what rendered inspection shows; the stress tests below stay the source of findings.

## Before you finish

| Mistake | Fix |
| --- | --- |
| `margin-left` / `padding-right` in a localizable layout | `margin-inline-start` / `padding-inline-end` |
| Content-layout button touches the viewport edge | Inset within the project margins; keep intentional platform chrome |
| Breakpoints at 768/1024 because they're the defaults | Break where the content actually stops fitting |
| Fixed-width text container sized to one language | `max-width` and wrapping; test pseudo-localization |
| Primary action at the clip-prone bottom of a pane | Sticky positioning or stable chrome with safe-area padding |

## Reporting

**Severity.** `HIGH` blocks content or an action at a supported viewport. `MEDIUM` harms hierarchy, reading order, or adaptability. `LOW` is isolated alignment or spacing polish.

**Verification.** Without a browser: logical properties in place of physical ones, container and media queries against the supported viewport list and DOM order against the intended reading order. With one: every supported width, 200% zoom and the RTL mirror. Report every check you could not run as `Not verified`.

**Format.** Group findings under the principle each violates, ordered by severity, one row per root cause listing every location it appears in:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

`Location` is `path/to/file:line`. `Why` names the principle and the user impact.

End with `Block` when any `HIGH` remains, `Approve` otherwise, leaving the rest in the table as work to do. Never `Approve` coverage you did not inspect. With nothing to report, state "No actionable layout findings" and report verification.

## References — load when needed

- `references/grouping-and-alignment.md` — grouping rules, alignment edges and importance ordering.
- `references/spacing-and-adaptivity.md` — margins, breakpoints and container-query recipes.

## Validation checklist

- [ ] Groups separated by space (≥2× the intra-group gap), then shapes, then lines.
- [ ] Logical properties used for direction-dependent layout; RTL mirror verified.
- [ ] Reading order matches DOM order; most important content leads.
- [ ] Hidden content has a visible cue; controls distinct from content.
- [ ] Breakpoints follow the content; smallest and largest widths tested first.
- [ ] No fixed size on text containers; growth/clipping stress tested with pseudo-localization.
- [ ] Metrics (CLS at supported widths) reported when a browser was available.
- [ ] Findings in `Severity | Location | Before | After | Why` format; verdict `Block`/`Approve`.
