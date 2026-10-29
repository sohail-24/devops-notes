# The Fragrance Store SaaS — Project Handover Notes
## Last Two Days: October 28–29, 2026

**Project:** The Fragrance Store — House of Brands  
**Website A:** INHALE FRAGRANCES  
**Tenant slug:** `the-fragrance-store`  
**Production domain:** `https://amfruits.shop`  
**Platform domain:** `https://fragrance.sohaildevops.site`  
**Deployment:** Netlify  
**Database:** Neon PostgreSQL  
**Development assistant:** Google AI Studio (Gemini)  
**Code repository:** `sohail-24/the-fragrance-store`  
**Local project path:** `/Users/sohal/Downloads/testing-project/the-fragrance-store`

**Current status:** Website A's catalog has been populated, production API routing and tenant-resolution fixes have been implemented, and the user has confirmed that the website is now working after deployment.

---

# PART 1 — Project Architecture and Existing Decisions

## 1.1 Technology stack

- Frontend: React 19, Vite 7, TypeScript.
- Styling: Tailwind CSS 3.4, Shadcn/Radix UI.
- Routing: React Router v7.
- Backend: Hono v4, tRPC v11.
- Serialization: SuperJSON.
- Database: Neon PostgreSQL.
- ORM: Drizzle ORM.
- Hosting: Netlify with serverless functions.
- Tenant database connections: Tenant database connection manager and encrypted tenant credentials.
- Database schema and migrations: Drizzle migrations.
- Product images: Persistent product-image records and fragrance SVG assets.

## 1.2 Multi-tenant architecture

The application separates platform administration from each shop's commerce data.

**Super Master / Control Plane**
- Manages tenants, domains, database configuration, platform settings, and other platform-level operations.
- Uses the configured control-plane database and authentication infrastructure.

**Website A / Data Plane**
- Brand: INHALE FRAGRANCES.
- Dedicated Neon project: `website-a`.
- Database: `neondb`.
- Owns the fragrance catalog and tenant commerce records.

**Customers and shop administrators**
- Customers browse products and place orders.
- Authorized tenant administrators manage categories, products, inventory, and store operations.

Important security rule: Website A must never silently read its catalog from the central platform database. Unknown domains must not be assigned to Website A simply because they fail to resolve elsewhere.

## 1.3 Existing deployment and domain decisions

- Netlify is the deployment platform.
- Cloudflare manages DNS for `sohaildevops.site`.
- Website A uses a custom domain rather than relying exclusively on a subdomain.
- The canonical tenant storefront route is `/store/the-fragrance-store`.
- The production domain used during the latest investigation is `amfruits.shop`.
- Netlify environment variables and deployed serverless-function configuration must agree with the current application architecture.

---

# PART 2 — October 28: Tenant Database and Catalog Investigation

## 2.1 Problem discovered

The Website A admin Categories page displayed:

- Total Categories: 0
- Active Categories: 0

The storefront catalog was empty even though the application had previously been developed with fragrance categories and products.

The initial investigation also encountered this configuration error:

`Control-plane database is required in production: CONTROL_PLANE_DATABASE_URL and CONTROL_PLANE_DATABASE_NAME must be configured.`

The problem involved tenant-context resolution and database configuration, but fixing the configuration error alone did not populate the catalog.

## 2.2 Database isolation investigation

We established the intended source of truth:

| Database | Responsibility |
|---|---|
| `website-a` | Website A's actual fragrance catalog and commerce data |
| `fragrance-project` | Central/platform data and historical template data |

The central database contained 13 category records and 15 products. However, those products originated from the old Tex's Chicken & Burgers template, including fast-food items.

The original fragrance catalog was defined in application mock data, including `api/queries/mockDb.ts` and `src/pages/LandingPage.tsx`. Those definitions had not been seeded into Website A's PostgreSQL database.

**Decision:** Reject fallback to the central catalog and reject copying the central products into Website A.

This preserves physical tenant isolation and prevents fast-food data from appearing on the fragrance storefront.

## 2.3 Tenant database routing fixes

The investigation covered the following files and areas:

- `api/controlPlane/connection.ts`
- `api/controlPlane/registry.ts`
- `api/middleware.ts`
- `api/services/websiteADatabaseHealthService.ts`
- `api/services/websiteAConfigService.ts`
- `api/tenantDatabase/secretProvider.ts`
- `api/tenantDatabase/connectionManager.ts`
- Tenant routing and database diagnostics tests.

The key goals were to:

1. Resolve the correct Website A tenant context.
2. Retrieve the encrypted tenant database credentials.
3. Acquire the dedicated tenant database connection pool.
4. Execute catalog queries inside the correct tenant scope.
5. Prevent accidental fallback to the central database.

