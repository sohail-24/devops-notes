# The Fragrance Store — House of Brands
## Project Handoff & Technical Progress Notes

**Last updated:** 21 October 2026  
**Purpose:** Continue the project in a future ChatGPT, Codex, or Google AI Studio session without re-explaining previous work.

---

## 1. Executive summary

The Fragrance Store is being developed as a multi-tenant e-commerce SaaS platform. The platform owner should eventually be able to create and manage independent online shops, while each shop owner manages their own storefront, products, inventory, orders, branding, and customers.

### Current milestone

- [x] Netlify production deployment published.
- [x] Custom subdomain `fragrance.sohaildevops.site` configured and website accessible.
- [x] Super Master dashboard accessible on the deployed website.
- [x] Website A is registered as a tenant and appears as active in the dashboard.
- [x] Website A's dedicated Neon database connection and schema validation reported successful by Google AI Studio.
- [x] Focused tenant-isolation and security tests reported passing.
- [x] Production build and lint reported passing locally.
- [x] Secret-scanning issues addressed in the latest reported commit.
- [ ] Perform final end-to-end checks of actual Website A reads and writes on the live deployment.
- [ ] Complete a deliberate cross-tenant isolation test before declaring tenant isolation production-ready.
- [ ] Continue implementing and verifying the full SaaS provisioning and custom-domain lifecycle.

**Important:** A published website and a successful database connection do not, by themselves, prove that every storefront API operation uses the correct tenant database. Keep that distinction in future investigations.

## 2. Project environment

### Repository and deployment

- Project: The Fragrance Store — House of Brands
- Local repository: `/Users/sohal/Downloads/testing-project/the-fragrance-store`
- Git branch referenced in the recent report: `main`
- Hosting: Netlify
- Git deployment source: GitHub
- Public test domain: `https://fragrance.sohaildevops.site`
- Super Master route: `/super-master`
- Website A profile route seen in the browser: `/profile`

The Netlify screenshot shows the project `astonishing-otter-569514`, marked **Public**, with the domain `fragrance.sohaildevops.site` and a successful published production deployment. The latest screenshot also shows the Super Master dashboard loading through that domain.

### Technology stack

- Frontend: React 19, TypeScript, Vite 7, Tailwind CSS
- UI: Shadcn/Radix UI, Lucide React, Sonner
- Routing: React Router
- API: Hono and tRPC
- Database: PostgreSQL on Neon
- ORM: Drizzle ORM
- Hosting: Netlify Functions and static site deployment
- Existing server compatibility: Node-based build and startup path retained

Keep the existing Node deployment path working while continuing to support Netlify. Do not replace the architecture unnecessarily.

## 3. Architecture decisions

These decisions were established during the recent design discussions.

### 3.1 Database isolation

**Target: one separate Neon project/database per tenant.**

The architecture uses two distinct database responsibilities:

**Central platform database — `fragrance-project`**
- Super Master/platform operations.
- Tenant registry and lifecycle status.
- Domain-to-tenant mappings.
- Platform-level configuration.
- Database secret references and provisioning metadata.
- Platform governance and audit records.

**Dedicated Website A database — `website-a`**
- Website A's shop-specific records.
- Product catalogue and categories.
- Inventory and warehouse data.
- Orders and customers.
- Carts and other tenant-specific commerce data.
- Branding and other shop-specific information, according to the implemented schema.

The precise placement of authentication and tenant membership records still needs to be finalized after reviewing the existing implementation.

**Non-negotiable rule:** Never change the global central `DATABASE_URL` to Website A's connection string as a shortcut. That could redirect platform operations to the wrong database.

### 3.2 Domain resolution

The intended request flow is:

1. Receive the HTTP request.
2. Normalize its hostname.
3. Resolve the hostname against a trusted server-side domain registry.
4. Confirm that the tenant is active and ready.
5. Obtain that tenant's database configuration through a server-side secret provider.
6. Use the tenant-specific connection manager.
7. Execute the operation within the resolved tenant context.
8. Reject unknown, inactive, unready, or failing tenants safely.

Do not trust a client-provided tenant ID, query parameter, request body, or arbitrary `X-Tenant-ID` header as proof of tenant identity.

Unknown or invalid tenant resolution must not fall back to another tenant, the central database, mock storage, or another data source.

### 3.3 Tenant provisioning

Use a **hybrid provisioning model** initially:

