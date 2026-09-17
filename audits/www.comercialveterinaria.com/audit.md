# Website Audit Report: www.comercialveterinaria.com

**Audit Date:** 2026-09-17  
**Target Domain:** `https://www.comercialveterinaria.com/`  
**CMS / Platform:** PrestaShop 8 / PHP 8.3 / Nginx (Plesk)  
**Audit Protocol:** Technical SEO, Generative Engine Optimization (GEO), and Performance Readiness  
**Overall Status:** Needs Optimization (Significant Technical SEO & GEO Gaps)

---

## 1. Executive Summary & Readiness Scores

| Audit Dimension | Score | Status | Key Evaluation |
|---|:---:|:---:|---|
| **Technical SEO (Google, Bing, Brave)** | **65 / 100** | Warning | Sitemap missing from robots.txt, 404 on `/sitemap.xml`, missing OpenGraph, missing canonicals |
| **Generative Engine Optimization (GEO)**| **25 / 100** | Critical | 0 Schema.org JSON-LD entities, no `/llms.txt`, no entity disambiguation for AI engines |
| **AI Crawler & Retrieval Access** | **75 / 100** | Acceptable | Allowed by wildcard `*`, but lacks explicit `GPTBot`/`ClaudeBot`/`PerplexityBot` declarations |
| **Server & Edge Performance (TTFB)** | **50 / 100** | Warning | Slow TTFB ($1.34\text{s}$), uncompressed HTML ($311\text{KB}$), aggressive `no-store` headers |

---

## 2. Subdomain URL Inventory & Status Codes

Sample of 15 representative URLs from the 30-page subdomain crawl:

| Discovered URL | Status Code | Title Tag | Canonical Tag | Issues Detected |
|---|:---:|---|---|---|
| `https://www.comercialveterinaria.com/` | **200 OK** | Tienda de Mascotas Online | Self-referencing | Generic title, missing OG tags |
| `https://www.comercialveterinaria.com/contenido/politica-de-cookies.html` | **200 OK** | Politica de Cookies | **Missing** | Missing canonical tag |
| `https://www.comercialveterinaria.com/acuariofilia/` | **200 OK** | Acuariofilia en Burgos \| Acuarios, peces... | Valid | Good regional keyword focus |
| `https://www.comercialveterinaria.com/acuariofilia/acuarios-peceras/` | **200 OK** | Acuarios y peceras en Burgos... | Valid | Clean taxonomy |
| `https://www.comercialveterinaria.com/acuariofilia/estanques/` | **200 OK** | Productos para estanques en Burgos... | Valid | Category active |
| `https://www.comercialveterinaria.com/acuariofilia/acuarios-sumps/` | **200 OK** | Sump para acuario marino... | Valid | Good specialized terminology |
| `https://www.comercialveterinaria.com/acuariofilia/comida/` | **200 OK** | Comida para peces en Burgos... | Valid | Category active |
| `https://www.comercialveterinaria.com/acuariofilia/acuarios-temperatura/` | **200 OK** | Calentadores para acuarios... | Valid | Category active |
| `https://www.comercialveterinaria.com/acuariofilia/reactores-de-calcio/` | **200 OK** | reacteres calcio para acuarios | Valid | **Typo in `<title>`:** "reacteres" |
| `https://www.comercialveterinaria.com/perros/` | **200 OK** | Comida y accesorios para perros... | Valid | Main vertical |
| `https://www.comercialveterinaria.com/perros/alimentacion/` | **200 OK** | Alimentación para perros... | Valid | Category active |
| `https://www.comercialveterinaria.com/perros/alimentacion/pienso-para-perros/` | **200 OK** | Piensos para perros en Burgos... | Valid | Category active |
| `https://www.comercialveterinaria.com/perros/alimentacion/dieta-veterinaria-perros/` | **200 OK** | Dieta veterinaria perros en Burgos... | Valid | Specialized diet category |
| `https://www.comercialveterinaria.com/perros/vitaminas-y-suplementos/` | **200 OK** | Vitaminas y suplementos para perros... | Valid | Specialized category |
| `https://www.comercialveterinaria.com/perros/articulos-cachorros/` | **200 OK** | Artículos para cachorros... | Valid | Category active |

---

## 3. Technical SEO Diagnostics (Google, Bing, Brave)

