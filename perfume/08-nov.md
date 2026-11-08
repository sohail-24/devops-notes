# The Fragrance Store — SaaS Database Recovery Notes

**Project:** The Fragrance Store — House of Brands  
**Brand:** INHALE FRAGRANCES  
**Recovery period:** November 6–8, 2026  
**Status:** SUCCESSFULLY RECOVERED AND VERIFIED  
**Primary environment:** Cloudflare Workers — Staging

---

# 1. Executive Summary

During November 6–8, we worked on recovering Website A's dedicated Neon PostgreSQL database connection.

The SaaS platform uses two separate Neon databases:

1. SaaS Control Plane database — responsible for central platform governance.
2. Website A database — responsible for the INHALE FRAGRANCES storefront and its tenant data.

The Control Plane database was connecting successfully, but Website A repeatedly reported:

- Connection Failed.
- Data Access Mismatch.
- Database identity unavailable.
- Fingerprint NONE or unavailable.
- Approximately 5000 ms connection timeout.
- HTTP 500 errors.
- Super Master dashboard loading delays.

We investigated the database architecture, recovered the missing Control Plane foundation schema, completed Website A registration and credential integration, corrected Cloudflare Worker request-isolation problems, synchronized the missing code changes with GitHub, and deployed the recovered implementation.

**Final result:** Both databases are now connected, Website A data loads, product CRUD works, and the connection remains healthy after refresh.

# 2. Infrastructure Architecture

## SaaS Control Plane

- Neon project: `fragrance-project`
- Branch: `production`
- Database: `neondb`
- Responsibility: Central SaaS governance, tenant registry, credentials, domains, identities, and memberships.

## Website A — INHALE FRAGRANCES

- Tenant slug: `the-fragrance-store`
- Neon project: `website-a`
- Branch: `production`
- Database: `neondb`
- Responsibility: Website A products, categories, images, inventory, customers, and orders.

## Cloudflare

**Staging Worker**
- Name: `the-fragrance-store-staging`
- URL: `https://the-fragrance-store-staging.mdsohail88008.workers.dev`
- R2 bucket: `fragrance-saas-media-preview`

**Production Worker**
- Name: `the-fragrance-store`
- R2 bucket: `fragrance-saas-media`

Important: Staging and production must remain separate. Do not accidentally change production while troubleshooting staging.

# 3. Initial Problems

The following issues occurred during the recovery period.

### Problem A — Control Plane foundation missing

The Control Plane Neon database did not initially contain the required platform registry tables.

Missing tables included:

- platform_tenants
- tenant_database_registrations
- tenant_database_credentials
- tenant_domains
- platform_identities
- platform_legacy_identity_links
- platform_tenant_memberships
- tenant_provisioning_audit
- control_plane_migrations

Without these tables, the platform could not reliably resolve Website A's registration and credentials.

### Problem B — Website A credential resolution failure

Website A's health check attempted to resolve its tenant registration and database credentials.

The credential lookup could fail before the application even reached the actual Website A Neon database.

The diagnostic sometimes showed:

- Identity unavailable.
- Fingerprint NONE.
- TENANT_DATABASE_UNAVAILABLE.
- Data Access Mismatch.

This was important: an unavailable tenant credential did not prove that Website A's Neon database itself was down.

### Problem C — Cloudflare Worker cross-request I/O

Cloudflare Worker logs showed:

`Cannot perform I/O on behalf of a different request.`

They also showed warnings about promises being resolved from a different request context.

The investigation identified shared module-level database connections, pools, managers, and in-flight promises as lifecycle problems.

Cloudflare Worker request contexts must not reuse request-bound Neon I/O objects from another request.

### Problem D — Slow Super Master initialization

The dashboard sometimes remained on:

`Connecting to Neon PostgreSQL & synchronizing SaaS Platform Control Center...`

Serial database health checks, connection timeouts, and problematic connection lifecycle management contributed to the slow initialization.

### Problem E — Git synchronization

Google AI Studio contained important Phase 7 code changes, but those changes were not initially present in the Mac's local Git repository or GitHub main.

A successful AI Studio build did not mean that the changes had been committed and pushed to GitHub.

# 4. Control Plane Foundation Recovery

We first verified the intended Control Plane database.

The preflight environment was configured with:

- CONTROL_PLANE_DATABASE_URL
- CONTROL_PLANE_EXPECTED_ENDPOINT_HOSTNAME
- CONTROL_PLANE_EXPECTED_NEON_PROJECT
- CONTROL_PLANE_EXPECTED_NEON_BRANCH
- CONTROL_PLANE_EXPECTED_DATABASE_NAME

Expected target:

- Project: fragrance-project
- Branch: production
- Database: neondb

The preflight completed successfully.

Reported state:

- State: clean
- Ledger: absent
- Existing foundation tables: none
- Existing foundation enums: none

