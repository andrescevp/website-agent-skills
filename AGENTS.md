# Website Auditor Agent Directives & Architecture

Specialized agent configurations, skills, and execution protocols for auditing websites across technical SEO, Generative Engine Optimization (GEO), and Lighthouse performance.

---

## 1. Specialist Personas & Directives

### 1.1 Technical SEO Specialist
- **Engines:** Google, Bing, Brave Search.
- **Directives:**
  - Audit crawlability: inspect status codes, redirect chains, canonical tags, and `/robots.txt`.
  - Validate XML sitemap presence and indexing hygiene.
  - Review semantic HTML structure: unique descriptive `<title>` (30-65 chars), `<meta name="description">` (70-160 chars), exactly one `<h1>` per page, and logical `<h2>`/`<h3>` hierarchy.
  - Check OpenGraph tags for rich social snippets and cross-indexer discovery.

### 1.2 Generative Engine Optimization (GEO) Specialist
- **AI Search Engines:** ChatGPT Search, Perplexity AI, Claude, Google AI Overviews (AIO), Microsoft Copilot.
- **Directives:**
  - **AI Bot Access:** Verify `robots.txt` explicitly allows modern retrieval agents (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Bytespider`, `CCBot`).
  - **Entity Disambiguation:** Verify Schema.org JSON-LD data (`Organization`, `Service`, `FAQPage`, `Article`).
  - **Extractability & Chunkability:** Content must provide direct answer nuggets (40-80 words), structured comparison tables, and question-based headers.
  - **LLM Context Standards:** Check for `/llms.txt` and `<link rel="describedby" href="...">` in HTML `<head>`.

### 1.3 Performance & Core Web Vitals Auditor
- **Tooling:** Lighthouse via `chrome-devtools` or `playwright`.
- **Directives:**
  - Audit Core Web Vitals: LCP ($\le 2.5\text{s}$), INP ($\le 200\text{ms}$), CLS ($\le 0.1$).
  - Measure Accessibility, Best Practices, and SEO scores.

---

## 2. Directory & Reporting Conventions

```text
website-auditor-skills/
├── AGENTS.md                          # Master directives (this document)
├── pyproject.toml                     # Python dependencies (managed via uv)
├── .agents/
│   └── skills/
│       └── website-audit/
│           ├── SKILL.md               # Main audit execution skill
│           ├── scripts/
│           │   ├── crawler.py         # Subdomain crawler (<300 lines)
│           │   └── seo_geo_check.py   # Multi-engine SEO/GEO analyzer (<300 lines)
│           └── references/
│               ├── seo_guidelines.md  # Multi-engine SEO rules
│               └── geo_guidelines.md  # GEO & AI search rules
└── audits/
    └── <sub.domain.me>/
        ├── context.md                 # User-provided context (optional intake)
        └── audit.md                   # Final standardized audit report
```

### Context Intake Rule
Before auditing a target domain `<sub.domain.me>`:
1. Check if `audits/<sub.domain.me>/context.md` exists. If present, load business goals, target audience, and key competitors.
2. **If missing:** Prompt the user interactively:
   > *"No context file found at `audits/<sub.domain.me>/context.md`. What is the primary target or business goal of this website, and who is the ideal audience?"*

### Report Delivery Rule
All audit reports must be saved directly to `audits/<sub.domain.me>/audit.md`.

---

## 3. Tooling & MCP Requirements

This repository requires one of the following browser MCP servers:
- **`chrome-devtools` (Recommended):** Provides `lighthouse_audit`, `navigate_page`, and performance tracing.
- **`playwright`:** Provides `browser_navigate`, `browser_snapshot`, and client-side DOM evaluation.

---

## 4. Execution Workflow

```mermaid
flowchart TD
    A["Target Domain: <sub.domain.me>"] --> B{"Context Intake"}
    B -->|"context.md exists"| C["Load Business Goals"]
    B -->|"Missing"| D["Prompt User for Target/Goal"]
    D --> C
    C --> E["Step 1: Subdomain Crawl (crawler.py)"]
    E --> F["URL Inventory & Status Codes"]
    C --> G["Step 2: SEO & GEO Check (seo_geo_check.py)"]
    G --> H["Robots, Schema, AI Bots, llms.txt"]
    C --> I["Step 3: Lighthouse Audit (MCP Tool)"]
    I --> J["Performance & Core Web Vitals"]
    F & H & J --> K["Synthesize Final Report"]
    K --> L["Save to audits/<sub.domain.me>/audit.md"]
```

### Quick Commands
```bash
# Run full subdomain crawl
uv run python .agents/skills/website-audit/scripts/crawler.py https://<sub.domain.me> -o /tmp/crawl.json

# Run multi-engine SEO and GEO analysis
uv run python .agents/skills/website-audit/scripts/seo_geo_check.py https://<sub.domain.me> -o /tmp/seo_geo.json

# Run all test suites
uv run pytest
```
