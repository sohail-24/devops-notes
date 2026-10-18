# THE FRAGRANCE STORE — HOUSE OF BRANDS
## Complete Project Continuation Notes

**Last updated:** 18 October 2026  
**Project:** The Fragrance Store — Multi-Tenant SaaS E-commerce Platform  
**Current priority:** Complete reliable tenant provisioning, authentication, and isolated storefront management.

---

# 1. PROJECT OVERVIEW

I am building a SaaS multi-tenant e-commerce platform called:

**The Fragrance Store — House of Brands**

The goal is to let me, as the platform owner, create and manage multiple independent online shops through one central Super Master dashboard.

Examples:
- Website A: INHALE FRAGRANCES
- Website B: Another perfume business
- Website C: Another independent shop
- Website D and additional tenants in the future

Each shop must have its own identity, administrator credentials, branding, products, customers, orders, and tenant-specific business data.

The platform must not behave like one shared shop where changing Website A accidentally changes Website B or Website C.

## Primary product requirement

From the Super Master dashboard, I should eventually be able to:

1. Create a new shop.
2. Set its shop name.
3. Upload its logo.
4. Create its administrator account and credentials securely.
5. Assign the correct tenant and role membership.
6. Open the newly created storefront.
7. Let that shop's administrator manage only the data and functions they are authorized to access.

The platform owner and shop administrators must have different access levels.

# 2. PROJECT LOCATION AND DEVELOPMENT ENVIRONMENT

**Local project path:**

`/Users/sohal/Downloads/testing-project/the-fragrance-store`

**Git branch previously reported:** `main`

**Environment:**
- MacBook Pro with Apple Silicon.
- Node.js and npm.
- Vite development server.
- Codex for code changes, debugging, testing, and code review.
- Google AI Studio has also been used for earlier implementation work.
- Local development URL previously used: `http://localhost:3000`.

Always verify the current Git status and branch before making significant changes. The branch and remote synchronization status must be rechecked rather than assumed.

The project has an existing `.env` file. It is gitignored. Never request that I paste secrets into chat, and never commit `.env`.

## Existing npm scripts

Run `npm run` to inspect the actual scripts available in the current checkout.

Previously observed scripts:

- `npm run dev` — start Vite development server on port 3000.
- `npm run build` — build the frontend and bundle the API server.
- `npm run check` — run TypeScript project checks.
- `npm run lint` — run ESLint.
- `npm run test` — run Vitest.
- `npm run preview` — preview the Vite production build.
- `npm run db:generate` — generate Drizzle migrations.
- `npm run db:migrate` — run Drizzle migrations.
- `npm run db:push` — push schema changes.
- `npm run db:baseline` — run the existing baseline script.

Do not run database migration, push, baseline, seed, or reset commands casually. First determine whether the change actually requires them.

# 3. TECHNOLOGY STACK

The project has been described and implemented around the following stack:

- Frontend: React 19, TypeScript, Vite 7.
- Styling: Tailwind CSS 3.4, Shadcn/Radix UI.
- Icons: Lucide React.
- Notifications: Sonner.
- Routing: React Router 7.
- Backend: Hono 4 integrated with Vite in development.
- API: tRPC 11.
- Database: Neon PostgreSQL.
- ORM: Drizzle ORM.
- Authentication: Existing session and cookie-based authentication mechanisms.
- Tests: Vitest.
- Build tooling: Vite and esbuild.

Verify the installed versions and current files before upgrading packages or changing architecture.

**Important:** Preserve the existing Neon PostgreSQL database, Drizzle schema, product data, orders, users, images, and authentication. Do not replace the existing application with a new scaffold.

# 4. SAAS ROLE HIERARCHY

The planned role hierarchy has four operational levels.

## Level 1 — Super Master / Platform Owner

The Super Master manages the SaaS platform itself.

Responsibilities:
- Platform overview.
- Create and manage shops.
- Inspect tenant status and metrics.
- Manage shop administrator access.
- Configure shop branding.
- View platform analytics.
- Manage subscriptions and platform settings.
- Inspect monitoring and audit logs.

The Super Master must not be treated as an ordinary tenant administrator.

## Level 2 — Business Owner / Shop Owner

Each shop owner manages their own shop.

Responsibilities:
- Shop profile and permitted settings.
- Products and catalog.
- Inventory.
- Orders.
- Customer management within the tenant.
- Staff and permissions where implemented.
- Storefront appearance.