We explicitly approved the migration.

Executed:

`npm run control-plane:migrate`

Result:

`Control-plane foundation migration completed or was already applied.`

We independently verified the tables in Neon SQL Editor.

The migration ledger recorded:

`0000_control_plane_foundation`

The migration checksum was:

`c7feba645ffa7bd6c78b8f3f0690535b6468380fb5e9968b49a8fce32849b541`

The migration was recorded as applied on November 8, 2026.

Important: This migration created the Control Plane foundation. It did not automatically register Website A.

# 5. Website A Tenant Registration

Google AI Studio implemented the tenant registration and credential integration.

Important files:

- api/controlPlane/credentials.ts
- api/controlPlane/repository.ts
- api/controlPlane/service.ts
- api/controlPlane/registry.ts
- api/superMasterRouter.ts
- api/controlPlane/tenantRegistrationIntegration.test.ts

Reported implementation:

1. Connected TenantDatabaseCredentialService to ControlPlaneService.
2. Integrated the service with getControlPlaneService().
3. Implemented AES-256-GCM credential storage.
4. Added credential version synchronization.
5. Improved idempotent tenant registration.
6. Added duplicate checks and domain synchronization.
7. Added Website A registration operation through registerWebsiteA.
8. Added recognized staging and production Website A hostnames.

Website A registration target:

- Tenant slug: the-fragrance-store
- Project: website-a
- Branch: production
- Database: neondb

The implementation was reported as passing its tests.

# 6. Phase 7 — Cloudflare Worker Connection Stabilization

This was the major engineering correction.

Google AI Studio investigated the Cloudflare Worker runtime errors and implemented request-scoped database connection handling.

Eight files were changed.

## File 1

`api/tenantDatabase/runtimeEnv.ts`

Added WorkerRequestScope containing:

- Environment bindings.
- Request-specific cache.
- Cleanup callbacks.

Implemented request lifecycle management through runWithWorkerEnv().

Cleanup callbacks execute when the request finishes.

## File 2

`api/tenantDatabase/driverAdapter.ts`

Enabled:

`neonConfig.poolQueryViaFetch = true`

for Cloudflare Workers.

This allows suitable single-statement database queries to use stateless HTTP transport instead of depending on persistent WebSocket connections.

Transactions continue to use their required connection handling.

## File 3

`api/controlPlane/connection.ts`

Changed Control Plane connection handling to use the request-specific cache.

Registered connection cleanup when the Worker request completes.

## File 4

`api/controlPlane/registry.ts`

Moved Worker runtime service and connection-manager caching into the request scope.

Applied this to:

- Control Plane service.
- Tenant connection manager.
- Tenant secret provider.
- Tenant credential service.

Registered manager cleanup.

## File 5

`api/queries/connection.ts`

Changed getCentralDb() to use request-scoped database connections in Workers.

Registered pool cleanup after the request.

## File 6

`api/services/websiteADatabaseHealthService.ts`

Moved in-flight health-check deduplication into the request-specific cache.

This prevents one Worker request from sharing an in-flight health promise with another request.

## File 7

`api/services/databaseControlCenterService.ts`

Changed database inventory health checks to run concurrently using:

`Promise.allSettled()`

This prevents a slow Website A check from unnecessarily delaying the Control Plane health check.

## File 8

`api/tenantDatabase/cloudflareWorkersConnectionIsolation.test.ts`

Added tests for:

- Sequential request isolation.
- Concurrent request isolation.
- Request-specific database pools.
- Cleanup behavior.
- Neon HTTP query transport.
- Health-check promise isolation.
- Concurrent health probes.

Reported verification:

- 19 tenant database test files.
- 257 tenant database tests passed.
- 8 Control Plane and Super Master test files.
- 37 Control Plane and Super Master tests passed.
- Build succeeded.
- ESLint completed without errors.

These are the reported AI Studio validation results.

# 7. Why Google AI Studio Preview Was Not Enough

AI Studio Preview and Cloudflare Workers do not necessarily execute with identical runtime environments.

The local preview could use Node.js process.env and development/mock database behavior.

Cloudflare Workers use request-scoped runtime bindings and the actual Neon serverless driver.

Therefore:

- A successful preview did not prove the real Worker connection was fixed.
- A successful local test did not prove staging was fixed.
- Real Cloudflare staging deployment and actual database queries were necessary.

We eventually deployed the recovered changes to staging and verified the actual runtime.

# 8. Git Recovery and Synchronization

A major part of the recovery was ensuring that AI Studio's code changes reached GitHub.

Initially:

`git status -sb`

showed:

`## main...origin/main`

The Mac repository was clean.

Google AI Studio's investigation confirmed that eight Phase 7 code changes were still in its workspace but were not yet in GitHub main.

The recommended recovery was to synchronize the exact code changes without force-pushing or overwriting existing files.