The application was also updated to support the tenant's database configuration and diagnostics.

The exact list of files changed in each earlier iteration should be verified from Git history if a detailed code audit is needed.

---

# PART 3 — October 28: Safe Catalog Seeder

## 3.1 Seeder implementation

Google AI Studio created the following files:

` scripts/seed-website-a-catalog.ts `

` api/tenantDatabase/websiteACatalogPersistence.test.ts `

The script was designed to populate Website A with the intended fragrance catalog, not the old central database records.

### Safety features

- Dry-run mode by default.
- Explicit execution confirmation required for writes.
- Target endpoint validation.
- Rejection of central database targets.
- Connection-string and password redaction.
- Schema and migration validation before execution.
- Transactional insertion.
- Idempotent handling of existing category and product slugs.
- No DROP, DELETE, or TRUNCATE operations.
- Preservation of existing administrator-managed records.

The intended live execution command was:

```bash
npx tsx scripts/seed-website-a-catalog.ts --confirm-execution
```

The user initially ran the script without confirmation:

```bash
npx tsx scripts/seed-website-a-catalog.ts
```

The output correctly indicated dry-run mode and proposed 7 categories, 15 products, and 15 inventory rows, with zero writes.

## 3.2 Successful database population

The user subsequently executed the approved seed operation from the local terminal. The Neon console then showed the categories and products in the `website-a` database.

### Seeded category definitions

| # | Category | Slug |
|---|---|---|
| 1 | Oud & Oriental | `oud-oriental` |
| 2 | Woody & Amber | `woody-amber` |
| 3 | Fresh & Citrus | `fresh-citrus` |
| 4 | Floral | `floral` |
| 5 | Gourmand | `gourmand` |
| 6 | Attar & Perfume Oils | `attar-perfume-oils` |
| 7 | Gift Sets & Discovery Sets | `gift-sets-discovery-sets` |

### Intended fragrance products

The seed definitions included these 15 products:

1. Sauvage Extrait de Parfum
2. Baccarat Rouge 540
3. Aventus Luxury Millésime
4. Bleu de Chanel Parfum
5. Oud Wood Private Blend
6. Miss Dior Blooming Bouquet
7. 1 Million Elixir Parfum Intense
8. Jazz Club Replica Eau de Toilette
9. Royal Taif Rose Artisanal Attar
10. Cambodian Agarwood Supreme Bakhoor
11. Haute Parfumerie Discovery Coffret
12. Dehn el Oud Cambodi Special Reserve
13. Velvet Bourbon Vanilla & Cocoa
14. Neroli Portofino Aqua Fraiche
15. Midnight Jasmine & Tuberose Extrait

The script also created the intended inventory associations.

Product definitions include fragrance descriptions, pricing in INR, presentation and bottle-size options, and SVG image paths.

**Important distinction:** The seed operation was intended to insert 15 products. A later Neon screenshot showed 18 rows, including three additional entries named `Test Fragrance Creation`, `Diagnostic Fragrance P...`, and `INHALE SPECIAL`. These may be test records created during later troubleshooting. Their exact origin and intended disposition have not been confirmed. Preserve them until their ownership and dependencies are checked.

## 3.3 Database persistence verification

The following was established:

- Website A's dedicated database contains the intended fragrance categories and products.
- The Categories admin page subsequently displayed 7 total and 7 active categories in the AI Studio preview.
- The storefront preview displayed fragrance product cards.
- The catalog did not need to be reseeded again.

The catalog's persistence was not the remaining root cause of the production problem.

---

# PART 4 — October 28–29: API and Admin Error Investigation

## 4.1 The JSON parsing error

The admin Categories page previously displayed an error similar to:

`Unexpected token '<', "<html><hea..." is not valid JSON`

This indicated that the client was attempting to parse an HTML response as JSON. The source could be a missing API route, a server error page, or a fallback response rather than the expected tRPC payload.

The investigation led to changes involving:

- `vite.config.ts`
- `netlify/functions/api.ts`
- `api/app.ts`
- `src/providers/trpc.tsx`
- `api/queries/cart.ts`
- `src/pages/Categories.tsx`
- `api/tenantDatabase/adminApiHtmlResponseHandling.test.ts`

The tRPC client and server needed consistent response handling, especially for batched requests.

## 4.2 tRPC and SuperJSON handling

The application uses tRPC v11 and SuperJSON.

The changes were intended to:

- Preserve valid tRPC responses.
- Handle malformed or non-tRPC responses more safely.
- Avoid treating HTML as valid tRPC JSON.
- Preserve batch response count and ordering.
- Surface useful server errors instead of displaying misleading generic messages.
- Avoid fabricating successful API responses.

