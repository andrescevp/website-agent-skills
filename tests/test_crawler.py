"""Unit tests for the Subdomain Crawler Engine (TDD)."""

import pytest
from unittest.mock import AsyncMock, patch
import httpx


# Import the module to test (will be created in .agents/skills/website-audit/scripts/crawler.py)
import sys
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent / ".agents" / "skills" / "website-audit" / "scripts"
sys.path.insert(0, str(scripts_dir))

from crawler import SubdomainCrawler, PageResult, CrawlReport


def test_normalize_url_resolves_relative_and_strips_fragments():
    """Test URL normalization for absolute, relative, and fragmented links."""
    crawler = SubdomainCrawler("https://example.com")
    
    # Relative path
    assert crawler.normalize_url("/about", "https://example.com") == "https://example.com/about"
    # Fragment stripping
    assert crawler.normalize_url("/about#team", "https://example.com") == "https://example.com/about"
    # Scheme relative
    assert crawler.normalize_url("//example.com/contact", "https://example.com") == "https://example.com/contact"
    # Non-HTTP schemes ignored
    assert crawler.normalize_url("mailto:info@example.com", "https://example.com") is None
    assert crawler.normalize_url("tel:+123456789", "https://example.com") is None
    assert crawler.normalize_url("javascript:void(0)", "https://example.com") is None


def test_is_in_scope():
    """Test domain/subdomain boundary checking."""
    crawler = SubdomainCrawler("https://example.com")
    
    assert crawler.is_in_scope("https://example.com/page1") is True
    assert crawler.is_in_scope("https://www.example.com/page1") is True
    assert crawler.is_in_scope("https://sub.example.com/page1") is True
    assert crawler.is_in_scope("https://otherdomain.com/page1") is False


def test_extract_page_metadata():
    """Test HTML parsing for basic SEO tags and links."""
    crawler = SubdomainCrawler("https://example.com")
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Test Page Title</title>
        <meta name="description" content="This is a test description." />
        <link rel="canonical" href="https://example.com/canonical" />
        <meta name="robots" content="index, follow" />
      </head>
      <body>
        <h1>Hello</h1>
        <a href="/about">About Us</a>
        <a href="https://external.org/info">External Info</a>
      </body>
    </html>
    """
    metadata = crawler.parse_html(html, "https://example.com")
    assert metadata["title"] == "Test Page Title"
    assert metadata["description"] == "This is a test description."
    assert metadata["canonical"] == "https://example.com/canonical"
    assert metadata["robots"] == "index, follow"
    assert "https://example.com/about" in metadata["internal_links"]
    assert "https://external.org/info" in metadata["external_links"]


@pytest.mark.asyncio
async def test_crawl_traversal():
    """Test asynchronous crawling traversal of mock pages."""
    crawler = SubdomainCrawler("https://example.com", max_urls=5)

    pages = {
        "https://example.com": (
            200,
            "text/html",
            '<title>Home</title><a href="/page1">P1</a><a href="/page2">P2</a>',
        ),
        "https://example.com/page1": (
            200,
            "text/html",
            "<title>Page 1</title><a href='/page2'>P2</a>",
        ),
        "https://example.com/page2": (
            404,
            "text/html",
            "<title>Not Found</title>",
        ),
    }

    async def mock_get(url, *args, **kwargs):
        norm_url = str(url).rstrip("/")
        # check base
        if norm_url == "https://example.com":
            key = "https://example.com"
        else:
            key = norm_url
        
        if key in pages:
            status, ctype, body = pages[key]
            return httpx.Response(
                status_code=status,
                headers={"content-type": ctype},
                text=body,
                request=httpx.Request("GET", url),
            )
        return httpx.Response(404, request=httpx.Request("GET", url))

    with patch.object(httpx.AsyncClient, "get", new=AsyncMock(side_effect=mock_get)):
        report = await crawler.crawl()

    assert isinstance(report, CrawlReport)
    assert report.total_crawled == 3
    urls_crawled = [p.url.rstrip("/") for p in report.pages]
    assert "https://example.com" in urls_crawled
    assert "https://example.com/page1" in urls_crawled
    assert "https://example.com/page2" in urls_crawled
    
    # Find 404 page in results
    page2 = next(p for p in report.pages if p.url.rstrip("/") == "https://example.com/page2")
    assert page2.status_code == 404
