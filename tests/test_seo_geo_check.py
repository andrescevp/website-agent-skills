"""Unit tests for the Multi-Engine SEO & GEO Analyzer (TDD)."""

import json
from pathlib import Path
import sys
import pytest

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / ".agents" / "skills" / "website-audit" / "scripts"
sys.path.insert(0, str(scripts_dir))

from seo_geo_check import (
    analyze_robots_txt,
    analyze_schema_ldjson,
    analyze_page_seo_geo,
    evaluate_full_audit,
)


SAMPLE_ROBOTS_TXT = """
User-agent: Googlebot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: *
Allow: /

Sitemap: https://www.example.com/sitemap.xml
"""

SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Optimización Web y Mentoría IA en 24 Horas | Ejemplo</title>
  <meta name="description" content="Aprende y optimiza tus procesos con mentoría en IA práctica y directa con ingenieros expertos." />
  <link rel="canonical" href="https://www.example.com/" />
  <link rel="describedby" href="https://www.example.com/llms.txt" />
  <meta property="og:title" content="Optimización Web y Mentoría IA" />
  <meta property="og:description" content="Mentoría en IA práctica con ingenieros." />
  <meta property="og:type" content="website" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "¿Qué es la mentoría en IA?",
        "acceptedAnswer": {"@type": "Answer", "text": "Un programa práctico de 24 horas."}
      }
    ]
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Ejemplo IA",
    "url": "https://www.example.com"
  }
  </script>
</head>
<body>
  <h1>Aumenta tu productividad con IA</h1>
  <h2>Retos principales</h2>
  <p>Resumen claro y directo para usuarios y agentes IA.</p>
  <ul>
    <li>Automatización</li>
    <li>Ahorro de costes</li>
  </ul>
  <img src="/logo.png" alt="Logotipo Ejemplo" />
</body>
</html>
"""


def test_analyze_robots_txt():
    """Verify detection of modern search indexers and AI grounding bots in robots.txt."""
    result = analyze_robots_txt(SAMPLE_ROBOTS_TXT)
    assert result["has_sitemap"] is True
    assert "https://www.example.com/sitemap.xml" in result["sitemaps"]
    
    # Check AI bot permissions
    ai_bots = result["ai_bots"]
    assert ai_bots["GPTBot"] == "allowed"
    assert ai_bots["ClaudeBot"] == "allowed"
    assert ai_bots["PerplexityBot"] == "allowed"
    assert ai_bots["Google-Extended"] == "allowed"
    assert result["ai_crawler_score"] >= 80


def test_analyze_schema_ldjson():
    """Verify extraction and validation of Schema.org structured data."""
    schemas = analyze_schema_ldjson(SAMPLE_HTML)
    assert len(schemas["items"]) == 2
    assert "FAQPage" in schemas["types"]
    assert "Organization" in schemas["types"]
    assert schemas["has_faq"] is True
    assert schemas["has_organization"] is True


def test_analyze_page_seo_geo():
    """Verify traditional SEO elements and GEO extractability signals."""
    analysis = analyze_page_seo_geo(SAMPLE_HTML, "https://www.example.com/")
    
    # Traditional SEO
    assert analysis["seo"]["title_valid"] is True
    assert analysis["seo"]["description_valid"] is True
    assert analysis["seo"]["h1_count"] == 1
    assert analysis["seo"]["canonical_present"] is True
    assert analysis["seo"]["og_complete"] is True
    
    # GEO Signals
    assert analysis["geo"]["has_llms_txt_link"] is True
    assert analysis["geo"]["has_structured_faq"] is True
    assert analysis["geo"]["has_bullet_or_table_data"] is True


def test_evaluate_full_audit():
    """Verify composite audit scoring and recommendation generation."""
    audit = evaluate_full_audit(SAMPLE_HTML, SAMPLE_ROBOTS_TXT, "https://www.example.com/")
    assert audit["scores"]["traditional_seo"] >= 80
    assert audit["scores"]["geo_readiness"] >= 80
    assert audit["scores"]["ai_crawler_access"] >= 80
    assert "recommendations" in audit
