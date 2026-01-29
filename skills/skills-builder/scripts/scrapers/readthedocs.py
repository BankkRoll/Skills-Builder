"""
ReadTheDocs/Sphinx Documentation Scraper

Specialized scraper for ReadTheDocs and Sphinx-powered documentation sites.
Handles static HTML with Sphinx-specific page structure.

Version/Language Handling:
- ReadTheDocs URLs follow pattern: /{lang}/{version}/page
- Example: /en/stable/, /en/2.3.x/, /fr/latest/
- If user passes a versioned URL, only that version is scraped
- If user passes base URL, only current version is scraped
"""

import re
from .base import BaseScraper


class ReadTheDocsScraper(BaseScraper):
    """Scraper optimized for ReadTheDocs/Sphinx documentation sites."""

    platform_name = "readthedocs"

    # Sphinx sites are static HTML, no browser needed
    default_use_browser = False
    default_use_sitemap = True

    # ReadTheDocs URL patterns: /{lang}/{version}/
    # Language codes: en, fr, de, es, ja, zh, ko, etc.
    # Versions: stable, latest, 2.3.x, v1.0, 3.0, etc.
    VERSION_PATTERN = r"/([a-z]{2}(?:-[a-z]{2})?)/([^/]+)/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Detect language and version from base URL
        self._target_lang, self._target_version = self._detect_lang_version(self.base_url)
        if self._target_lang or self._target_version:
            print(f"Targeting: lang={self._target_lang or 'any'}, version={self._target_version or 'any'}", flush=True)

    def _detect_lang_version(self, url: str) -> tuple[str | None, str | None]:
        """Detect language and version from URL."""
        match = re.search(self.VERSION_PATTERN, url)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def _is_different_version(self, url: str) -> bool:
        """Check if URL belongs to a different lang/version than target."""
        url_lang, url_version = self._detect_lang_version(url)

        # If we have a target language, enforce it
        if self._target_lang and url_lang and url_lang != self._target_lang:
            return True

        # If we have a target version, enforce it
        if self._target_version and url_version and url_version != self._target_version:
            return True

        return False

    def get_content_selectors(self) -> list[str]:
        """ReadTheDocs/Sphinx content area selectors."""
        return [
            # Sphinx standard selectors
            "[role='main']",
            "div.body",
            "div.document",
            "div.section",
            # ReadTheDocs theme
            "div.rst-content",
            "div[itemprop='articleBody']",
            # Alabaster theme
            "div.bodywrapper",
            # Generic fallbacks
            "main",
            "article",
            "#content",
        ]

    def get_nav_selectors(self) -> list[str]:
        """ReadTheDocs/Sphinx navigation selectors."""
        return [
            # Sphinx sidebar
            "div.sphinxsidebarwrapper",
            "div.sphinxsidebar",
            # ReadTheDocs theme
            "nav.wy-nav-side",
            "div.wy-side-nav-search",
            "div.wy-menu-vertical",
            # Generic
            "aside",
            "nav",
            ".sidebar",
            ".toctree-wrapper",
        ]

    def get_unwanted_selectors(self) -> list[str]:
        """Elements to remove from ReadTheDocs/Sphinx pages."""
        return [
            # Basic elements
            "script", "style", "noscript", "iframe",

            # Navigation and layout
            "nav", "header", "footer",
            "[role='navigation']", "[role='banner']", "[role='contentinfo']",

            # Sphinx-specific
            "div.sphinxsidebar",
            "div.sphinxsidebarwrapper",
            "div.sphinxfooter",
            "div.relations",
            "div#searchbox",
            "form.search",

            # ReadTheDocs theme
            "nav.wy-nav-side",
            "nav.wy-nav-top",
            "div.wy-side-nav-search",
            "div.wy-nav-content-wrap > nav",
            "div.rst-versions",

            # Breadcrumbs
            "div.breadcrumbs",
            "ul.wy-breadcrumbs",
            "p.caption",

            # Edit/source links
            "a.viewcode-link",
            "a.viewcode-back",
            "a.headerlink",
            ".rst-content .edit-on-github",
            "[class*='edit-']",

            # Footer elements
            "div.footer",
            ".copyright",

            # Buttons and interactive
            "button",
            ".copy-button",
            ".copybtn",
        ]

    def get_wait_selector(self) -> str:
        """Selector to wait for on Sphinx pages."""
        return "[role='main'], div.body, div.document, div.rst-content"

    def get_skip_url_patterns(self) -> list[str]:
        """URL patterns to skip for ReadTheDocs sites."""
        return [
            r"\.(pdf|zip|png|jpg|jpeg|gif|svg|ico|css|js|woff|woff2|ttf|eot)$",
            r"#",
            r"\?",
            # Sphinx-specific paths to skip
            r"genindex",
            r"py-modindex",
            r"search\.html",
            r"_sources/",
            r"_static/",
            r"_images/",
            # Note: Version/language skipping is handled dynamically in should_skip_url()
        ]

    def should_skip_url(self, url: str) -> bool:
        """Check if URL should be skipped, with smart version/language handling."""
        # First check base class logic (domain, path, patterns)
        if super().should_skip_url(url):
            return True

        # Then check version/language-specific logic
        if self._is_different_version(url):
            return True

        return False
