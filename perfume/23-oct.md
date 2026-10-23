The Fragrance Store --- SaaS Project Handover Notes
Last updated: 23 October 2026
Purpose: Continue in a new ChatGPT / Google AI Studio session
without re-explaining the project.
1. Current confirmed status
The project is The Fragrance Store --- House of Brands, a
multi-tenant SaaS e-commerce platform. Website A's storefront branding
is INHALE FRAGRANCES.

As of 23 October 2026, the user confirmed: - amfruits.shop opens the
deployed INHALE FRAGRANCES storefront after the custom domain was
registered in Netlify. - Login and database-backed behavior work on the
custom domain. - The Super Master console is available at
fragrance.sohaildevops.site/super-master. - Netlify deployment now
succeeds after earlier build/deployment issues. - Recent work addressed
physical tenant database isolation, custom-domain routing, route
collisions, and domain-seeding problems. - The next goal is to continue
building the SaaS product, not rebuild the working deployment.

The screenshots show Cloudflare DNS for amfruits.shop configured as a
CNAME to fragrance.sohaildevops.site, DNS-only (grey cloud), TTL Auto.
The domain was then added to the deployed site in Netlify's Domain
management/custom domains. Before that Netlify showed "Site not found";
adding the hostname in Netlify fixed it.

Caution: One screenshot of the Super Master "Add Domain" modal
displayed a production warning that CONTROL_PLANE_DATABASE_URL and
CONTROL_PLANE_DATABASE_NAME are required. The user later confirmed the
custom domain and database-backed login worked, but this warning must
still be investigated before onboarding more tenants. Verify domain
records persist in the real control-plane database across refresh,
login/logout, redeploy and runtime restart.
2. Product and tenant model
The goal is a SaaS platform where the platform owner provisions
independent storefronts. Each tenant needs its own domain, branding,
catalog, inventory, customer/order data, and database boundary.
Roles
1. Super Master (super_master) --- manages tenants/websites, shop
   owners, domain registration, platform settings, subscriptions,
   analytics and governance.
2. Brand/Tenant Owner (business_owner) --- manages their
   storefront, branding, products, inventory, orders and shop
   configuration.
3. Tenant Operations / Staff --- roles such as manager,
   warehouse_staff, with limited tenant-scoped permissions.
4. Buyer / Customer (buyer) --- browses, manages cart/account and
   checks out.
Authorization must be enforced server-side. Hiding UI controls is not
security.
3. Technology and deployment context
Known stack from current and earlier work: - Frontend: React 19,
TypeScript, Vite 7, Tailwind CSS 3.4, Shadcn/Radix UI, Lucide React,
Sonner. - Routing: React Router v7. - API/server: Hono v4 mounted in
Vite dev server; tRPC v11. - ORM: Drizzle ORM. - Database: Neon
PostgreSQL. - Hosting: Netlify; DNS managed through Cloudflare. - AI
coding environment: Google AI Studio, Gemini 3.8 Flash; workspace linked
to Git and deployed to Netlify. - A recent migration/repair report
described Node.js runtime, standard npm (removed stray bun.lock), Vite
SPA + Hono API, and dev port 3000. Verify actual scripts and Netlify
settings in the current repository.

NGINX recommendation: Do not add NGINX merely to route domains on
Netlify. NGINX is appropriate for a server/VM/container you manage, not
as a persistent reverse proxy in a standard Netlify static/serverless
deployment. Use Netlify custom domains/domain aliases, DNS,
redirects/rewrites, and supported edge/serverless functions.
4. Critical route contract --- do not regress
The user explicitly requires:

  Path                           Required behavior
  /                            Super Master login page
  /admin/login                 Same Super Master login page
  /store/the-fragrance-store   Website A storefront

This issue happened more than once: the storefront rendered at /,
which belongs to the Super Master login. The user requested a permanent
fix.

