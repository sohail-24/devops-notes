# THE FRAGRANCE STORE — SaaS PROJECT HANDOVER NOTES

**Date:** November 9, 2026  
**Project:** The Fragrance Store — House of Brands  
**Current milestone:** Cloudflare Worker deployment, multi-domain routing, and tenant isolation verified  
**Next milestone:** Continue upgrading SaaS platform features.

---

# 1. Project Overview

The project is a multi-tenant B2B wholesale and fragrance e-commerce SaaS platform.

It supports:
- Multiple independent storefront websites.
- Individual shop owners.
- Separate tenant databases.
- Central SaaS administration.
- Product and inventory management.
- Customer accounts and orders.
- Custom domain routing.
- Cloudflare R2 image storage.
- Platform-level analytics and governance.

### Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript |
| Build | Vite 7, esbuild |
| Styling | Tailwind CSS 3.4, Shadcn UI |
| Routing | React Router 7 |
| Backend | Hono 4 |
| API | tRPC 11 |
| Database | Neon PostgreSQL |
| ORM | Drizzle ORM |
| Deployment | Cloudflare Workers |
| Object Storage | Cloudflare R2 |
| Previous deployment support | Netlify |
| Version control | GitHub |

# 2. SaaS Architecture

The platform follows a multi-tenant architecture with four role levels.

### Level 1 — Super Master

Platform administrator.

Responsibilities:
- Manage all websites.
- Manage tenant databases.
- Manage shop owners.
- View platform-wide analytics.
- Manage subscriptions.
- Manage platform settings.
- Monitor infrastructure and errors.
- Manage domain routing.

### Level 2 — Business Owner

Individual tenant/shop owner.

Responsibilities:
- Manage their shop.
- Manage products and categories.
- Manage inventory.
- Manage customers and orders.
- Configure storefront branding.
- Manage their business settings.

### Level 3 — Tenant Operations & Staff

Roles:
- Manager
- Warehouse Staff

Responsibilities depend on assigned permissions.

### Level 4 — Buyer & Customer

Responsibilities:
- Browse products.
- Add products to cart.
- Place orders.
- Manage account.
- Track orders.
- View Live Deals and wishlist.

# 3. Current Domains and Deployment

All three URLs have been confirmed working by the user.

### Website A — Customer Storefront

https://amfruits.shop

Brand: INHALE FRAGRANCES.

Expected functionality:
- Customer storefront.
- Product catalog.
- Categories.
- Product details.
- Cart and checkout.
- Customer accounts.
- Orders.
- Live Deals.

### Super Master — Platform Administration

https://platform.amfruits.shop/super-master

Expected functionality:
- Super Master login.
- Platform Control Center.
- Website management.
- Database management.
- Shop owners.
- Analytics and usage.
- Subscriptions.
- Monitoring and errors.
- Audit logs.
- Platform settings.

### Cloudflare Worker URL

https://the-fragrance-store-staging.mdsohail88008.workers.dev/super-master

This is the current technical Worker URL.

It also successfully opens Super Master and displays platform data.

**Important:** The Worker name contains `staging`. Do not assume this is a separate production Worker. Confirm the actual environment before changing deployment configuration.

# 4. Database Architecture

There are two important Neon PostgreSQL databases.

### Database A — SaaS Control Plane

Purpose:
- Platform governance.
- Tenant registry.
- Tenant configuration.
- Platform-level information.
- Tenant database credentials/configuration.

### Database B — Website A Tenant Database

Purpose:
- Website A products.
- Categories.
- Inventory.
- Product images and metadata.
- Customers.
- Orders.
- Tenant commerce information.

**Important database isolation rule:**

Website A's catalog belongs to Website A's dedicated Neon database.

The Control Plane database must not be treated as the authoritative Website A product catalog.

Never recreate either Neon database.

Never run unapproved migrations, seeds, or destructive SQL.

# 5. Cloudflare R2 Storage

Existing R2 configuration:

- Bucket: `fragrance-saas-media`
- Existing R2 connectivity test passed.
- Images are stored in Cloudflare R2.
- Application uses the existing R2 configuration.

Existing configuration includes:
- R2_ACCOUNT_ID
- R2_ACCESS_KEY_ID
- R2_SECRET_ACCESS_KEY
- R2_BUCKET_NAME

Do not change credentials or recreate buckets.

Do not perform another image migration without an explicit requirement.

# 6. Netlify and Deployment History

The project originally supported Netlify deployment.

Existing Netlify integrations and configuration were retained during the Cloudflare migration.

The application now supports Cloudflare Workers while preserving Node.js/Netlify database adapter compatibility.

Important distinction:
- Cloudflare Workers use the Neon serverless adapter.
- Node.js/Netlify uses the existing PostgreSQL adapter.

Do not delete Netlify integrations just because Cloudflare is now the active deployment platform.

