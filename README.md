# Skills Builder

Build Claude Code skills from documentation websites. This repo includes pre-built skills and a scraper to create your own directly by running `/skills-builder` once installed.

## Available Skills

Ready-to-use skills built from popular documentation:

| Skill               | Source                                                              | Platform    |
| ------------------- | ------------------------------------------------------------------- | ----------- |
| `mintlify-docs`     | [Mintlify Docs](https://mintlify.com/docs)                          | Mintlify    |
| `flask-docs`        | [Flask Docs](https://flask.palletsprojects.com/en/stable/)          | ReadTheDocs |
| `react-native-docs` | [React Native Docs](https://reactnative.dev/docs/getting-started)   | Docusaurus  |
| `cortex-docs`       | [Cortex Docs](https://docs.cortex.io/)                              | GitBook     |
| `skills-builder`    | This repo                                                           | -           |

## Installation

Install any skill with a single command:

```bash
npx skills add BankkRoll/Skills-Builder
```

Or install a specific skill:

```bash
npx skills add BankkRoll/Skills-Builder/skills/mintlify-docs
npx skills add BankkRoll/Skills-Builder/skills/flask-docs
npx skills add BankkRoll/Skills-Builder/skills/react-native-docs
npx skills add BankkRoll/Skills-Builder/skills/cortex-docs
npx skills add BankkRoll/Skills-Builder/skills/skills-builder
```

### Telemetry

The skills CLI collects anonymous telemetry to rank skills on the leaderboard. No personal information is collected.

To opt out:

```bash
DISABLE_TELEMETRY=1 npx skills add BankkRoll/Skills-Builder
```

## Usage

Once installed, use skills as slash commands in Claude Code:

```
/mintlify-docs
/flask-docs
/react-native-docs
/cortex-docs
/skills-builder
```

## Build Your Own Skills

Use the skills-builder to build skills from any documentation site.

### Quick Start

```bash
pip install -e .
playwright install chromium

skillgen build https://mintlify.com/docs mintlify-docs
```

Or run directly:

```bash
pip install requests beautifulsoup4 lxml playwright
playwright install chromium

python scripts/cli.py build https://mintlify.com/docs mintlify-docs
```

### Commands

```bash
skillgen build <url> <name>   # Build skill from docs
skillgen scrape <url>         # Scrape docs to markdown
skillgen list                 # List platforms
```

### Examples

```bash
skillgen build https://resend.com/docs resend-api
skillgen build https://mintlify.com/docs mintlify --max-pages 100
skillgen build https://docs.python.org/3/ python -p generic
```

### Options

| Flag             | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| `-o, --output`   | Output directory                                                    |
| `-p, --platform` | Platform: auto, mintlify, readthedocs, docusaurus, gitbook, generic |
| `--max-pages`    | Limit pages (0 = unlimited)                                         |
| `--max-depth`    | Max crawl depth (default: 10)                                       |
| `--delay`        | Delay between requests in seconds (default: 0.3)                    |
| `--no-browser`   | Disable browser rendering                                           |
| `--no-sitemap`   | Disable sitemap discovery                                           |
| `--keep-raw`     | Keep raw markdown (build only)                                      |
| `-v, --verbose`  | Verbose output                                                      |

## Supported Platforms

| Platform      | Example                                                                   | Description                         |
| ------------- | ------------------------------------------------------------------------- | ----------------------------------- |
| `mintlify`    | [mintlify.com/docs](https://mintlify.com/docs)                            | Mintlify-powered docs (JS-rendered) |
| `readthedocs` | [flask.palletsprojects.com](https://flask.palletsprojects.com/en/stable/) | ReadTheDocs / Sphinx sites          |
| `docusaurus`  | [reactnative.dev/docs](https://reactnative.dev/docs/getting-started)      | Docusaurus-powered docs             |
| `gitbook`     | [docs.cortex.io](https://docs.cortex.io/)                                 | GitBook documentation               |
| `generic`     | Any static site                                                           | Fallback for static HTML            |
| `auto`        | -                                                                         | Auto-detect platform (default)      |

## Version Handling

Each platform scraper intelligently handles versioned documentation:

| Platform      | URL Pattern                    | Example                                           |
| ------------- | ------------------------------ | ------------------------------------------------- |
| `docusaurus`  | `/docs/{version}/`             | `/docs/0.77/`, `/docs/next/`, `/docs/v2/`         |
| `readthedocs` | `/{lang}/{version}/`           | `/en/stable/`, `/fr/latest/`, `/en/2.3.x/`        |
| `gitbook`     | `/{variant}/`                  | `/v1/`, `/api-v2/`, `/latest/`                    |
| `mintlify`    | `/{section}/`                  | `/v1/`, `/api/`, `/sdk/`                          |

**How it works:**

- **Versioned URL provided**: Scrapes ONLY that specific version
  ```bash
  skillgen build https://reactnative.dev/docs/0.77/ rn-077  # Only v0.77
  skillgen build https://flask.palletsprojects.com/en/2.3.x/ flask-23  # Only v2.3.x
  ```

- **Base URL provided**: Scrapes only the current/latest version (skips old versions)
  ```bash
  skillgen build https://reactnative.dev/docs/ react-native  # Latest only
  skillgen build https://flask.palletsprojects.com/en/stable/ flask  # Stable only
  ```

## Structure

```
Skills-Builder/
├── scripts/                    # Scraper tooling
│   ├── cli.py
│   ├── builder.py
│   ├── generator.py
│   └── scrapers/
├── skills/
│   ├── mintlify-docs/          # Pre-built skill
│   ├── flask-docs/             # Pre-built skill
│   ├── react-native-docs/      # Pre-built skill
│   ├── cortex-docs/            # Pre-built skill
│   └── skills-builder/         # Meta skill for building skills
├── pyproject.toml
└── LICENSE
```

## Adding Custom Scrapers

```python
# scripts/scrapers/newplatform.py
from .base import BaseScraper

class NewPlatformScraper(BaseScraper):
    platform_name = "newplatform"
    default_use_browser = False
    default_use_sitemap = True

    def get_content_selectors(self) -> list[str]:
        return ["main", "article", ".content"]

    def get_nav_selectors(self) -> list[str]:
        return ["nav", ".sidebar"]

    def get_unwanted_selectors(self) -> list[str]:
        return ["script", "style", "footer"]
```

## Requirements

- Python 3.10+
- requests, beautifulsoup4, lxml, playwright

## Contributing

> **Note:** The pre-built skills in this repo were scraped from public documentation. If you are a documentation owner and would like your content removed, please [open an issue](https://github.com/BankkRoll/Skills-Builder/issues).

Want to add support for a new documentation platform? PRs welcome! See [Adding Custom Scrapers](#adding-custom-scrapers) above.

## License

MIT