A previous implementation attempted to normalize non-tRPC responses into error envelopes. This area should be reviewed carefully if any new response-transformation errors occur.

## 4.3 Cart schema issue

A previous investigation also identified `cart_items.selectedOption`.

The schema already included the selected option, and the relevant migration history had been examined. Runtime DDL was removed from `api/queries/cart.ts` to avoid unapproved schema changes during ordinary requests.

Graceful error handling was added for cart totals.

No new production migration should be run merely to address the catalog routing problem.

---

# PART 5 — October 29: Administrator Membership Authorization

## 5.1 The product creation error

When the user tried to publish a fragrance from `/admin/products/new`, the interface displayed:

`You do not have permission to perform this action.`

The actual server error was:

`403 FORBIDDEN — Tenant access denied: You do not have an active administrator membership for this store.`

The failing procedure was:

`product.create`

It was invoked by the Publish Fragrance and Save Draft actions in `src/pages/AddProduct.tsx`.

## 5.2 Root cause

The application's administrator membership data and tenant commerce data were being looked up in different database contexts.

The request flowed through:

`product.create` → `tenantAdminQuery` → `requireTenantContext` → `verifyUserTenantMembership` → `findMembership`.

When `getDb()` ran inside the tenant scope, it resolved to Website A's dedicated Neon database.

However, the administrator membership record was held in the central authentication/control-plane database. Because the membership row was not found in the tenant database, the authorization check denied the legitimate administrator.

## 5.3 Fixes reported by Google AI Studio

Files changed:

- `api/queries/memberships.ts`
- `src/providers/trpc.tsx`
- `api/productRouter.test.ts`

The membership lookup was updated to consult the central database when required.

The tRPC client was updated to unwrap batch response arrays appropriately so actual server errors could be displayed.

Regression tests were added for legitimate administrator access, unauthenticated requests, Super Master access, and cross-tenant rejection.

The subsequent Phase 6 implementation further changed membership handling to reconcile or provision tenant membership rows for eligible administrators.

**Security condition:** Administrator reconciliation must only occur after the server has authenticated the user and verified trusted identity and tenant membership attributes. It must not turn a user-supplied company ID or role into an authorization grant.

---

# PART 6 — October 29: Why Google AI Studio Worked but Production Failed

## 6.1 Production symptoms

The user tested `https://amfruits.shop/categories` and inspected the browser console.

The console showed:

- `GET /api/trpc/product.list,...` → `404 Not Found`
- `GET /api/trpc/category.list` → `404 Not Found`
- `POST /api/trpc/category.create` → `409 Conflict`

The interface also displayed:

`Storefront domain is not registered or active in the tenant registry.`

Meanwhile, Google AI Studio's preview could show fragrance product cards and the seeded category count.

This established that a working preview was not sufficient proof of correct production API routing.

## 6.2 Production domain resolution root cause

The investigation found that `createContext` in `api/context.ts` called `service.resolveActiveTenantByDomain(host)` directly rather than using the shared domain-resolution helper.

The public tenant-scoping path in `api/middleware.ts` rejected the request when no tenant context was resolved for a custom domain.

The admin path had a fallback for verified Website A domains, but the public category and product listing paths did not apply the same resolution behavior.

As a result, the application could reject `amfruits.shop` before the public catalog queries reached Website A's database.

## 6.3 Phase 6 changes reported by Gemini

The following files were reported as changed:

| File | Intended correction |
|---|---|
| `api/controlPlane/registry.ts` | Added a shared verified-domain helper for Website A. |
| `api/tenantDatabase/requestContext.ts` | Unified tenant context resolution for verified domains. |
| `api/context.ts` | Used the shared tenant-resolution helper when creating request context. |
| `api/middleware.ts` | Unified public and admin tenant resolution while retaining authorization checks. |
| `netlify.toml` | Added an explicit `/api/*` rewrite before the SPA fallback. |
| `netlify/functions/api.ts` | Normalized Netlify function request paths before dispatching to Hono. |
| `api/app.ts` | Added support for the intended tRPC handler paths and consistent error handling. |
| `api/amfruitsProductionRouting.test.ts` | Added regression tests for production routing, domain resolution, and authorization. |

The implementation was intended to recognize `amfruits.shop`, `www.amfruits.shop`, and configured Website A domain aliases while continuing to reject unknown third-party domains.

The report also noted that `WEBSITE_A_DATABASE_URL`, `CUSTOM_DOMAIN` or `STOREFRONT_DOMAIN`, `SESSION_SECRET`, and `VITE_TRPC_URL` may need to be checked in Netlify.