A shop owner must not access another shop's private data.

## Level 3 — Tenant Operations and Staff

Roles include:
- `manager`
- `warehouse_staff`

Their permissions must be limited to the capabilities assigned to their roles and tenant memberships.

## Level 4 — Buyer / Customer

Buyers can access public storefront functionality and their own authorized customer/order data.

They must not access administrative APIs, platform management, other customers' records, or another tenant's private data.

**Security principle:** Hiding buttons in React is not sufficient. Every protected API must enforce authentication, authorization, and tenant isolation on the server.

# 5. SUPER MASTER DASHBOARD

The Super Master dashboard is available locally at:

`http://localhost:3000/super-master`

The dashboard contains or has been developed around:
- Platform Overview.
- Websites.
- Shop Owners.
- Analytics & Usage.
- Subscriptions.
- Monitoring & Errors.
- Audit Logs.
- Platform Settings.

The Websites section displays existing shops, including Website A.

Selecting Website A and opening Details displays its profile and configuration.

The details UI has separate areas such as:
- Profile & Metrics.
- Environment & Config.
- Shop Branding.

The exact current component implementation should be inspected before further changes.

## Website Details isolation requirement

Opening Website A → Details must display Website A's relevant configuration and branding, not the complete set of platform credentials or other tenants' private settings.

The same principle must apply to Website B, Website C, and all future tenants.

# 6. IMPORTANT AUTHENTICATION AND CONFIGURATION WORK COMPLETED

We previously discovered that the tenant configuration inventory incorrectly included platform Super Master credentials.

The platform-only keys were:

- `SUPER_MASTER_EMAIL`
- `SUPER_MASTER_PASSWORD`

These must remain platform-level credentials.

## Fix implemented

The Website A configuration service was updated to:
- Remove Super Master credentials from the Website A tenant configuration allowlist and inventory.
- Reject platform-only keys server-side.
- Avoid exposing or editing these credentials through the tenant configuration API.
- Filter historical platform-key events from Website A audit reads.
- Preserve existing Super Master authentication code and deployment-managed platform credentials.

Relevant file:

`api/services/websiteAConfigService.ts`

The dashboard was also updated to remove obsolete client-side validation for Super Master credentials in tenant settings.

Relevant tests included:

- `api/websiteAConfig.test.ts`
- `api/websiteAConfigPersistence.test.ts`
- `api/superMasterAuth.test.ts`

The focused configuration tests passed in previous runs. An earlier full authentication test had ordinary-admin failures because a persisted Website A administrator override took precedence over the default credentials assumed by the test.

Do not assume all authentication regression tests are now fixed. Inspect the current state and rerun tests safely.

# 7. TENANT ADMIN PASSWORD ENCRYPTION AND PERSISTENCE

We wanted to manage Website A's administrator credentials from its own configuration without exposing Super Master credentials.

An initial attempt to save `ADMIN_PASSWORD` failed.

## Root causes discovered

The encryption key was missing from local deployment configuration.

The relevant variable is:

`TENANT_CONFIG_ENCRYPTION_KEY`

The service correctly refused to store a secret in plaintext, but its error handling initially obscured the missing-key error.

A later correction made encryption occur before the database-write error handler so that missing-key and encryption-precondition failures could be reported accurately.

The encryption implementation was updated to use the live `process.env` value and validate the expected 256-bit key format.

## Local encryption setup

If the key is missing from the local environment, generate a fresh value with:

`openssl rand -hex 32`

Store the resulting 64-character hexadecimal value in the existing local `.env` file:

`TENANT_CONFIG_ENCRYPTION_KEY=<generated-value>`

Do not share the value, commit it, or expose it to frontend code.

Restart the development server after changing environment variables.

## Current understanding

The user subsequently confirmed that Website A's `ADMIN_PASSWORD` setting appeared saved and active in the Super Master configuration screen.

However, do not assume that every historical credential issue is resolved or that a specific administrator password is known. Verify login behavior manually before relying on it.

Never run a test that could overwrite a real administrator credential in the connected Neon database.

# 8. TENANT PROVISIONING WORK

We began extending the Create Website workflow so that the Super Master can provision a new tenant and its administrator.

Files previously modified or introduced in this work included:

- `api/queries/tenants.ts`
- `api/superMasterRouter.ts`
- `src/pages/SuperMasterDashboard.tsx`

The provisioning procedure was designed to validate tenant slug, administrator email, and password, and create the tenant, administrator, and membership transactionally.

This work is important but must be inspected and validated against the current repository before being considered complete.

Required behavior:
1. Validate shop details.
2. Validate the requested administrator identity.
3. Create the tenant.
4. Create or securely associate the administrator account.
5. Create the correct tenant membership and role.
6. Commit the related database writes atomically.
7. Roll back the transaction if provisioning fails.
8. Never assign unintended ownership or overwrite another user's existing tenant association.

Do not create default passwords or expose passwords in API responses.

A previous Codex report noted a possible test-process encryption key reaching a real PostgreSQL write and potentially replacing a Website A admin password with a test fixture. This was a reported potential mutation, not a confirmed recovered credential.

Never perform a blind database reset or overwrite to address that historical warning. Use an authorized manual login check and safe recovery flow if required.

# 9. TENANT BRANDING — LATEST FEATURE

This is the most recent completed feature.

## Requirement

From Super Master → Websites → Website A → Details, I want to configure:
- Shop Name.
- Shop Logo.

For example, Website A can be named `INHALE FRAGRANCES` and have its own logo.

When the storefront opens, the saved tenant name and logo must appear in the storefront instead of the old hardcoded platform branding.

Each tenant must retain its own branding.

## Existing database design discovered

The existing `companies` table already contains:
- `companies.name`
- `companies.logo`

The implementation uses the existing tenant data model rather than introducing a separate branding table.

The existing `product_images` asset store was selected for durable logo storage.

The intended design stores the logo bytes in the asset store and saves the appropriate tenant-specific logo reference in `companies.logo`.

Do not assume `companies.logo` must contain raw image bytes. Inspect the current implementation and schema to determine its expected representation.

## Files involved

The branding implementation involved these files:

- `api/services/tenantBranding.ts`
- `api/queries/tenants.ts`
- `api/boot.ts`
- `api/superMasterRouter.ts`
- `src/pages/SuperMasterDashboard.tsx`
- `src/pages/LandingPage.tsx`
- `api/tenantBranding.test.ts`

## Branding functionality implemented

The implementation added:
- Shop name editing.
- Logo upload and preview.
- PNG, JPEG, and WebP support.
- A maximum file size of 2 MB.
- Server-side file validation.
- Super Master-only branding mutations.
- Tenant existence validation.
- Tenant-specific database updates.
- An asset storage workflow.
- Clear Logo functionality with confirmation.
- Error and loading states.
- Tenant-aware storefront branding.
- Dynamic storefront header, mobile menu, footer, and document title.
- Safe generic fallback branding.

The backend uses the existing Super Master authorization mechanism.

No platform credentials should be exposed through the branding APIs.

## Previous testing

Codex reported:
- 11 focused tests passing across `api/tenantBranding.test.ts` and `api/websiteAConfigPersistence.test.ts`.
- Backend and frontend syntax checks passing.
- `git diff --check` passing.

At that point, no real database write, local server run, or browser verification had been performed.

## Branding save issue

The first implementation did not reliably save branding. The logo appeared temporarily, then disappeared after saving, and the old name returned.

We therefore asked Codex to trace the full save flow rather than merely change the UI.

The investigation needed to cover:
- Frontend form state.
- Save handler.
- tRPC request and response.
- Backend router.
- Super Master authorization.
- Tenant branding service.
- Database update.
- Logo asset storage.
- Logo retrieval.
- Cache invalidation and stale-state behavior.
- Storefront tenant resolution.

The required behavior was to return the saved branding from the server and update the UI from that successful result rather than restoring stale cached values.

## CURRENT STATUS — USER CONFIRMED WORKING

On 18 October 2026, I confirmed that the branding save flow is now working.

The Super Master Website Details screen shows the Shop Branding section, including:
- Shop Logo file selection.
- Logo preview.
- Shop Name input.
- Save Branding button.
- Clear Logo functionality.

The intended storefront URL pattern is:

`/store/<tenant-slug>`

The storefront should display the saved name and logo for the active tenant.

Important: the user confirmed the fix is working. However, a server-restart persistence check and full Website A/Website B browser isolation check should still be completed if they have not already been performed.

Do not claim those additional checks have passed unless there is actual evidence.

