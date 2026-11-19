# The Fragrance Store — SaaS Project
## Development Handover & Continuation Notes
**Date:** 19 November 2026  
**Next session:** 20 November 2026

---

# 1. Project Overview

**Project:** The Fragrance Store — House of Brands

We are building a multi-tenant SaaS e-commerce platform where multiple businesses can operate their own branded online stores using a shared SaaS platform.

### Main architecture

There are three major user-facing levels:

1. **Super Master** — Platform owner who controls the SaaS platform, websites, databases, configurations, subscriptions, and platform operations.
2. **Business Owner / Admin** — Manages their own tenant website, products, inventory, orders, customers, and settings.
3. **Buyer / Customer** — Visits the storefront, registers, logs in, shops, and places orders.

Website A has its own customer-facing storefront and admin functionality. We are not introducing an unnecessary Store Staff role into the existing business-owner and buyer structure.

### Project URLs

| Component | URL |
|---|---|
| Website A storefront | https://amfruits.shop |
| Super Master dashboard | https://platform.amfruits.shop/super-master |
| Staging Worker | https://the-fragrance-store-staging.mdsohail88008.workers.dev/super-master |

Website A's canonical tenant slug is:

`the-fragrance-store`

Its brand is INHALE FRAGRANCES.

---

# 2. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 19 |
| Build tool | Vite 7 |
| Language | TypeScript |
| Styling | Tailwind CSS 3.4 |
| UI | Shadcn / Radix UI |
| Icons | Lucide React |
| Routing | React Router 7 |
| Backend | Hono 4 |
| API | tRPC 11 |
| Database | Neon PostgreSQL |
| ORM | Drizzle ORM |
| Hosting | Cloudflare Workers |
| Image storage | Cloudflare R2 |
| Email | Resend |
| Payments | Razorpay |

The platform uses separate tenant databases with a central SaaS Control Plane database.

---

# 3. Database Architecture — Important

Our SaaS architecture uses physical tenant database isolation.

There are three database connections in our current setup, and all three are connected and working according to today's verification.

### Database responsibilities

**A. SaaS Control Plane Database**
- Platform-level information.
- Tenant and website registration.
- Tenant configurations.
- Encrypted integration credentials.
- Super Master operations.

**B. Website A Dedicated Neon Database**
- Website A products.
- Product images and inventory.
- Orders and customer records.
- Website A commerce operations.
- Customer authentication identities.

**C. The other configured database connection**
- Its precise role and ownership must continue to be verified from the platform's Database Control Center before any database operation.

### Critical database rules

- Never use the Control Plane database for tenant commerce data.
- Never silently fall back to the central database when a tenant database is unavailable.
- Tenant-specific migrations must execute against the correct dedicated tenant database.
- Never run migrations against a database simply because it is connected.
- Never expose database credentials in terminal output, screenshots, or chat.

Previously, we fixed tenant database isolation, encrypted tenant credentials, Worker runtime configuration, and database connection management. These are important foundations and must not be casually changed.

---

# 4. What We Completed Today — Google OAuth

## 4.1 Initial problem

Website A already had a Google sign-in button on the customer account page.

However, it was only a placeholder.

When customers clicked Google sign-in, the application displayed:

"Google sign-in is not configured yet."

There was no real Google OAuth authentication flow.

## 4.2 Architecture investigation

We investigated the existing authentication system and configuration architecture.

Important findings:

- Existing authentication supports local and mobile providers.
- Google OAuth credentials already had configuration fields in the platform.
- Website A uses its own tenant database.
- Existing customer sessions are issued through `issueSessionCookies()`.
- Existing configuration services support encrypted secret storage.

We decided to implement Google OAuth using the existing architecture rather than introducing Firebase, Auth0, or another authentication provider.

## 4.3 Google OAuth configuration fields

Super Master → Websites → Website A → Details → Group D: Customer Authentication (Google OAuth)

Three configuration fields are available:

1. `GOOGLE_CLIENT_ID`
2. `GOOGLE_CLIENT_SECRET`
3. `GOOGLE_CALLBACK_URL`

All three currently show **Not configured**.

We will configure them tomorrow.

## 4.4 Database changes

We introduced a new tenant-local identity table:

`user_identities`

It stores:

- User ID.
- Authentication provider.
- Provider subject.
- Provider email.
- Created and updated timestamps.

We also added Google to the authentication provider enum.

Important: Google identities are matched using Google's stable `sub` identifier, not email alone.

An existing local/mobile account is not automatically linked just because the Google account has the same email address.

This protects customer account ownership.

## 4.5 Separate tenant migration architecture

We discovered an important migration safety issue.

The existing application boot process runs legacy migrations using the regular database connection. That connection could resolve to the Control Plane outside a tenant request scope.

Therefore, we introduced a separate tenant migration bundle:

`db/tenant-migrations/`

The new migration is:

`0010_google_user_identities.sql`

We also added:

- `scripts/migrate-tenant.ts`
- Tenant-specific Drizzle configuration.
- Target database safety checks.
- Explicit migration execution approval.
- Tenant migration runner tests.

The existing `db/migrations/` folder remains the legacy Control Plane migration location.

**Important:** The migration has NOT been executed against a live database yet.

Before executing it, we must inspect the existing Website A migration history and confirm that only the required pending migration will run.

Do not blindly execute all historical migrations against an existing tenant database.

## 4.6 Backend Google OAuth implementation

New implementation:

`api/auth/google-oauth.ts`

New API endpoints:

- `GET /api/auth/google/start`
- `GET /api/auth/google/callback`

The implemented flow includes:

1. Resolve the trusted tenant.
2. Confirm Website A context.
3. Load the tenant's Google OAuth configuration.
4. Generate secure OAuth state and nonce.
5. Generate PKCE verifier and challenge.
6. Redirect the customer to Google's authentication page.
7. Receive Google's authorization callback.
8. Exchange the authorization code on the server.
9. Validate the Google ID token and signature.
10. Verify issuer, audience, expiry, nonce, subject, and verified email.
11. Find or create the customer in Website A's tenant database.
12. Save the Google identity.
13. Issue the existing application session cookies.

Google scopes are limited to:

`openid email profile`

We are not requesting Gmail inbox access.

The Google Client Secret stays on the server and must never be exposed to the frontend.

## 4.7 Frontend changes

File:

`src/pages/Account.tsx`

The Google sign-in button is now connected to:

`/api/auth/google/start`

It is no longer just a placeholder.

---

# 5. Testing Completed Today

We ran focused tests for the Google OAuth implementation and related changes.

### Focused test results

| Test file | Result |
|---|---|
| Google OAuth tests | Passed |
| Google OAuth configuration tests | Passed |
| Google identity schema tests | Passed |
| Tenant migration runner tests | Passed |
| Account page tests | Passed |
| Desktop feature parity tests | Passed |

**Total: 6 test files passed, 59 tests passed, 0 failed.**

### Additional checks

- `npm run check` — Passed.
- `npm run lint` — Passed.
- `npm run build` — Passed.
- `git diff --check` — Passed.

The build produced bundle-size warnings, but no build failure.

We did not run the complete test suite today because previous sessions had known unrelated failures. Do not describe the entire project test suite as fully green.

---

# 6. Git Commit and Push Status

We created the following commit:

**Commit:** `df88c2a`

**Commit message:**

`feat: implement tenant-scoped Google OAuth login`

The commit contains 35 files changed.

The following two uploaded product images were deliberately excluded from the commit:

- `uploads/products/product-4ed079c3-0d55-4e5e-b924-8b1d608a3906.png`
- `uploads/products/tenant-logo-1-a12c735d-1c9e-4edd-9912-be3cf1626f3f.png`

One additional file remained modified but unstaged:

`db/migrations/meta/_journal.json`

Do not include it automatically in another commit without checking why it changed.

**Git push status:** The commit was created successfully, but the final `git push origin main` result has not yet been confirmed in this handover. Verify it first tomorrow.

Commands:

```bash
git status
git log -1 --oneline
git push origin main
```

Only push if the commit has not already reached `origin/main`.

---

# 7. Resend Email Integration — Today's Progress

We opened the Resend dashboard and added the domain:

`amfruits.shop`

The Resend domain configuration currently shows:

- Status: Pending
- Resend verification: Pending
- Provider: Cloudflare
- Region: Tokyo (ap-northeast-1)

The dashboard is checking DNS records.

The DKIM TXT record is still pending.

This means Resend domain verification is not complete yet.

### Tomorrow's Resend tasks

1. Open Resend → Domains → `amfruits.shop`.
2. Review the DNS records provided by Resend.
3. Open Cloudflare DNS for `amfruits.shop`.
4. Check whether all required records are present.
5. Add or correct records only if necessary.
6. Wait for DNS propagation.
7. Return to Resend and verify the domain.
8. Confirm the domain status becomes verified.
9. Test sending an email from Website A.
10. Check delivery and application logs.

Do not invent DNS values. Copy the exact records supplied by Resend.

Do not confuse a pending domain verification with a broken email integration.

---

# 8. Google OAuth — Tomorrow's Implementation Plan

This is our first priority tomorrow.

### Step 1 — Google Cloud Console

Open:

https://console.cloud.google.com/

Select or create the Google Cloud project for our SaaS.

Configure the OAuth consent screen:

- Application name: The Fragrance Store
- User support email: An email address we control.
- Developer contact email: An email address we control.
- Audience: External, if customers outside our organization need to sign in.
- Add test users if the application is still in testing.

Request only:

- `openid`
- `email`
- `profile`

### Step 2 — Create OAuth credentials

Navigate to Google Auth Platform → Clients.

Create an OAuth client:

**Application type:** Web application

Add the authorized redirect URI:

`https://amfruits.shop/api/auth/google/callback`

