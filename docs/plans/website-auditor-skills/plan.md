---
title: "Plan: Website Auditor Agents, Skills, and SEO/GEO Engine"
slug: "website-auditor-skills"
description: "Specialized agent configurations, skills, and tooling to audit websites for SEO, GEO, and Lighthouse metrics"
status: "Pending"
created: "2026-09-17"
updated: "2026-09-17"
tags:
  - seo
  - geo
  - lighthouse
  - agents
  - skills
  - audit
---

# Plan: Website Auditor Agents, Skills, and SEO/GEO Engine

## Objective

Establish a specialized agent audit environment with directives (`AGENTS.md`), modular skills in `.agents/`, automated crawling, and multi-engine SEO/GEO evaluation (Google, Bing, Brave, ChatGPT, Perplexity). Support structured reports in `audits/<sub.domain.me>/audit.md`, optional user context via `context.md` (or interactive goal prompts), and end-to-end verification against `mentoria24.com`.

## Requirements Snapshot

- **R1 (Agent Directives):** Create `AGENTS.md` with SEO/GEO Specialist directives, browser MCP prerequisites (`playwright` / `chrome-devtools`), and repository workflow instructions.
- **R2 (Agent Skills):** Implement website auditing skills inside `.agents/skills/website-audit/` with CLI scripts and clear instructions in `SKILL.md`.
- **R3 (Audit Output Structure):** Audit reports must be generated at `audits/<sub.domain.me>/audit.md`.
- **R4 (Context Intake & Prompting):** Read user-provided context at `audits/<sub.domain.me>/context.md`; if missing, interactively prompt for website goals and target audience.
- **R5 (Lighthouse & Multi-Engine SEO/GEO Metrics):** Audit combining Lighthouse data with indexing rules from Google, Bing, Brave, and Generative Engine Optimization (GEO) standards (entity schema, extractability, `llms.txt`, AI bot access).
- **R6 (Full Subdomain Crawl & URL Report):** Provide full subdomain crawling capability to discover all accessible pages, verify HTTP status codes, and run baseline SEO/GEO checks.
- **R7 (Test Verification):** Execute end-to-end audit on `mentoria24.com` validating the created environment and output report.

## Scope

- Python helper scripts for crawling (`crawler.py`) and SEO/GEO parsing (`seo_geo_check.py`) using `uv` with strict unit tests (`pytest`).
- `.agents/skills/website-audit/` containing `SKILL.md`, reference guides (`references/seo_guidelines.md`, `references/geo_guidelines.md`), and scripts.
- Root `AGENTS.md` covering agent protocols, MCP integrations, and audit output schemas.
- Sample context and verified audit report for `mentoria24.com`.
- Strict file length compliance (under 300 lines per file).

## Assumptions and Constraints

- **Python Toolchain:** `uv` is available at `~/.local/bin/uv` (Python 3.14).
- **MCP Servers:** `chrome-devtools` (with `lighthouse_audit`) and `playwright` are registered and available.
- **TDD:** Scripts must be developed test-first using `pytest`.
- **Line Limit:** All source and documentation files must strictly remain under 300 lines.

## Risks and Areas Requiring Care

- **Crawler Rate Limiting & Bot Blocking:** Certain servers return 403/503 to unknown user agents. Crawlers must set realistic User-Agents and respect polite concurrency.
- **SPA & Client-Side Rendering:** Modern sites (like Vite/React) rely on client-side hydration. Audits must blend static inspection (`curl`/`httpx`) with browser MCP rendering (`playwright`/`chrome-devtools`).
- **GEO Indexer Variability:** AI engines (Perplexity, Bing Copilot, OpenAI, Google AIO) have evolving requirements; guidelines must separate confirmed signals from experimental metrics.

## Core concepts

Generative Engine Optimization (GEO) differs from traditional SEO by optimizing for factual extraction, entity authority, and citation frequency in AI responses rather than blue link position.

```python
# Core GEO signal extraction example
def check_geo_signals(html: str, robots_txt: str) -> dict:
    has_llms_txt = 'rel="describedby"' in html and 'llms.txt' in html
    ai_bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]
    allowed_bots = [bot for bot in ai_bots if f"User-agent: {bot}\nAllow: /" in robots_txt]
    return {"llms_txt": has_llms_txt, "allowed_ai_bots": allowed_bots}
```