- Create each Neon project manually.
- Register its tenant and server-side database secret reference securely.
- Apply or verify the expected schema.
- Run automated readiness checks.
- Require explicit Super Master approval before activating the tenant.

Automate Neon project creation later, once the manual provisioning and isolation workflows have been verified.

### 3.4 Tenant lifecycle

The intended lifecycle is:

`Draft → Provisioning → Ready for review → Active`

Suspended and deactivated states must also be supported.

Suspension or deactivation should restrict access without physically deleting tenant data. Do not introduce irreversible tenant deletion or destructive cascade behavior without a separately reviewed retention and recovery policy.

### 3.5 Domain strategy

Initial testing uses subdomains such as:

- `fragrance.sohaildevops.site`
- `website-a.sohaildevops.site`
- `website-b.sohaildevops.site`

Later, support customer-owned custom domains.

Do not modify the root domain or DNS configuration used by the existing portfolio at `sohaildevops.site`. Add only the records necessary for the new test subdomains and platform.

NGINX is not required in the Netlify request path. It may be used in a separate containerized or self-hosted deployment if needed.

---

## 4. Work completed across the recent sessions

### A. Netlify deployment compatibility

The repository was adapted to support Netlify without discarding the existing Node server path.

Files and areas involved:

- `api/app.ts`
  - Separates construction of the Hono application from Node-specific startup side effects.

- `api/boot.ts`
  - Retains the Node bootstrap path, including the existing listener and relevant startup tasks.

- `netlify/functions/api.ts`
  - Provides the Netlify function entry point using the Fetch-style handler.
  - Enables fail-closed serverless database behavior.

- `netlify.toml`
  - Configures the production build, published frontend directory, functions directory, and SPA fallback.

- `api/queries/connection.ts`
  - Supports opt-in fail-closed serverless behavior.

- `api/queries/productImages.ts`
  - Allows durable image-write failures to propagate rather than silently masking them.

- `api/services/websiteAConfigService.ts`
  - Removes import-time configuration loading.

- `api/lib/vite.ts`
  - Includes a related type adjustment.

- `api/netlifyAdapter.test.ts`
  - Adds adapter-focused verification.

**Preserve this work.** Do not rebuild the Netlify adapter from scratch unless a new investigation proves it necessary.

### B. Initial tenant database investigation

The original problem was that entering Website A's Neon `DATABASE_URL` through Super Master settings produced errors, while Website A's Neon project appeared to show little activity.

The investigation found:

- The URL was encrypted and stored in the central database's `tenant_configurations` record for tenant ID `1`.
- The setting was marked `requiresDeployment: true` and `isRuntimeActive: false`.
- The configuration UI treated it as a deployment override, rather than a live tenant-specific connection.
- The validation procedure used `getDb().execute(SELECT 1)`, which checked the current shared/global database pool instead of necessarily testing Website A's configured URL.
- The environment module read the process-level `DATABASE_URL`.
- The original connection layer used a module-global PostgreSQL pool.
- The early control-plane foundation was not yet wired into all live request paths.

This explained why saving a Website A database URL was not enough to establish tenant-specific routing.

**Do not repeat the original workaround of changing the global environment variable.** The intended solution is a central platform connection plus tenant-specific database routing.

### C. Tenant database routing and secret-provider work

According to the latest Google AI Studio technical report, the code now includes or uses the following components:

- `api/tenantDatabase/secretProvider.ts`
- `api/tenantDatabase/connectionManager.ts`
- Tenant database validation and schema-readiness logic.
- Tenant-aware routing and context management.
- Domain-based tenant resolution.
- Tenant migration/readiness support.
- Isolation-focused tests.

The report states that `secretProvider.ts` was corrected so that `secretVersion` uses the input's secret version instead of an internal configuration-row update counter. This resolved a version mismatch that had prevented connection-pool initialization.

It also reports that `AsyncLocalStorage` maintains separate tenant database contexts across concurrent requests.

**Future verification:** Confirm that these components are connected to every relevant live commerce query. Do not assume that implementing the connection manager automatically routes every old query through it.

### D. Secret-scanning fix

An earlier Netlify build failed at the secret-scanning stage with exit code `2`.

The reported finding was a production `SUPER_MASTER_EMAIL` value embedded as a literal in `api/security-hardening.test.ts`.

