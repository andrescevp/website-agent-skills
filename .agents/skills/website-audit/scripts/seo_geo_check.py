#!/usr/bin/env python3
"""Multi-Engine SEO & GEO Analyzer for Website Audits.

Evaluates websites against Google, Bing, Brave, and AI Search Engines (Perplexity, ChatGPT, Claude).
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seo_geo_check")

KNOWN_AI_BOTS = [
    "GPTBot",
    "ClaudeBot",
    "PerplexityBot",
    "Google-Extended",
    "Bytespider",
    "CCBot",
]


def analyze_robots_txt(robots_text: str) -> Dict[str, Any]:
    """Analyze robots.txt for AI bots, indexers, and sitemaps."""
    lines = [line.strip() for line in robots_text.splitlines() if line.strip() and not line.startswith("#")]
    current_agents: List[str] = []
    rules: Dict[str, List[tuple[str, str]]] = {}
    sitemaps: List[str] = []

    for line in lines:
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip().lower(), val.strip()

        if key == "sitemap":
            sitemaps.append(val)
        elif key == "user-agent":
            current_agents.append(val)
        elif key in ("allow", "disallow"):
            for ag in current_agents:
                rules.setdefault(ag.lower(), []).append((key, val))
        else:
            current_agents = []

    ai_bot_status: Dict[str, str] = {}
    allowed_count = 0
    star_rules = rules.get("*", [])
    star_disallowed = any(r[0] == "disallow" and r[1] in ("/", "/*") for r in star_rules)

    for bot in KNOWN_AI_BOTS:
        bot_lower = bot.lower()
        if bot_lower in rules:
            has_disallow = any(r[0] == "disallow" and r[1] in ("/", "/*") for r in rules[bot_lower])
            has_allow = any(r[0] == "allow" and r[1] in ("/", "/*") for r in rules[bot_lower])
            if has_disallow and not has_allow:
                ai_bot_status[bot] = "blocked"
            else:
                ai_bot_status[bot] = "allowed"
                allowed_count += 1
        else:
            if star_disallowed:
                ai_bot_status[bot] = "blocked_by_wildcard"
            else:
                ai_bot_status[bot] = "allowed"
                allowed_count += 1

    score = int((allowed_count / max(len(KNOWN_AI_BOTS), 1)) * 100)
    return {
        "has_sitemap": len(sitemaps) > 0,
        "sitemaps": sitemaps,
        "ai_bots": ai_bot_status,
        "ai_crawler_score": score,
    }


def analyze_schema_ldjson(html: str) -> Dict[str, Any]:
    """Parse JSON-LD structured data and identify Schema.org entities."""
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    items: List[Dict[str, Any]] = []
    types: List[str] = []

    for tag in scripts:
        try:
            content = tag.string or tag.get_text()
            if not content:
                continue
            data = json.loads(content.strip())
            if isinstance(data, list):
                items.extend(data)
            elif isinstance(data, dict):
                items.append(data)
        except Exception:
            continue

    def extract_types(obj: Any) -> None:
        if isinstance(obj, dict):
            t = obj.get("@type")
            if t:
                if isinstance(t, list):
                    types.extend(t)
                else:
                    types.append(t)
            for v in obj.values():
                extract_types(v)
        elif isinstance(obj, list):
            for v in obj:
                extract_types(v)

    extract_types(items)
    unique_types = sorted(list(set(types)))

    return {
        "items": items,
        "types": unique_types,
        "has_faq": "FAQPage" in unique_types,
        "has_organization": "Organization" in unique_types,
        "has_service": "Service" in unique_types,
        "has_article": any(t in unique_types for t in ("Article", "NewsArticle", "BlogPosting")),
    }


def analyze_page_seo_geo(html: str, current_url: str) -> Dict[str, Any]:
    """Analyze traditional SEO signals and GEO extractability signals."""
    soup = BeautifulSoup(html, "html.parser")

    # Traditional SEO
    title_el = soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""
    title_valid = 10 <= len(title) <= 75

    desc_el = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    desc = desc_el.get("content", "").strip() if desc_el else ""
    desc_valid = 50 <= len(desc) <= 200

    canon_el = soup.find("link", attrs={"rel": re.compile(r"^canonical$", re.I)})
    canon = canon_el.get("href", "").strip() if canon_el else ""
    canonical_present = bool(canon)

    h1_tags = soup.find_all("h1")
    h1_count = len(h1_tags)
    h2_count = len(soup.find_all("h2"))
    h3_count = len(soup.find_all("h3"))

    og_tags = {
        prop: soup.find("meta", attrs={"property": f"og:{prop}"}) is not None
        for prop in ("title", "description", "type")
    }
    og_complete = all(og_tags.values())

    images = soup.find_all("img")
    images_with_alt = sum(1 for img in images if img.get("alt", "").strip())
    image_alt_coverage = (images_with_alt / len(images)) * 100 if images else 100.0

    # GEO Signals
    llms_txt_link = soup.find("link", attrs={"rel": "describedby", "href": re.compile(r"llms\.txt")})
    has_llms_txt_link = llms_txt_link is not None

    has_structured_faq = "FAQPage" in str(soup)
    has_tables = bool(soup.find_all("table"))
    has_lists = bool(soup.find_all(["ul", "ol"]))
    has_bullet_or_table_data = has_tables or has_lists

    return {
        "seo": {
            "title": title,
            "title_valid": title_valid,
            "description": desc,
            "description_valid": desc_valid,
            "canonical": canon,
            "canonical_present": canonical_present,
            "h1_count": h1_count,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "og_complete": og_complete,
            "image_alt_coverage": round(image_alt_coverage, 1),
        },
        "geo": {
            "has_llms_txt_link": has_llms_txt_link,
            "has_structured_faq": has_structured_faq,
            "has_bullet_or_table_data": has_bullet_or_table_data,
            "content_length_words": len(soup.get_text().split()),
        },
    }


def evaluate_full_audit(html: str, robots_txt: str, current_url: str) -> Dict[str, Any]:
    """Produce composite audit scores, findings, and recommendations."""
    robots_data = analyze_robots_txt(robots_txt)
    schema_data = analyze_schema_ldjson(html)
    page_data = analyze_page_seo_geo(html, current_url)

    seo = page_data["seo"]
    geo = page_data["geo"]

    # Calculate SEO score
    seo_pts = 0
    if seo["title_valid"]:
        seo_pts += 20
    if seo["description_valid"]:
        seo_pts += 20
    if seo["canonical_present"]:
        seo_pts += 20
    if seo["h1_count"] == 1:
        seo_pts += 20
    if seo["og_complete"]:
        seo_pts += 20

    # Calculate GEO score
    geo_pts = 0
    if geo["has_llms_txt_link"]:
        geo_pts += 30
    if schema_data["has_faq"] or geo["has_structured_faq"]:
        geo_pts += 25
    if schema_data["has_organization"] or schema_data["has_service"]:
        geo_pts += 20
    if geo["has_bullet_or_table_data"]:
        geo_pts += 25

    recs: List[str] = []
    if not seo["title_valid"]:
        recs.append("Optimize <title> tag to length between 30 and 65 characters.")
    if not seo["description_valid"]:
        recs.append("Add or refine meta description (70-160 characters).")
    if seo["h1_count"] != 1:
        recs.append(f"Ensure exactly one <h1> heading on the page (found {seo['h1_count']}).")
    if not geo["has_llms_txt_link"]:
        recs.append("Add <link rel='describedby' href='/llms.txt'> to expose authoritative LLM context.")
    if not schema_data["has_faq"]:
        recs.append("Incorporate Schema.org FAQPage for direct citation by AI search engines (Perplexity, Bing Copilot).")
    if robots_data["ai_crawler_score"] < 80:
        recs.append("Allow verified AI crawlers (GPTBot, ClaudeBot, PerplexityBot) in robots.txt for AI search grounding.")

    return {
        "url": current_url,
        "scores": {
            "traditional_seo": seo_pts,
            "geo_readiness": geo_pts,
            "ai_crawler_access": robots_data["ai_crawler_score"],
        },
        "robots": robots_data,
        "schema": schema_data,
        "page_signals": page_data,
        "recommendations": recs,
    }


def main() -> None:
    """CLI runner to evaluate an online URL."""
    parser = argparse.ArgumentParser(description="Multi-Engine SEO & GEO Analyzer")
    parser.add_argument("url", help="URL to audit (e.g. https://mentoria24.com)")
    parser.add_argument("--output", "-o", help="Output file for JSON report")
    args = parser.parse_args()

    url = args.url.rstrip("/")
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    headers = {"User-Agent": "Mozilla/5.0 (compatible; WebsiteAuditor/1.0)"}
    with httpx.Client(verify=False, timeout=12.0) as client:
        resp_html = client.get(url, headers=headers, follow_redirects=True)
        try:
            resp_robots = client.get(robots_url, headers=headers, follow_redirects=True)
            robots_txt = resp_robots.text if resp_robots.status_code == 200 else ""
        except Exception:
            robots_txt = ""

    result = evaluate_full_audit(resp_html.text, robots_txt, str(resp_html.url))
    output_str = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        logger.info("Saved analysis to %s", args.output)
    else:
        print(output_str)


if __name__ == "__main__":
    main()
