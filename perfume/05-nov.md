# THE FRAGRANCE STORE — CLOUDFLARE MIGRATION
## Complete Project Handover & Technical Progress Notes

**Document date:** 5 November 2026  
**Project:** The Fragrance Store — House of Brands  
**Website A:** INHALE FRAGRANCES  
**Migration:** Netlify → Cloudflare Workers  
**Current status:** Phase 3.6.1 completed according to AI Studio report. Cloudflare staging and production deployment have NOT started.

---

# 1. PROJECT OVERVIEW

We are developing a multi-tenant SaaS e-commerce platform called **The Fragrance Store — House of Brands**.

The platform allows multiple fragrance businesses to operate independently through isolated tenant databases, separate storefronts, and centralized SaaS administration.

### Current Website A

- Brand: INHALE FRAGRANCES
- Tenant slug: `the-fragrance-store`
- Production URL: https://fragrance.sohaildevops.site
- Storefront route: `/store/the-fragrance-store`
- Super Master dashboard: `/super-master`
- Admin login: `/admin/login`

### Technology stack

| Component | Technology |
|---|---|
| Frontend | React 19 |
| Build tool | Vite 7 |
| Language | TypeScript |
| Styling | Tailwind CSS 3.4 |
| UI | Shadcn UI / Radix UI |
| Icons | Lucide React |
| Routing | React Router v7 |
| Backend | Hono v4 |
| API | tRPC v11 |
| Database | Neon PostgreSQL |
| ORM | Drizzle ORM |
| Existing hosting | Netlify |
| Target hosting | Cloudflare Workers |
| Image storage | Cloudflare R2 |
| Source control | GitHub |

### Repository details

- GitHub repository: `sohail-24/saas-fragrance-store`
- Branch: `main`
- Local Mac directory:

`/Users/sohal/Downloads/saas-fragrance-store`

We use Google AI Studio for code investigation and implementation, GitHub for synchronization, and the local Mac terminal for verification.

---

# 2. MULTI-TENANT SAAS ARCHITECTURE

The platform has four main role levels.

### Level 1 — Super Master

Platform owner.

Responsibilities:
- Manage all tenant websites.
- Create and manage shop owners.
- Monitor platform-wide statistics.
- Manage subscriptions.
- Manage database connections.
- Configure platform settings.
- Monitor platform health.
- Manage audit logs.

### Level 2 — Business Owner

Individual shop or tenant owner.

Responsibilities:
- Manage their storefront.
- Manage inventory.
- Manage products and categories.
- Manage orders.
- Manage customers.
- Manage business settings.

### Level 3 — Tenant Operations and Staff

Roles:
- Manager
- Warehouse staff

Responsibilities depend on assigned permissions.

### Level 4 — Buyers and Customers

Responsibilities:
- Browse products.
- Register and log in.
- Add products to cart.
- Complete checkout.
- Make payments.
- View orders.

### Database isolation

We chose physical database isolation.

Architecture:

- Central control-plane PostgreSQL database.
- Separate Neon PostgreSQL database for each tenant.
- Tenant-specific database credentials.
- Tenant-aware database connection management.
- Tenant-aware query execution.
- Fail-closed database credential resolution.

IMPORTANT:

The central database must never accidentally become the default database for tenant-specific operations.

Website A's authoritative catalog is Website A's dedicated Neon database.

---

# 3. CLOUDFLARE MIGRATION OBJECTIVE

We decided to migrate from Netlify to **Cloudflare Workers**, not Cloudflare Pages.

Reasons:
- Native Cloudflare R2 integration.
- Worker-based backend execution.
- Edge deployment.
- Reduced dependency on Netlify Functions.
- Better integration with Cloudflare services.
- Potentially cost-effective hosting.

### Migration safety strategy

We selected parallel migration.

This means:

1. Keep Netlify production running.
2. Build Cloudflare independently.
3. Deploy a separate Cloudflare staging Worker.
4. Connect staging-only databases and R2 storage.
5. Test all application functionality.
6. Prepare production configuration.
7. Deploy production Worker only after approval.
8. Keep Netlify available for rollback.

**Never delete or disable the existing Netlify deployment during migration.**

---

# 4. PHASE-BY-PHASE WORK COMPLETED

