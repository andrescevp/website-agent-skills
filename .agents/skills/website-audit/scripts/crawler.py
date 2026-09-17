#!/usr/bin/env python3
"""Asynchronous Subdomain Crawler for Website Audits.

Discovers accessible pages, records HTTP status codes, and extracts basic SEO tags.
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import asdict, dataclass, field
import json
import logging
import re
import sys
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("crawler")


@dataclass
class PageResult:
    """Represents the audit result for a single URL."""

    url: str
    status_code: int
    content_type: str = ""
    title: str = ""
    canonical: str = ""
    description: str = ""
    robots: str = ""
    internal_links: List[str] = field(default_factory=list)
    external_links: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class CrawlReport:
    """Represents the aggregated crawl report for a subdomain."""

    base_url: str
    total_crawled: int
    pages: List[PageResult] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert report to serializable dictionary."""
        return {
            "base_url": self.base_url,
            "total_crawled": self.total_crawled,
            "pages": [asdict(p) for p in self.pages],
        }


class SubdomainCrawler:
    """Crawls pages strictly within the target subdomain boundary."""

    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36 WebsiteAuditorBot/1.0"
    )

    def __init__(
        self,
        base_url: str,
        max_urls: int = 100,
        max_depth: int = 3,
        concurrency: int = 5,
        timeout: float = 12.0,
        user_agent: Optional[str] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        parsed = urlparse(self.base_url)
        self.scheme = parsed.scheme or "https"
        self.target_host = parsed.netloc.lower()
        self.domain_root = self._extract_root_domain(self.target_host)
        self.max_urls = max_urls
        self.max_depth = max_depth
        self.concurrency = concurrency
        self.timeout = timeout
        self.user_agent = user_agent or self.DEFAULT_USER_AGENT
        self.semaphore = asyncio.Semaphore(concurrency)
        self.visited: Set[str] = set()

    @staticmethod
    def _extract_root_domain(netloc: str) -> str:
        parts = netloc.split(":")[0].split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return netloc

    def normalize_url(self, raw_url: str, current_url: str) -> Optional[str]:
        """Normalize URL, resolve relative paths, strip fragments and non-http schemes."""
        if not raw_url:
            return None
        raw_url = raw_url.strip()
        if raw_url.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            return None

        joined = urljoin(current_url, raw_url)
        parsed = urlparse(joined)
        if parsed.scheme not in ("http", "https"):
            return None

        netloc = parsed.netloc.lower()
        path = parsed.path or "/"
        # Normalize duplicate slashes in path
        path = re.sub(r"/+", "/", path)
        query = f"?{parsed.query}" if parsed.query else ""
        return f"{parsed.scheme}://{netloc}{path}{query}"

    def is_in_scope(self, url: str) -> bool:
        """Check if URL belongs to the target domain/subdomain."""
        parsed = urlparse(url)
        host = parsed.netloc.lower().split(":")[0]
        if not host:
            return False
        return host == self.target_host or host.endswith(f".{self.domain_root}") or host == self.domain_root

    def parse_html(self, html: str, current_url: str) -> Dict:
        """Parse HTML string and extract metadata and outgoing links."""
        soup = BeautifulSoup(html, "html.parser")
        title_el = soup.find("title")
        title = title_el.get_text(strip=True) if title_el else ""

        desc_el = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        description = desc_el.get("content", "").strip() if desc_el else ""

        robots_el = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
        robots = robots_el.get("content", "").strip() if robots_el else ""

        canon_el = soup.find("link", attrs={"rel": re.compile(r"^canonical$", re.I)})
        canonical = canon_el.get("href", "").strip() if canon_el else ""

        internal_links: List[str] = []
        external_links: List[str] = []

        for anchor in soup.find_all("a", href=True):
            resolved = self.normalize_url(anchor["href"], current_url)
            if not resolved:
                continue
            if self.is_in_scope(resolved):
                if resolved not in internal_links:
                    internal_links.append(resolved)
            else:
                if resolved not in external_links:
                    external_links.append(resolved)

        return {
            "title": title,
            "description": description,
            "canonical": canonical,
            "robots": robots,
            "internal_links": internal_links,
            "external_links": external_links,
        }

    async def _fetch(self, client: httpx.AsyncClient, url: str) -> PageResult:
        async with self.semaphore:
            headers = {"User-Agent": self.user_agent, "Accept": "text/html,application/xhtml+xml"}
            try:
                resp = await client.get(url, headers=headers, timeout=self.timeout, follow_redirects=True)
                content_type = resp.headers.get("content-type", "").lower()
                final_url = str(resp.url)

                if "text/html" in content_type:
                    meta = self.parse_html(resp.text, final_url)
                    return PageResult(
                        url=final_url,
                        status_code=resp.status_code,
                        content_type=content_type,
                        title=meta["title"],
                        canonical=meta["canonical"],
                        description=meta["description"],
                        robots=meta["robots"],
                        internal_links=meta["internal_links"],
                        external_links=meta["external_links"],
                    )
                return PageResult(
                    url=final_url,
                    status_code=resp.status_code,
                    content_type=content_type,
                )
            except Exception as exc:
                return PageResult(url=url, status_code=0, error=str(exc))

    async def crawl(self) -> CrawlReport:
        """Perform breadth-first traversal across subdomain URLs."""
        queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue()
        queue.put_nowait((self.base_url, 0))
        self.visited.add(self.base_url)
        pages: List[PageResult] = []

        limits = httpx.Limits(max_keepalive_connections=10, max_connections=self.concurrency)
        async with httpx.AsyncClient(limits=limits, verify=False) as client:
            while not queue.empty() and len(self.visited) <= self.max_urls:
                current_url, depth = await queue.get()
                result = await self._fetch(client, current_url)
                pages.append(result)

                if depth < self.max_depth and result.status_code == 200:
                    for link in result.internal_links:
                        norm = link.rstrip("/")
                        if norm not in self.visited and len(self.visited) < self.max_urls:
                            self.visited.add(norm)
                            queue.put_nowait((link, depth + 1))
                queue.task_done()

        return CrawlReport(base_url=self.base_url, total_crawled=len(pages), pages=pages)


def main() -> None:
    """CLI entry point for standalone crawl runs."""
    parser = argparse.ArgumentParser(description="Subdomain Crawler for Website Audits")
    parser.add_argument("url", help="Target start URL (e.g. https://mentoria24.com)")
    parser.add_argument("--max-urls", type=int, default=50, help="Maximum URLs to crawl")
    parser.add_argument("--max-depth", type=int, default=3, help="Max crawling depth")
    parser.add_argument("--output", "-o", help="Path to write JSON output report")
    args = parser.parse_args()

    crawler = SubdomainCrawler(args.url, max_urls=args.max_urls, max_depth=args.max_depth)
    report = asyncio.run(crawler.crawl())

    out_data = json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_data)
        logger.info("Report written to %s (%d pages)", args.output, report.total_crawled)
    else:
        print(out_data)


if __name__ == "__main__":
    main()
