# Claude Code + OmniRoute + FreeLLMAPI — Project Handover Notes

**Date:** 22 November 2026  
**Device:** MacBook Pro M3 Pro (Apple Silicon)  
**Purpose:** Develop, debug, improve and maintain The Fragrance Store SaaS using Claude Code with OmniRoute and FreeLLMAPI.

## 1. Main Project

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

## 2. Claude Code

- Claude Code installed and working.
- Version: `2.1.330`
- Mac: Apple Silicon M3 Pro.
- Working directory: SaaS project directory.
- Successfully tested with a simple Hello message.
- Latest successful model response identified: Claude Opus 5.5 (`claude-opus-5-5`).

**Important:** We now launch Claude Code through OmniRoute instead of relying on the old direct FreeLLMAPI setup.

## 3. OmniRoute Installation and Configuration

**Application:** Keak OmniRoute  
**Version:** 3.8.54  
**Node.js:** v24.13.0  
**npm:** 11.6.2

OmniRoute is installed globally using npm.

**Dashboard:**
```text
http://localhost:20128
```

**API Base URL:**
```text
http://localhost:20128/v1
```

OmniRoute is our central AI routing gateway.

### API Key

Created an API key in:

OmniRoute → API Keys

Key name:
```text
Claude-Code-Local
```

- Key created successfully.
- Key has access to configured models.
- API key is stored securely.
- Never paste the actual key into project files, GitHub or shared notes.

Environment variable:
```bash
OMNIROUTE_API_KEY
```

## 4. FreeLLMAPI Connection

FreeLLMAPI desktop application is installed and connected to OmniRoute.

**Provider configuration in OmniRoute:**

- Provider: Anthropic Compatible
- Provider name: FreeLLMAPI
- Connection: FreeLLMAPI Main
- Connection status: Connected
- Base URL configured to use FreeLLMAPI's local API.
- Models imported successfully.
- 85/85 models active in the latest screenshot.

**Important settings enabled in FreeLLMAPI provider:**
- Auto-fetch upstream models
- Auto-Sync

These allow OmniRoute to retrieve and synchronize available models.

## 5. OmniRoute Model Routing

OmniRoute supports multiple models and providers.

Models visible in the current catalog include:
- Claude Opus 4.5
- Claude Sonnet 4.5
- Claude Haiku 4.5
- Gemini 3.8 Flash
- Gemini 3.7 Flash
- GLM 5.3 Flash
- Qwen models
- GPT-OSS models
- Kimi and other models

**Routing strategies available:**
- Manual
- Balanced
- Smartest
- Fastest
- Most reliable
- Custom
- Decision

We can configure intelligent routing and fallback chains later.

## 6. Token Budget Understanding

Two separate dashboards show different quota information.

**OmniRoute:**
- Estimated combined free-tier budget: 1.62B tokens.
- This is a catalog-wide estimate, NOT our personal account balance.

**FreeLLMAPI:**
- Monthly budget shown: 231M.
- Used: 51.8M.
- Remaining: 179.2M.
- Remaining percentage: 78%.

These budgets must not be added together.

Actual availability depends on each provider, model, account and its restrictions.

## 7. Important Terminal Commands

### Terminal 1 — Start OmniRoute

```bash
omniroute
```

Keep this terminal running.

Dashboard:
```text
http://localhost:20128
```

### Terminal 2 — Launch Claude Code

First, make sure the API key is available in the terminal environment.

```bash
export OMNIROUTE_API_KEY="YOUR_OMNIROUTE_API_KEY"
```

Then:

```bash
cd ~/Downloads/testing-project/saas-fragrance-store

omniroute launch --api-key "$OMNIROUTE_API_KEY"
```

Claude Code will connect through OmniRoute.

**Security:** Never commit the API key or put it in the SaaS project's `.env` file.

### Generate Claude model profiles (optional)

```bash
omniroute setup-claude --api-key "$OMNIROUTE_API_KEY" --dry-run
```

Remove `--dry-run` when ready to generate profiles.

## 8. Previous Authentication Issue — SOLVED

Initially:
```text
Failed to fetch models: HTTP 401
Authentication required
```

Diagnosis:
- OmniRoute was running.
- The API endpoint worked with a valid Bearer token.
- The CLI needed the API key explicitly.

Verified successfully using:
```bash
curl -sS http://localhost:20128/v1/models \
-H "Authorization: Bearer $OMNIROUTE_API_KEY"
```

Returned HTTP 200.

Using `--api-key` resolved the authentication issue.

## 9. FreeLLMAPI Search Providers

Previously configured search/research providers:

| Provider | Allowance shown during setup |
|---|---|
| Tavily | 1,000 searches/month |
| Firecrawl | 1,000 credits/month |
| Parallel | No API key needed |
| Exa | $10 search credits/month |
| Outcrawl | 1,000 credits/month |

These are research/search providers, NOT AI chat models.

Do not assume they are automatically available inside Claude Code. Verify their integrations separately.

## 10. Development Rules

When working on the SaaS:

1. Inspect existing architecture before changing code.
2. Read relevant files before modifications.
3. Preserve tenant database isolation.
4. Never use the control-plane database for tenant data.
5. Avoid unnecessary dependencies.
6. Prefer free and open-source solutions.
7. Do not modify unrelated features.
8. Run relevant tests and production builds.
9. Review `git diff` before committing.
10. Never expose API keys, passwords or database credentials.
11. Work on one feature at a time.
12. Explain important changes before implementing them.

## 11. Next Session — Starting Checklist

1. Start OmniRoute in Terminal 1.
2. Open the SaaS project in Terminal 2.
3. Export the API key if it is not already available.
4. Run Claude Code through OmniRoute.
5. Verify the active model.
6. Check Git status and existing project changes.
7. Continue the requested development task.

Commands:

```bash
cd ~/Downloads/testing-project/saas-fragrance-store

git status

git remote -v

omniroute launch --api-key "$OMNIROUTE_API_KEY"
```

## 12. Next Development Goals

- Test different models through OmniRoute.
- Configure smart model routing.
- Explore fallback chains.
- Monitor provider quotas and usage.
- Verify search/research integrations separately.
- Continue improving The Fragrance Store SaaS.

**Important:** Do not reinstall Claude Code, OmniRoute or FreeLLMAPI. All three are installed and working. Start by verifying the existing setup and continue development.

---

**Current Setup:**

Claude Code → OmniRoute → FreeLLMAPI → Available AI Models

OmniRoute is our central gateway for managing AI models, routing and provider connections.
