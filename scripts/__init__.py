"""
Skill Generator

Build Claude Code skills from documentation.
"""

from .scrapers import get_scraper, detect_platform, SCRAPERS
from .generator import generate_skill, sanitize_skill_name
from .builder import build_skill

__all__ = [
    "get_scraper",
    "detect_platform",
    "SCRAPERS",
    "generate_skill",
    "sanitize_skill_name",
    "build_skill",
]