## Phase 0 — Infrastructure and Compatibility Audit

Completed.

We audited the application for Cloudflare Workers compatibility.

Identified issues:
- Missing Worker entry point.
- Incorrect Wrangler asset directory.
- Node filesystem dependencies.
- Node PostgreSQL driver compatibility.
- Global `process.env` assumptions.
- Missing native R2 integration.
- Neon serverless driver requirements.
- Custom domain handling.

This audit established the migration roadmap.

## Phase 1 — Cloudflare Workers Foundation

<status>Completed</status>

### Files created or modified

- `api/worker.ts`
- `api/app.ts`
- `api/profileRouter.ts`
- `api/controlPlane/types.ts`
- `src/App.tsx`
- `wrangler.toml`

### Main implementation

Created a Cloudflare Worker entry point.

The Worker:
- Handles `/health`.
- Routes `/api/*` to Hono.
- Routes `/uploads/*` to Hono.
- Handles `/.netlify/*` compatibility routes.
- Delegates static assets to `env.ASSETS.fetch`.

Changed application initialization to support:

`createApp({ filesystemCache: false })`

This avoids filesystem-dependent behavior in the Worker runtime.

### Wrangler configuration

Current reported configuration:

```toml
name = "the-fragrance-store"
main = "api/worker.ts"
compatibility_date = "2024-11-01"
compatibility_flags = ["nodejs_compat"]

[assets]
directory = "./dist/public"
binding = "ASSETS"
html_handling = "auto-trailing-slash"
not_found_handling = "single-page-application"

[[r2_buckets]]
binding = "MEDIA_BUCKET"
bucket_name = "fragrance-saas-media"
preview_bucket_name = "fragrance-saas-media-preview"
```

The actual repository configuration must be rechecked before deployment.

### Git commits

- `d1445d1` — fix: restore complete npm optional dependencies
- `e7b5366` — update package-lock

## Phase 2 — Neon PostgreSQL Compatibility

<status>Implemented; runtime validation still required</status>

### Objective

Make the existing database architecture compatible with Cloudflare Workers while preserving Node.js compatibility for Netlify and local development.

### Important implementation

Created or modified:

- `api/tenantDatabase/runtimeEnv.ts`
- `api/tenantDatabase/driverAdapter.ts`
- `api/tenantDatabase/secretProvider.ts`
- `api/controlPlane/connection.ts`
- `api/queries/connection.ts`
- Worker-related tests
- `package.json`

### Database adapters

Two database adapters were introduced.

**Neon serverless adapter**
- Uses `@neondatabase/serverless`.
- Uses `drizzle-orm/neon-serverless`.
- Supports Worker-oriented PostgreSQL connectivity.
- Uses WebSocket Pool where transactions require it.

**Node PostgreSQL adapter**
- Uses `pg`.
- Uses Drizzle Node PostgreSQL integration.
- Retains local and Netlify compatibility.

### Request-scoped runtime environment

Implemented Worker environment handling using AsyncLocalStorage.

The Worker wraps requests with:

`runWithWorkerEnv(env, ...)`

This allows Worker bindings to be accessed by application services without depending on a global Node environment.

### Important remaining validation

We must still prove:
- Actual Worker startup.
- Real Neon connectivity.
- Real transaction execution.
- Concurrent tenant isolation.
- Correct runtime behavior in `workerd`.

Node-based tests alone do not establish all of these.

### Git commit

`e23c0d8` — refactor: abstract database driver via adapter pattern

---

# 5. PHASE 3 — CLOUDFLARE R2 IMAGE STORAGE

## Phase 3.0 — R2 preparation and image migration

<status>Completed</status>

### Buckets created

Production:

`fragrance-saas-media`

Preview:

`fragrance-saas-media-preview`

Both buckets:
- Private.
- Standard storage.
- Automatic Asia Pacific location.
- Production and preview kept separate.

### Existing Website A image records

Before migration:

- 29 product image records.
- Original PostgreSQL storage: `42,492,019` bytes.
- Existing images stored in PostgreSQL `bytea`.

### Migration 0008

Added these columns to `product_images`:

- `storageProvider`
- `r2Key`
- `r2Etag`
- `checksumSha256`
- `migratedAt`

Added index:

`product_images_r2_key_idx`

