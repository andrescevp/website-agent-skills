# Website Auditor Skills

Specialized agent skills for auditing websites — technical SEO, Generative Engine Optimization (GEO), Lighthouse performance — plus a complete suite of interface design skills covering UI polish, typography, color systems, accessibility, layout, copy, and component iteration.

## Skills

### Website auditing

| Skill | What it does |
| --- | --- |
| **`website-audit`** | Full website audit: subdomain crawl, multi-engine SEO/GEO analysis, and Lighthouse performance & Core Web Vitals (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1). Saves reports to `audits/<sub.domain.me>/audit.md`. |

### Design system documentation

| Skill | What it does |
| --- | --- |
| **`audit-design-md`** | Create, update, and validate `DESIGN.md` files following the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec: YAML design tokens (colors, typography, rounded, spacing, components) + Markdown body in canonical section order. Uses the official `@google/design.md` CLI directly (`lint`, `diff`, `export`). |

### Interface design & review (adapted from [jakubkrehel/skills](https://github.com/jakubkrehel/skills), MIT)

| Skill | What it does |
| --- | --- |
| **`better-interface`** | Combines all of the `better-*` skills into a single cross-domain review with one ranked findings table and a `Block`/`Approve` verdict. |
| **`better-ui`** | Improves UI across the board: concentric border radius, optical alignment, contextual icons, hit areas, animation, surfaces and more. |
| **`better-typography`** | Improves type: type scale, spacing, sizing, variable fonts, OpenType features, wrapping, truncation and more. |
| **`better-colors`** | Builds a color system and answers anything about color: palettes, semantic tokens, format conversion, contrast. |
| **`better-accessibility`** | Helps projects comply with accessibility standards and best practices: keyboard, focus, ARIA, screen readers, hit areas, reduced motion. |
| **`better-layout`** | Helps with grouping, alignment, reading order, progressive disclosure and other layout details. |
| **`better-writing`** | Improves product copy and keeps it consistent: voice, buttons, errors, empty states, links, capitalization. |

### User-invoked skills

| Skill | What it does |
| --- | --- |
| **`interface-review`** | Reviews a branch, PR, commit range, or uncommitted changes across UI, typography, layout, color, writing, and accessibility; classifies findings as `Introduced` / `Regression` / `Pre-existing`. |
| **`explain-interface`** | Figures out how an animation, design, or piece of UI was built on the web (from a URL or a screenshot). |
| **`break-site`** | Renders a chosen component in every state and scenario on a temporary page and stress tests it. |
| **`component-variant`** | Builds multiple variants of a component on the real page and helps you pick one. |

## Lighthouse metrics support

The `better-*` and review skills use the **chrome-devtools MCP** to extract supporting metrics where a browser is available:

- `lighthouse_audit` — accessibility (axe-based), best-practices, and color-contrast checks.
- `performance_start_trace` — Core Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.

Metrics are evidence for findings, never standalone findings; exact runs (URL, device, viewport) are reported under verification.

## Prerequisites

- **Browser MCP** for Lighthouse and rendered inspection: `chrome-devtools` (recommended) or `playwright` (see `AGENTS.md`).
- **`@google/design.md` CLI** for `audit-design-md` (used directly; never reimplemented):

```bash
npm install -g @google/design.md
designmd lint DESIGN.md
```

## Directory structure

```text
website-auditor-skills/
├── AGENTS.md                          # Master directives & architecture
├── pyproject.toml                     # Python dependencies (managed via uv)
├── .agents/
│   └── skills/
│       ├── website-audit/             # SEO/GEO/Lighthouse audit skill
│       ├── audit-design-md/           # DESIGN.md create/update/validate
│       ├── better-interface/          # Cross-domain review
│       ├── better-ui/                 # UI polish & motion
│       ├── better-typography/         # Type systems
│       ├── better-colors/             # Color systems & contrast
│       ├── better-accessibility/      # a11y compliance
│       ├── better-layout/             # Layout structure
│       ├── better-writing/            # Product copy
│       ├── interface-review/          # Change-scoped review
│       ├── explain-interface/         # Interface forensics
│       ├── break-site/                # Component stress testing
│       └── component-variant/         # Variant exploration
└── audits/
    └── <sub.domain.me>/               # audit.md reports
```

Each skill keeps a lean `SKILL.md` (under 200 lines) with detailed domain content in `references/`, loaded on demand.

## Quick commands

```bash
# Full website audit (crawl + SEO/GEO + Lighthouse)
uv run python .agents/skills/website-audit/scripts/crawler.py https://<sub.domain.me> -o /tmp/crawl.json
uv run python .agents/skills/website-audit/scripts/seo_geo_check.py https://<sub.domain.me> -o /tmp/seo_geo.json
uv run pytest

# Design system validation
designmd lint DESIGN.md

# Run all test suites
uv run pytest
```

## Licenses & attribution

- `website-audit` and `audit-design-md`: project-internal.
- The 11 interface skills are adapted from [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (© 2026 Jakub Krehel, [MIT](https://github.com/jakubkrehel/skills/blob/main/LICENSE)), with names and specs per project requirements.
- The `audit-design-md` skill implements the [design.md](https://github.com/google-labs-code/design.md) format spec (Apache-2.0).