These variables must be validated against the actual current code and deployment configuration. The report alone does not prove that every variable is required or that production already has the correct values.

## 6.4 Why the category creation returned 409

The database already contained the seven seeded fragrance categories.

Because the public listing request failed, the page appeared empty. The user attempted to create a category that already existed.

The backend's duplicate name/slug checks and database uniqueness constraints rejected the duplicate request with HTTP 409 Conflict.

This was a downstream consequence of the listing failure, not evidence that the categories had disappeared.

Do not delete the existing categories or remove uniqueness constraints to suppress this error.

---

# PART 7 — Final Verification and Deployment

## 7.1 Reported verification results

The final Google AI Studio Phase 6 report stated:

- 66 test files passed.
- 486 tests passed with zero failures.
- ESLint completed with zero errors and zero warnings.
- The application build completed successfully.
- Regression tests covered the custom domain, public catalog routes, duplicate category behavior, authorization, and Netlify request path normalization.

These are the reported results from the AI Studio session.

## 7.2 Production deployment

The recommended next steps were to commit and push the changed files to the GitHub branch connected to Netlify, then trigger a new production deployment.

The user subsequently confirmed that the website was working after the deployment process.

The final user-confirmed state is:

- The fragrance catalog is available.
- Website A's dedicated database is populated.
- The previous production API and tenant-resolution issues have been addressed.
- The user reports that the website is now working.

No further seed operation is required.

---

# PART 8 — Current Known State

| Area | Current understanding |
|---|---|
| Website A Neon database | Populated with the intended fragrance catalog. |
| Categories | 7 seeded categories; the admin preview displayed all 7 as active. |
| Products | 15 intended seeded products; a later database screenshot showed 18 total rows, including 3 apparent test records. |
| Inventory | 15 inventory rows were intended by the seeder. |
| Tenant isolation | Must remain strict; no fallback to the central catalog. |
| Admin membership | Central membership lookup and tenant authorization changes implemented. |
| Custom-domain resolution | Verified-domain handling implemented in Phase 6. |
| Netlify API routing | Explicit API rewrite and function path normalization implemented in Phase 6. |
| Tests | Final AI Studio report stated 486 passing tests. |
| Production | User confirmed the website works after deployment. |
| Google AI Studio | Available for continued project work, subject to usage quotas. |
| Codex | Usage limit had expired at the time of the latest debugging session. |

**Tenant ID note:** The latest investigation reports identify Website A's tenant ID as `00000000-0000-4000-8000-000000000001`. Earlier reports contained a different ID. Verify the authoritative tenant ID from the current registry before writing scripts or changing tenant records.

---

# PART 9 — What We Should Do Next

The urgent production issue is resolved according to the user's latest confirmation. The next phase should focus on stability and product quality, not another broad rewrite.

## Priority 1 — Protect the working production system

1. Record the current successful production deployment and its Git commit.
2. Preserve the current Neon database and tenant configuration.
3. Confirm that no accidental fallback to the central catalog was introduced.
4. Review the latest changes to authorization and domain resolution.
5. Keep a record of the three extra product rows before deciding whether any cleanup is appropriate.

Do not reseed or migrate the live database without a specific reason.

## Priority 2 — Test the admin-to-storefront workflow

Use a controlled test to verify:

1. Sign in as the authorized Website A administrator.
2. Create a clearly identifiable test category.
3. Refresh the admin page and verify persistence.
4. Create a test fragrance product with a valid category and inventory.
5. Confirm the product appears on the storefront.
6. Edit the product and verify that the changes persist.
7. Verify that unauthorized users cannot access admin mutations.
8. Remove temporary test records only after checking dependencies and confirming that they are not real catalog data.

The goal is to verify the entire data flow, not merely whether a page renders.

## Priority 3 — Validate production on mobile

Test the live domain on the phone:

- Homepage and hero.
- Shop and category listings.
- Product detail and bottle-size options.
- Cart and checkout.
- Account registration and login.
- Admin login and catalog management.
- Mobile bottom navigation: Home, Shop, Bag, More, Account.

Check for console errors, broken product images, incorrect redirects, and layout problems.

## Priority 4 — Verify checkout and order persistence

Once catalog and admin workflows are stable, verify the complete customer journey:

`Storefront → Product → Cart → Customer Information → Payment → Bill / Order Confirmation`

Check that orders, order items, inventory, and selected bottle options persist in the intended tenant database.

Payment testing must use the configured test or sandbox mode where available. Do not assume that a successful order page proves a real payment was processed.

