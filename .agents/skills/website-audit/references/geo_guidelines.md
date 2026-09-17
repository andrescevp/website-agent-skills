# Generative Engine Optimization (GEO) Guidelines

Generative Engine Optimization (GEO) is the discipline of optimizing digital content to be selected, synthesized, and cited by AI engines—such as **ChatGPT Search**, **Perplexity**, **Google AI Overviews (AIO)**, **Microsoft Copilot**, and **Claude**.

## 1. Traditional SEO vs. Generative Engine Optimization

| Dimension | Traditional SEO | Generative Engine Optimization (GEO) |
|---|---|---|
| **Primary Goal** | Rank high in search result blue links | Be cited as an authoritative source in AI answers |
| **Success Metric** | Impressions, CTR, organic clicks | Citation share, entity grounding, brand mentions |
| **Format Preference**| Keyword-focused page content | Chunkable, direct answer nuggets with factual proof |
| **Traffic Dynamics**| Direct traffic to page destination | Zero-click answers, high-intent citation traffic |

---

## 2. Core Pillars of Generative Engine Optimization

### Pillar 1: Content Extractability & Chunkability
- **Answer First (Direct Answers):** Open major sections with a 40–80 word direct answer to the user's intent. AI retrieval agents prefer concise, self-contained paragraphs.
- **Header-as-Question Architecture:** Use `<h2>` and `<h3>` tags phrased as natural language questions that users ask AI assistants.
- **Structured Data Formats:** Incorporate comparative Markdown/HTML tables and concise bulleted lists. AI models prioritize tabular and structured data for entity comparison.
- **Factual Grounding:** Pair claims with verifiable numbers, metrics, or technical specifics. Original proprietary data is a primary citation magnet.

### Pillar 2: AI Crawler & Ingestion Access
Verify `robots.txt` explicitly permits modern AI retrieval agents:
- **`GPTBot`:** OpenAI ChatGPT Search and model grounding.
- **`ClaudeBot`:** Anthropic Claude web search and grounding.
- **`PerplexityBot`:** Perplexity AI real-time search engine.
- **`Google-Extended` & `GoogleOther`:** Gemini and Vertex AI ingestion.
- **`Bytespider` & `CCBot`:** Global indexers and open research datasets.

### Pillar 3: Semantic Schema & LLM Discovery Files
- **Schema.org Structured Data:**
  - `FAQPage`: Explicit Question/Answer entities for direct citation.
  - `Organization` & `Service`: Disambiguates brand identity, offers, and geographic scope.
  - `Article` & `Author`: Provides verifiable author E-E-A-T credentials.
- **The `llms.txt` Standard:**
  - Expose `/llms.txt` and `/llms-full.txt` at domain root.
  - Declare in HTML `<head>`: `<link rel="describedby" href="https://<domain>/llms.txt">`.
  - Provides a curated Markdown overview designed specifically for agent consumption without scraping noise.

### Pillar 4: Topical Authority & Citation Consensus
- Deep topical coverage across interrelated concepts builds strong entity associations in LLM knowledge graphs.
- Cross-platform citations and brand mentions across news, social platforms, and technical repositories reinforce grounding confidence.