# 7. Major Issues Solved During Recent Upgrades

## Issue 1 — Storefront Branding Not Updating

**Problem:**

Shop Name and Shop Logo configured inside:

Super Master → Websites → Website A → Details → Profile & Metrics → Shop Branding

were not consistently displayed across Website A pages.

**Root causes:**
- Branding was stored in the central Control Plane database.
- Storefront resolution was reading from the tenant database.
- An in-memory default business cache retained old branding.
- Logo delivery checked the wrong database.
- React Query did not invalidate all relevant caches.
- StorefrontHeader could disable its query when receiving a null tenant prop.

**Solutions implemented:**
- Updated `resolvePublicStorefront()`.
- Used authoritative Control Plane branding resolution.
- Added `clearDefaultBusinessCache()`.
- Improved logo delivery fallback.
- Added React Query cache invalidation.
- Fixed StorefrontHeader query hydration.

**Verification reported:**
- Branding updates propagated across storefront routes.
- Other tenants did not inherit Website A branding.
- Logo delivery was tested.
- 787 tests passed in that earlier verification run.

## Issue 2 — Cloudflare Worker Deployment Failure

**Error:**

`TypeError: The argument 'path' must be a file URL object, a file URL string, or an absolute path string. Received 'undefined'`

**Root cause:**

Cloudflare Workers use an ESM-based runtime.

The database adapter attempted to initialize Node.js `createRequire()` during Worker module initialization.

`import.meta.url` and `process.cwd()` were not providing a valid file path.

**Files updated:**
- `api/tenantDatabase/runtimeEnv.ts`
- `api/worker.ts`
- `api/tenantDatabase/driverAdapter.ts`

**Solutions:**
- Added `markWorkersRuntime(true)`.
- Improved Worker runtime detection.
- Prevented Node.js `createRequire()` from executing in Workers.
- Preserved Neon serverless adapter for Cloudflare.
- Preserved Node PostgreSQL adapter for Netlify.

## Issue 3 — Platform Domain Redirecting to Website A

**Problem:**

`platform.amfruits.shop/super-master`

was incorrectly opening Website A's storefront.

**Root causes:**
- Platform hostname was not recognized as a reserved platform domain.
- `isCustomerCustomDomain()` classified it as a customer domain.
- Unauthenticated Super Master routing redirected to `/`.
- The root route loaded Website A's storefront.
- Website A fallback tenant resolution was not excluded.

**Files updated:**
- `api/controlPlane/types.ts`
- `api/controlPlane/registry.ts`
- `api/context.ts`
- `api/middleware.ts`
- `src/App.tsx`
- `src/pages/SuperMasterDashboard.tsx`

**Solutions:**
- Registered `platform.amfruits.shop` as a platform governance hostname.
- Updated `isPlatformHost()`.
- Updated `isCustomerCustomDomain()`.
- Prevented platform domains from resolving to Website A's default tenant.
- Rejected customer storefront procedures on platform governance hosts.
- Preserved Super Master login routing.

## Issue 4 — Cloudflare Worker Deployment Configuration

**Changes:**

`wrangler.toml`:
- Added explicit staging environment.
- Preserved production Worker configuration.
- Added `nodejs_compat`.

`package.json`:
- Added `deploy:staging`.
- Configured explicit staging deployment.

Command:

```bash
npm run deploy:staging
```

Equivalent:

```bash
npx --yes wrangler deploy --env staging
```

The previous deployment validation command:

```bash
npm run deploy:staging:dry-run
```

completed successfully.

**Important:** A dry run is not an actual deployment. The user subsequently confirmed that all three URLs were working.

# 8. Cloudflare DNS and Custom Domain Resolution

Initially, Website A returned:

`Cloudflare Error 522 — Connection Timed Out`

The DNS configuration showed:

```text
CNAME
Name: amfruits.shop
Target: platform.amfruits.shop
Proxy: DNS only
```

This was an incorrect configuration for the intended architecture.

**Solution:**
1. Removed the incorrect root-domain CNAME.
2. Opened Cloudflare Workers & Pages.
3. Selected `the-fragrance-store-staging`.
4. Opened Domains.
5. Added `amfruits.shop` as a Custom Domain.
6. Preserved `platform.amfruits.shop` as an existing Worker domain.
7. Verified both domains.

Final observed configuration:

```text
Worker: the-fragrance-store-staging

Custom Domains:
1. platform.amfruits.shop
2. amfruits.shop
```

Both domains use the same Worker.

The application distinguishes requests using hostname-based routing.

# 9. Important Current Behavior — Website A Data on Platform Domain

The following test was performed:

**Website A:**

```text
https://amfruits.shop/products
```

Result:
- Products visible.
- Five releases displayed.
- Categories visible.
- Storefront working.

**Platform domain customer storefront route:**

```text
https://platform.amfruits.shop/store/the-fragrance-store/products
```

