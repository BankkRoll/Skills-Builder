"""
GitBook Documentation Scraper

Specialized scraper for GitBook-powered documentation sites.
Handles JS-rendered content and GitBook-specific page structure.

Version Handling:
- GitBook uses "Content Variants" for versioning
- Variants appear as path prefixes: /v1/, /v2/, /api-v2/, etc.
- If user passes a variant URL, only that variant is scraped
- Otherwise, we scrape from the root without crossing into other variants
"""

import re
from .base import BaseScraper


class GitBookScraper(BaseScraper):
    """Scraper optimized for GitBook documentation sites."""

    platform_name = "gitbook"

    # GitBook sites are JS-rendered, browser needed
    default_use_browser = True
    default_use_sitemap = True

    # GitBook variant patterns - these are common version/variant path prefixes
    VARIANT_PATTERNS = [
        r"^/(v\d+(?:\.\d+)*)(/|$)",           # /v1/, /v2.0/, /v2.1/
        r"^/(api-v\d+)(/|$)",                  # /api-v1/, /api-v2/
        r"^/(\d+\.\d+(?:\.\d+)?)(/|$)",       # /1.0/, /2.3.1/
        r"^/(latest|stable|next|legacy)(/|$)", # /latest/, /stable/
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Detect variant from base URL path
        self._target_variant = self._detect_variant(self.base_path)
        if self._target_variant:
            print(f"Targeting variant: {self._target_variant}", flush=True)

    def _detect_variant(self, path: str) -> str | None:
        """Detect if path contains a GitBook variant/version."""
        for pattern in self.VARIANT_PATTERNS:
            match = re.search(pattern, path)
            if match:
                return match.group(1)
        return None

    def _get_url_variant(self, url: str) -> str | None:
        """Extract variant from a URL's path."""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        # Check the path relative to domain root
        return self._detect_variant(parsed.path)

    def _is_different_variant(self, url: str) -> bool:
        """Check if URL belongs to a different variant than target."""
        url_variant = self._get_url_variant(url)

        if self._target_variant:
            # User specified a variant - skip URLs from OTHER variants
            # Allow URLs with no variant (shared pages) or same variant
            if url_variant and url_variant != self._target_variant:
                return True
        else:
            # User didn't specify a variant (root docs)
            # Skip URLs that belong to a versioned variant
            if url_variant:
                return True

        return False

    def get_content_selectors(self) -> list[str]:
        """GitBook content area selectors."""
        return [
            # GitBook v2+ selectors
            "[data-testid='page.contentEditor']",
            "[class*='page-body']",
            "[class*='markdown-body']",
            ".gitbook-content",
            # Main content area
            "main",
            "article",
            "[role='main']",
            # Specific content wrappers
            "[class*='content']",
            ".page-inner",
            ".page-wrapper",
            # Generic fallbacks
            ".body",
            "#content",
        ]

    def get_nav_selectors(self) -> list[str]:
        """GitBook navigation selectors."""
        return [
            # GitBook sidebar
            "[data-testid='table-of-contents']",
            "[class*='sidebar']",
            "[class*='navigation']",
            "nav",
            "aside",
            # Table of contents
            ".toc",
            "[class*='toc']",
        ]

    def get_unwanted_selectors(self) -> list[str]:
        """Elements to remove from GitBook pages."""
        return [
            # Basic elements
            "script", "style", "noscript", "iframe",

            # Navigation and layout
            "nav", "header", "footer",
            "[role='navigation']", "[role='banner']", "[role='contentinfo']",

            # GitBook-specific
            "[data-testid='table-of-contents']",
            "[class*='sidebar']",
            "[class*='navigation']",
            "[class*='header']",
            "[class*='footer']",

            # Search
            "[class*='search']",
            "[data-testid='search']",
            "[role='search']",

            # Interactive elements
            "button",
            "[role='button']",
            "[class*='button']",

            # Icons and decorative
            "svg",
            "[class*='icon']",

            # Feedback/rating
            "[class*='feedback']",
            "[class*='rating']",
            "[class*='helpful']",

            # Page controls
            "[class*='page-nav']",
            "[class*='pagination']",
            "[class*='breadcrumb']",

            # Edit links
            "[class*='edit']",
            "a[href*='edit']",

            # Theme toggle
            "[class*='theme']",
            "[class*='mode-toggle']",

            # GitBook branding
            "[class*='powered-by']",
            "[class*='gitbook-']",

            # Hints (keep the text but remove the wrapper styling markers)
            # Actually, keep hints - they often contain important info
        ]

    def get_wait_selector(self) -> str:
        """Selector to wait for on GitBook pages."""
        return "main, article, [class*='page-body'], [class*='markdown-body']"

    def get_skip_url_patterns(self) -> list[str]:
        """URL patterns to skip for GitBook sites."""
        return [
            r"\.(pdf|zip|png|jpg|jpeg|gif|svg|ico|css|js|woff|woff2|ttf|eot)$",
            r"#",
            r"\?",
            # GitBook-specific paths to skip
            r"/~/",  # Internal GitBook paths
            r"\.gitbook\.",  # GitBook assets
            # Note: Variant/version skipping is handled dynamically in should_skip_url()
        ]

    def should_skip_url(self, url: str) -> bool:
        """Check if URL should be skipped, with smart variant handling."""
        # First check base class logic (domain, path, patterns)
        if super().should_skip_url(url):
            return True

        # Then check variant-specific logic
        if self._is_different_variant(url):
            return True

        return False
