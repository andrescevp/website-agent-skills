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

### System requirements

- **Node.js 20+ (LTS recommended) + npm/npx** — required by both browser MCP servers (`chrome-devtools`, `playwright`).
- **Google Chrome stable (or Chrome for Testing)** — required by `chrome-devtools` MCP. `playwright` manages its own browser binaries (installed on demand, see below).
- **Python 3.11+ and `uv`** — required by the audit scripts (`crawler.py`, `seo_geo_check.py`) and tests.

### Browser MCP servers (required for Lighthouse & rendered inspection)

One of the two servers below must be registered in your agent's MCP configuration (`mcpServers` JSON — location depends on the client: Claude Code, Cursor, VS Code, Copilot, Antigravity, etc.). `chrome-devtools` is recommended for Lighthouse / Core Web Vitals; `playwright` is recommended for accessibility-tree interaction and cross-browser work.

#### `chrome-devtools` (recommended) — https://github.com/ChromeDevTools/chrome-devtools-mcp

Runs ad-hoc via `npx` (no global install). Provides `lighthouse_audit`, `navigate_page`, `performance_start_trace`, screenshots, and DOM evaluation.

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Optional flags (append to `args`):
- `"--headless"` — run without a visible browser window.
- `"--slim"` — reduced tool surface (used with `--headless` for CI).
- `"--no-usage-statistics"` — opt out of Google usage stats.

Smoke test: *"Check the performance of https://developers.chrome.com"*.

#### `playwright` — https://playwright.dev/docs/getting-started-mcp

Runs ad-hoc via `npx` (no global install). Provides `browser_navigate`, `browser_snapshot` (accessibility tree), `browser_click`, `browser_type`, and client-side DOM evaluation.

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

First run may require browser binaries:

```bash
npx playwright install chromium   # or firefox / webkit / msedge
```

Optional flags (append to `args`): `"--headless"`, `"--browser=firefox"`, `"--browser=webkit"`, `"--browser=msedge"`.

Smoke test: *"Navigate to https://demo.playwright.dev/todomvc and add a few todo items."*

### Python dependencies

```bash
uv sync   # installs httpx + beautifulsoup4 (runtime) and pytest + pytest-asyncio (dev)
```

### `@google/design.md` CLI (optional, for `audit-design-md`)

Used directly; never reimplemented:

```bash
npm install -g @google/design.md
designmd lint DESIGN.md
```

## One-shot setup prompt (copy & paste)

Paste the block below into your AI agent (Claude Code, Cursor, VS Code Copilot, Antigravity, opencode, etc.) to install this harness — either into an existing project or from a clone of this repository. The prompt is self-contained: any agent that can read this `README.md` can execute it.

````markdown
Install/configure the **Website Auditor Skills** harness described in the repository README.md: `https://github.com/andrescevp/website-agent-skills`

MACHINE PREREQUISITES (verify/install if missing):
- Node.js 20+ (LTS recommended) and npm/npx available (`node -v`, `npm -v`).
- Google Chrome stable (or Chrome for Testing) for the chrome-devtools MCP.
- Python 3.11+ and `uv` (https://docs.astral.sh/uv/) installed.

CASE A — This directory is a clone of `website-auditor-skills` (repo root):
1. Install Python dependencies: `uv sync`.
2. Register the browser MCP servers in the agent/client MCP config (create the config if it does not exist):
   - chrome-devtools (recommended): {"mcpServers": {"chrome-devtools": {"command": "npx", "args": ["-y", "chrome-devtools-mcp@latest"]}}}
   - playwright (alternative): {"mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}}}
3. If using playwright, ensure browser binaries: `npx playwright install chromium`.
4. Optional (design.md skill): `npm install -g @google/design.md`.
5. Verify: `uv run pytest` passes, and each configured MCP server passes its smoke test:
   - chrome-devtools: "Check the performance of https://developers.chrome.com"
   - playwright: "Navigate to https://demo.playwright.dev/todomvc and add a few todo items."
6. Run a full audit following the "Quick commands" section of README.md.

CASE B — Installing this harness into an EXISTING project (not a clone):
1. Copy the `.agents/skills/` directory from this repository into the target project (keep the same relative path so the skills resolve).
2. If the target project has no `.agents/skills`, create the path and copy all skill folders.
3. Register the browser MCP servers listed in CASE A step 2 in the target project/client MCP config.
4. Ensure the Python runtime deps are available in the target project: `httpx>=0.28.0`, `beautifulsoup4>=4.13.0` (dev: `pytest>=8.3.0`, `pytest-asyncio>=0.25.0`).
5. Optional: `npm install -g @google/design.md`.
6. Smoke-test the MCP servers and run the audit scripts from README.md "Quick commands" to confirm the harness works.

Report: confirm each step, the MCP servers configured, and the smoke-test results.
````

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