Migration 0008 was applied manually to Website A's production Neon database after verifying migration hashes for 0000–0007.

### Migration scripts

Created:

- `api/services/r2StorageService.ts`
- `scripts/migrate-images-to-r2.ts`
- `scripts/test-r2-connectivity.ts`
- `api/tenantDatabase/r2ImageMigration.test.ts`

Available commands:

```bash
npm run image:migrate:dry-run
npm run image:migrate
npm run test:r2-connectivity
```

Actual migration requires explicit approval:

```bash
npm run image:migrate -- --confirm-execution
```

### Actual migration result

- 29 images migrated.
- 42,492,019 bytes uploaded.
- 0 checksum mismatches.
- 0 failures.

Cloudflare dashboard confirmed 29 objects and approximately 42.5 MB in the production bucket.

Neon verification confirmed:
- All 29 records have `storageProvider = 'dual'`.
- All original PostgreSQL image bytes remain.
- All 29 records have R2 keys.
- All 29 records have SHA-256 checksums.

### CRITICAL DATA SAFETY RULE

Do not:
- Delete the original PostgreSQL image bytes.
- Change all records to `r2` automatically.
- Re-run migration unnecessarily.
- Delete existing production R2 objects.

Keep the existing dual-storage records until the complete production migration is proven safe.

## Phase 3.1 — Native R2 integration

<status>Implemented</status>

GitHub commit:

`7c1d873` — feat(product-images): integrate Cloudflare R2 storage

### Integration points

Updated:
- `api/app.ts`
- `api/middleware.ts`
- `api/productRouter.ts`
- `api/queries/mockDb.ts`
- `api/queries/productImages.ts`
- `api/services/r2StorageService.ts`
- `api/tenantDatabase/runtimeEnv.ts`
- `api/worker.ts`

Created:

`api/tenantDatabase/r2NativeStorage.test.ts`

### Native R2 functionality

Integrated:
- R2 reads.
- R2 uploads.
- R2 deletes.
- Tenant-specific object prefixes.
- Product ownership validation.
- MIME and upload-size validation.
- Checksums.
- Safe replacement handling.

Netlify continues using its existing storage compatibility path.

### Tests

- R2 native storage: 20/20 passed.
- R2 migration: 36/36 passed.

## Phase 3.5 — R2 Security Hardening

<status>Implemented; security tests passed</status>

GitHub commit:

`f1ef665`

Six files changed.

### Main security changes

- Trusted tenant identity resolution.
- Hostname registration and verification.
- Client-controlled tenant headers are not authoritative.
- Tenant-aware product image database resolution.
- Product ownership checks during upload.
- Cross-tenant R2 key rejection.
- Safer deletion handling.
- Partial failure handling.
- Database error handling.

Important implementation:

`getTenantImageDb`

and:

`resolveTrustedTenantFromRequest`

### Focused tests

R2 security isolation:

13/13 passed.

### Important issue discovered

The first local full test run contradicted the AI Studio report.

Actual local result:

- 649 passed.
- 5 failed.

This led to Phase 3.6.

---

# 6. PHASE 3.6 — FIVE FAILING TESTS FIXED

<status>Reported complete</status>

Initial local failures:

### Customer authentication — 3 failures

File:

`api/websiteACustomerAuth.test.ts`

Problems:
- Registration returned undefined user.
- Role was undefined.
- Customer context resolved as `admin` instead of `user`.

### Root cause

Customer registration and login used unscoped database queries.

`getDb()` could resolve to the central control-plane database rather than Website A's tenant database.

There was also a serious user-ID collision issue:

A customer token with user ID 1 could resolve against the central database, where ID 1 belonged to a platform administrator.

### Fixes reported

- Customer registration and login now execute in the public tenant scope.
- Customer session hydration executes against the correct tenant database.
- Customer roles are strictly enforced.
- Customer sessions cannot elevate themselves to `admin` or `super_master`.

Files modified:

- `api/auth-router.ts`
- `api/context.ts`
- `api/auth/session.ts`
- `api/auth/admin-session.ts`

### Tenant routing isolation — 1 failure

File:

`api/tenantDatabase/routingIsolation.test.ts`

Root cause:

Stale module-level Website A configuration remained in memory between test suites.