## Sub-Tasks

### Sub-Task 1: Environment & Project Setup

- **Status:** Completed
- **Objective:** Configure Python workspace with `uv`, `pyproject.toml`, and dependencies for crawling, HTML parsing, and testing.
- **Related Requirements:** R1, R6
- **Dependencies and Preconditions:** Empty workspace initialized.
- **In Scope for This Sub-Task:** Create `pyproject.toml` with `httpx`, `beautifulsoup4`, `pytest`, `pytest-asyncio`; configure `.gitignore`.
- **Out of Scope for This Sub-Task:** Implementation of audit logic or skills.
- **Instructions:** Initialize project via `uv init --no-pin` or minimal `pyproject.toml`, lock dependencies, and verify `pytest` runs.
- **Acceptance Criteria:** `uv run pytest` runs cleanly with 0 failures.
- **Cautionary Points:** Keep configuration minimal; avoid unused heavy dependencies.
- **Implementation Suggestions:** Use standard library where possible; keep files under 300 lines.
- **Testing Suggestions:** Run `uv run pytest` to verify test harness.
- **Done When:** Dependencies install cleanly and pytest passes.

### Sub-Task 2: Subdomain Crawler Engine with TDD

- **Status:** Completed
- **Objective:** Build an asynchronous subdomain crawler discovering internal URLs and recording status codes and basic tags.
- **Related Requirements:** R6
- **Dependencies and Preconditions:** Sub-Task 1 completed.
- **In Scope for This Sub-Task:** `tests/test_crawler.py` and `.agents/skills/website-audit/scripts/crawler.py` (<300 lines).
- **Out of Scope for This Sub-Task:** Complex browser execution (handled via MCP).
- **Instructions:** Write unit tests for URL normalization, scope boundary check (subdomain filtering), and async link extraction; then implement `crawler.py`.
- **Acceptance Criteria:** Crawler outputs a JSON/dict structure with `url`, `status_code`, `title`, `canonical`, and outgoing internal links.
- **Cautionary Points:** Avoid recursive infinite loops from calendar or query parameters; apply maximum depth and URL limits.
- **Implementation Suggestions:** Implement `SubdomainCrawler` class with bounded concurrency (`asyncio.Semaphore`).
- **Testing Suggestions:** Run `uv run pytest tests/test_crawler.py`.
- **Done When:** Crawler unit tests pass 100% and test crawls correctly respect domain boundaries.

### Sub-Task 3: Multi-Engine SEO & GEO Analyzer with TDD

- **Status:** Completed
- **Objective:** Build an SEO and GEO heuristic evaluation module verifying technical SEO, crawler accessibility, and AI extraction readiness.
- **Related Requirements:** R5
- **Dependencies and Preconditions:** Sub-Task 1 completed.
- **In Scope for This Sub-Task:** `tests/test_seo_geo_check.py` and `.agents/skills/website-audit/scripts/seo_geo_check.py` (<300 lines).
- **Out of Scope for This Sub-Task:** Running live Lighthouse audits (orchestrated in Sub-Task 4/6).
- **Instructions:** Write tests for robots.txt AI bot directives (`GPTBot`, `ClaudeBot`, `PerplexityBot`), Schema.org types, `llms.txt`, heading hierarchy, meta descriptions, and OpenGraph; then implement analyzer.
- **Acceptance Criteria:** Analyzer provides structured scores/findings across SEO (Google, Bing, Brave) and GEO (Perplexity, ChatGPT, Claude) categories.
- **Cautionary Points:** Handle malformed HTML and absent schema JSON-LD gracefully without throwing unhandled exceptions.
- **Implementation Suggestions:** Create clean functions/classes for `check_robots`, `check_schema_org`, and `check_geo_extractability`.
- **Testing Suggestions:** Run `uv run pytest tests/test_seo_geo_check.py`.
- **Done When:** All analyzer tests pass and produce clean diagnostic dictionaries.

### Sub-Task 4: Audit Skill & Knowledge References in `.agents/`

