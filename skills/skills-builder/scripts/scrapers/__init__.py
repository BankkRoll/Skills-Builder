"""
Documentation Scrapers

Modular scraper architecture for different documentation platforms.
Each scraper extends BaseScraper and implements platform-specific logic.

Supported platforms:
- Mintlify - JS-rendered documentation sites (version pattern: /v1/, /api/, /sdk/)
- ReadTheDocs - Sphinx/ReadTheDocs sites (version pattern: /{lang}/{version}/)
- Docusaurus - React-based documentation (version pattern: /docs/{version}/)
- GitBook - GitBook-powered sites (version pattern: /{variant}/)
- Generic - Static HTML sites (no version handling)

Version Handling:
All platform scrapers (except generic) support intelligent version detection.
- If the base URL contains a version (e.g., /docs/0.77/), only that version is scraped
- If the base URL is unversioned (e.g., /docs/), only the current/latest version is scraped
- Old/archived versions are automatically skipped to avoid duplicate content
"""

from .base import BaseScraper
from .mintlify import MintlifyScraper
from .generic import GenericScraper
from .readthedocs import ReadTheDocsScraper
from .docusaurus import DocusaurusScraper
from .gitbook import GitBookScraper

SCRAPERS = {
    "mintlify": MintlifyScraper,
    "readthedocs": ReadTheDocsScraper,
    "docusaurus": DocusaurusScraper,
    "gitbook": GitBookScraper,
    "generic": GenericScraper,
    "auto": None,
}


def get_scraper(platform: str = "auto"):
    if platform == "auto":
        return MintlifyScraper
    scraper_class = SCRAPERS.get(platform.lower())
    if not scraper_class:
        raise ValueError(f"Unknown platform: {platform}")
    return scraper_class


def detect_platform(url: str) -> str:
    """
    Auto-detect documentation platform from URL patterns.
    Only matches official platform domains.
    """
    url_lower = url.lower()

    if ".readthedocs.io" in url_lower or ".readthedocs.org" in url_lower:
        return "readthedocs"
    if ".gitbook.io" in url_lower:
        return "gitbook"
    if "docusaurus.io" in url_lower:
        return "docusaurus"
    if "mintlify.com" in url_lower or "mintlify.dev" in url_lower:
        return "mintlify"

    return "mintlify"


__all__ = [
    "BaseScraper",
    "MintlifyScraper",
    "ReadTheDocsScraper",
    "DocusaurusScraper",
    "GitBookScraper",
    "GenericScraper",
    "get_scraper",
    "detect_platform",
    "SCRAPERS",
]