This must exactly match the callback URL configured in Website A.

Create the OAuth client and obtain:

- Client ID
- Client Secret

Never share the Client Secret in chat or screenshots.

### Step 3 — Add credentials in Super Master

Navigate to:

Super Master → Websites → Website A → Details → Group D: Customer Authentication (Google OAuth)

Configure:

| Field | Value |
|---|---|
| GOOGLE_CLIENT_ID | Google OAuth Client ID |
| GOOGLE_CLIENT_SECRET | Google OAuth Client Secret |
| GOOGLE_CALLBACK_URL | `https://amfruits.shop/api/auth/google/callback` |

Use the platform's configuration editor.

The secret should remain encrypted and masked.

The fields show a Redeploy indicator. After saving, verify what the platform requires to make the configuration active in the Worker runtime.

### Step 4 — Apply the tenant migration safely

Before running the migration:

1. Confirm Website A's dedicated Neon database endpoint.
2. Inspect its current migration history.
3. Confirm the existing migrations are already applied or otherwise safely reconciled.
4. Run the tenant migration runner in dry-run mode.
5. Verify that the only pending migration is `0010_google_user_identities.sql`.
6. Only then execute the approved migration against Website A's dedicated tenant database.

Never use the Control Plane database as the migration target.

### Step 5 — Deploy and test Google login

Test the following:

1. Open `https://amfruits.shop`.
2. Open the customer Account page.
3. Click Continue with Google.
4. Confirm Google authentication opens.
5. Select a Google account.
6. Confirm the customer returns to Website A.
7. Verify the customer session is created.
8. Verify the customer appears in Website A's dedicated database.
9. Verify the Google identity is stored in `user_identities`.
10. Sign out and test login again.

Also test error handling for missing credentials, invalid state, and unverified email.

---

# 9. Development Rules for Tomorrow and Future Sessions

We agreed to continue with small, controlled updates rather than large risky changes.

Our workflow:

1. Understand the current issue.
2. Inspect only the relevant code.
3. Give Codex a focused implementation task.
4. Review the actual changes.
5. Run targeted tests.
6. Run TypeScript, lint, and build.
7. Commit and push.
8. Deploy only after confirming the correct environment.
9. Test the actual application.

### Important rules

- Do not refactor unrelated working features.
- Do not casually change tenant database architecture.
- Do not expose secrets.
- Do not run unverified migrations.
- Do not use Control Plane credentials for tenant commerce operations.
- Keep the two untracked product images untouched.
- Do not introduce extra roles without a clear business requirement.
- Keep changes small and independently testable.

Our preferred tools remain:

- Codex for repository implementation and code review.
- ChatGPT Mentor for architecture, debugging, technical review, and step-by-step guidance.
- Google AI Studio when useful and available.

---

# 10. Tomorrow's Priority Checklist

## Priority A — Google OAuth

- [ ] Verify Git push and deployment status.
- [ ] Create/configure Google Cloud OAuth consent screen.
- [ ] Create Web Application OAuth credentials.
- [ ] Add authorized callback URI.
- [ ] Save Client ID in Website A.
- [ ] Save Client Secret securely in Website A.
- [ ] Save Callback URL.
- [ ] Verify Worker runtime configuration.
- [ ] Inspect Website A migration history.
- [ ] Apply only the pending tenant migration.
- [ ] Deploy the correct Worker version.
- [ ] Test Google login end-to-end.

## Priority B — Resend

- [ ] Check `amfruits.shop` domain verification.
- [ ] Check Cloudflare DNS records.
- [ ] Complete DKIM and other required DNS verification.
- [ ] Verify the Resend domain.
- [ ] Test sending an email from Website A.
- [ ] Check email delivery and logs.

## Priority C — Small SaaS improvements

After Google OAuth and Resend are working, continue with small updates.

For every update, follow our established workflow: inspect → implement → test → build → push → deploy → verify.

---

# 11. Starting Prompt for Our Next Chat

Copy the following message tomorrow to continue without explaining the project again:

"Mentor, let's continue The Fragrance Store SaaS project from our 19 November 2026 handover notes.

Today we completed the tenant-scoped Google OAuth implementation, created commit df88c2a, and prepared the separate tenant migration bundle. TypeScript, lint, build, and 59 focused tests passed.

Our next priorities are:

1. Verify Git push and deployment status.
2. Configure Google Cloud OAuth Web Application credentials.
3. Add GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_CALLBACK_URL in Super Master → Website A → Group D.
4. Safely inspect and apply the pending Google identity migration to Website A's dedicated Neon database.
5. Deploy and test Google customer login.
6. Complete Resend domain verification for amfruits.shop using Cloudflare DNS and test email delivery.

Remember our tenant database isolation architecture. Never run tenant migrations against the Control Plane database. Work in small, controlled steps and avoid unnecessary investigations or unrelated refactoring.

Let's start with verifying Git push and then configure Google OAuth."

---

**End of 19 November 2026 handover notes.**
