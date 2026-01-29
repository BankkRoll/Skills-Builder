"""
Generic Documentation Scraper

General-purpose scraper for static HTML documentation sites.
Works with most documentation that doesn't require JavaScript rendering.
"""

from .base import BaseScraper


class GenericScraper(BaseScraper):
    """Generic scraper for static documentation sites."""

    platform_name = "generic"

    # Static sites don't need browser rendering
    default_use_browser = False
    default_use_sitemap = True

    def get_content_selectors(self) -> list[str]:
        """Generic content area selectors."""
        return [
            "article",
            "main",
            ".content",
            ".main-content",
            "#content",
            "#main",
            ".documentation",
            ".doc-content",
            ".page-content",
            "[role='main']",
            ".markdown-body",
            ".post-content",
            "body",
        ]

    def get_nav_selectors(self) -> list[str]:
        """Generic navigation selectors."""
        return [
            "nav",
            ".sidebar",
            ".nav",
            ".navigation",
            "#sidebar",
            "#nav",
            "[role='navigation']",
            "aside",
            ".toc",
            ".menu",
        ]

    def get_unwanted_selectors(self) -> list[str]:
        """Elements to remove from generic pages."""
        return [
            # Basic elements
            "script", "style", "noscript", "iframe",

            # Navigation and layout
            "nav", "header", "footer",
            "[role='navigation']", "[role='banner']", "[role='contentinfo']",

            # Sidebars
            ".sidebar", "#sidebar", "aside",

            # Common UI elements
            ".breadcrumb", ".breadcrumbs",
            ".pagination",
            ".edit-page", ".edit-link",
            ".feedback",

            # Interactive elements
            "button",
            ".copy-button",

            # Icons
            "svg", ".icon",

            # Ads and tracking
            ".ad", ".ads", ".advertisement",
            "[class*='tracking']",
        ]

    def get_wait_selector(self) -> str:
        """Selector to wait for on generic pages."""
        return "article, main, .content, #content"
