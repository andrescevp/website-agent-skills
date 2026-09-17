# Modern Technical SEO Guidelines (Google, Bing, Brave)

Technical SEO ensures web properties are crawlable, indexable, performant, and correctly interpreted by major search engines.

## 1. Multi-Engine Indexer Landscape

| Indexer | Engine Characteristics | Key Ranking & Indexing Priorities |
|---|---|---|
| **Google** | World's primary indexer; Mobile-First Indexing | Core Web Vitals (LCP, INP, CLS), Helpful Content, E-E-A-T, mobile parity |
| **Bing** | Powers Bing, Yahoo, DuckDuckGo, Microsoft Copilot | Fast indexation via IndexNow, strict Schema.org fidelity, social signals |
| **Brave** | Completely independent web index (~10B+ pages) | Clean HTML, fast load times, manual URL submission via Brave Webmaster |

---

## 2. Technical SEO Checklist

### Crawlability & Indexation
- **Status Codes:** Ensure all public canonical URLs return `200 OK`. Immediately resolve `4xx` (broken links) and `5xx` (server errors).
- **Robots.txt:** Keep at the root (`/robots.txt`). Explicitly declare `Sitemap:` directive. Ensure search crawlers (`Googlebot`, `Bingbot`, `Bravebot`) are not accidentally blocked.
- **XML Sitemap:** Submit sitemap containing valid canonical URLs (`<loc>`, `<lastmod>`). Avoid redirecting or `noindex` URLs in sitemaps.
- **Canonicalization:** Every page must include `<link rel="canonical" href="...">` self-referencing the canonical URL to prevent duplicate content dilution.

### On-Page Metadata & Structure
- **Title Tag:** 30–65 characters. Clear brand identifier and primary topical keyword. Unique across all domain pages.
- **Meta Description:** 70–160 characters. Compelling summary with actionable value proposition.
- **Heading Structure:** Exactly one `<h1>` tag matching main page topic. Logical hierarchy (`<h2>` for major sections, `<h3>` for subsections).
- **OpenGraph & Social:** Include `og:title`, `og:description`, `og:image`, `og:url`, and `og:type` to maximize snippet fidelity across social sharing and discovery engines.

### Performance & Core Web Vitals
- **Largest Contentful Paint (LCP):** Target $\le 2.5\text{s}$. Preload hero assets and optimize server response times (TTFB).
- **Interaction to Next Paint (INP):** Target $\le 200\text{ms}$. Avoid heavy main-thread blocking JavaScript tasks.
- **Cumulative Layout Shift (CLS):** Target $\le 0.1$. Explicitly define `width` and `height` on all image and video elements.

### Image & Asset Hygiene
- Provide descriptive `alt` text for all informative images.
- Use modern formats (`.webp`, `.avif`, or optimized vector `.svg`).
- Enable compression and HTTP caching headers (`Cache-Control: public, max-age=...`).