- **Status:** Completed
- **Objective:** Create `.agents/skills/website-audit/SKILL.md` along with reference documentation on modern SEO and GEO standards.
- **Related Requirements:** R2, R4, R5
- **Dependencies and Preconditions:** Sub-Tasks 2 and 3 completed.
- **In Scope for This Sub-Task:** `.agents/skills/website-audit/SKILL.md`, `references/seo_guidelines.md`, and `references/geo_guidelines.md`.
- **Out of Scope for This Sub-Task:** Test audit execution.
- **Instructions:** Write `SKILL.md` detailing the execution workflow: checking `audits/<sub.domain.me>/context.md` (or prompting user), running scripts, invoking MCP Lighthouse tools, and compiling `audit.md`.
- **Acceptance Criteria:** `SKILL.md` contains valid YAML frontmatter, step-by-step instructions, and output templates.
- **Cautionary Points:** Ensure file lengths remain under 300 lines. Split references into dedicated markdown files.
- **Implementation Suggestions:** Document both single-page quick audit and full subdomain audit flows.
- **Testing Suggestions:** Inspect skill structure using `view_file` and validate against agent guidelines.
- **Done When:** All skill files exist, adhere to rules, and are discoverable.

### Sub-Task 5: Master Directives (`AGENTS.md`)

- **Status:** Completed
- **Objective:** Create root `AGENTS.md` defining the SEO/GEO Specialist role, repository architecture, and execution contracts.
- **Related Requirements:** R1, R3, R4
- **Dependencies and Preconditions:** Sub-Task 4 completed.
- **In Scope for This Sub-Task:** Root `AGENTS.md` (<300 lines).
- **Out of Scope for This Sub-Task:** Modifying files outside documentation scope.
- **Instructions:** Document specialist personas (Technical SEO, GEO/LLM Grounding Specialist, Performance Auditor), directory conventions (`audits/<domain>/`), MCP requirements (`playwright`, `chrome-devtools`), and report templates.
- **Acceptance Criteria:** `AGENTS.md` provides complete operating instructions for any agent entering the workspace.
- **Cautionary Points:** Ensure instructions clearly state the interactive prompt fallback when `context.md` is absent.
- **Implementation Suggestions:** Include quick-start commands and clear Mermaid architecture diagrams.
- **Testing Suggestions:** Review `AGENTS.md` against prompt constraints.
- **Done When:** `AGENTS.md` is complete and within line limits.

### Sub-Task 6: Verification & End-to-End Audit on `mentoria24.com`

- **Status:** Pending
- **Objective:** Execute the entire audit pipeline on `mentoria24.com` and produce `audits/mentoria24.com/audit.md`.
- **Related Requirements:** R3, R4, R6, R7
- **Dependencies and Preconditions:** Sub-Tasks 1 through 5 completed.
- **In Scope for This Sub-Task:** Generate `audits/mentoria24.com/context.md` and `audits/mentoria24.com/audit.md`.
- **Out of Scope for This Sub-Task:** Modifying remote site content.
- **Instructions:** Run crawler on `mentoria24.com`, execute SEO/GEO analyzer, gather Lighthouse metrics via `chrome-devtools`, synthesize recommendations, and write final report.
- **Acceptance Criteria:** `audits/mentoria24.com/audit.md` contains full subdomain URL table with status codes, Lighthouse scores, SEO/GEO findings, and prioritized action plan.
- **Cautionary Points:** Respect site rate limits; do not flood the server.
- **Implementation Suggestions:** Incorporate live findings (e.g. `llms.txt`, Schema.org FAQPage/Service, modern robots.txt).
- **Testing Suggestions:** Validate output report markdown rendering and file existence.
- **Done When:** `audits/mentoria24.com/audit.md` is generated and verified complete.

## Final Integration & Verification

- **System-Wide Test:** Run `uv run pytest` across all test suites, verify `.agents/` skill discovery, and confirm `audits/mentoria24.com/audit.md` contains comprehensive analysis.
- **Completion Checklist:**
  - [ ] `pyproject.toml` and test suite configured with TDD.
  - [ ] `crawler.py` discovers URLs, maps status codes, and checks basic SEO tags.
  - [ ] `seo_geo_check.py` validates SEO and GEO standards.
  - [ ] `.agents/skills/website-audit/` structured with `SKILL.md` and references.
  - [ ] `AGENTS.md` documents specialist directives and MCP prerequisites.
  - [ ] `audits/mentoria24.com/audit.md` generated with full report.
  - [ ] All files strictly comply with the 300-line limit.

## Open Questions

- None. All requirements, tools, and test targets are well-defined.