## Priority 5 — Audit tenant isolation and security

Test that:

- Website A can only access its own commerce records.
- Unknown domains are rejected safely.
- Cross-tenant users cannot create or modify products.
- The Super Master role is distinct from tenant administrator roles.
- Secrets and database connection strings are never exposed to the browser or logs.
- Database credentials and tenant configuration remain isolated.

## Priority 6 — Improve observability

Once the application is stable, consider:

- Structured, sanitized server logs.
- Request IDs for tracing production errors.
- Clear health checks for API, control plane, and tenant database.
- Monitoring for failed API requests.
- A repeatable smoke-test checklist after each deployment.

Avoid noisy monitoring that consumes unnecessary free-tier resources.

---

# PART 10 — Important Files to Know

The following are the key files identified during this investigation. Always inspect their current contents before making another change.

### Production routing and serverless runtime

- `netlify.toml`
- `netlify/functions/api.ts`
- `api/app.ts`
- `api/boot.ts`
- `vite.config.ts`

### Tenant resolution and authorization

- `api/context.ts`
- `api/middleware.ts`
- `api/controlPlane/registry.ts`
- `api/tenantDatabase/requestContext.ts`
- `api/queries/memberships.ts`
- `api/tenantDatabase/connectionManager.ts`
- `api/tenantDatabase/secretProvider.ts`

### Catalog operations

- `api/categoryRouter.ts`
- `api/productRouter.ts`
- `api/queries/categories.ts`
- `api/queries/products.ts`
- `api/queries/mockDb.ts`
- `scripts/seed-website-a-catalog.ts`

### Client and error handling

- `src/providers/trpc.tsx`
- `src/pages/Categories.tsx`
- `src/pages/AddProduct.tsx`

### Regression tests

- `api/tenantDatabase/websiteACatalogPersistence.test.ts`
- `api/tenantDatabase/routingIsolation.test.ts`
- `api/tenantDatabase/websiteAStorefrontRouting.test.ts`
- `api/productRouter.test.ts`
- `api/amfruitsProductionRouting.test.ts`

Some paths may have changed or been renamed. Confirm them from the current repository before editing.

---

# PART 11 — Rules for Continuing This Project

1. Never rebuild the project from scratch when the existing implementation can be extended.
2. Never assume that Google AI Studio preview behavior proves production correctness.
3. Always distinguish frontend rendering, API routing, tenant resolution, authorization, and database persistence.
4. Never fall back to the central database to make a tenant storefront appear populated.
5. Never rerun the catalog seeder just because a page looks empty.
6. Investigate the actual HTTP status and server error before changing error handling.
7. Protect existing category, product, inventory, customer, and order data.
8. Prefer small, evidence-based changes and focused regression tests.
9. Verify administrator authorization before allowing membership reconciliation or provisioning.
10. Do not deploy after every small code edit. Test the complete affected workflow first.
11. Keep secrets out of prompts, screenshots, reports, logs, and Git.
12. If Google AI Studio reaches its quota, preserve the latest working code and handover notes before switching tools or sessions.

---

# PART 12 — Ready-to-Use Prompt for the Next ChatGPT Session

Paste the following prompt when continuing this project in a new conversation:

Continue mentoring me on my existing project, **The Fragrance Store SaaS**, based on the complete handover notes above.

My Website A brand is INHALE FRAGRANCES, with tenant slug `the-fragrance-store` and production domain `https://amfruits.shop`.

We spent October 28–29, 2026, diagnosing and fixing the Website A catalog database, tenant routing, administrator authorization, custom-domain resolution, tRPC response handling, and Netlify production API routing.

The Website A Neon database was successfully populated with 7 fragrance categories and 15 intended fragrance products. The catalog seeder is `scripts/seed-website-a-catalog.ts`; do not rerun it or alter existing catalog records without a specific reason.

Google AI Studio implemented production fixes across the Netlify function, API router, tenant context, domain registry, middleware, and regression tests. Its final report stated that 486 tests passed, lint passed, and the build succeeded. I subsequently confirmed that the website works after deployment.

I want you to continue from this state, not restart the project.

First, help me verify and stabilize the working production application. Then guide me through the admin-to-storefront persistence workflow, mobile testing, checkout and order persistence, and tenant security.

Use direct, practical mentor-style guidance. If a problem occurs, identify the exact failing layer before suggesting changes. Protect the existing Neon data and strict physical tenant isolation. If you need to inspect files or logs, ask for only the specific information required. Do not assume that previous AI-generated reports prove that the current code or production environment is correct.

At the beginning, summarize the current state briefly and recommend the single highest-priority next task.

---

**End of handover notes.**
