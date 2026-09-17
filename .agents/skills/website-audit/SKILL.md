---
name: website-audit
description: Comprehensive website audit evaluating Lighthouse metrics, technical SEO, and Generative Engine Optimization (GEO).
license: MIT
compatibility: opencode, copilot, antigravity
allowed-tools: read, write, bash, mcp
metadata:
  audience: developers
  workflow: audit
---

# Website Audit Skill

Performs in-depth technical SEO, Generative Engine Optimization (GEO), and Lighthouse performance audits for any web property.

## Prerequisites & Dependencies

1. **Python Tooling:** Python environment with `httpx` and `beautifulsoup4` (run via `uv run python`).
2. **MCP Browser Tools:** Requires either `chrome-devtools` (preferred for `lighthouse_audit`) or `playwright`.
3. **Helper Scripts:** Located in `.agents/skills/website-audit/scripts/`:
   - `crawler.py`: Asynchronous subdomain page discoverer and status code mapper.
   - `seo_geo_check.py`: Multi-engine SEO and GEO signal analyzer.

---

## Audit Workflow

### Step 1: Context Intake
Check for user context at `audits/<sub.domain.me>/context.md`:
- **If exists:** Read and incorporate the website's stated purpose, target audience, and primary competitors.
- **If missing:** Prompt the user before proceeding:
  > *"No context file found at `audits/<sub.domain.me>/context.md`. What is the primary target or business goal of this website, and who is the ideal audience?"*

### Step 2: Subdomain URL Discovery
For full-domain audits, crawl all accessible URLs on the subdomain:
```bash
uv run python .agents/skills/website-audit/scripts/crawler.py <target-url> --max-urls 50 -o /tmp/crawl.json
```
Extracts all discoverable URLs, HTTP status codes, titles, and canonical tags.

### Step 3: Multi-Engine SEO & GEO Analysis
Analyze robots.txt, Schema.org entities, AI bot permissions, and extractability signals:
```bash
uv run python .agents/skills/website-audit/scripts/seo_geo_check.py <target-url> -o /tmp/seo_geo.json
```
Evaluates:
- **SEO Engines:** Googlebot, Bingbot, Bravebot, sitemap references, meta tags, and canonical integrity.
- **GEO Engines:** ChatGPT Search (`GPTBot`), Claude (`ClaudeBot`), Perplexity (`PerplexityBot`), Gemini (`Google-Extended`), `llms.txt`, and Schema JSON-LD.

### Step 4: Browser & Lighthouse Performance
- Using `chrome-devtools`:
  1. Open page: `navigate_page(url)`
  2. Run audit: `lighthouse_audit(pageId=..., device="desktop", mode="navigation")`
- Alternatively, use `playwright` to evaluate DOM metrics, visual layouts, and network timings.

### Step 5: Generate the Final Audit Report
Compile findings into `audits/<sub.domain.me>/audit.md` using the Standard Report Template below.

---

## Standard Report Template (`audits/<sub.domain.me>/audit.md`)

```markdown
# Website Audit Report: <sub.domain.me>

**Audit Date:** YYYY-MM-DD  
**Audited Target:** https://<sub.domain.me>  
**Status:** Completed  

## 1. Executive Summary & Readiness Scores

| Audit Dimension | Score / Status | Assessment |
|---|---|---|
| **Lighthouse Performance & Best Practices** | Score / 100 | Fast, stable Core Web Vitals |
| **Traditional SEO (Google / Bing / Brave)** | Score / 100 | Metadata, canonicals, sitemap |
| **Generative Engine Optimization (GEO)** | Score / 100 | AI bots, llms.txt, Schema.org |

## 2. Full Subdomain URL Discovery

| URL | Status Code | Title | Canonical Tag | Issues Detected |
|---|---|---|---|---|
| `https://<domain>/` | 200 OK | Home Title | Matches | None |

## 3. Traditional SEO Diagnostics (Google, Bing, Brave)
- Indexability & Status Codes
- Metadata & OpenGraph
- Heading Hierarchy (H1, H2, H3)
- Sitemap & Robots.txt Declarations

## 4. Generative Engine Optimization (GEO) Diagnostics
- AI Crawler Permissions (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`)
- Schema.org Structured Data (`FAQPage`, `Organization`, `Service`)
- AI Discovery Standards (`/llms.txt`, `<link rel="describedby">`)
- Extractability & Answer Chunking (Direct answers, comparative tables)

## 5. Prioritized Action Plan
- **P0 (Immediate Fixes):** Blocking issues (4xx/5xx codes, missing titles, blocked bots).
- **P1 (High Impact):** Schema additions, llms.txt implementation, Core Web Vitals tuning.
- **P2 (Optimizations):** Meta description refinements, internal link expansion.
```
