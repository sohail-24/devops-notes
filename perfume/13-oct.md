# The Fragrance Store SaaS — Complete Project Continuation Notes

**Project:** The Fragrance Store — House of Brands  
**Repository:** `sohail-24/the-fragrance-store`  
**Development environment:** Google AI Studio Build  
**Current date:** October 14, 2026  
**Project type:** Multi-tenant SaaS e-commerce platform  
**Current phase:** Super Master platform foundation, authentication hardening, and tenant-aware website routing  
**Working style:** Mentor guidance, step-by-step implementation, focused Google AI Studio prompts, and verification after each phase.

---

# 1. Project Vision

We are building a SaaS platform that allows multiple independent businesses to operate their own e-commerce websites through one shared platform.

The first shop is **The Fragrance Store — House of Brands**. Future shops may be called Website B, Website C, and so on internally, while each business can have its own public brand name and custom domain.

The platform must allow the platform owner to create, configure, manage, and monitor every shop without entering each shop's administrative dashboard for routine platform-level operations.

The long-term architecture should support many shops, even though the initial target is only 4–5 shops.

## Core principle

One SaaS platform, multiple independent websites, strong tenant isolation.

Each website must have its own:
- Products, categories, images, and prices.
- Inventory and orders.
- Customer accounts and private order history.
- Shop owner and authorized staff.
- Branding, logo, colors, banners, and contact details.
- Payment-provider credentials and configuration.
- Email notification and forwarding configuration.
- Custom domain and domain verification status.
- Settings and business-level analytics.

Customers must never access another customer's private data or another shop's private business information.

---

# 2. Technology Stack

Based on the implementation reports received from Google AI Studio:

- Frontend: React 19, TypeScript, Vite.
- Styling: Tailwind CSS and existing UI components.
- Routing: React Router.
- Backend: Hono and tRPC.
- Validation: Zod.
- ORM: Drizzle ORM.
- Database: Neon PostgreSQL.
- Authentication: Signed JWT/session architecture using `jose`.
- Testing: Vitest and existing integration tests.
- Development environment: Google AI Studio Build.
- Source repository: `sohail-24/the-fragrance-store`.

Important: Gemini's implementation reports are historical evidence of claimed changes. Future work must inspect the current code before assuming every reported behavior is correct.

---

# 3. The Three Main User Levels

## Level 1 — Super Master

The platform owner.

Responsibilities:
- Create websites/shops.
- Edit shop configuration.
- Activate, suspend, or deactivate shops.
- Assign shop owners and authorized staff.
- Reset access securely.
- Manage custom domains and verification.
- View platform-wide statistics.
- Monitor shop status, errors, uptime, and usage.
- Manage subscription plans and billing configuration.
- Configure platform-wide security and settings.
- Review platform audit logs.

The Super Master dashboard should be the central control center for the entire SaaS platform.

## Level 2 — Master / Shop Owner

The owner of an individual business.

Responsibilities:
- Manage that shop's products, prices, categories, and images.
- Manage inventory, warehouses, and orders.
- Customize branding and storefront settings.
- View their own sales and customers.
- Manage authorized staff if enabled.
- Configure their payment provider and email settings.
- Manage only their own website.

A shop owner must never gain platform-wide Super Master access.

## Level 3 — Customer / User

Responsibilities:
- Browse a selected shop.
- Search and view products.
- Add products to the cart.
- Check out and place orders.
- Track their own orders.
- Manage their own account and order history.

Customers must not access another customer's private data.

Note: The current codebase also has operational role concepts such as `manager`, `warehouse_staff`, and `buyer`. These can remain as subordinate roles within the three main business levels.

---

# 4. Database Status and Safety

The project uses a dedicated Neon PostgreSQL project named `fragrance-project`.

The user confirmed that the correct database is connected to the website and persistent saving is working.

Previous troubleshooting identified a dangerous legacy endpoint associated with the old Tex's Chicken & Burgers project. That endpoint must never be used for this SaaS.

## Database safety rules

- Never connect this project to the old restaurant database.
- Never reset or truncate the database.
- Never delete customer, product, order, inventory, cart, or image records as part of routine development.
- Do not run a migration without understanding its impact and obtaining explicit approval.
- Verify the active database endpoint before any database-changing operation.
- Never print connection strings or credentials.
- Do not silently accept mock/in-memory database mode as proof of persistence.
- Prefer non-destructive lifecycle status changes over physical deletion.

The earlier implementation reports describe a `tenant_memberships` table and migration `0006_tenant_memberships.sql`, plus an earlier migration `0007_order_items_options.sql`. Inspect actual migration state before creating or applying further migrations.

---

# 5. Work Completed According to Google AI Studio Reports

## Phase 1 — Super Master foundation

