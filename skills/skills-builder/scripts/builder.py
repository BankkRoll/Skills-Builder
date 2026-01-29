"""
Skill Builder

Combines scraping and generation into a single pipeline.
"""

import sys
import tempfile
from pathlib import Path

try:
    from .scrapers import get_scraper, detect_platform
    from .generator import generate_skill, sanitize_skill_name
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from scrapers import get_scraper, detect_platform
    from generator import generate_skill, sanitize_skill_name


def build_skill(
    url: str,
    skill_name: str,
    output_dir: str = "./skills",
    platform: str = "auto",
    description: str | None = None,
    max_depth: int = 10,
    max_pages: int = 0,
    delay: float = 0.3,
    use_browser: bool | None = None,
    use_sitemap: bool | None = None,
    keep_raw: bool = False,
    verbose: bool = False,
) -> Path:
    """
    Build a skill from a documentation URL.

    Args:
        url: Base URL of the documentation site
        skill_name: Name for the generated skill
        output_dir: Output directory for the skill
        platform: Documentation platform (auto, mintlify, generic, etc.)
        description: Optional skill description
        max_depth: Maximum crawl depth
        max_pages: Maximum pages to crawl (0 = unlimited)
        delay: Delay between requests
        use_browser: Use Playwright for JS rendering (None = platform default)
        use_sitemap: Use sitemap for URL discovery (None = platform default)
        keep_raw: Keep raw scraped markdown files
        verbose: Enable verbose output

    Returns:
        Path to the generated skill directory
    """
    skill_name = sanitize_skill_name(skill_name)
    output_path = Path(output_dir)

    if platform == "auto":
        platform = detect_platform(url)
        print(f"Auto-detected platform: {platform}")

    ScraperClass = get_scraper(platform)

    with tempfile.TemporaryDirectory() as temp_dir:
        raw_docs_dir = Path(temp_dir) / "raw_docs"

        if keep_raw:
            raw_docs_dir = output_path / f"{skill_name}_raw"
            raw_docs_dir.mkdir(parents=True, exist_ok=True)

        print(f"Step 1/2: Scraping documentation from {url}")
        print("-" * 50)

        scraper = ScraperClass(
            base_url=url,
            output_dir=str(raw_docs_dir),
            max_depth=max_depth,
            max_pages=max_pages,
            delay=delay,
            use_browser=use_browser,
            use_sitemap=use_sitemap,
            verbose=verbose,
        )
        scraper.crawl()
        scraper.save()

        print()
        print(f"Step 2/2: Generating skill '{skill_name}'")
        print("-" * 50)

        skill_path = generate_skill(
            docs_dir=raw_docs_dir,
            skill_name=skill_name,
            output_dir=output_path,
            description=description,
            source_url=url,
        )

        print()
        print("=" * 50)
        print(f"SUCCESS: Skill created at {skill_path}")
        print()

        return skill_path