A permanent document was also created:

`docs/database/SAAS_DATABASE_INFO.md`

It contains the architecture, database history, troubleshooting findings, and recovery instructions.

On November 8, the Mac successfully pulled the changes:

`git pull origin main`

GitHub advanced:

`eabfb60..96b7f59`

The fast-forward update included:

- 8 Phase 7 application/test files.
- 1 database documentation file.

Git reported:

`9 files changed, 841 insertions(+), 48 deletions(-)`

The new isolation test file and database handoff document were created successfully.

This confirmed that the Phase 7 changes were now present in the local Mac repository.

# 9. Staging Deployment

Deployed using:

`npm run deploy:staging`

The deployment targeted:

`the-fragrance-store-staging`

The staging R2 binding was:

`fragrance-saas-media-preview`

The deployed staging Worker URL:

`https://the-fragrance-store-staging.mdsohail88008.workers.dev`

Do not confuse this deployment with production.

# 10. Final Verification — November 8, 2026

The Super Master Database Control Center finally reported both databases healthy.

## Control Plane

- Status: Connected.
- Role: Matched.
- Fingerprint: C720.
- Latency: approximately 143 ms in the final screenshot.

## Website A

- Status: Connected.
- Role: Matched.
- Data Access: Verified.
- Fingerprint: D8E7.
- Latency: approximately 49 ms in the final screenshot.
- Products/SKUs: 21.

The Website A connection changed from Connection Failed and Data Access Mismatch to Connected and Data Access Verified.

## Functional checks performed by Sohail

All three checks were explicitly confirmed:

1. Website A storefront products and images load successfully.
2. Admin CRUD operations work.
3. Website A remains connected after refreshing the Super Master Database Control Center.

**Recovery status: SUCCESSFULLY VERIFIED.**

# 11. Important Lessons Learned

1. A missing tenant credential is not necessarily a failed database server.
2. A database schema migration does not automatically register a tenant.
3. A connected Control Plane does not automatically prove that the tenant database is connected.
4. Cloudflare Worker request contexts must not share request-bound database I/O objects.
5. Global pools and in-flight promises require special care in Workers.
6. AI Studio Preview is not equivalent to the deployed Cloudflare Worker runtime.
7. A passing build does not prove database connectivity.
8. AI Studio workspace changes do not automatically reach GitHub.
9. Git history and actual file diffs must be checked before assuming changes are saved.
10. Keep the Control Plane and tenant database physically separate.

# 12. Current Project State

The following are completed:

- [x] Control Plane foundation migration.
- [x] Control Plane foundation tables verified.
- [x] Website A tenant registration implementation.
- [x] AES-256-GCM credential integration.
- [x] Phase 7 Worker request isolation implementation.
- [x] Neon HTTP query transport optimization.
- [x] Request-scoped database connection handling.
- [x] Request-scoped health-check handling.
- [x] Concurrent database health checks.
- [x] Isolation tests added.
- [x] Database recovery documentation created.
- [x] GitHub main synchronized to commit 96b7f59.
- [x] Staging Worker deployed.
- [x] Control Plane database connected.
- [x] Website A database connected.
- [x] Website A products and images load.
- [x] Admin CRUD works.
- [x] Website A remains connected after refresh.

# 13. Tomorrow's Starting Point

When starting the next conversation, use this handoff document as the source of truth.

Start with:

"We successfully recovered Website A's dedicated Neon PostgreSQL connection on November 8, 2026. Both Control Plane and Website A are healthy. Website A products and images load, admin CRUD works, and the connection remains stable after refresh. Phase 7 request-scoped Worker connection changes are synchronized to GitHub main at commit 96b7f59. Read the database handoff notes and continue from the current verified state."

Before starting new work:

1. Confirm local Git status.
2. Confirm the current branch and latest commit.
3. Confirm the staging Worker is still healthy.
4. Avoid repeating completed migrations.
5. Do not recreate Neon databases.
6. Do not change credentials unnecessarily.
7. Do not modify production during staging work.

Recommended first command:

`git status -sb`

Then inspect the next project task.

# 14. Strict Engineering Rules Going Forward

- Preserve existing multi-tenant database isolation.
- Never share tenant database credentials across tenants.
- Never expose secrets in logs or documentation.
- Never bypass encrypted credential resolution.
- Never silently fall back to another tenant database.
- Never run destructive SQL without explicit approval.
- Never force-push Git.
- Never reset working branches to recover changes without investigation.
- Never deploy staging changes to production accidentally.
- Keep changes minimal and focused.
- Verify real runtime behavior before declaring a problem fixed.

---

**Final milestone:** Website A — INHALE FRAGRANCES is successfully connected to its dedicated Neon PostgreSQL database, and storefront and admin functionality have been verified.

**Last verified:** November 8, 2026.