Reported implementation:
- Added the `super_master` role.
- Added the `isSuperMaster` authorization helper.
- Added server-side Super Master authorization middleware.
- Created tenant query helpers for platform statistics, listing, creation, updates, and status changes.
- Registered a `superMaster` tRPC router.
- Created `src/pages/SuperMasterDashboard.tsx`.
- Added routing for `/super-master`.
- Added initial navigation integration.
- Updated default business information to The Fragrance Store.

## Phase 2 — Security and tenant lifecycle hardening

Reported implementation:
- Tightened Super Master authorization.
- Removed broad admin/owner authorization bypasses.
- Removed physical tenant deletion from the implementation.
- Added non-destructive status controls.
- Added tenant membership schema and query helpers.
- Added tenant-aware order permissions.
- Added checks preventing carts/orders from mixing products from different shops.
- Filtered public product visibility for inactive shops.
- Added security and tenant-isolation tests.

The required shop lifecycle is:
- `ACTIVE`
- `SUSPENDED`
- `DEACTIVATED`

Suspension/deactivation must preserve historical business data.

## Phase 2.1 — Security review fixes

Reported implementation:
- Removed the `deleteTenant` mutation.
- Removed deletion controls from the Super Master UI.
- Tightened `isSuperMaster` and `superMasterQuery`.
- Added the `tenant_memberships` relation.
- Improved product and order isolation.
- Added security and tenant-isolation tests.

Earlier security review identified risks around missing tenant scoping, owner provisioning, and physical deletion. These were addressed in reported changes, but must continue to be tested as the platform grows.

## Super Master dashboard and console

The user initially could not find the dashboard because the preview was displaying the public storefront.

The implementation was then expanded to include the Super Master console at `/super-master`.

Reported sections:
1. Platform Overview
2. Websites
3. Shop Owners
4. Analytics & Usage
5. Subscriptions
6. Monitoring & Errors
7. Audit Logs
8. Platform Settings

Reported website management features:
- Create Website.
- Edit website settings.
- Assign a shop owner.
- Activate, suspend, or deactivate a website.
- View website details and metrics.
- Open a website's catalog/storefront.
- Display website status, catalog counts, order counts, and sales.

Reported monitoring/configuration states:
- Neon PostgreSQL connection and latency.
- Runtime information.
- External telemetry status.
- Recurring billing gateway configuration status.
- Central error aggregation configuration status.
- Audit log/streaming configuration status.

These external integrations were explicitly described as not configured where applicable. Do not present them as fully operational unless they are subsequently integrated and tested.

## Latest reported verification

Gemini reported:
- 24 test files passed and 106 tests passed after the authentication changes.
- Earlier, 23 test files and 99 tests were reported passing.
- ESLint completed with zero errors.
- `compile_applet` succeeded.

These results belong to different implementation runs. Re-run the current suite at the start of any major new phase rather than assuming the latest code still passes every test.

---

# 6. Current Authentication Configuration

The user requested only these five core application Secrets:

1. `DATABASE_URL`
2. `SUPER_MASTER_PASSWORD`
3. `JWT_REFRESH_SECRET`
4. `SUPER_MASTER_EMAIL`
5. `JWT_ACCESS_SECRET`

The `SUPER_MASTER_ID` setting is not wanted because the login form uses email and password.

## Authentication requirements

- Super Master signs in using `SUPER_MASTER_EMAIL` and `SUPER_MASTER_PASSWORD`.
- Super Master credentials are verified on the server.
- Super Master receives an authenticated session with the authoritative `super_master` role.
- JWT access and refresh tokens use the appropriate server-side signing secrets.
- Generic admin credentials cannot obtain Super Master privileges.
- Client-supplied roles and emails are not trusted.
- Ordinary shop-admin login remains functional.
- Missing Super Master configuration must fail closed.
- No passwords, JWT secrets, or database URLs may appear in browser bundles, API responses, or logs.

Gemini reported the original login failure was caused by references to `SUPER_MASTER_ID` instead of `SUPER_MASTER_EMAIL`, and by a configuration helper that was not exported/reading environment values correctly.

Gemini then reported fixes in:
- `api/lib/env.ts`
- `.env.example`
- `api/auth/admin-session.ts`
- `api/auth-router.ts`
- `src/pages/AdminLogin.tsx`
- `contracts/roles.ts`
- `api/superMasterDashboard.test.ts`
- `api/superMasterAuth.test.ts`
- `package.json`

The report says Super Master login should now be supported. However, the most recent screenshot showed the Super Master dashboard open in the preview, not a final successful login retest after all environment changes.

## Secrets cleanup

The five settings above are the desired core application Secrets. Before removing other Secrets from AI Studio, inspect whether existing integrations still use them.

Previously identified optional settings include:
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `RESEND_API_KEY`
- `SMTP_*`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `OWNER_EMAIL`
- `ADMIN_ORDER_EMAIL`