The latest report says the test fixture was replaced with a synthetic `.invalid` address, retaining the normalization test without including the configured production email.

Other test fixtures were sanitized to avoid resembling live Neon hosts or credentials.

Reported files changed:

- `api/security-hardening.test.ts`
- `api/tenantDatabase/secretProvider.ts`
- `api/tenantDatabase/websiteANeonDatabaseConfig.test.ts`
- `api/tenantDatabase/routingIsolation.test.ts`
- `api/tenantDatabase/tenantMigrationRunner.test.ts`
- `api/tenantDatabase/validation.test.ts`
- `package-lock.json`

The report also says `api/tenantDatabase/websiteANeonDatabaseConfig.test.ts` was updated, although its proposed Git command omitted it. Review the actual Git diff and latest commit rather than relying on the proposed command alone.

**Security rule:** Never disable Netlify secret scanning to force a deployment through.

If a value that was ever a real production password was committed to Git history, rotate it. Replacing a test fixture in the current commit does not remove an old secret from previous commits.

### E. Latest reported validation

The Google AI Studio report states that these focused test suites were run:

- `api/security-hardening.test.ts`
- `api/tenantDatabase/routingIsolation.test.ts`
- `api/tenantDatabase/connectionManager.test.ts`
- `api/tenantDatabase/websiteANeonDatabaseConfig.test.ts`
- `api/tenantDatabase/tenantMigrationRunner.test.ts`
- `api/tenantDatabase/validation.test.ts`
- `api/websiteAConfig.test.ts`
- `api/websiteAConfigPersistence.test.ts`

Reported results:

- **8 test files passed**
- **77 of 77 tests passed**
- `npm run lint`: 0 errors and 0 warnings
- `npm run build`: successful
- Reported secret-pattern grep: zero matches for the checked values and patterns

These are results reported by Google AI Studio; they should not be described as independently rerun by ChatGPT.

### F. Dedicated Website A database verification

The latest Google AI Studio report claims the following live, read-only checks passed:

| Check | Reported result |
|---|---|
| Central `fragrance-project` connection | PASS |
| Website A dedicated Neon connection | PASS |
| Read-only `SELECT 1` on Website A | PASS |
| Website A schema readiness | PASS |
| Expected migrations | 8 of 8 |
| Missing tables | 0 |
| Missing columns | 0 |
| DDL or migration writes during verification | None |
| Seed or production data writes during verification | None |

The report states that Website A's encrypted URL was retrieved through the server-side secret provider and tested through the tenant connection manager.

It also states that requests for unknown, inactive, unready, or failing tenants fail closed, and that tenant routing does not fall back to the central database or mock storage.

**Current interpretation:** This is strong reported evidence of database connectivity and schema readiness. Still verify real storefront reads and writes through the live deployed application, and test that cross-tenant requests cannot read or modify the other tenant's records.

### G. Netlify deployment and domain

The latest screenshots show:

- Netlify deployment published successfully.
- Netlify's deploy summary shows one function deployed and redirect rules processed without errors.
- The website is available at `fragrance.sohaildevops.site`.
- The Super Master dashboard renders.
- The Website A tenant card is visible and marked Active.
- The dashboard displays the tenant's catalogue metrics.
- The Website A profile page renders.
- Neon Monitoring shows some server-connection activity, although some metrics are reported as unavailable.

The screenshots confirm that the site is published and accessible. They do not independently prove every database route or every security property.

---

## 5. Current architecture map

```text
Customer browser
      |
      v
fragrance.sohaildevops.site
      |
      v
Netlify CDN / Functions
      |
      v
Hono API / tRPC
      |
      +---- Super Master request
      |           |
      |           v
      |     Central Neon database
      |     fragrance-project
      |
      +---- Storefront request
                  |
                  v
          Trusted hostname lookup
                  |
                  v
          Tenant lifecycle check
                  |
                  v
          Encrypted DB secret provider
                  |
                  v
          Tenant connection manager
                  |
                  v
          Dedicated Neon database
                  |
                  v
             Website A data
```

This is the intended architecture. The next task is to verify that actual storefront queries follow this path consistently, including legacy query modules.

---

## 6. What we must do next

### Priority 1 — Verify the live Website A database route

Perform a controlled end-to-end check on the deployed site.

