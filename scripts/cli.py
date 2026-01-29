#!/usr/bin/env python3
"""
Skill Generator CLI

Usage:
    skillgen build <url> <name>     Build a skill from documentation
    skillgen scrape <url>           Scrape documentation to markdown
    skillgen list                   List available platforms
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

# Handle both installed package and direct script execution
try:
    from .scrapers import get_scraper, detect_platform, SCRAPERS
    from .builder import build_skill
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from scrapers import get_scraper, detect_platform, SCRAPERS
    from builder import build_skill


def cmd_build(args):
    """Build a skill from documentation URL."""
    use_browser = None if not args.no_browser else False
    use_sitemap = None if not args.no_sitemap else False

    build_skill(
        url=args.url,
        skill_name=args.name,
        output_dir=args.output,
        platform=args.platform,
        description=args.description,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        delay=args.delay,
        use_browser=use_browser,
        use_sitemap=use_sitemap,
        keep_raw=args.keep_raw,
        verbose=args.verbose,
    )


def cmd_scrape(args):
    """Scrape documentation to markdown."""
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print(f"Error: Invalid URL: {args.url}")
        sys.exit(1)

    if args.platform == "auto":
        platform = detect_platform(args.url)
        print(f"Auto-detected platform: {platform}")
    else:
        platform = args.platform

    ScraperClass = get_scraper(platform)

    use_browser = None if not args.no_browser else False
    use_sitemap = None if not args.no_sitemap else False

    scraper = ScraperClass(
        base_url=args.url,
        output_dir=args.output,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        delay=args.delay,
        use_browser=use_browser,
        use_sitemap=use_sitemap,
        verbose=args.verbose,
    )

    scraper.crawl()
    scraper.save()
    print(f"\nSaved to: {args.output}")


def cmd_list(args):
    """List available platforms."""
    print("Available platforms:\n")
    print("  mintlify     Mintlify-powered docs (JS-rendered)")
    print("  readthedocs  ReadTheDocs/Sphinx sites (static)")
    print("  docusaurus   Docusaurus/React docs (JS-rendered)")
    print("  gitbook      GitBook-powered sites (JS-rendered)")
    print("  generic      Static HTML documentation")
    print("  auto         Auto-detect (default)")


def add_common_args(parser):
    """Add common arguments."""
    parser.add_argument(
        "-p", "--platform",
        default="auto",
        choices=list(SCRAPERS.keys()),
        help="Platform (default: auto)"
    )
    parser.add_argument("--max-depth", type=int, default=10, help="Max crawl depth")
    parser.add_argument("--max-pages", type=int, default=0, help="Max pages (0=unlimited)")
    parser.add_argument("--delay", type=float, default=0.3, help="Request delay (seconds)")
    parser.add_argument("--no-browser", action="store_true", help="Disable browser rendering")
    parser.add_argument("--no-sitemap", action="store_true", help="Disable sitemap discovery")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")


def main():
    parser = argparse.ArgumentParser(
        prog="skillgen",
        description="Build Claude Code skills from documentation",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # build
    build_p = subparsers.add_parser("build", help="Build skill from URL")
    build_p.add_argument("url", help="Documentation URL")
    build_p.add_argument("name", help="Skill name")
    build_p.add_argument("-o", "--output", default="./.agents/skills", help="Output directory (default: .agents/skills)")
    build_p.add_argument("--description", help="Skill description")
    build_p.add_argument("--keep-raw", action="store_true", help="Keep raw markdown")
    add_common_args(build_p)
    build_p.set_defaults(func=cmd_build)

    # scrape
    scrape_p = subparsers.add_parser("scrape", help="Scrape docs to markdown")
    scrape_p.add_argument("url", help="Documentation URL")
    scrape_p.add_argument("-o", "--output", default="./scraped_docs", help="Output directory")
    add_common_args(scrape_p)
    scrape_p.set_defaults(func=cmd_scrape)

    # list
    list_p = subparsers.add_parser("list", help="List platforms")
    list_p.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nCancelled")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(args, "verbose") and args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