Some may still be required for payment checkout, notifications, or shop-admin authentication. Do not delete them blindly.

Editing `.env.example` does not remove a Secret from Google AI Studio's Secrets panel.

The user previously selected the AI Studio Secrets approach rather than a local `.env` workaround. Do not revert to local `.env` as a shortcut.

---

# 7. Current Routing Requirement — Most Recent Task

This is the immediate continuation point for tomorrow.

The user requested:

> Switch `/admin/login` to `/` as the main page, and switch `/` to Website A's page. When we click Website A inside the Super Master dashboard, Website A should open.

The assistant provided a focused implementation prompt to Google AI Studio. There is no confirmed final report yet showing that this routing task has completed successfully.

## Desired route behavior

### `/`
Display Website A's public storefront.

Website A currently corresponds to The Fragrance Store, using its actual tenant record and slug.

The root route must not redirect everyone to `/admin/login`.

### `/admin/login`
Keep this route available as the dedicated login page.

Expected behavior:
- Super Master login → `/super-master`
- Shop-admin login → authorized shop-admin workspace
- Customer navigation → public storefront/customer experience

### `/super-master`
Display the Super Master platform control center.

This is a platform management route, not the default public customer storefront.

### Clicking Website A in the Super Master dashboard
Open the selected tenant's storefront with its tenant context preserved.

The storefront must load only Website A's:
- Products.
- Categories.
- Branding.
- Public shop details.

There must be a clear way to return to `/super-master`.

### Future tenant routes
Prepare for Website B, Website C, and additional shops without hardcoding Website A as the only possible tenant.

Use tenant-aware routing and actual database records. Suspended, deactivated, or unknown shops must not accidentally show another shop's data.

## Important distinction

The same application serves two different kinds of pages:
- Public storefront: `/`
- Platform control center: `/super-master`

Do not merge them into one page or expose platform administration to customers.

---

# 8. Responsive UI Requirements

The user reported that mobile and desktop navigation were inconsistent.

Previously:
- Mobile storefront bottom navigation included Home, Shop, Categories, Cart, and Account.
- Desktop included a Super Master Console option.
- The Super Master console was not always easy to find in the mobile view.

The later UI report described:
- Platform-level navigation exclusively inside the Super Master console.
- Shop-owner operational navigation preserved separately.
- Mobile platform menu and header entry points.

Future UI work must verify the behavior rather than assume the reported implementation is correct.

Requirements:
- Mobile and desktop must offer consistent access to the same permitted capabilities.
- Layout may differ by screen size, but important actions must not disappear.
- Super Master-only controls must remain protected.
- Customers should not see platform administration controls.
- Shop owners must see only their authorized shop-management navigation.
- The storefront should remain mobile-first, with the existing luxury black-and-gold fragrance styling preserved.

---

# 9. Future Website Provisioning Design

The Super Master console will eventually become the main control center for creating and managing multiple shops.

Each shop's provisioning form should support:

## Basic identity
- Website display name.
- Internal website label, e.g. Website A, Website B, Website C.
- Unique slug.
- Business description/tagline.
- Contact email and phone.
- Business location.

## Owner and access
- Assign an existing shop owner.
- Securely invite/create a new shop owner.
- Reset owner access.
- Assign authorized staff.
- Store persistent memberships and roles.
- Prevent owners from accessing other tenants.

## Domain and branding
- Custom domain.
- DNS verification status.
- Logo and favicon.
- Theme colors.
- Homepage banners.
- Public contact information.

## Integrations
- Payment provider selection and configuration.
- Server-side payment credentials.
- Email notification provider and forwarding configuration.
- Shipping, tax, and checkout settings as needed.

## Operations
- Activate, suspend, or deactivate.
- View website health and usage.
- View product/order/sales metrics.
- Review security and audit events.
- Preserve historical data.

Sensitive payment and email credentials must be encrypted or managed through an appropriate secret-management mechanism. They must never be displayed in full after saving or returned to client-side code.

Do not place every shop's credentials in a public configuration object or expose them to other tenants.

---

# 10. Multi-Tenant Data Isolation Rules

All future implementation must follow these rules.

1. Every tenant-owned database query must be scoped to the authorized tenant.
2. Product listings must not combine products from unrelated shops.
3. Cart items must belong to the selected shop.
4. A checkout/order must not accidentally assign a multi-shop cart to the first product's supplier.
5. Customer accounts and order histories must be separated by shop as required by the product design.
6. Shop admins must be limited to their assigned tenant memberships.
7. Only Super Master may access platform-wide management and aggregates.
8. Suspended/deactivated tenants must not appear as active public shops.
9. Historical orders and financial records must be preserved.
10. Tenant IDs, roles, and permissions must be validated server-side.
11. Database foreign keys, indexes, and uniqueness constraints must enforce the intended relationships.
12. Security and isolation tests must accompany changes to APIs and tenant-aware queries.

