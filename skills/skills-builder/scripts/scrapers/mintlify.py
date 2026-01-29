"""
Mintlify Documentation Scraper

Specialized scraper for Mintlify-powered documentation sites.
Handles JS-rendered content and Mintlify-specific page structure.

Version Handling:
- Mintlify uses custom folder-based versions defined in mint.json
- Common patterns: /v1/, /v2/, /api/, /sdk/, etc.
- If user passes a versioned URL, only that version/section is scraped
- Otherwise, we stay within the detected path prefix
"""

import re
from .base import BaseScraper


class MintlifyScraper(BaseScraper):
    """Scraper optimized for Mintlify documentation sites."""

    platform_name = "mintlify"

    # Mintlify sites are JS-rendered, so browser is essential
    default_use_browser = True
    default_use_sitemap = True

    # Mintlify version/section patterns - common folder structures
    VERSION_PATTERNS = [
        r"^/(v\d+(?:\.\d+)*)(/|$)",           # /v1/, /v2.0/
        r"^/(api(?:-v?\d+)?)(/|$)",            # /api/, /api-v2/
        r"^/(sdk(?:-v?\d+)?)(/|$)",            # /sdk/, /sdk-v2/
        r"^/(\d+\.\d+(?:\.\d+)?)(/|$)",       # /1.0/, /2.3.1/
        r"^/(latest|stable|legacy)(/|$)",     # /latest/, /stable/
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Detect version/section from base URL path
        self._target_version = self._detect_version(self.base_path)
        if self._target_version:
            print(f"Targeting version/section: {self._target_version}", flush=True)

    def _detect_version(self, path: str) -> str | None:
        """Detect if path contains a version/section identifier."""
        for pattern in self.VERSION_PATTERNS:
            match = re.search(pattern, path)
            if match:
                return match.group(1)
        return None

    def _get_url_version(self, url: str) -> str | None:
        """Extract version/section from a URL's path."""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return self._detect_version(parsed.path)

    def _is_different_version(self, url: str) -> bool:
        """Check if URL belongs to a different version than target."""
        url_version = self._get_url_version(url)

        if self._target_version:
            # User specified a version - skip URLs from OTHER versions
            if url_version and url_version != self._target_version:
                return True
        else:
            # User didn't specify a version
            # Skip URLs that belong to a versioned section
            if url_version:
                return True

        return False

    def get_content_selectors(self) -> list[str]:
        """Mintlify content area selectors."""
        return [
            "article",
            "main article",
            "[data-testid='content']",
            ".prose",
            ".markdown-body",
            "main .content",
            "#content",
            "[class*='DocContent']",
            "[class*='doc-content']",
            "main",
        ]

    def get_nav_selectors(self) -> list[str]:
        """Mintlify navigation selectors."""
        return [
            "nav[aria-label='Main']",
            "nav[aria-label='Sidebar']",
            "nav.sidebar",
            "[data-testid='sidebar']",
            ".DocsSidebarNav",
            "aside nav",
            "#sidebar",
            "[class*='sidebar'] nav",
            "[class*='Sidebar'] nav",
        ]

    def get_unwanted_selectors(self) -> list[str]:
        """Elements to remove from Mintlify pages."""
        return [
            # Basic elements
            "script", "style", "noscript", "iframe",

            # Navigation and layout
            "nav", "header", "footer", "aside",
            "[role='navigation']", "[role='banner']", "[role='contentinfo']",

            # Sidebars and TOC
            ".sidebar", "[class*='sidebar']", "[class*='Sidebar']",
            ".toc", "[class*='TableOfContents']", "[class*='toc']",

            # Breadcrumbs and pagination
            ".breadcrumb", "[class*='breadcrumb']", "[class*='Breadcrumb']",
            ".pagination", "[class*='pagination']", "[class*='Pagination']",

            # Feedback and edit buttons
            ".edit-page", ".feedback", "[class*='feedback']",
            "[class*='EditPage']", "[class*='edit-page']",

            # Interactive elements
            "[aria-hidden='true']",
            "button", "[role='button']",
            ".copy-button", "[class*='CopyButton']", "[class*='copy-button']",
            "[class*='IconButton']",

            # Icons
            "svg",

            # Skip links
            "[class*='skip-to']", "[class*='SkipTo']",
            "a[href='#content-area']", "a[href='#main-content']",

            # Theme toggles
            "[class*='ThemeToggle']", "[class*='theme-toggle']",

            # Search
            "[class*='Search']", "[class*='search']", "[role='search']",

            # Mobile menu
            "[class*='mobile-menu']", "[class*='MobileMenu']",

            # Helpful section
            "[class*='helpful']", "[class*='Helpful']",
        ]

    def get_wait_selector(self) -> str:
        """Selector to wait for on Mintlify pages."""
        return "article, main, .prose, [class*='DocContent']"

    def get_skip_url_patterns(self) -> list[str]:
        """URL patterns to skip for Mintlify sites."""
        return [
            r"\.(pdf|zip|png|jpg|jpeg|gif|svg|ico|css|js|woff|woff2|ttf|eot)$",
            r"#",
            r"\?",
            # Mintlify-specific paths to skip
            r"/_next/",  # Next.js internals
            # Note: /api/ removed - it's often legitimate API docs
            # Version skipping is handled dynamically in should_skip_url()
        ]

    def should_skip_url(self, url: str) -> bool:
        """Check if URL should be skipped, with smart version handling."""
        # First check base class logic (domain, path, patterns)
        if super().should_skip_url(url):
            return True

        # Then check version-specific logic
        if self._is_different_version(url):
            return True

        return False