1. Open the Super Master dashboard.
2. Open Website A's storefront.
3. Confirm that products and categories load from the intended tenant database.
4. Make one harmless, identifiable test change through the supported admin interface, if available.
5. Verify that the change persists after refreshing.
6. Verify the record exists in Website A's Neon database.
7. Verify that the same change did not appear in the central database or another tenant's data.
8. Remove the test record only after confirming that it is safe to remove.

Do not use production orders or real customer data for the initial test.

If a write test cannot be performed safely, stop at read-only checks and document what remains unverified.

### Priority 2 — Verify tenant isolation

Use a dedicated test tenant or non-production data.

Check that:

- Website A cannot read Website B's products, orders, customers, carts, or inventory.
- Website B cannot read Website A's records.
- A client-supplied tenant ID cannot override hostname-based resolution.
- Unknown domains fail safely.
- Suspended or unready tenants cannot access protected shop data.
- A tenant database outage does not redirect requests to another database.
- Concurrent requests cannot leak tenant context.
- Super Master operations continue using the central database.

Do not declare isolation complete merely because unit tests pass.

### Priority 3 — Verify Git and deployment state

Before changing code:

```bash
cd /Users/sohal/Downloads/testing-project/the-fragrance-store

git status --short
git log -5 --oneline
git diff --stat
```

Confirm that the latest sanitized changes are committed and pushed, and that Netlify deployed the expected commit.

Do not blindly rerun the previous `git add`/`git commit` command. First inspect the working tree; the changes may already have been committed.

### Priority 4 — Complete tenant provisioning

Implement and verify a safe workflow that covers:

1. Create a tenant record.
2. Register a dedicated Neon database secret securely.
3. Validate connectivity.
4. Check schema and migration version.
5. Record provisioning status and audit information.
6. Present the tenant for Super Master review.
7. Activate only after explicit approval.
8. Suspend or deactivate without deleting data.

The readiness process must check more than `SELECT 1`.

### Priority 5 — Custom-domain lifecycle

After subdomain routing and isolation are reliable, support customer-owned domains.

Required future work:

- Register a requested hostname.
- Verify domain ownership.
- Provide DNS instructions.
- Confirm DNS resolution.
- Configure and verify HTTPS.
- Map the verified hostname to the correct tenant.
- Prevent one hostname from being claimed by multiple tenants.
- Support domain changes, removal, and ownership re-verification.
- Handle unknown and unverified hosts safely.

Do not modify the existing portfolio's root DNS records to implement this.

### Priority 6 — Authentication and membership

The platform still needs a fully verified identity and tenant-membership model.

The recommended starting direction is centralized identity with tenant-bound authorization, provided it fits the current auth implementation:

- Central identity and platform-level roles.
- Tenant membership and tenant-specific roles.
- Sessions validated against the tenant resolved from the request hostname.
- Explicit authorization for Super Master operations.
- No assumption that being authenticated automatically grants access to every tenant.

Before implementing this, inspect the current authentication and session code. Confirm where user identities, memberships, invitations, and roles are stored. Do not create a second conflicting auth system.

---

## 7. Risks and rules to preserve

1. **Never replace the central `DATABASE_URL` with Website A's URL.**
2. Never expose database URLs, encryption keys, passwords, or production identity values in frontend code, screenshots, logs, or committed tests.
3. Never disable secret scanning to get a green deployment.
4. Never trust client-supplied tenant IDs as the source of tenant identity.
5. Never silently fall back to another tenant database or mock data after a database failure.
6. Never perform production schema migrations, destructive cleanup, or data cutover without explicit approval and a recovery plan.
7. Preserve existing Website A data during migration or routing changes.
8. Keep the Node deployment path operational.
9. Avoid unnecessary schema migrations.
10. Avoid repeated full-suite testing after every small edit; run focused checks during implementation and meaningful broader verification at security-critical milestones.
11. Review actual Git diffs and deployment commit IDs before claiming that changes are live.
12. Rotate any real credential that was committed, if applicable.

---

## 8. Suggested implementation sequence

