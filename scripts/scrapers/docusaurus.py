"""
Docusaurus Documentation Scraper

Specialized scraper for Docusaurus-powered documentation sites.
Handles React-rendered content and Docusaurus-specific page structure.

Version Handling:
- If user passes a versioned URL (e.g., /docs/0.77/), only that version is scraped
- If user passes the base docs URL (e.g., /docs/), only the latest/current version is scraped
"""

import re
from .base import BaseScraper


class DocusaurusScraper(BaseScraper):
    """Scraper optimized for Docusaurus documentation sites."""

    platform_name = "docusaurus"

    # Docusaurus sites are React-rendered, browser recommended
    default_use_browser = True
    default_use_sitemap = True

    # Version patterns for Docusaurus sites
    # These match version identifiers in URLs like /docs/{version}/page
    VERSION_PATTERNS = [
        r"/docs/(\d+\.\d+(?:\.\d+)?)(/|$)",  # /docs/0.77, /docs/0.77.1, /docs/0.77/foo
        r"/docs/(v\d+(?:\.\d+)*)(/|$)",       # /docs/v2, /docs/v2.1, /docs/v2/foo
        r"/docs/(next)(/|$)",                 # /docs/next, /docs/next/foo
        r"/docs/(latest)(/|$)",               # /docs/latest, /docs/latest/foo
        r"/docs/(legacy)(/|$)",               # /docs/legacy
        r"/docs/(stable)(/|$)",               # /docs/stable
        r"/docs/(canary)(/|$)",               # /docs/canary
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Detect if base URL targets a specific version
        self._target_version = self._detect_version(self.base_url)
        if self._target_version:
            print(f"Targeting version: {self._target_version}", flush=True)

    def _detect_version(self, url: str) -> str | None:
        """Detect if URL contains a specific version."""
        for pattern in self.VERSION_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _is_different_version(self, url: str) -> bool:
        """Check if URL belongs to a different version than target."""
        url_version = self._detect_version(url)

        if self._target_version:
            # User specified a version - skip URLs from OTHER versions
            # But allow URLs with no version (shared pages) or same version
            if url_version and url_version != self._target_version:
                return True
        else:
            # User didn't specify a version (wants latest/current)
            # Skip ALL versioned URLs - they're older versions
            if url_version:
                return True

        return False

    def get_content_selectors(self) -> list[str]:
        """Docusaurus content area selectors."""
        return [
            # Docusaurus v2+ selectors
            "article",
            "[class*='docItemContainer']",
            "[class*='docMainContainer']",
            ".markdown",
            "div.theme-doc-markdown",
            # Main content area
            "main",
            ".container .row .col",
            # Generic fallbacks
            "#__docusaurus article",
            ".docusaurus-content",
        ]

    def get_nav_selectors(self) -> list[str]:
        """Docusaurus navigation selectors."""
        return [
            # Sidebar navigation
            "[class*='sidebar']",
            "aside[class*='docSidebar']",
            "nav.menu",
            "[class*='menu__list']",
            # Top navigation
            "nav.navbar",
            ".navbar__items",
            # Table of contents
            "[class*='tableOfContents']",
            ".table-of-contents",
        ]

    def get_unwanted_selectors(self) -> list[str]:
        """Elements to remove from Docusaurus pages."""
        return [
            # Basic elements
            "script", "style", "noscript", "iframe",

            # Navigation and layout
            "nav", "header", "footer",
            "[role='navigation']", "[role='banner']", "[role='contentinfo']",

            # Docusaurus-specific
            "aside[class*='sidebar']",
            "[class*='docSidebar']",
            "nav.navbar",
            "[class*='navbar']",
            "[class*='tableOfContents']",
            ".table-of-contents",

            # Breadcrumbs and pagination
            "[class*='breadcrumbs']",
            ".breadcrumbs",
            "[class*='pagination']",
            ".pagination-nav",

            # Footer
            "[class*='footer']",
            ".footer",

            # Theme/UI elements
            "[class*='announcementBar']",
            "[class*='colorModeToggle']",
            "[class*='searchBox']",
            "[class*='DocSearch']",
            "button",
            "[role='button']",

            # Edit links
            "[class*='editThis']",
            "a[href*='edit']",
            ".theme-edit-this-page",

            # Skip links
            "#__docusaurus_skipToContent_fallback",
            "[class*='skipToContent']",

            # Tabs that might duplicate content
            "[class*='tabs__item']",

            # Icons
            "svg",
            "[class*='icon']",

            # Version badges
            "[class*='badge']",
        ]

    def get_wait_selector(self) -> str:
        """Selector to wait for on Docusaurus pages."""
        return "article, main, .markdown, [class*='docItemContainer']"

    def get_skip_url_patterns(self) -> list[str]:
        """URL patterns to skip for Docusaurus sites."""
        return [
            r"\.(pdf|zip|png|jpg|jpeg|gif|svg|ico|css|js|woff|woff2|ttf|eot)$",
            r"#",
            r"\?",
            # Docusaurus-specific paths to skip
            r"/search$",
            r"/search/",
            r"/tags/",
            r"/tags$",
            r"/page/\d+",  # Blog pagination
            # Note: Version skipping is handled dynamically in should_skip_url()
            # based on whether user specified a target version
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