Rules: - Never make the platform root / render or redirect to Website
A's storefront. - / and /admin/login render the same Super Master
login. - /store/the-fragrance-store explicitly renders Website A's
storefront on the platform/path-based host. - Do not rely on incidental
route order or a broad wildcard that captures /. - Review
src/App.tsx, src/components/AppLayout.tsx, route guards, navigation
links, and Netlify redirects/rewrites. - Hostname-based tenant routing
is separate from platform path routing: on a registered, verified,
active customer domain such as amfruits.shop, the hostname root /
may serve that tenant's storefront. This must not change the platform
hostname's root behavior.
Required regression tests
1. / renders Super Master login.
2. /admin/login renders the same Super Master login.
3. /store/the-fragrance-store renders Website A storefront.
4. Unknown paths do not silently render Website A.
5. Storefront navigation preserves /store/the-fragrance-store in
   path-based preview.
6. A verified customer hostname resolves / to its tenant storefront
   without changing platform-host /.
7. Direct reload/deep-linking works after deployment.
Earlier AI Studio output mentioned edits to src/App.tsx,
src/components/AppLayout.tsx, src/pages/LandingPage.tsx,
src/pages/Products.tsx,
api/platformRootAndStorefrontRouting.test.ts,
api/websiteAStorefrontNavigation.test.ts, and
api/websiteACustomerAuth.test.ts. Another run reported editing 10
files and showed the Super Master console at /super-master. Inspect
the final code and tests; do not assume AI-generated reports alone prove
the final state.
5. Physical tenant database isolation
The intended architecture is central control plane + separate tenant
databases, not merely one shared commerce database filtered by
tenant_id.
- Central/control-plane DB (centralDb): tenant registry,
  registered domains, platform memberships/status and governance
  metadata.
- Tenant DB: that tenant's products/catalog, carts, customers,
  orders, inventory and other commerce data.
- Resolve tenant identity from a normalized, trusted hostname/domain
  registry, then bind the request to the correct tenant database.
- Super Master requests on the platform host use the central control
  plane and must not inherit customer tenant context.
- A tenant DB outage must fail closed. Never fall back to another
  tenant's DB or commerce data.
Relevant files reported in recent domain-hardening work
- api/controlPlane/types.ts
- api/controlPlane/registry.ts
- api/controlPlane/service.ts
- api/tenantDatabase/requestContext.ts
- api/context.ts
- api/superMasterRouter.ts
- src/pages/SuperMasterDashboard.tsx
- api/tenantDatabase/domainManagement.test.ts
- api/tenantDatabase/seededDomainsRegression.test.ts
Other security/auth files known from earlier audit: -
api/auth-router.ts - api/auth/admin-session.ts -
api/middleware.ts - api/context.ts
Seeded-domain issue and reported fix
The audit reported that unwanted hostnames were not in persistent
database tables. They came from the in-memory seed fixture
WEBSITE_A_VERIFIED_DOMAINS in api/controlPlane/registry.ts and
automatic hostname assignment in api/superMasterRouter.ts.

Reported changes: - WEBSITE_A_VERIFIED_DOMAINS set to an empty frozen
array. - Automatic domain registration removed from registry
initialization. - Automatic ${company.slug}.sohaildevops.site
assignment removed. - Platform host detection/reservation added. -
Localhost verification bypass removed. - Unknown/unverified domains fail
closed. - Duplicate hostname claims rejected. - Regression tests added
for seeded domains, tenant isolation, conflicts, and fail-closed
behavior.

AI Studio reported: - Seeded-domain regression suite: 13/13 passed. -
Domain-management suite: 28/28 passed. - Full tenant isolation/Super
Master suites: 31/31 passed. - Lint: 0 errors, 0 warnings. -
Build/compilation succeeded.

These are reported results, not independently re-run in this handover.
Re-run them after any new edits.
Security requirements to preserve
- No hardcoded Super Master email/password. Use secure server-side
  environment configuration and dedicated Super Master authorization.
- Keep superMasterQuery separate from tenant admin/customer auth.
- Persist tenant memberships and invitation/acceptance workflows.
- Use tenant lifecycle states such as ACTIVE / SUSPENDED /
  DEACTIVATED; avoid routine irreversible physical deletion.
- Scope all catalog, cart, checkout, account, inventory and order APIs
  to the resolved tenant.