Fixes reported:
- Reset cached Website A configuration during test-store changes.
- Restrict test fallback to explicitly mounted isolated test stores.
- Preserve fail-closed behavior.

Files:

- `api/services/websiteAConfigService.ts`
- `api/tenantDatabase/secretProvider.ts`

### Catalog persistence — 1 failure

File:

`api/tenantDatabase/websiteACatalogPersistence.test.ts`

Root cause:

Stale in-memory configuration caused an unidentifiable seed target to receive a connection string.

Fix:
- Restrict test configuration loading.
- Throw `WebsiteASeedError` when the target cannot be securely identified.

File:

- `scripts/seed-website-a-catalog.ts`

### Phase 3.6 reported test results

- 77 test files.
- 654 tests.
- 654 passed.
- 0 failed.
- Typecheck passed.
- Lint passed.
- Build passed.

---

# 7. PHASE 3.6.1 — PRODUCTION SAFETY VERIFICATION

<status>Reported complete; needs final independent review</status>

This phase was performed specifically to avoid premature Cloudflare deployment.

## A. Control-plane fail-closed protection

File:

`api/controlPlane/registry.ts`

Previous risk:

Missing `CONTROL_PLANE_DATABASE_URL` could allow a silent in-memory fallback.

### Fix reported

Implemented:

- `isProductionOrStagingEnvironment()`
- `isInMemoryControlPlaneAllowed()`

Rules reported:

- Production requires durable PostgreSQL.
- Staging requires durable PostgreSQL.
- Missing required configuration throws `ControlPlaneConfigurationError`.
- `ALLOW_IN_MEMORY_CONTROL_PLANE=true` cannot bypass production protection.
- Local development and isolated tests retain permitted in-memory behavior.

Tests added or modified:

- `api/controlPlane/connection.test.ts`
- `api/worker.runtime.test.ts`

## B. Wrangler compatibility audit

Reported actual configuration:

```toml
compatibility_date = "2024-11-01"
compatibility_flags = ["nodejs_compat"]
```

AsyncLocalStorage usage audited in:

- `api/tenantDatabase/runtimeEnv.ts`
- `api/queries/connection.ts`

AI Studio reports that code uses:
- `.run()`
- `.getStore()`

No usage reported for:
- `.enterWith()`
- `.disable()`

Worker-path services reportedly read bindings through `getActiveRuntimeEnv()` rather than depending on global `process.env`.

## C. Worker runtime tests

Created:

`api/worker.runtime.test.ts`

Reported coverage:

1. Worker startup.
2. Health endpoint.
3. Static asset routing.
4. Production control-plane fail-closed behavior.
5. Staging fail-closed behavior.
6. Override rejection.
7. AsyncLocalStorage propagation.
8. Concurrent tenant request isolation.
9. R2 binding availability and upload delegation.

The report describes seven test cases covering these behaviors.

IMPORTANT:

The report calls this a Worker runtime integration suite, but we still need to confirm whether it executes in actual Cloudflare `workerd` or uses a simulated environment under Vitest.

Do not consider a simulated Worker test equivalent to a real Cloudflare runtime test.

## D. Phase 3.6.1 final reported verification

| Verification | Reported result |
|---|---|
| Test files | 78/78 passed |
| Total tests | 664/664 passed |
| TypeScript check | Passed |
| ESLint | Passed |
| Production build | Passed |
| Worker runtime suite | 7/7 passed |
| Control-plane tests | 7/7 passed |

The report states that no production database mutations, R2 modifications, DNS changes or Cloudflare deployment were performed.

Modified files:

- `api/controlPlane/registry.ts`
- `api/controlPlane/connection.test.ts`
- `api/worker.runtime.test.ts`

---

# 8. CURRENT WRANGLER DRY-RUN RESULT

Command executed locally:

```bash
npx wrangler deploy --dry-run
```

Wrangler version:

`4.158.0`

Result:

```text
Read 70 files from dist/public

Total Upload: 3778.97 KiB
Gzip: 700.86 KiB

env.MEDIA_BUCKET
R2 Bucket: fragrance-saas-media

env.ASSETS
Assets binding detected

--dry-run: exiting now.
```

This confirms:
- Wrangler can read the built assets.
- Asset directory is recognized.
- R2 binding is recognized.
- The Worker can be prepared for bundling.