# 10. CURRENT MULTI-TENANT ISOLATION RULES

These are non-negotiable requirements.

## Tenant branding

- Website A branding changes affect Website A only.
- Website B branding changes affect Website B only.
- Website C branding changes affect Website C only.

## Credentials

- Each tenant must have its own administrator identity and credentials.
- Super Master credentials remain platform-only.
- Tenant configuration APIs must reject platform-only credentials.
- A buyer must not inherit administrator privileges.
- A tenant administrator must not become a Super Master.
- Tenant-specific credential updates must not modify another tenant.

## Products, customers and orders

- Products must be scoped to the correct tenant.
- Orders must use the correct tenant context.
- Customers must not see other customers' private records.
- Inventory must remain tenant-specific.
- A cart containing products from multiple tenants must not be silently assigned to a single supplier or tenant based on its first item.
- Tenant isolation must be enforced server-side, not only through frontend filtering.

## Lifecycle

The tenant lifecycle must use explicit states such as ACTIVE, SUSPENDED, and DEACTIVATED where supported.

Avoid irreversible physical deletion of a tenant and its related data as an ordinary dashboard operation. Review the existing lifecycle implementation before making changes.

# 11. CURRENT ROUTING AND STOREFRONT CONTEXT

Previously discussed routes include:

- `/super-master` — Super Master dashboard.
- `/admin/login` — dedicated administrator login.
- `/store/<tenant-slug>` — tenant storefront.

A prior requirement was that `/` should show the login page, while the storefront remains accessible through the appropriate Website entry in Super Master.

Routing has been modified in earlier work. Inspect `src/App.tsx` and the actual router configuration before changing route behavior.

The storefront should resolve its tenant from trusted server-side routing context, not arbitrary client-provided tenant identifiers.

The storefront's brand name, logo, and document title should reflect the active tenant.

# 12. RECOMMENDED DEVELOPMENT AND VERIFICATION WORKFLOW

For each new task:

1. Inspect the current Git status.
2. Read the relevant existing implementation.
3. Identify the root cause and affected files.
4. Preserve unrelated uncommitted work.
5. Implement the smallest safe change.
6. Add focused tests.
7. Run the focused tests.
8. Run `npm run check`.
9. Run `npm run build`.
10. Run `git diff --check`.
11. Review the actual diff.
12. Perform a local browser test when UI or integration behavior is involved.
13. Report exactly what was tested and what remains unverified.

Use the current project's actual scripts. If a check fails, diagnose the failure rather than suppressing it.

Tests must use isolated mock storage or a dedicated test database. They must not accidentally write fixture credentials into real Neon tenant records.

# 13. NEXT TASKS — PRIORITY ORDER

## PRIORITY 1 — Finish branding verification

The save issue is confirmed fixed by the user.

Still verify, where not already done:
- Shop name remains after closing and reopening Details.
- Logo remains after refresh.
- Branding remains after restarting the local server.
- Website A storefront uses Website A's saved branding.
- Website B branding changes do not affect Website A.
- Clearing a logo does not damage unrelated tenant assets.

Do not unnecessarily rewrite the working branding feature.

## PRIORITY 2 — Integrate branding into Create Website

The existing Create Website workflow previously did not include an atomic logo upload.

The long-term desired workflow is:

1. Click Create Website.
2. Enter the new shop name.
3. Enter a unique shop slug.
4. Enter administrator email and password through a secure form.
5. Upload the shop logo.
6. Create the tenant, administrator and membership safely.
7. Store the logo against the newly created tenant.
8. Show the new shop in the Super Master dashboard.
9. Open its storefront and see the correct branding.

Design this as a safe multi-step or transactional workflow.

A tenant ID must exist before its branding is associated with it, or the workflow must use a deliberate transaction that creates the tenant and asset association together.

Do not implement a fragile workflow that uploads an asset, loses the tenant association, or leaves orphaned assets when provisioning fails.

## PRIORITY 3 — Complete tenant administrator authentication

Verify:
- Each shop's administrator can sign in with that tenant's credentials.
- The authentication flow resolves the correct tenant.
- Only active tenant memberships are accepted.
- The user and membership roles are validated.
- Disabled or suspended tenants are handled according to the lifecycle policy.
- Buyer and administrator permissions remain separate.
- Super Master login continues working independently.

