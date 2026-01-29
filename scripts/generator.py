"""
Skill Generator

Converts scraped documentation into a Claude Code skill format.
"""

import json
import re
from pathlib import Path
from typing import Optional


def sanitize_skill_name(name: str) -> str:
    """Convert name to valid hyphen-case skill name."""
    name = name.lower()
    name = re.sub(r"[\s_]+", "-", name)
    name = re.sub(r"[^a-z0-9-]", "", name)
    name = re.sub(r"-+", "-", name)
    name = name.strip("-")
    return name[:40]


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def estimate_tokens(text: str) -> int:
    """Rough token estimate (words * 1.3)."""
    return int(count_words(text) * 1.3)


def extract_title_from_markdown(content: str) -> str:
    """Extract first H1 title from markdown."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def extract_description_from_markdown(content: str) -> str:
    """Extract description from markdown (blockquote after title or first paragraph)."""
    # Try blockquote first
    match = re.search(r"^>\s*(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Try first paragraph after title
    match = re.search(r"^#[^\n]+\n+([^#\n][^\n]+)", content, re.MULTILINE)
    if match:
        desc = match.group(1).strip()
        if len(desc) > 20 and len(desc) < 200:
            return desc

    return ""


def extract_topics_from_content(content: str) -> list[str]:
    """Extract key topics/headings from markdown content."""
    topics = []
    for match in re.finditer(r"^##\s+(.+)$", content, re.MULTILINE):
        topic = match.group(1).strip()
        # Clean up topic (remove special chars, anchors)
        topic = re.sub(r"[^\w\s-]", "", topic).strip()
        if topic and len(topic) > 2:
            topics.append(topic)
    return topics[:10]  # Limit to top 10


def clean_markdown_for_reference(content: str) -> str:
    """Clean markdown content for use as a reference file."""
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


def categorize_docs(docs_dir: Path) -> dict[str, list[Path]]:
    """Categorize documentation files by topic/directory."""
    categories: dict[str, list[Path]] = {}

    for md_file in sorted(docs_dir.rglob("*.md")):
        if md_file.name.startswith("_"):
            continue

        rel_path = md_file.relative_to(docs_dir)
        parts = rel_path.parts

        if len(parts) > 1:
            category = parts[0]
        else:
            category = "general"

        if category not in categories:
            categories[category] = []
        categories[category].append(md_file)

    return categories


def merge_small_files(files: list[Path], max_tokens: int = 8000) -> list[tuple[str, str, list[str]]]:
    """Merge small files into larger chunks while respecting token limits.

    Returns list of (title, content, topics) tuples.
    """
    chunks: list[tuple[str, str, list[str]]] = []
    current_content = []
    current_tokens = 0
    current_titles = []
    current_topics = []

    for file_path in files:
        content = file_path.read_text(encoding="utf-8")
        content = clean_markdown_for_reference(content)
        tokens = estimate_tokens(content)

        title = extract_title_from_markdown(content) or file_path.stem.replace("-", " ").title()
        topics = extract_topics_from_content(content)

        if tokens > max_tokens:
            if current_content:
                chunk_title = current_titles[0] if len(current_titles) == 1 else f"{current_titles[0]} and more"
                chunks.append((chunk_title, "\n\n---\n\n".join(current_content), current_topics))
                current_content = []
                current_tokens = 0
                current_titles = []
                current_topics = []

            chunks.append((title, content, topics))
            continue

        if current_tokens + tokens > max_tokens and current_content:
            chunk_title = current_titles[0] if len(current_titles) == 1 else f"{current_titles[0]} and more"
            chunks.append((chunk_title, "\n\n---\n\n".join(current_content), current_topics))
            current_content = []
            current_tokens = 0
            current_titles = []
            current_topics = []

        current_content.append(content)
        current_tokens += tokens
        current_titles.append(title)
        current_topics.extend(topics)

    if current_content:
        chunk_title = current_titles[0] if len(current_titles) == 1 else f"{current_titles[0]} and more"
        chunks.append((chunk_title, "\n\n---\n\n".join(current_content), current_topics))

    return chunks


def generate_skill(
    docs_dir: Path,
    skill_name: str,
    output_dir: Path,
    description: Optional[str] = None,
    source_url: Optional[str] = None,
) -> Path:
    """Generate a skill from documentation directory."""

    skill_name = sanitize_skill_name(skill_name)
    skill_dir = output_dir / skill_name
    references_dir = skill_dir / "references"

    skill_dir.mkdir(parents=True, exist_ok=True)
    references_dir.mkdir(exist_ok=True)

    # Load navigation if available
    nav_file = docs_dir / "_navigation.json"
    nav_structure = []
    if nav_file.exists():
        nav_structure = json.loads(nav_file.read_text(encoding="utf-8"))

    # Categorize and process documentation
    categories = categorize_docs(docs_dir)

    # Generate reference files
    reference_files: list[dict] = []
    all_topics: list[str] = []

    for category, files in categories.items():
        chunks = merge_small_files(files)

        for i, (title, content, topics) in enumerate(chunks):
            if len(chunks) == 1:
                filename = f"{category}.md"
            else:
                filename = f"{category}-{i + 1}.md"

            filepath = references_dir / filename

            full_content = f"# {title}\n\n{content}\n"
            filepath.write_text(full_content, encoding="utf-8")

            # Get a brief description for this reference
            ref_desc = extract_description_from_markdown(content)

            reference_files.append({
                "filename": filename,
                "category": category,
                "title": title,
                "tokens": estimate_tokens(content),
                "topics": topics[:5],
                "description": ref_desc,
            })
            all_topics.extend(topics)

    # Generate description if not provided
    if not description:
        index_file = docs_dir / "_index.md"
        if index_file.exists():
            index_content = index_file.read_text(encoding="utf-8")
            match = re.search(r"^>\s*(.+)$", index_content, re.MULTILINE)
            if match:
                description = match.group(1).strip()

        if not description:
            display_name = skill_name.replace('-', ' ').title()
            # Build description from categories
            cat_names = [c.replace("-", " ") for c in categories.keys() if c != "general"]
            if cat_names:
                description = f"Documentation for {display_name} covering {', '.join(cat_names[:5])}"
                if len(cat_names) > 5:
                    description += f", and {len(cat_names) - 5} more topics"
            else:
                description = f"Reference documentation for {display_name}"

    # Build SKILL.md content
    skill_md = _build_skill_md(
        skill_name=skill_name,
        description=description,
        reference_files=reference_files,
        categories=list(categories.keys()),
        source_url=source_url,
        all_topics=list(set(all_topics)),
    )

    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_md, encoding="utf-8")

    print(f"Generated skill: {skill_dir}")
    print(f"  - SKILL.md")
    print(f"  - {len(reference_files)} reference files in references/")

    return skill_dir


def _build_skill_md(
    skill_name: str,
    description: str,
    reference_files: list[dict],
    categories: list[str],
    source_url: Optional[str] = None,
    all_topics: Optional[list[str]] = None,
) -> str:
    """Build the SKILL.md content."""

    display_name = skill_name.replace("-", " ").title()

    # Calculate total tokens
    total_tokens = sum(ref["tokens"] for ref in reference_files)

    # Group reference files by category
    by_category: dict[str, list[dict]] = {}
    for ref in reference_files:
        cat = ref["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(ref)

    # Build enhanced description for frontmatter
    enhanced_desc = description
    if source_url:
        enhanced_desc += f" Source: {source_url}."
    # Add trigger hints
    cat_names = [c.replace("-", " ") for c in categories if c != "general"]
    if cat_names:
        enhanced_desc += f" Use when questions involve: {', '.join(cat_names[:6])}."

    # Escape quotes in description
    enhanced_desc = enhanced_desc.replace('"', '\\"')

    # Build content
    lines = [
        "---",
        f'name: "{skill_name}"',
        f'description: "{enhanced_desc}"',
        "---",
        "",
        f"# {display_name}",
        "",
    ]

    if source_url:
        lines.extend([
            f"> Official documentation: {source_url}",
            "",
        ])

    # Overview section
    lines.extend([
        "## Overview",
        "",
        f"This skill provides comprehensive documentation for {display_name.lower()}.",
        "",
        f"**Total references:** {len(reference_files)} files (~{total_tokens:,} tokens)",
        "",
    ])

    # Topics covered
    if all_topics and len(all_topics) > 3:
        sample_topics = all_topics[:12]
        lines.extend([
            "**Topics covered:**",
            ", ".join(sample_topics) + ("..." if len(all_topics) > 12 else ""),
            "",
        ])

    # Reference files section
    lines.extend([
        "## Reference Files",
        "",
        "Load only the reference files relevant to the user's question:",
        "",
    ])

    # List references by category with descriptions
    for category in sorted(by_category.keys()):
        refs = by_category[category]
        cat_display = category.replace("-", " ").title()

        if len(categories) > 1:
            lines.append(f"### {cat_display}")
            lines.append("")

        for ref in refs:
            line = f"- **[{ref['title']}](references/{ref['filename']})** (~{ref['tokens']:,} tokens)"

            # Add topic hints if available
            if ref.get("topics"):
                topics_str = ", ".join(ref["topics"][:3])
                line += f"\n  - Topics: {topics_str}"

            lines.append(line)

        lines.append("")

    # Usage instructions
    lines.extend([
        "## Usage Guidelines",
        "",
        "1. **Identify relevant sections** - Match the user's question to the appropriate reference file(s)",
        "2. **Load minimally** - Only read files directly relevant to the question to conserve context",
        "3. **Cite sources** - Reference specific sections when answering",
        "4. **Combine knowledge** - For complex questions, you may need multiple reference files",
        "",
        "### When to use each reference:",
        "",
    ])

    # Add category-specific guidance
    for category in sorted(by_category.keys()):
        cat_display = category.replace("-", " ").title()
        refs = by_category[category]

        # Generate usage hint based on category name
        if category == "general":
            hint = "General documentation, overview, and getting started"
        elif category in ("api", "api-reference", "api-playground"):
            hint = "API endpoints, parameters, responses, and examples"
        elif category in ("components", "ui"):
            hint = "UI components, styling, and visual elements"
        elif category in ("deploy", "deployment"):
            hint = "Deployment, hosting, and infrastructure"
        elif category in ("create", "content"):
            hint = "Creating and managing content"
        elif category in ("customize", "config", "settings"):
            hint = "Configuration, customization, and settings"
        elif category in ("ai", "integrations"):
            hint = "AI features and third-party integrations"
        else:
            hint = f"{cat_display}-related features and documentation"

        lines.append(f"- **{cat_display}**: {hint}")

    lines.append("")

    return "\n".join(lines)


__all__ = ["generate_skill", "sanitize_skill_name"]