### 3.1 Sitemap & Robots.txt Hygiene
- **Critical Sitemap Defect:** The standard endpoint `https://www.comercialveterinaria.com/sitemap.xml` returns **404 Not Found**. The real PrestaShop sitemap is located at `https://www.comercialveterinaria.com/1_index_sitemap.xml`.
- **Missing `Sitemap:` Directive:** `robots.txt` contains zero references to any sitemap.
- **Staging Domain Leak:** Line 69 of `robots.txt` publicly exposes the development domain: `# Directories for comercialveterinaria.difadi.net`.
- **Query Parameter Disallows:** Extensive `Disallow: /*?order=` and `Disallow: /*?search_query=` help prevent crawler crawl-budget waste on faceted navigation.

### 3.2 Metadata & Semantic HTML
- **Title Tag:** Homepage title is `Tienda de Mascotas Online` (25 characters). Lacks brand name (`Comercial Veterinaria`) and geographic anchor (`Burgos`).
- **Meta Description:** Present (`Tienda de mascotas online de productos especializados...`), length 168 chars (slightly exceeds 160 char snippet limit).
- **OpenGraph Tags:** Missing required OpenGraph tags (`og:title`, `og:description`, `og:image`, `og:url`), hurting social snippets and modern discovery tools.
- **Image Accessibility:** 23.9% of product/category images lack `alt` text.

---

## 4. Generative Engine Optimization (GEO) Diagnostics

Generative AI search engines (Perplexity, ChatGPT Search, Microsoft Copilot, Claude) rely on semantic structuring and explicit machine-readable context.

### 4.1 Schema.org Entity Grounding
- **Zero JSON-LD Detected:** No Schema.org entities (`OnlineStore`, `LocalBusiness`, `Organization`, `Product`, `AggregateOffer`, `BreadcrumbList`) are declared in the HTML header or body.
- **Impact:** AI engines cannot reliably disambiguate product pricing, stock availability, business physical location, or customer ratings.

### 4.2 LLM Context Standards (`llms.txt`)
- **Missing `llms.txt`:** `https://www.comercialveterinaria.com/llms.txt` returns **404 Not Found**.
- **Missing `<link rel="describedby">`:** No LLM manifest linking machine agents to structured documentation.

### 4.3 Content Chunking & Extractability
- Content consists primarily of PrestaShop category grids without conversational Q&A blocks or concise explanatory answers for common pet care queries.

---

## 5. Server & Edge Performance Diagnostics

- **Time to First Byte (TTFB):** $\approx 1.34\text{s}$ (exceeds Google's 800ms threshold; over 6x slower than optimal $\le 200\text{ms}$).
- **HTML Payload Size:** $311\text{KB}$ uncompressed for the root document alone.
- **Cache Policy:** `Cache-Control: no-store, no-cache, must-revalidate` on anonymous landing page requests, preventing reverse-proxy caching (Nginx/Cloudflare).
- **Cookies on Static Requests:** Sets two large PrestaShop session cookies on first visit, preventing static edge caching.

---

## 6. Prioritized Action Plan

### P0 (Immediate Fixes - Next 48 Hours)
1. **Fix Sitemap Discovery:** Add `Sitemap: https://www.comercialveterinaria.com/1_index_sitemap.xml` to `robots.txt` and create an Nginx rewrite from `/sitemap.xml` to `/1_index_sitemap.xml`.
2. **Clean `robots.txt`:** Remove the internal staging domain reference (`difadi.net`).
3. **Add Canonical to Legal Pages:** Add `<link rel="canonical" href="https://www.comercialveterinaria.com/contenido/politica-de-cookies.html">`.

### P1 (High Impact - Next 2 Weeks)
1. **Implement Schema.org JSON-LD:**
   - Add `LocalBusiness` / `Store` Schema with address in Burgos, opening hours, and phone contact.
   - Add `Product` and `Offer` Schema across product detail pages.
   - Add `BreadcrumbList` across all category pages.
2. **Expose `llms.txt`:** Create `/llms.txt` providing a concise overview of store specialties (veterinary diets, technical aquarium equipment, shipping coverage).
3. **Improve TTFB & Caching:** Configure microcaching or page caching for non-logged-in guest sessions in Nginx/PrestaShop to drop TTFB below 300ms.

### P2 (Optimizations - Next 30 Days)
1. **Refine Homepage Title:** Change to `Comercial Veterinaria | Tienda de Mascotas y Acuariofilia Online y en Burgos`.
2. **OpenGraph Tags:** Add standard `og:title`, `og:image`, and `og:description` tags.
3. **Fix Image Alt Attributes:** Audit product and banner uploads to ensure 100% `alt` tag coverage.
4. **Fix Editorial Typos:** Correct typos in category titles (e.g. `reacteres` -> `reactores de calcio`).
