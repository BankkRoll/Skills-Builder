"""
Base Documentation Scraper

Abstract base class that provides common functionality for all documentation scrapers.
Extend this class to add support for new documentation platforms.
"""

import json
import re
import time
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from collections import deque
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

# Optional Playwright support
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass


class PlaywrightFetcher:
    """Fetches pages using Playwright for JavaScript rendering."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    def __enter__(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._page = self._browser.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page:
            self._page.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def fetch(self, url: str, wait_selector: str = "article, main, .prose") -> Optional[str]:
        """Fetch page and wait for content to render."""
        try:
            self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
            try:
                self._page.wait_for_selector(wait_selector, timeout=10000)
            except Exception:
                pass
            time.sleep(0.5)
            return self._page.content()
        except Exception as e:
            print(f"  Playwright error fetching {url}: {e}")
            return None


class BaseScraper(ABC):
    """
    Abstract base class for documentation scrapers.

    Subclasses should implement:
    - get_content_selectors(): CSS selectors for main content
    - get_nav_selectors(): CSS selectors for navigation
    - get_unwanted_selectors(): CSS selectors for elements to remove
    - get_wait_selector(): CSS selector to wait for (JS rendering)
    """

    # Platform identifier
    platform_name: str = "base"

    # Default settings (can be overridden by subclasses)
    default_use_browser: bool = True
    default_use_sitemap: bool = True

    def __init__(
        self,
        base_url: str,
        output_dir: str = "./scraped_docs",
        max_depth: int = 10,
        max_pages: int = 0,
        delay: float = 0.3,
        use_browser: Optional[bool] = None,
        use_sitemap: Optional[bool] = None,
        verbose: bool = False,
    ):
        # Ensure base_url ends with / for proper urljoin behavior
        self.base_url = base_url.rstrip("/") + "/"
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        self.verbose = verbose

        # Use class defaults if not specified
        if use_browser is None:
            use_browser = self.default_use_browser
        if use_sitemap is None:
            use_sitemap = self.default_use_sitemap

        self.use_browser = use_browser and PLAYWRIGHT_AVAILABLE
        self.use_sitemap = use_sitemap

        parsed = urlparse(self.base_url)
        self.base_domain = parsed.netloc
        self.base_path = parsed.path.rstrip("/")
        self.base_scheme = parsed.scheme

        self.visited: set[str] = set()
        self.pages: dict[str, dict] = {}
        self.nav_structure: list[dict] = []
        self.sitemap_urls: list[str] = []

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })

        self._browser_fetcher: Optional[PlaywrightFetcher] = None

        if use_browser and not PLAYWRIGHT_AVAILABLE:
            print("Warning: Playwright not installed. Install with: pip install playwright && playwright install chromium")
            print("Falling back to requests-based fetching.")
            self.use_browser = False

    # =========================================================================
    # Abstract methods - MUST be implemented by subclasses
    # =========================================================================

    @abstractmethod
    def get_content_selectors(self) -> list[str]:
        """Return CSS selectors for main content area, in priority order."""
        pass

    @abstractmethod
    def get_nav_selectors(self) -> list[str]:
        """Return CSS selectors for navigation/sidebar, in priority order."""
        pass

    @abstractmethod
    def get_unwanted_selectors(self) -> list[str]:
        """Return CSS selectors for elements to remove from content."""
        pass

    # =========================================================================
    # Optional overrides - subclasses CAN override these
    # =========================================================================

    def get_wait_selector(self) -> str:
        """Return CSS selector to wait for when using browser rendering."""
        return "article, main, .prose, .content"

    def get_skip_url_patterns(self) -> list[str]:
        """Return regex patterns for URLs to skip."""
        return [
            r"\.(pdf|zip|png|jpg|jpeg|gif|svg|ico|css|js|woff|woff2|ttf|eot)$",
            r"#",
            r"\?",
        ]

    def should_skip_url(self, url: str) -> bool:
        """Check if URL should be skipped. Override for custom logic."""
        parsed = urlparse(url)

        # Must be same domain
        if parsed.netloc != self.base_domain:
            return True

        # Must be under base path (if specified)
        if self.base_path and not parsed.path.startswith(self.base_path):
            return True

        # Check skip patterns
        for pattern in self.get_skip_url_patterns():
            if re.search(pattern, parsed.path, re.IGNORECASE):
                return True

        return False

    def extract_page_title(self, soup: BeautifulSoup) -> str:
        """Extract page title. Override for custom logic."""
        title_elem = soup.select_one("h1") or soup.select_one("title")
        if title_elem:
            title = title_elem.get_text(strip=True)
            # Remove site name suffix
            title = re.sub(r"\s*[|–-]\s*.*$", "", title)
            return title
        return ""

    def extract_page_description(self, soup: BeautifulSoup) -> str:
        """Extract page description. Override for custom logic."""
        desc_elem = soup.select_one('meta[name="description"]')
        if desc_elem:
            return desc_elem.get("content", "")
        return ""

    # =========================================================================
    # Core functionality - generally don't need to override
    # =========================================================================

    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message, flush=True)

    def normalize_url(self, url: str) -> str:
        """Normalize URL for comparison and storage."""
        parsed = urlparse(url)
        path = parsed.path.rstrip("/") or "/"
        return f"{parsed.scheme}://{parsed.netloc}{path}"

    def fetch_sitemap(self) -> list[str]:
        """Fetch URLs from sitemap.xml."""
        urls = []
        sitemap_locations = [
            f"{self.base_url}/sitemap.xml",
            f"{self.base_scheme}://{self.base_domain}/sitemap.xml",
            f"{self.base_scheme}://{self.base_domain}/docs/sitemap.xml",
        ]

        for sitemap_url in sitemap_locations:
            try:
                self.log(f"Checking sitemap: {sitemap_url}")
                response = self.session.get(sitemap_url, timeout=30)
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

                    for url_elem in root.findall(".//sm:url/sm:loc", ns):
                        url = url_elem.text
                        if url and not self.should_skip_url(url):
                            urls.append(url)

                    if not urls:
                        for url_elem in root.findall(".//url/loc"):
                            url = url_elem.text
                            if url and not self.should_skip_url(url):
                                urls.append(url)

                    if urls:
                        self.log(f"Found {len(urls)} URLs in sitemap")
                        return urls
            except Exception as e:
                self.log(f"  Sitemap error: {e}")

        return urls

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a page with retry logic for rate limiting."""
        html = None

        if self.use_browser and self._browser_fetcher:
            html = self._browser_fetcher.fetch(url, self.get_wait_selector())
        else:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 429:
                        # Rate limited - wait and retry
                        wait_time = (attempt + 1) * 5  # 5s, 10s, 15s
                        print(f"  Rate limited (429), waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    response.raise_for_status()
                    content_type = response.headers.get("content-type", "")
                    if "text/html" not in content_type:
                        return None
                    html = response.text
                    break
                except requests.RequestException as e:
                    if attempt < max_retries - 1:
                        self.log(f"  Retry {attempt + 1}/{max_retries} for {url}: {e}")
                        time.sleep(2)
                    else:
                        self.log(f"  Error fetching {url}: {e}")
                        return None

        if html:
            return BeautifulSoup(html, "lxml")
        return None

    def find_content_element(self, soup: BeautifulSoup) -> Optional[Tag]:
        """Find main content element using configured selectors."""
        for selector in self.get_content_selectors():
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if len(text) > 100:
                    return elem
        return soup.body

    def find_nav_element(self, soup: BeautifulSoup) -> Optional[Tag]:
        """Find navigation element using configured selectors."""
        for selector in self.get_nav_selectors():
            elem = soup.select_one(selector)
            if elem:
                return elem

        # Fallback: find any nav with doc links
        for nav_elem in soup.find_all("nav"):
            links = nav_elem.find_all("a", href=True)
            if links and any(not self.should_skip_url(urljoin(self.base_url, a.get("href", ""))) for a in links):
                return nav_elem

        return None

    def extract_navigation(self, soup: BeautifulSoup) -> list[dict]:
        """Extract navigation structure from page."""
        nav_items = []
        nav = self.find_nav_element(soup)

        if not nav:
            return nav_items

        for link in nav.find_all("a", href=True):
            href = link.get("href", "")
            text = link.get_text(strip=True)

            if text and href and not href.startswith(("#", "javascript:")):
                full_url = urljoin(self.base_url, href)
                if not self.should_skip_url(full_url):
                    nav_items.append({
                        "title": text,
                        "url": self.normalize_url(full_url),
                        "href": href
                    })

        return nav_items

    def extract_content(self, soup: BeautifulSoup, url: str) -> dict:
        """Extract main content from a page."""
        title = self.extract_page_title(soup)
        description = self.extract_page_description(soup)
        content_elem = self.find_content_element(soup)

        markdown = self.html_to_markdown(content_elem, url)

        # Extract internal links
        links = []
        if content_elem:
            for a in content_elem.find_all("a", href=True):
                href = a.get("href", "")
                full_url = urljoin(url, href)
                if not self.should_skip_url(full_url):
                    links.append(self.normalize_url(full_url))

        # Also check nav for links
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            full_url = urljoin(url, href)
            if not self.should_skip_url(full_url):
                links.append(self.normalize_url(full_url))

        return {
            "title": title,
            "description": description,
            "markdown": markdown,
            "links": list(set(links)),
            "url": url,
        }

    def html_to_markdown(self, element: Optional[Tag], base_url: str) -> str:
        """Convert HTML element to clean markdown."""
        if not element:
            return ""

        soup = BeautifulSoup(str(element), "lxml")

        # Remove unwanted elements
        for selector in self.get_unwanted_selectors():
            try:
                for unwanted in soup.select(selector):
                    unwanted.decompose()
            except Exception:
                pass

        return self._convert_element(soup.body or soup, base_url).strip()

    def _convert_element(self, element, base_url: str, depth: int = 0) -> str:
        """Recursively convert HTML elements to markdown."""
        if isinstance(element, NavigableString):
            text = str(element)
            if text.strip():
                return text
            return " " if text else ""

        if not isinstance(element, Tag):
            return ""

        tag = element.name.lower() if element.name else ""

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            text = element.get_text(strip=True)
            if text:
                return f"\n\n{'#' * level} {text}\n\n"

        elif tag == "p":
            inner = self._process_children(element, base_url, depth)
            if inner.strip():
                return f"\n\n{inner.strip()}\n\n"

        elif tag == "a":
            href = element.get("href", "")
            text = element.get_text(strip=True)
            if href and text:
                if not href.startswith(("http://", "https://", "#", "mailto:")):
                    href = urljoin(base_url, href)
                return f"[{text}]({href})"
            return text

        elif tag == "code":
            if element.parent and element.parent.name == "pre":
                return element.get_text()
            else:
                code = element.get_text()
                if code:
                    return f"`{code}`"
                return ""

        elif tag == "pre":
            code_elem = element.find("code")
            if code_elem:
                code = code_elem.get_text()
                lang = ""
                classes = code_elem.get("class", [])
                for cls in classes:
                    if isinstance(cls, str):
                        if cls.startswith("language-"):
                            lang = cls.replace("language-", "")
                            break
                        elif cls.startswith("lang-"):
                            lang = cls.replace("lang-", "")
                            break
                return f"\n\n```{lang}\n{code.strip()}\n```\n\n"
            else:
                return f"\n\n```\n{element.get_text().strip()}\n```\n\n"

        elif tag == "blockquote":
            inner = self._process_children(element, base_url, depth)
            lines = inner.strip().split("\n")
            quoted = "\n".join(f"> {line}" for line in lines)
            return f"\n\n{quoted}\n\n"

        elif tag in ("ul", "ol"):
            items = []
            for i, li in enumerate(element.find_all("li", recursive=False)):
                inner = self._process_children(li, base_url, depth + 1)
                prefix = "-" if tag == "ul" else f"{i + 1}."
                lines = inner.strip().split("\n")
                first_line = f"{prefix} {lines[0]}"
                rest = "\n".join("  " + line for line in lines[1:] if line.strip())
                items.append(first_line + ("\n" + rest if rest else ""))
            return "\n\n" + "\n".join(items) + "\n\n"

        elif tag == "li":
            return self._process_children(element, base_url, depth)

        elif tag == "strong" or tag == "b":
            text = element.get_text(strip=True)
            if text:
                return f"**{text}**"

        elif tag == "em" or tag == "i":
            text = element.get_text(strip=True)
            if text:
                return f"*{text}*"

        elif tag == "br":
            return "\n"

        elif tag == "hr":
            return "\n\n---\n\n"

        elif tag == "img":
            src = element.get("src", "")
            alt = element.get("alt", "image")
            if src:
                if not src.startswith(("http://", "https://", "data:")):
                    src = urljoin(base_url, src)
                return f"![{alt}]({src})"

        elif tag == "table":
            return self._convert_table(element)

        elif tag in ("div", "span", "section", "article", "main", "body", "html", "[document]"):
            return self._process_children(element, base_url, depth)

        return self._process_children(element, base_url, depth)

    def _process_children(self, element: Tag, base_url: str, depth: int = 0) -> str:
        """Process all children of an element."""
        parts = []
        for child in element.children:
            converted = self._convert_element(child, base_url, depth)
            if converted:
                parts.append(converted)
        return "".join(parts)

    def _convert_table(self, table: Tag) -> str:
        """Convert HTML table to markdown table."""
        rows = []
        headers = []

        thead = table.find("thead")
        if thead:
            for th in thead.find_all(["th", "td"]):
                headers.append(th.get_text(strip=True))

        if not headers:
            first_row = table.find("tr")
            if first_row:
                for cell in first_row.find_all(["th", "td"]):
                    headers.append(cell.get_text(strip=True))

        if headers:
            rows.append("| " + " | ".join(headers) + " |")
            rows.append("| " + " | ".join(["---"] * len(headers)) + " |")

        tbody = table.find("tbody") or table
        for tr in tbody.find_all("tr"):
            if not thead and tr == table.find("tr"):
                continue
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if cells:
                while len(cells) < len(headers):
                    cells.append("")
                rows.append("| " + " | ".join(cells[: len(headers)]) + " |")

        return "\n\n" + "\n".join(rows) + "\n\n" if rows else ""

    def crawl(self) -> None:
        """Crawl the documentation site."""
        print(f"Starting crawl of {self.base_url}", flush=True)
        print(f"Platform: {self.platform_name}", flush=True)
        print(f"Output directory: {self.output_dir}", flush=True)
        if self.use_browser:
            print("Using Playwright for JavaScript rendering", flush=True)

        if self.use_sitemap:
            self.sitemap_urls = self.fetch_sitemap()
            if self.sitemap_urls:
                print(f"Found {len(self.sitemap_urls)} URLs in sitemap", flush=True)

        context_manager = None
        if self.use_browser:
            context_manager = PlaywrightFetcher(headless=True)
            self._browser_fetcher = context_manager.__enter__()

        try:
            if self.sitemap_urls:
                self._crawl_from_sitemap()
            else:
                self._crawl_recursive()
        finally:
            if context_manager:
                context_manager.__exit__(None, None, None)
                self._browser_fetcher = None

        print(f"Crawl complete. Found {len(self.pages)} pages.", flush=True)

    def _crawl_from_sitemap(self) -> None:
        """Crawl using sitemap URLs."""
        urls_to_crawl = self.sitemap_urls
        if self.max_pages > 0:
            urls_to_crawl = urls_to_crawl[:self.max_pages]

        for i, url in enumerate(urls_to_crawl):
            normalized = self.normalize_url(url)
            if normalized in self.visited:
                continue

            self.visited.add(normalized)
            print(f"[{len(self.visited)}/{len(urls_to_crawl)}] Crawling: {url}", flush=True)

            soup = self.fetch_page(url)
            if not soup:
                continue

            if not self.nav_structure:
                self.nav_structure = self.extract_navigation(soup)

            page_data = self.extract_content(soup, url)

            if page_data["markdown"] and len(page_data["markdown"]) > 50:
                self.pages[normalized] = page_data
            else:
                self.log(f"  Skipped (no content): {url}")

            if self.delay > 0:
                time.sleep(self.delay)

    def _crawl_recursive(self) -> None:
        """Crawl recursively following links."""
        queue: deque[tuple[str, int]] = deque([(self.base_url, 0)])

        while queue:
            if self.max_pages > 0 and len(self.pages) >= self.max_pages:
                print(f"Reached max pages limit ({self.max_pages})", flush=True)
                break

            url, depth = queue.popleft()
            normalized = self.normalize_url(url)

            if normalized in self.visited:
                continue
            if depth > self.max_depth:
                continue

            self.visited.add(normalized)
            print(f"[{len(self.visited)}] Crawling: {url}", flush=True)

            soup = self.fetch_page(url)
            if not soup:
                continue

            if not self.nav_structure:
                self.nav_structure = self.extract_navigation(soup)
                for nav_item in self.nav_structure:
                    if nav_item["url"] not in self.visited:
                        queue.append((nav_item["url"], depth + 1))

            page_data = self.extract_content(soup, url)

            if page_data["markdown"] and len(page_data["markdown"]) > 50:
                self.pages[normalized] = page_data
            else:
                self.log(f"  Skipped (no content): {url}")

            for link in page_data["links"]:
                if link not in self.visited:
                    queue.append((link, depth + 1))

            if self.delay > 0:
                time.sleep(self.delay)

    def clean_markdown(self, text: str) -> str:
        """Clean up markdown formatting issues."""
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        text = text.strip() + "\n"
        return text

    def url_to_filepath(self, url: str) -> Path:
        """Convert URL to filesystem path."""
        parsed = urlparse(url)
        path = parsed.path.strip("/")

        if not path:
            path = "index"

        if self.base_path:
            base = self.base_path.strip("/")
            if path.startswith(base):
                path = path[len(base):].strip("/") or "index"

        parts = path.split("/")
        sanitized = []
        for part in parts:
            part = re.sub(r'[<>:"|?*]', "-", part)
            part = part.strip(".-")
            if part:
                sanitized.append(part)

        if not sanitized:
            sanitized = ["index"]

        return Path("/".join(sanitized) + ".md")

    def save(self) -> None:
        """Save scraped content to files."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for url, data in self.pages.items():
            filepath = self.output_dir / self.url_to_filepath(url)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            content_parts = []

            if data["title"]:
                content_parts.append(f"# {data['title']}\n")

            if data["description"]:
                content_parts.append(f"\n> {data['description']}\n")

            content_parts.append(f"\n<!-- Source: {url} -->\n")
            content_parts.append("\n" + data["markdown"])

            content = self.clean_markdown("\n".join(content_parts))
            filepath.write_text(content, encoding="utf-8")
            self.log(f"  Saved: {filepath}")

        nav_file = self.output_dir / "_navigation.json"
        nav_file.write_text(json.dumps(self.nav_structure, indent=2), encoding="utf-8")

        self._create_index()

        print(f"Saved {len(self.pages)} files to {self.output_dir}")

    def _create_index(self) -> None:
        """Create an index file with links to all pages."""
        index_path = self.output_dir / "_index.md"

        lines = [
            "# Documentation Index",
            f"\n> Scraped from {self.base_url}",
            f"\n> Platform: {self.platform_name}",
            "\n## Pages\n",
        ]

        sorted_pages = sorted(self.pages.items(), key=lambda x: self.url_to_filepath(x[0]))

        current_section = ""
        for url, data in sorted_pages:
            filepath = self.url_to_filepath(url)
            parts = str(filepath).split("/")

            if len(parts) > 1:
                section = parts[0].replace("-", " ").title()
                if section != current_section:
                    current_section = section
                    lines.append(f"\n### {section}\n")

            title = data["title"] or filepath.stem.replace("-", " ").title()
            lines.append(f"- [{title}]({filepath})")

        index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