It does NOT prove:
- Actual Worker runtime success.
- Real Neon connectivity.
- Successful PostgreSQL transactions.
- Production environment variables.
- Full storefront functionality.
- Production domain routing.

**No actual Cloudflare deployment has been performed.**

---

# 9. IMPORTANT SECURITY AND OPERATIONAL WARNINGS

## Neon credential exposure

An earlier terminal test failure accidentally printed a complete Neon PostgreSQL connection string, including its password.

The password should be rotated in Neon.

Then update all affected runtime configurations securely.

Never paste:
- Database passwords.
- Full connection strings.
- R2 access keys.
- JWT secrets.
- Razorpay secrets.

into ChatGPT, Google AI Studio or GitHub.

Use secure environment-variable or secret-management interfaces.

## Database separation

Before staging, establish three distinct configuration groups:

1. Production control-plane database.
2. Production tenant databases.
3. Staging control-plane and tenant databases.

Staging must not accidentally connect to production databases.

## R2 separation

Use:
- Production bucket: `fragrance-saas-media`
- Preview bucket: `fragrance-saas-media-preview`

Verify staging writes only to preview storage.

Do not delete original PostgreSQL image bytes.

## Netlify rollback

Keep the current Netlify deployment active until Cloudflare production is proven.

Do not delete Netlify environment variables or production configurations prematurely.

---

# 10. WHAT IS STILL LEFT?

This is the most important section for our next session.

We have completed the application foundation and automated verification according to AI Studio reports.

The remaining objective is to prove the existing application works in the actual Cloudflare environment.

## Stage B — Genuine Cloudflare runtime validation

Priority: FIRST.

We need to verify:

- Does the runtime suite use actual `workerd`?
- Can the Worker start under the Cloudflare runtime?
- Does AsyncLocalStorage isolate concurrent requests?
- Does the Neon serverless adapter connect to a real non-production Neon database?
- Do PostgreSQL queries and transactions work?
- Can R2 read, upload and delete objects in preview storage?
- Do environment bindings resolve correctly?
- Do missing credentials fail closed?
- Do Worker exceptions and timeouts behave safely?

Cloudflare's Workers Vitest integration should be considered for actual runtime testing.

No production writes.

## Stage C — Cloudflare staging deployment

After Stage B:

Create a separate staging Worker.

Suggested name:

`the-fragrance-store-staging`

Suggested staging environment:
- Separate control-plane Neon database.
- Separate tenant Neon database.
- Preview R2 bucket.
- Separate JWT secret.
- Separate payment gateway test credentials.
- Separate Worker secrets.

Use the staging `workers.dev` URL initially.

Do not connect production custom domains.

## Stage D — Full application testing

Test all major workflows.

### Super Master
- Login.
- Dashboard.
- Website creation.
- Tenant registration.
- Database management.
- Shop owner management.
- Subscription management.
- Analytics.
- Audit logs.

### Business Owner
- Login.
- Product creation.
- Product editing.
- Product deletion.
- Inventory.
- Product image upload.
- Categories.
- Orders.
- Settings.

### Customer
- Registration.
- Login.
- Product browsing.
- Cart.
- Checkout.
- Payment.
- Order history.
- Account management.

### Storefront
- Hero.
- Product carousel.
- Bestsellers.
- Live Deals.
- Product detail pages.
- Mobile navigation.
- Custom domain routing.
- Refresh and deep links.

### Tenant isolation
- Tenant A must never read Tenant B's catalog.
- Tenant A must never access Tenant B's images.
- Tenant A must never access Tenant B's customer information.
- Tenant A must never modify Tenant B's inventory.

## Stage E — Production readiness

Before cutover:

- Configure production Worker secrets.
- Verify production Neon credentials.
- Verify production R2 binding.
- Test payment gateway callbacks.
- Configure monitoring and error reporting.
- Review logs for secrets.
- Verify request limits and performance.
- Prepare backup and recovery procedures.
- Prepare rollback instructions.
- Document Netlify fallback.

## Stage F — Production cutover

Only after all previous stages pass:

1. Deploy the production Cloudflare Worker.
2. Verify Worker health.
3. Verify APIs.
4. Verify production domain routing.
5. Verify product images.
6. Verify customer authentication.
7. Verify checkout and payment.
8. Switch traffic carefully.
9. Keep Netlify available for rollback.
10. Monitor production after cutover.

---

# 11. ESTIMATED CLOUDFLARE MIGRATION TIME

These are planning estimates, not guaranteed deadlines.

| Stage | Estimate |
|---|---:|
| B — Runtime validation | 1–2 days |
| C — Staging deployment | 1 day |
| D — Application testing | 2–3 days |
| E — Production readiness | 1–2 days |
| F — Production cutover | 0.5–1 day |

Estimated remaining engineering work:

**Approximately 5–9 working days**, assuming no major compatibility or database issues.

After production cutover, keep an observation period of approximately 3–7 days.

---

# 12. OUR DECIDED MIGRATION STRATEGY

We discussed three approaches:

A. Parallel migration.
B. Direct production migration.
C. Gradual migration.

Our recommended strategy is:

**OPTION A — PARALLEL MIGRATION**

Why:
- Netlify already hosts the working production website.
- We do not need to risk customer access.
- Cloudflare can be tested independently.
- We can use separate staging resources.
- We can roll back safely if problems occur.

Netlify remains the production fallback until the Cloudflare cutover is approved.

---

# 13. EXACT NEXT SESSION STARTING POINT

When continuing in a new ChatGPT conversation, start with:

"We are continuing The Fragrance Store Cloudflare migration. Read these complete handover notes before suggesting anything. We have completed Phase 0, Phase 1, Phase 2 implementation, Phase 3 R2 migration and integration, Phase 3.5 security hardening, Phase 3.6 authentication and tenant isolation fixes, and Phase 3.6.1 production safety verification according to Google AI Studio reports. The latest reported result is 664/664 tests passing, with check, lint and build passing. Wrangler dry-run also passed. We have NOT deployed to Cloudflare. Netlify production must remain untouched. Do not start Phase 4 or deployment automatically. First, help me verify whether our Worker tests actually execute in workerd, then plan genuine Cloudflare runtime validation and staging."

## First task next time

**Audit the existing Worker runtime test environment.**

Inspect:
- `api/worker.runtime.test.ts`
- `vitest.config.ts` or equivalent Vitest configuration
- `package.json`
- `wrangler.toml`
- `api/worker.ts`
- `api/tenantDatabase/driverAdapter.ts`

Determine whether actual Cloudflare `workerd` execution is happening.

If not, plan a safe integration test using Cloudflare's Workers Vitest integration.

Do not deploy.

Do not modify production databases.

Do not change DNS.

Do not start production cutover.

---

# 14. IMPORTANT WORKING RULES FOR THE NEXT SESSION

1. Always work step by step.
2. Investigate before changing code.
3. Ask Google AI Studio to provide evidence for important changes.
4. Never trust a success report without checking local results.
5. Run the exact failing tests before the full suite.
6. Preserve tenant database isolation.
7. Preserve the original PostgreSQL image bytes.
8. Never use the central database as an automatic tenant fallback.
9. Keep Netlify production active.
10. Never deploy without explicit approval.
11. Never expose credentials in logs or prompts.
12. Avoid unrelated refactoring.
13. Prefer low-cost solutions.
14. Do not repeatedly run expensive or unnecessary commands.
15. Do not rush the Cloudflare production migration.

---

# FINAL PROJECT STATUS

**Application foundation:** Implemented.

**Tenant isolation:** Hardened according to reported test results.

**R2 migration:** 29 images migrated, original PostgreSQL bytes preserved.

**R2 native integration:** Implemented and tested.

**Authentication security:** Remediated according to Phase 3.6 report.

**Control-plane fail-closed protection:** Implemented and tested according to Phase 3.6.1 report.

**Automated verification:** 664/664 tests reportedly passing.

**Wrangler dry-run:** Passed.

**Actual Cloudflare production deployment:** Not performed.

**Current production hosting:** Netlify.

**Next objective:** Genuine Cloudflare runtime validation, followed by isolated staging deployment.

**Final objective:** Safely migrate The Fragrance Store to Cloudflare Workers without risking the existing INHALE FRAGRANCES production website.

END OF HANDOVER DOCUMENT.
