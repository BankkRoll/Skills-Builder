#!/usr/bin/env python3
"""
Build a Claude Code skill from documentation.

Usage:
    python build.py <url> <skill_name> [options]

Examples:
    python build.py https://mintlify.com/docs mintlify-docs
    python build.py https://resend.com/docs resend-api --max-pages 100
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from builder import build_skill
from scrapers import SCRAPERS, detect_platform


def main():
    parser = argparse.ArgumentParser(description="Build Claude Code skill from docs")
    parser.add_argument("url", help="Documentation URL")
    parser.add_argument("name", help="Skill name")
    parser.add_argument("-o", "--output", default="./skills", help="Output directory")
    parser.add_argument("-p", "--platform", default="auto", choices=list(SCRAPERS.keys()))
    parser.add_argument("--description", help="Skill description")
    parser.add_argument("--max-pages", type=int, default=0, help="Max pages (0=unlimited)")
    parser.add_argument("--max-depth", type=int, default=10, help="Max crawl depth")
    parser.add_argument("--no-browser", action="store_true", help="Disable browser")
    parser.add_argument("--no-sitemap", action="store_true", help="Disable sitemap")
    parser.add_argument("--keep-raw", action="store_true", help="Keep raw markdown")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    build_skill(
        url=args.url,
        skill_name=args.name,
        output_dir=args.output,
        platform=args.platform,
        description=args.description,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        use_browser=None if not args.no_browser else False,
        use_sitemap=None if not args.no_sitemap else False,
        keep_raw=args.keep_raw,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