| Phase | Goal | Exit condition |
|---|---|---|
| 1 | Verify current live routing | Actual storefront reads use Website A's database |
| 2 | Verify cross-tenant boundaries | Negative isolation tests pass |
| 3 | Stabilize tenant connection lifecycle | Pool reuse, cleanup, failures, and secret rotation are safe |
| 4 | Complete tenant provisioning | New tenant can reach Ready for review |
| 5 | Add explicit activation workflow | Only approved and ready tenants become Active |
| 6 | Finish tenant-bound authentication | Cross-tenant authorization attempts are denied |
| 7 | Complete subdomain routing | Each verified subdomain maps to its intended tenant |
| 8 | Add custom domains | Ownership, DNS, HTTPS, and removal are verified |
| 9 | Operational readiness | Logging, backup/restore, monitoring, and recovery procedures are documented |

This is a proposed sequence, not a claim that every phase has already been implemented.

---

## 9. How to work efficiently with Google AI Studio and Codex

The goal is to minimize repeated investigation, token use, and paid credits.

### Before asking an agent to modify code

- Provide this handoff document.
- Ask it to inspect the current code and Git state first.
- Ask it to distinguish implemented functionality from tests, assumptions, and missing integration.
- Require a small, explicit scope.
- For database-related changes, require a clear statement of whether the operation is read-only or writes data.
- Do not authorize migrations or destructive actions by default.

### Testing strategy

- Small UI-only change: run the relevant build or focused check when appropriate.
- Tenant routing or secret-provider change: run the relevant connection and routing tests.
- Authentication or tenant authorization change: run security and isolation tests.
- Release milestone: run the focused suite, lint, build, then verify the published deployment.
- Do not ask the agent to rerun all 77 tests after every unrelated text or styling change.

### Completion report required from agents

Ask for:

- Exact files changed.
- Root cause and implemented fix.
- Tests actually executed and their results.
- Build and lint results.
- Whether any live database was accessed.
- Whether any writes, migrations, or seed operations occurred.
- Commit ID and push status.
- Netlify deployment status.
- Remaining risks and next steps.

Agents must not claim a live database connection, successful deployment, or secret scan unless they have direct evidence.

---

## 10. Copy this prompt when starting the next session

You are continuing work on **The Fragrance Store — House of Brands**, a multi-tenant e-commerce SaaS platform.

Read the attached project handoff notes completely before taking action.

Repository:

`/Users/sohal/Downloads/testing-project/the-fragrance-store`

Current hosting and databases:

- Netlify production deployment.
- Public test domain: `https://fragrance.sohaildevops.site`
- Central Neon project/database: `fragrance-project`
- Dedicated Website A Neon project/database: `website-a`

The latest reported production deployment is published. Google AI Studio reported that the dedicated Website A connection and schema validation passed, all 8 focused test files passed (77/77 tests), lint passed, and the production build passed. Treat those as reported results, not as tests you personally reran. The current screenshots confirm that the published site and Super Master dashboard are accessible.

**Start with verification, not a rewrite.**

1. Inspect `git status`, recent commits, and the latest deployed commit.
2. Inspect the current tenant database resolver, secret provider, connection manager, request context, and actual product/order query paths.
3. Determine whether live Website A storefront reads and writes really use the dedicated Website A database.
4. Identify the smallest safe next step.
5. Do not change the global central `DATABASE_URL`.
6. Do not run migrations, seed production data, or perform destructive operations without explicit approval.
7. Do not disable secret scanning or expose credentials.
8. Do not change the root DNS for `sohaildevops.site`.
9. Keep the Node deployment path working.
10. Minimize agent credits: avoid redundant investigations and unnecessary full-suite tests.

Before making changes, provide a concise status report with:

- What is confirmed.
- What is implemented but not verified live.
- What is still missing.
- The safest next action.

Then proceed in small, security-focused phases. Preserve the existing Website A data and fail closed if tenant resolution or database access fails.

The next immediate goal is **to verify live tenant routing and cross-tenant isolation**, then continue with tenant provisioning, authentication, and custom-domain support.

---

## 11. Session restart checklist

When returning to this project:

- [ ] Open this handoff document.
- [ ] Confirm the repository and Git branch.
- [ ] Confirm the latest deployed commit in Netlify.
- [ ] Open `https://fragrance.sohaildevops.site/super-master`.
- [ ] Verify the Website A tenant status.
- [ ] Check actual tenant-specific storefront data routing.
- [ ] Test cross-tenant isolation safely.
- [ ] Record the results before beginning the next implementation phase.

**End state to remember:** The deployment and subdomain are working, and the latest technical report describes successful database and test verification. The next task is not to rebuild deployment; it is to independently verify the live tenant data path and complete the remaining SaaS isolation and provisioning work.
