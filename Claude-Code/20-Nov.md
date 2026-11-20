# Claude Code Setup — Project Handover Notes

**Date:** 20 November 2026  
**Device:** MacBook Pro M3 Pro (Apple Silicon)  
**Purpose:** Use Claude Code to develop, debug, improve and maintain The Fragrance Store SaaS project.

## 1. Claude Code Installation

- Claude Code is installed and working.
- Version: `2.1.329`
- Tested successfully by creating a Hello World webpage.
- Terminal command used for launching the test session: `claude-free`
- A separate SaaS project Terminal tab is available.

## 2. Main Project

**Project:** The Fragrance Store — Multi-tenant SaaS E-commerce Platform.

**Local project directory:**

```bash
~/Downloads/testing-project/saas-fragrance-store
```

**Technology stack:**
- React 19, Vite 7, TypeScript
- Tailwind CSS and Shadcn UI
- Hono API and tRPC
- Neon PostgreSQL and Drizzle ORM
- Cloudflare Workers and R2
- Git and GitHub

**Architecture:**
- Super Master
- Business Owner
- Tenant Admin and Buyer
- Separate tenant databases and control-plane database

## 3. FreeLLMAPI Configuration

FreeLLMAPI desktop application is installed on the Mac.

The following search providers have been added and showed healthy status:

| Provider | Free allowance shown in setup list |
|---|---|
| Tavily | 1,000 searches/month |
| Firecrawl | 1,000 credits/month |
| Parallel | No API key needed |
| Exa | $10 search credits/month |
| Outcrawl | 1,000 credits/month |

These are web-search/research providers, not AI chat models.

Other configured model providers visible in FreeLLMAPI:
- Google AI Studio
- Groq
- NVIDIA NIM
- Kilo Gateway
- OVH AI Endpoints
- AI Horde

**Important:** Verify FreeLLMAPI's Anthropic/unified API configuration and its connection to Claude Code before assuming all providers are available inside Claude Code.

## 4. GitHub Integration

The user has a GitHub account and has previously forked Graphify, but Graphify is not being installed.

The SaaS project's actual GitHub remote still needs verification.

Run:

```bash
cd ~/Downloads/testing-project/saas-fragrance-store

git status

git remote -v
```

Do not clone or change the remote until the correct repository is confirmed.

## 5. Search and Research Capabilities

The objective is to give Claude Code access to current internet information.

Available search providers through FreeLLMAPI:
- Tavily
- Firecrawl
- Parallel
- Exa
- Outcrawl

Use these for:
- Latest Cloudflare documentation and updates.
- Neon PostgreSQL and Drizzle documentation.
- React and Vite updates.
- GitHub issues and release notes.
- Technical research with source links.
- Security and compatibility investigations.

Do not assume all providers are automatically connected to Claude Code. Test their availability first.

## 6. Development Rules

When working on the SaaS:

1. Inspect the existing architecture before changing code.
2. Read relevant files before making modifications.
3. Preserve tenant database isolation.
4. Never accidentally use the control-plane database for tenant data.
5. Avoid unnecessary dependencies.
6. Prefer free and open-source tools.
7. Do not modify unrelated features.
8. Run relevant tests and production builds.
9. Review `git diff` before committing.
10. Never expose API keys, passwords or database credentials.

## 7. Next Session — Starting Commands

Open Terminal:

```bash
cd ~/Downloads/testing-project/saas-fragrance-store

git status

git remote -v

claude
```

If the usual `claude` command is not configured for FreeLLMAPI, inspect the existing `claude-free` setup instead of changing credentials or environment variables.

First verify:
- Claude Code authentication.
- FreeLLMAPI connection.
- Search provider availability.
- Correct GitHub repository.
- Current project state.

## 8. Next Session's Goal

Use Claude Code as an additional development assistant alongside Google AI Studio and Codex.

Start by understanding the existing Fragrance SaaS project, then work on the requested website improvements one task at a time.

**Important:** Graphify was evaluated but intentionally rejected. Do not install it unless explicitly requested.
