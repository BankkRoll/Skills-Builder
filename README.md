# Skills Builder

A collection of **28 pre-built Claude Code skills** scraped from popular documentation sites, plus an AI-powered tool to build your own.

[![Skills](https://img.shields.io/badge/skills-28-blue)](DIRECTORY.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Quick Start

```bash
npx skills add BankkRoll/Skills-Builder
```

Select the skills you want from the interactive menu.

## Build Your Own

The core of this repo is the `skills-builder` skill—an AI-powered tool that creates Claude Code skills from any documentation site.

```bash
npx skills add BankkRoll/Skills-Builder/skills/skills-builder
```

Once installed, just run `/skills-builder` in Claude Code and tell it what you want:

```
/skills-builder

> "Create a skill from the Stripe docs"
> "Build me a skill for the Tailwind CSS documentation"
> "I need a skill for the FastAPI framework"
```

The AI will:
- Find and validate the documentation URL
- Auto-detect the platform (Mintlify, Docusaurus, ReadTheDocs, etc.)
- Scrape the full documentation
- Generate a ready-to-use skill

No manual configuration needed—just describe what you want and let Claude handle the rest.

### Supported Platforms

| Platform | Example Sites |
|----------|---------------|
| **Mintlify** | Resend, Clerk, Loops |
| **Docusaurus** | React Native, Jest, Prettier |
| **ReadTheDocs** | Flask, SQLAlchemy, Ansible |
| **GitBook** | Cortex, various API docs |
| **Generic** | Any static HTML documentation |

## Pre-Built Skills

All skills below were created using `skills-builder`. **[Browse full directory →](DIRECTORY.md)**

| Category | Skills | Examples |
|----------|--------|----------|
| **Cloud & APIs** | 6 | OpenAI, Anthropic, AWS, GitHub, Google Cloud |
| **Web Frameworks** | 10 | Next.js, Astro, FastAPI, Django, Hono |
| **Frontend** | 4 | React, Vue, Angular, React Native |
| **Databases & ORMs** | 4 | Drizzle, SQLAlchemy, TypeORM, Sequelize |
| **DevOps** | 1 | Docker |
| **Meta** | 3 | skills-builder, Mintlify, Cortex |

### Usage

Once installed, invoke any skill as a slash command:

```
/nextjs        # Next.js documentation
/prisma        # Prisma ORM reference
/tailwindcss   # Tailwind CSS utilities
/stripe-api    # Stripe API reference
```

## Contributing

PRs welcome for new platform scrapers or skill improvements.

If you're a documentation owner and want content removed, [open an issue](https://github.com/BankkRoll/Skills-Builder/issues).

## License

MIT