Result:
- Zero products.
- No fragrance catalog displayed.
- Only the All category appeared.

**Super Master:**

```text
https://platform.amfruits.shop/super-master
```

Result:
- Super Master works.
- Platform information is accessible.

### Why this happens

The recent domain-isolation changes explicitly classify `platform.amfruits.shop` as a platform governance domain.

Customer storefront requests on that domain do not receive the default Website A tenant context.

Therefore, the zero-product result is consistent with the new hostname isolation rules.

It does not, by itself, prove that Website A's database is empty or disconnected.

### Final architecture decision

Keep these responsibilities separate:

- `amfruits.shop` = Website A customer storefront.
- `platform.amfruits.shop` = SaaS administration.
- `workers.dev` = technical Worker access and testing.

Do not change the platform-domain isolation merely to display Website A products on the Super Master domain.

# 10. Latest Verification Results

Google AI Studio reported the following results after the November 9 changes:

| Verification | Result |
|---|---|
| Test files | 90/90 passed |
| Total tests | 794 passed |
| ESLint | 0 errors |
| Vite production build | Passed |
| Cloudflare staging dry run | Passed |
| R2 bindings | Validated in dry run |
| Worker runtime adapter | Tests passed |
| Platform hostname classification | Tests passed |
| Website A fallback isolation | Tests passed |

These are AI Studio's reported verification results, not a new independent test run.

# 11. Non-Negotiable Safety Rules

Before future upgrades, preserve the following:

1. Never recreate the existing Neon databases.
2. Never delete or reset Website A tenant data.
3. Never delete existing Netlify integrations.
4. Never change R2 bucket settings or credentials without approval.
5. Never run destructive SQL without explicit approval.
6. Never run tenant migrations without checking their purpose and impact.
7. Never seed the database unnecessarily.
8. Never remove existing Cloudflare custom domains.
9. Never overwrite production Worker configuration while deploying staging.
10. Never expose database URLs, passwords, API keys, or credentials in logs or reports.
11. Maintain tenant isolation.
12. Verify existing data persistence after relevant changes.

# 12. Next Upgrade Roadmap

Infrastructure and routing are now working. The next focus should be SaaS functionality.

### Phase 1 — SaaS Platform Audit

Before introducing new features:
- Review the current Super Master dashboard.
- Review all existing routes.
- Review role permissions.
- Check the website management workflow.
- Check tenant database status.
- Identify incomplete features and bugs.
- Avoid rebuilding functionality that already exists.

### Phase 2 — Website Management

Improve:
- Create Website workflow.
- Website activation and suspension.
- Tenant profile management.
- Custom domain management.
- Website-specific configuration.
- Website status and health.

### Phase 3 — Shop Owner Management

Improve:
- Shop owner creation.
- Shop owner authentication.
- Role assignment.
- Tenant ownership mapping.
- Staff management.
- Permission enforcement.

### Phase 4 — Database Control Center

Improve:
- Database connectivity monitoring.
- Tenant database identity verification.
- Migration status.
- Connection health.
- Database isolation diagnostics.
- Safe tenant provisioning.

### Phase 5 — SaaS Subscriptions

Improve:
- Subscription plans.
- Monthly/yearly billing.
- Tenant plan assignment.
- Usage limits.
- Subscription expiry.
- Payment status.
- Plan upgrades and downgrades.

### Phase 6 — Analytics and Monitoring

Improve:
- Platform-wide sales.
- Individual tenant sales.
- Orders and customers.
- API health.
- Worker errors.
- Storage usage.
- Tenant activity.

### Phase 7 — Production Readiness

Eventually:
- Configure a dedicated production Worker.
- Keep staging separate.
- Establish a deployment checklist.
- Configure backups and recovery procedures.
- Verify custom domains and SSL.
- Run security and tenant-isolation tests.
- Complete end-to-end production verification.

Do not start production migration until the staging architecture and deployment workflow are fully understood.

# 13. How to Resume in the Next Chat

When starting the next conversation, upload or paste these handover notes and say:

"Mentor, let's continue upgrading The Fragrance Store SaaS project. Read the complete November 9 handover notes first. Our Cloudflare deployment, all three URLs, domain routing, and tenant isolation are working. We must preserve both Neon databases, R2, Netlify integrations, and existing tenant data. We are now moving to the next SaaS upgrade phase. First audit what is already implemented, then recommend the next improvement. Guide me step by step."

### Current project status

- Cloudflare Worker: Working.
- Website A: Working.
- Super Master: Working.
- Custom domains: Working.
- Neon databases: Existing databases preserved.
- R2: Existing configuration preserved.
- Netlify: Integrations retained.
- Tenant isolation: Implemented and tested.
- Next task: Continue SaaS platform feature upgrades.

---

**END OF HANDOVER NOTES**

**Last updated: November 9, 2026**