- Order creation must validate every cart item against the same
  tenant; never infer tenant from only cart.items[0].
- Website A must not view/remove Website B's domains or data.
- Never silently fall back across tenant boundaries or use mock data
  in production if the database is unavailable.
Earlier audit gaps to re-check: persistent tenant
membership/invitations, tenant-scoped public catalog, mixed-tenant
cart/order validation, and destructive deletion safety. Later reports
mention hardening, but verify actual implementation and tests before
assuming all gaps are closed.
6. Custom-domain setup --- working path
Current domain
- Customer domain: amfruits.shop
- Cloudflare record shown:
  - Name: amfruits.shop
  - Type: CNAME
  - Target: fragrance.sohaildevops.site
  - Proxy: DNS only (grey cloud)
  - TTL: Auto
- User added amfruits.shop in Netlify's Domain management/custom
  domains for the deployed site.
- The storefront then loaded successfully at amfruits.shop.
- User confirmed database-backed login behavior also worked.
Why "Site not found" happened
DNS alone sends traffic toward a destination. Netlify must also be
configured to accept that hostname on the correct site and provision
TLS. The earlier Netlify "Site not found" was resolved after adding the
domain to Netlify.
Future tenant domain onboarding
1. Add the correct DNS record at the customer's DNS provider, following
   the current Netlify instructions for the deployed site. The current
   working amfruits.shop setup used a CNAME to
   fragrance.sohaildevops.site, DNS-only.
2. Add the hostname to the same deployed Netlify site as a custom
   domain/domain alias.
3. Wait for DNS propagation and HTTPS certificate provisioning.
4. In Super Master → Websites → tenant → Domain Management, register
   the hostname.
5. Complete the app's ownership challenge, if required (the app
   previously described a TXT record like _thefragrance-challenge
   with value thefragrance-verify=<tenantId_prefix>, or a supported
   CNAME challenge).
6. Click Verify DNS in Super Master.
7. Confirm Verified/Active status and tenant resolution.
8. Test login, products, cart, checkout/orders, refresh and deep links
   on the domain.
The application's ownership TXT challenge and Netlify's own domain
verification are separate checks. Complete both when required. DNS
resolution alone does not mean the app marks the domain Verified/Active.
Platform-host isolation reported
- fragrance.sohaildevops.site designated as
  PLATFORM_SUPER_MASTER_HOST.
- isPlatformHost(hostname) identifies the platform host and reserved
  supermaster.* / super-master.* patterns.
- Platform host rejected as a customer tenant domain.
- Platform-host requests set ctx.tenantContext = null and operate
  against centralDb.
- Unknown/unregistered/unverified hosts fail closed.
- Duplicate claims rejected; no cross-tenant fallback.
Warning still to investigate
The Super Master "Add Domain" modal showed:
Control-plane database is required in production: CONTROL_PLANE_DATABASE_URL and CONTROL_PLANE_DATABASE_NAME must be configured.
The custom domain later worked, but this warning may indicate that
domain administration is not persisting to the deployed control-plane
DB. Confirm records survive refresh, logout/login, redeploy and runtime
restart. Do not onboard more tenants until this is clear.
7. Netlify deployment history and checklist
Earlier Netlify deployments/builds failed, but a later deployment
succeeded. AI Studio reported: - Node.js web runtime. - React/Vite SPA +
Hono API. - npm package manager; stray bun.lock removed. -
Dependencies retained, including bcryptjs and @hono/node-server. -
In-memory/mock fallback for Drizzle/tenant DB connections when external
DB is offline/unconfigured. - Dev server on port 3000 serving client and
API. - .env.example synchronized with referenced environment
variables. - Tenant context in a category-delete test fixed.
Before every deploy
1. Review Git status/diff.
2. Run actual test, lint and build scripts from package.json.
3. Configure production environment variables in Netlify;
   .env.example does not configure production.
4. Ensure production does not silently use in-memory mock storage for
   data that must persist.
5. Verify Netlify build command and publish directory.
6. Verify API/server functions are deployed and receive correct
   server-side environment variables.