A shared PostgreSQL database with tenant-aware records is the current architecture. Do not switch databases or introduce a different database system without a specific reason and explicit approval.

---

# 11. Development Workflow

Continue using Google AI Studio Build and focused prompts.

For every implementation phase:

1. Define the exact objective.
2. Inspect the existing implementation first.
3. Ask Gemini to change only the relevant files.
4. Preserve current functionality and data.
5. Run lint, build, and relevant tests.
6. Review the actual changed files and verification report.
7. Test the behavior in the development preview.
8. Fix any regressions before proceeding.
9. Keep a clear record of completed work versus planned work.

Avoid giant prompts that redesign multiple subsystems at once.

Do not publish or deploy without explicit approval.

Do not treat a successful build as proof of security, tenant isolation, or working database persistence.

---

# 12. Immediate Plan for Tomorrow

## Step 1 — Resume from the latest routing task

First, ask the user to share the final Google AI Studio output for the routing prompt if it completed.

If no final report exists, inspect the current implementation and continue the pending task.

Verify:
- `/` displays Website A's storefront.
- `/admin/login` remains available.
- Super Master login reaches `/super-master`.
- Website A opens from the Websites section in the Super Master dashboard.
- The selected tenant's products and categories remain isolated.
- Existing cart, checkout, and order history still work.

Do not redesign the dashboard yet.

## Step 2 — Fix any routing regressions

Check route guards, tenant resolution, product queries, cart behavior, and checkout assumptions.

Correct only the problems found.

## Step 3 — Test multi-tenant isolation

Use two real tenant records if available. Confirm that one shop cannot see another shop's private management data.

Do not create or modify database records without explicit approval.

## Step 4 — Review Super Master authentication

Confirm the login works with the configured Secrets and the session is recognized by server-side middleware.

Never ask the user to paste a password or connection string into chat.

## Step 5 — Build the shop-owner provisioning workflow

Once routing and authentication are stable, implement a secure owner invitation/assignment workflow with persistent tenant memberships.

Do not create insecure default passwords or silently elevate existing users.

---

# 13. Longer-Term Roadmap

### Phase A — Routing and authentication stability
- Finish root route and Website A routing.
- Confirm Super Master login.
- Confirm tenant-aware storefront behavior.
- Confirm existing customer and shop-admin flows.

### Phase B — Secure tenant ownership
- Shop-owner invitation and assignment.
- Membership and role management.
- Secure password onboarding/reset.
- Tenant-scoped admin APIs.
- Access-control tests.

### Phase C — Website provisioning
- Create Website A/B/C and future shops.
- Assign owner and contact details.
- Configure branding.
- Configure custom domains and verification.
- Safe activation/suspension/deactivation.

### Phase D — Independent shop operations
- Product/category/image management.
- Inventory and warehouse isolation.
- Orders and customer records.
- Shop-specific checkout and tax/shipping settings.
- Per-shop payment-provider credentials.
- Per-shop email notifications.

### Phase E — Platform operations
- Global analytics and usage.
- Subscriptions and billing integration.
- Health monitoring and error aggregation.
- Audit logs.
- Domain, security, and platform settings.

### Phase F — Production readiness
- Full integration and authorization tests.
- Tenant-isolation testing.
- Data backup and recovery strategy.
- Secret management review.
- Rate limiting and abuse protection.
- Observability and error handling.
- Performance and SEO review.
- Final deployment planning only after approval.

---

# 14. Non-Negotiable Safety Rules

- Never connect to the old Tex's Chicken & Burgers database.
- Never publish/deploy without approval.
- Never delete customer, order, product, cart, inventory, or image data.
- Avoid physical tenant deletion; use lifecycle statuses.
- Never expose passwords, JWT secrets, or database credentials.
- Never trust client-side roles for authorization.
- Never allow cross-tenant access.
- Never break the existing checkout or shop-admin authentication just to simplify routing.
- Do not introduce local `.env` credential workarounds unless explicitly requested.
- Do not report unexecuted tests as passing.
- Do not claim integrations are live if they are still marked “Not Configured.”
- Make one focused implementation change at a time.

---

# 15. How to Resume Tomorrow

Start the next conversation by pasting these notes and saying:

“Mentor, continue The Fragrance Store SaaS from these notes. First, resume the pending routing task: `/` must display Website A, `/admin/login` remains the login page, `/super-master` remains the platform control center, and clicking Website A in the Super Master dashboard must open its own isolated storefront. Ask me for the latest AI Studio output only if needed. Work step by step, verify the code and tests, preserve all data, and do not publish or deploy.”

**End of continuation notes.**