Earlier work described an isolated `authenticateTenantAdmin(email, password, tenantSlug)` implementation, but its current usage and integration status must be checked before relying on it.

Do not replace the existing login flow without understanding its current implementation.

## PRIORITY 4 — Audit tenant isolation across all data

Inspect products, inventory, cart items, orders, customer records, warehouses, and tenant memberships.

Prioritize:
- Every query includes trusted tenant scope where required.
- Mutations verify resource ownership.
- No cross-tenant records leak through joins or aggregate queries.
- Order creation derives tenant context correctly.
- Admin APIs cannot be invoked by buyers.
- Super Master-only operations remain protected.

Add focused isolation tests before refactoring business logic.

## PRIORITY 5 — Owner, staff and membership management

Verify secure creation and assignment of:
- Business owners.
- Managers.
- Warehouse staff.
- Buyers.

Preserve existing users and memberships. Do not overwrite a user's existing company association to simplify provisioning.

Implement invitations or membership assignment with appropriate validation if still missing.

## PRIORITY 6 — Subscription and tenant lifecycle

Once core isolation and authentication are reliable:
- Define tenant activation and suspension behavior.
- Implement subscription states and entitlements.
- Decide what storefront buyers see when a tenant is suspended.
- Add safe deactivation and reactivation.
- Ensure lifecycle changes do not destroy tenant data.

## PRIORITY 7 — Production readiness

After the core functionality is verified:
- Review session security and cookie settings.
- Review rate limiting and authentication abuse protection.
- Validate upload content, file size, and retrieval access.
- Review audit logging and secret redaction.
- Verify backup and recovery procedures.
- Review production environment configuration.
- Configure deployment, custom domains, TLS, and monitoring.
- Run an end-to-end tenant isolation test suite.

# 14. IMPORTANT HISTORICAL WARNINGS

Keep these warnings in mind when continuing:

1. An earlier configuration test may have written an administrator password fixture into real PostgreSQL. The extent and current credential state were not conclusively established. Never run a credential-writing test against the real database.

2. `TENANT_CONFIG_ENCRYPTION_KEY` must be configured correctly for encrypted tenant secret storage. Do not store plaintext passwords to bypass encryption failures.

3. Previous isolated tests passing did not prove that real database persistence worked. The branding save issue demonstrated why integration and browser checks matter.

4. A successful frontend preview does not prove that backend authorization or tenant isolation is secure.

5. Do not add a generic tenant configuration endpoint that accepts arbitrary client-supplied tenant IDs without server-side authorization.

6. Do not expose `SUPER_MASTER_EMAIL`, `SUPER_MASTER_PASSWORD`, JWT secrets, encryption keys, database URLs, or other platform secrets through tenant configuration screens or API responses.

7. Do not delete, reset, or overwrite production or persistent tenant data without an explicit, safe plan.

8. Do not undo the existing branding implementation merely to make Create Website easier. Reuse it through a properly designed provisioning workflow.

# 15. HOW TO START THE NEXT SESSION

Start a new ChatGPT conversation and paste these notes.

Then send this message:

"Mentor, read my The Fragrance Store SaaS project continuation notes completely. We are continuing from the current Codex workspace at `/Users/sohal/Downloads/testing-project/the-fragrance-store`.

The tenant Shop Branding save issue is now fixed and I confirmed that it works.

First, summarize the current state and distinguish confirmed functionality from items still needing verification. Then help me continue with the next priority: integrating shop name and logo into the Create Website workflow, while preserving tenant administrator credentials, role-based authorization, and strict Website A/B/C data isolation.

Before changing code, inspect the current repository and Git status. Preserve all existing work. Do not run database resets or use real credentials in tests. Work step by step, and give me the exact local commands and browser checks to verify each change."

# 16. FINAL PROJECT PRINCIPLES

The main objective is to build a secure, maintainable, production-grade multi-tenant SaaS platform—not merely a collection of storefront pages.

Always prioritize:

1. Data isolation.
2. Secure authentication and authorization.
3. Durable database persistence.
4. Safe tenant provisioning.
5. Independent tenant branding.
6. Reliable storefront behavior.
7. Automated tests and manual verification.
8. Maintainable architecture.
9. Production readiness.

Preserve existing project work and the Neon/Drizzle architecture.

Do not assume a feature is complete just because a UI exists or a mock test passes. Verify the actual behavior and clearly report what has and has not been proven.
