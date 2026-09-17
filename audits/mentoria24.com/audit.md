# Website Audit Report: mentoria24.com

**Audit Date:** 2026-09-17  
**Target Domain:** `https://mentoria24.com` (Canonical: `https://www.mentoria24.com/`)  
**Audit Protocol:** Technical SEO, Generative Engine Optimization (GEO), and Lighthouse Performance  
**Overall Readiness Status:** Production-Ready (High Authority & Grounding)

---

## 1. Executive Summary & Readiness Scores

| Audit Dimension | Score | Status | Key Evaluation |
|---|:---:|:---:|---|
| **Technical SEO (Google, Bing, Brave)** | **100 / 100** | Optimal | Clean 301 apex redirect, canonical self-reference, valid metadata, 100% image alt tags |
| **Generative Engine Optimization (GEO)**| **100 / 100** | Optimal | `llms.txt` exposed, Schema FAQPage + Service + Org, direct answer nuggets |
| **AI Crawler & Grounding Permissions** | **100 / 100** | Optimal | Explicit allowances for GPTBot, ClaudeBot, PerplexityBot, Google-Extended in robots.txt |
| **Server & Edge Performance (TTFB)** | **95 / 100** | Optimal | TTFB $\approx 169\text{ms}$, total load $\approx 259\text{ms}$, compressed assets |

---

## 2. Full Subdomain URL Inventory & Status Codes

Discovered via BFS crawl starting from `https://mentoria24.com`:

| Discovered URL | Status Code | Content-Type | Title Tag | Canonical Tag | Indexability |
|---|:---:|---|---|---|:---:|
| `https://www.mentoria24.com/` | **200 OK** | `text/html` | Mentoría IA en 24 Horas \| Mentoria 24 | Self-referencing | Index, Follow |
| `https://www.mentoria24.com/privacidad` | **200 OK** | `text/html` | Política de Privacidad \| Mentoria 24 | Self-referencing | Noindex, Follow |
| `https://www.mentoria24.com/dossier-ventas-mentoria24.pdf` | **200 OK** | `application/pdf` | *(Binary Document)* | N/A | Downloadable Asset |
| `https://mentoria24.com` | **301 Redirect**| N/A | Redirects to `https://www.mentoria24.com/` | Target Canonical | Canonical Redirect |

*Zero broken links (4xx) or server errors (5xx) detected across the domain crawl.*

---

## 3. Technical SEO Diagnostics (Google, Bing, Brave)

### 3.1 Metadata & Headings Hygiene
- **Page Title:** `Mentoría IA en 24 Horas | Mentoria 24` (39 characters — within 30–65 target range).
- **Meta Description:** `Reduce tu tiempo de trabajo y gana autonomía tecnológica con nuestra mentoría 1:1 en IA de 24 horas. Ingenieros expertos, resultados desde la sesión 1.` (150 characters — within 70–160 target range).
- **Heading Hierarchy:**
  - Exactly one `<h1>`: *"Aumenta tu productividad, reduce a la mitad las tareas repetitivas y recorta costes con nuestra mentoría 1:1."*
  - 9 `<h2>` section headers logically structuring pain points, program modules, engineering team, and FAQs.
  - 17 `<h3>` subsection items breaking down specific learning milestones.
- **OpenGraph Tags:** Complete (`og:title`, `og:description`, `og:type="website"`, `og:url`).

### 3.2 Crawlability & Sitemaps
- **Robots.txt:** Located at `/robots.txt` with HTTP 200.
- **XML Sitemap:** Declared at `https://www.mentoria24.com/sitemap.xml`. Contains clean canonical endpoints.
- **Indexation Directives:** Main landing uses `max-snippet:-1, max-image-preview:large, max-video-preview:-1`, maximizing snippet exposure on Google and Bing SERPs.

---

## 4. Generative Engine Optimization (GEO) Diagnostics

Mentoria 24 exhibits best-in-class preparation for generative search engines (ChatGPT Search, Perplexity, Claude, Google AIO, Microsoft Copilot).

### 4.1 AI Retrieval Agent Access
The `robots.txt` configuration explicitly permits all major LLM search bots:
- `GPTBot` (OpenAI / ChatGPT Search): **Allowed**
- `ClaudeBot` (Anthropic / Claude Grounding): **Allowed**
- `PerplexityBot` (Perplexity AI Search): **Allowed**
- `Google-Extended` & `GoogleOther` (Gemini & Vertex AI): **Allowed**
- `Bytespider` & `CCBot`: **Allowed**

### 4.2 Semantic Structured Data (JSON-LD)
Three comprehensive Schema.org schemas are embedded:
1. **`FAQPage` Schema:** 6 structured questions covering program duration, audience, required technical level, tools used, and safety/security. Directly enables zero-click conversational extraction.
2. **`Service` Schema:** Declares `serviceType="Mentoring Program"`, `areaServed="ES"`, and provider organization.
3. **`Organization` Schema:** Anchors brand identity, URL, and corporate description.

### 4.3 LLM Context Standards (`llms.txt`)
- Declared in HTML `<head>`: `<link rel="describedby" href="https://www.mentoria24.com/llms.txt" />`.
- Exposes both `/llms.txt` (concise program overview) and `/llms-full.txt` (exhaustive specification for AI models), providing factual grounding for LLM agents.

---

## 5. Performance & Network Timings

- **DNS Resolution:** $\approx 1.2\text{ms}$
- **TLS Handshake:** $\approx 100\text{ms}$
- **Time to First Byte (TTFB):** $\approx 169\text{ms}$ (well under the 800ms Core Web Vitals threshold)
- **Total Transfer Time:** $\approx 259\text{ms}$
- **Static Assets:** Cleanly bundled into immutable hashed chunks (`app-Dm61jsCJ.js`, `app-DI430AGz.css`).

---

## 6. Action Plan & Recommendations

### P0 (Blocking Issues)
- *None detected.* The site is fully functional, crawlable, and indexable.

### P1 (High Impact Enhancements)
1. **Brave Search URL Submission:** Submit `https://www.mentoria24.com/` directly via `search.brave.com/submit-url` to accelerate discovery on Brave's independent index.
2. **Bing Webmaster Tools & IndexNow:** Ensure IndexNow API integration is active to notify Bing and Copilot instantly upon content updates.

### P2 (Continuous Optimizations)
1. **Case Studies Schema:** Consider adding `Review` or `AggregateRating` structured data when verifiable client testimonials or case studies are published.
2. **BreadcrumbList Schema:** If additional programmatic routes are introduced, incorporate `BreadcrumbList` JSON-LD to enhance rich snippets.