7. Review deploy logs.
8. Smoke-test platform login, path storefront, custom domain, auth,
   persistence and tenant isolation.
Never commit DB URLs, passwords, session secrets, OAuth secrets or
encryption keys. Do not expose server secrets through client-side
VITE_ variables.
8. Neon/database configuration notes
Neon Console screenshot shows the website-a project, production
branch, on Monitoring. This supports the presence of a dedicated Website
A Neon environment, but a monitoring screen alone does not prove
isolation. The user confirmed DB-backed login behavior works on
amfruits.shop.

Past problems included tenant-specific DB configuration saving and
differences between Google AI Studio preview/runtime and Netlify
production configuration. Google AI Studio's development runtime may use
an immutable Cloud Run revision; do not assume preview environment
changes automatically alter Netlify production.
- Confirm the control plane has its own DB/configuration.
- Confirm Website A uses its own Neon database.
- Never fall back from Website B to Website A.
- Test persistence by making a test change, refreshing, logging out/in
  and checking after deployment.
- Store tenant DB credentials securely. TENANT_CONFIG_ENCRYPTION_KEY
  was referenced in earlier work; configure it server-side, keep it
  strong and never expose/log it.
9. Storefront and branding
- Storefront brand: INHALE FRAGRANCES.
- Header tagline: HOUSE OF BRANDS --- LUXURY & NICHE FRAGRANCES.
- Visual direction: black/dark background, gold accents, premium
  luxury fragrance look, editorial serif headings.
- Homepage hero examples: "Haute Parfumerie & Artisanal Extraits" and
  "Curated Luxury Discovery Sets."
- Tenant slug previously shown: the-fragrance-store.
- Super Master console route shown: /super-master.
- Do not confuse the tenant storefront with the Super Master platform
  console.
10. Priority next steps
Phase A --- Freeze the known-good baseline
- Commit/tag the current working state in Git.
- Record Netlify site name, production branch, build command, publish
  directory, custom domains and required environment-variable
  names (not secret values).
- Record which Neon DB is control-plane and which is Website A.
- Save the latest successful test/build output.
Phase B --- Confirm permanent routing
- Run route regression tests.
- Verify /, /admin/login, /store/the-fragrance-store on the
  platform host.
- Verify amfruits.shop/ serves Website A based on hostname.
- Test reloads and nested routes.
- Ensure wildcard routes cannot make Website A appear at the platform
  root.
- Keep these cases in CI.
Phase C --- Confirm production persistence and isolation
- Confirm control-plane domain records survive refresh, logout/login,
  redeploy and runtime restart.
- Confirm Website A reads/writes only its own Neon DB.
- When Website B is created, give it a separate Neon DB and test both
  directions for cross-tenant access.
- Simulate a tenant DB outage and ensure the app fails safely without
  another tenant's data or production mock data.
Phase D --- Finish security review
- Confirm Super Master credentials are server-configured and distinct
  from generic admin auth.
- Review persistent memberships/invitations.
- Confirm ACTIVE / SUSPENDED / DEACTIVATED lifecycle instead of
  destructive deletion.
- Review every API procedure for tenant scoping.
- Validate all cart items belong to the same tenant before order
  creation.
- Add negative tests for cross-tenant catalog, cart, customer, order,
  inventory, domain and admin access.
Phase E --- Build SaaS features
After infrastructure/security baseline passes: - Tenant owner
onboarding/invitations. - Tenant-specific branding with durable DB
persistence. - Product/category CRUD, images, inventory and pricing. -
Customer auth and account pages. - Cart, checkout and tenant-scoped
order management. - Staff roles/permissions. - Subscription/billing
plans and platform analytics. - Monitoring, audit logs, error handling
and backups. - Mobile-first storefront QA, then desktop QA.

For each feature: inspect → acceptance criteria → focused implementation
→ tests → lint/build → diff review → deploy → production smoke test.
11. Smoke-test checklist after every deployment
- [ ] Platform hostname / shows Super Master login.
- [ ] /admin/login shows the same login.
- [ ] /store/the-fragrance-store shows Website A on the path-based
  platform host.
- [ ] amfruits.shop/ shows Website A because the hostname is
  registered to that tenant.
- [ ] Deep-link refresh does not produce Netlify 404.
- [ ] Super Master login works using configured credentials.
- [ ] Storefront/customer login works.
- [ ] Catalog and account data match the intended tenant.
- [ ] A test change persists after refresh and a new login.
- [ ] Domain registrations survive refresh and redeploy.
- [ ] Tenant DB failure fails closed without exposing another tenant's
  data.
- [ ] No secrets appear in browser bundles/logs.
- [ ] Tests, lint and production build pass.
12. How to continue in a new Google AI Studio session
Quota previously expired mid-task, so work in small, verifiable phases.
Do not ask the agent to rebuild the app or blindly repeat previous
changes.
1. Ask it to inspect the current repository, Git status/diff, routes,
   package scripts, Netlify config, DB configuration and tests.
2. State the exact acceptance criteria and forbidden regressions.
3. Ask for focused changes only.
4. Require automated regression tests.
5. Require exact commands and results.
6. Require changed files, assumptions, remaining risks and deployment
   steps.
7. If quota expires, use Git diff/checkpoint and the agent's report to
   continue; do not blindly rerun the whole implementation.
8. Do not accept preview-only tests as proof of production success.
13. Copy/paste starter prompt for the next AI Studio session
You are continuing an existing project, The Fragrance Store --- House
of Brands, a multi-tenant SaaS e-commerce platform. Do not rebuild or
replace the project. First inspect the current workspace, Git
status/diff, package scripts, routing, Netlify config, DB configuration
and tests.

Current confirmed status (23 October 2026): - Netlify deployment
succeeds. - amfruits.shop is registered as a custom domain on the
deployed Netlify site and opens the INHALE FRAGRANCES storefront. - The
user confirmed database-backed login behavior works on the custom
domain. - Website A is intended to use its own Neon database; the
control plane must be separate. - Platform host is
fragrance.sohaildevops.site; the Super Master console has been seen at
/super-master. - Critical platform-host route contract: / = Super
Master login; /admin/login = same login; /store/the-fragrance-store
= Website A storefront. - A repeated bug previously showed the
storefront at /. Do not reintroduce it. - Recent domain hardening
removed hardcoded/automatic seeded customer domains, reserved the
platform host, and added fail-closed tenant resolution and
domain/isolation tests. - Do not add NGINX for Netlify domain routing;
use Netlify custom domains/domain aliases and DNS. - A previous Super
Master modal warned that production needs CONTROL_PLANE_DATABASE_URL
and CONTROL_PLANE_DATABASE_NAME. Verify the deployed control-plane DB
is configured and domain records persist before onboarding more tenants.

Required behavior: 1. Preserve the working custom-domain deployment. 2.
Keep platform-root routes and storefront path separate exactly as
specified. 3. Keep Super Master requests on the central control-plane
DB. 4. Resolve customer domains only when explicitly registered,
verified and active. 5. Never allow cross-tenant DB/data fallback. 6.
Never silently use in-memory mock data in production when required DB
configuration is missing. 7. Do not delete real database records or run
destructive migrations without explicit approval. 8. Inspect first, then
propose a small implementation plan and make focused changes. 9.
Add/update regression tests, run actual test/lint/build commands,
inspect the diff and report exact results. 10. Finish with changed
files, tests/outcomes, deployment steps, remaining risks and the next
recommended task.

Begin by auditing the current state and reporting what is already
implemented versus what is missing. Do not assume earlier AI-generated
reports prove the current code is correct.
14. Final handover summary
The user reports two major milestones as solved: 1. Physical tenant
database isolation --- Website A is connected to its own Neon
environment and the design separates central control-plane data from
tenant commerce data. 2. Custom-domain deployment ---
amfruits.shop now opens the storefront after being registered in
Netlify; database-backed login behavior was confirmed.

Other recent fixes include Netlify deployment/build issues, route
collisions, domain fixture cleanup, platform-host separation and
regression tests. Do not rebuild these from scratch. First preserve the
working state, verify production configuration and persistence, then
continue product development in small test-driven phases.
