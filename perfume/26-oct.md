# The Fragrance Store — House of Brands
## Project Continuation Notes & Development Roadmap

**Last updated:** 27 October 2026  
**Project status:** Working production website; next development phase ready to begin  
**Primary brand:** INHALE FRAGRANCES  
**Developer's working style:** Step-by-step mentorship, detailed prompts for Google AI Studio, mobile-first design, and safe production changes.

---

# 1. Project Overview

We are building a multi-tenant SaaS e-commerce platform called **The Fragrance Store — House of Brands**.

The platform is designed to support multiple independent fragrance businesses, each with its own storefront, products, database configuration, domain, and customer experience.

### Platform roles

1. **Super Master (`super_master`)** — Platform owner who manages tenants, shop owners, platform configuration, subscriptions, monitoring, and usage.
2. **Brand/Tenant Owner (`business_owner`)** — Owns and manages an individual fragrance storefront.
3. **Tenant Operations & Staff** — Roles such as manager and warehouse staff.
4. **Buyer & End Customer** — Browses products, manages a wishlist, places orders, and uses the storefront.

### Current Website A

- **Brand:** INHALE FRAGRANCES
- **Storefront tenant slug:** `the-fragrance-store`
- **Storefront route:** `/store/the-fragrance-store`
- **Shop route:** `/store/the-fragrance-store/products`
- **Account route:** `/store/the-fragrance-store/account`
- **Production domain used in the recent troubleshooting session:** `amfruits.shop`
- **Platform domain:** `fragrance.sohaildevops.site`

Important: Verify the current domain-to-tenant mapping in Netlify before changing domain configuration. The domain shown in the recent browser screenshot was `amfruits.shop`, so do not assume every domain listed above points to the same deployment.

---

# 2. Technology Stack

The project has been developed with the following technologies.

### Frontend

- React 19
- Vite 7
- TypeScript
- Tailwind CSS 3.4
- Shadcn UI / Radix UI
- Lucide React icons
- Sonner notifications
- React Router 7

### Backend

- Hono
- tRPC v11
- Netlify Functions
- PostgreSQL
- Neon PostgreSQL
- Drizzle ORM

### Infrastructure and deployment

- Google AI Studio for AI-assisted development
- Git repository for code management
- Netlify for production deployment
- Cloudflare for DNS management
- Neon for PostgreSQL database hosting
- Custom domains for storefronts

**Important:** Before implementing new features, inspect the actual package files, routing configuration, database schema, deployment configuration, and current Git state. This list describes the established project stack, not a guarantee that every dependency or implementation remains unchanged.

---

# 3. Major Infrastructure Problems We Previously Addressed

## 3.1 Tenant database isolation

We established foundations for physically isolated tenant databases.

Previously identified components include:

- Control-plane tenant configuration.
- Encrypted tenant database credentials.
- Tenant database connection management.
- Tenant migration runner.
- Tenant-specific database resolution.
- Database connection health checks.
- Website A database readiness validation.

### Earlier problem

Website A's configured database URL was being saved, but the live Netlify function continued initializing its database connection from the general `process.env.DATABASE_URL`.

This meant the intended tenant database configuration was not necessarily being used by the live request.

### Work completed earlier

The project was updated to introduce tenant-specific connection handling, configuration validation, migration execution, and database health diagnostics.

A previous issue occurred when a newly created Neon database had no required migrations. We addressed the migration-readiness workflow rather than treating the empty database as a valid, fully initialized storefront.

### Current status

The production website is currently working according to the latest user confirmation.

However, do not assume every tenant-isolation edge case has been tested recently. Before introducing more tenants, verify that each tenant's reads and writes use its intended database and that no cross-tenant access is possible.

---

## 3.2 Custom domains and Netlify deployment

We previously worked on:

- Netlify production deployment.
- Cloudflare DNS.
- Custom domain registration.
- Tenant-specific domain routing.
- Database configuration on the deployed site.
- Redirect and route handling.
- Deployment failures and build configuration.

### Earlier outcome

The custom-domain and database connection issues were resolved sufficiently for Website A to become publicly accessible.

We also fixed routing problems where storefront and platform pages were opening under the wrong paths.

### Current status

The website is now working properly following the latest production fixes.

**Do not change DNS records, production environment variables, tenant database URLs, or Netlify domain assignments unless a new verified issue requires it.**

---

# 4. Route Architecture — Critical Rules

Routing problems have been a recurring source of production bugs.

The following behavior must be preserved.

| Route | Expected purpose |
|---|---|
| `/` | Super Master login |
| `/admin/login` | Existing Super Master authentication entry, subject to the current canonical redirect configuration |
| `/store/the-fragrance-store` | Website A storefront homepage |
| `/store/the-fragrance-store/products` | Website A customer Shop |
| `/store/the-fragrance-store/account` | Website A customer account |
| `/store/the-fragrance-store/wishlist` | Website A wishlist |
| `/store/:tenantSlug/...` | Tenant-specific storefront routes where implemented |
| Admin Product Catalog route | Admin fragrance management page |
| Admin Add Fragrance route | Product creation form |
| Admin Edit Fragrance route | Product editing form |

The exact admin catalog route must be confirmed from the current repository. Do not assume that `/products` can safely represent both the admin catalog and the customer Shop.

### Root routing rule

The root route `/` must open the Super Master login, not Website A's customer storefront.

The storefront has its own tenant route.

### Navigation rule

The admin sidebar must open admin pages. The customer bottom navigation must open customer pages.

Never fix a navigation bug by redirecting all users to the same destination.

---

# 5. Customer Storefront — Design and Functionality

We have been developing a mobile-first luxury fragrance storefront.

### Visual identity

The current design direction uses:

- Warm ivory and champagne beige.
- Deep burgundy accents.
- Elegant editorial serif headlines.
- Clean product imagery.
- Rounded cards and restrained borders.
- Luxury product presentation.
- Mobile-first layouts and bottom navigation.

### Customer bottom navigation

The intended navigation is:

- Home
- Shop
- Bag
- More
- Account

The active tab should reflect the current route, and each item should navigate to its intended page.

## 5.1 Homepage

We developed an editorial hero for INHALE FRAGRANCES with:

- Brand logo.
- Hero background imagery/video.
- “HYDERABAD — HOUSE OF BRANDS” messaging.
- “Find your signature scent.”
- “EXPLORE THE SHOP” CTA.
- “WATCH THE FILM” CTA.
- Scroll-down indicator.
- Sequential entrance animations.

### Hero video behavior

The intended behavior was:

- Play once on the first visit.
- Replay when the customer selects “WATCH THE FILM.”
- Preserve the existing hero layout and responsive behavior.

Do not change this behavior unless a new issue is identified.

## 5.2 Shop page

Route:

`/store/the-fragrance-store/products`

We redesigned the customer Shop page with:

- Editorial “SHOP ALL” heading.
- Home breadcrumb.
- Dynamic catalog description and product count.
- Filters and sorting controls.
- Fragrance categories.
- Product cards.
- Product imagery.
- Wishlist heart icons.
- Customer bottom navigation.

The description was adjusted to be smaller and fit the intended mobile layout.

The product count must come from the actual tenant catalog, not a hardcoded number.

## 5.3 Product detail page

We improved product display and variant selection.

The intended functionality includes:

- Primary fragrance image.
- Product gallery thumbnails.
- Bottle size selection.
- Variant-specific images.
- Variant-specific prices.
- Required-option validation.
- Presentation format or gift options when configured.
- Quantity controls.
- Add to Bag.
- Buy Now.
- Correct price display in Indian rupees.

### Currency

We requested changing the displayed currency from dollars to Indian rupees.

The intended customer-facing format is INR, using `₹` rather than `$`.

Check all customer and admin price displays, including product cards, product details, variant selectors, cart, checkout, order summaries, and invoices. Do not modify stored monetary values or exchange rates merely to change the display symbol.

---

# 6. Admin Product Catalog and Primary Fragrance Images

This was one of our most important recent development areas.

The admin previously contained a section titled “Bottle Photos (Optional in Variant Mode).”

We changed its purpose and presentation to:

**Primary Display Image & Bottle Photos**

The intention is to make the main fragrance image independent of bottle-size variants.

## 6.1 Intended admin behavior

The primary image section should:

- Allow the administrator to upload the main fragrance image.
- Allow optional additional product/gallery images.
- Clearly identify the primary image.
- Provide an image preview.
- Allow replacing or removing images.
- Preserve the saved primary image.
- Keep variant images independent.
- Avoid duplicating shopping actions inside the image-upload section.

The image section should not require “Add to Cart” or “Buy Now” actions. Those belong to the customer storefront, not the admin upload interface.

## 6.2 Primary image priority

The intended display priority is:

1. Saved primary fragrance image.
2. A deliberate fallback to a suitable gallery image, if required by the existing implementation.
3. A safe placeholder only when no real image is available.

The primary image should not automatically be replaced by the first bottle-size variant image.

## 6.3 Variant independence

Variant images for 30 ml, 50 ml and 100 ml must remain independently selectable.

Expected behavior:

- The product initially displays the saved primary image.
- Selecting a variant with an image displays that variant's image.
- Selecting a variant without an image falls back to the primary image.
- The primary image remains saved after the product is fetched again.
- The first gallery thumbnail reflects the primary image.

## 6.4 Image persistence

We previously implemented durable product image storage and serving through the application's API and database architecture.

A production image must not depend on a temporary local development file.

Any future image changes must be verified across the full lifecycle:

1. Upload in admin.
2. Save the product.
3. Fetch the product again.
4. Load the customer Shop.
5. Open product details.
6. Select a different bottle size.
7. Refresh the page.
8. Confirm that the saved image is still available after deployment.

---

# 7. Wishlist Functionality

We added wishlist functionality as part of the customer experience.

### Intended behavior

- A heart icon appears at the top-right of the product card.
- Selecting the heart adds the fragrance to the wishlist.
- Selecting it again removes the fragrance.
- The icon reflects the saved state.
- Wishlist contents are available from the More page's Wishlist card.
- The customer can open the wishlist, remove saved fragrances, and add an item to the Bag.
- Empty wishlist state provides a way to return to the catalog.

The earlier implementation report referenced:

- `src/hooks/useWishlist.ts`
- `src/pages/Wishlist.tsx`
- `src/pages/More.tsx`
- `src/pages/Products.tsx`

These filenames should be checked against the current repository.

### Future verification

Confirm whether wishlist persistence works across reloads and whether the intended customer identity or browser session is used.

Do not assume that browser-local persistence and account-synchronized persistence are the same thing. If wishlist synchronization across devices is desired, treat that as a separate enhancement.

---

# 8. More Page

Route and navigation:

The More tab previously redirected to the homepage. We created a dedicated More page instead.

The page includes three feature cards:

1. **Wishlist** — Fragrances you saved.
2. **Live Deals** — Everything on offer now.
3. **Chat with us** — WhatsApp the shop.

### Design direction

- Wishlist uses a soft pink/ivory treatment.
- Live Deals uses a burgundy treatment.
- WhatsApp uses a soft green treatment.
- Cards use icons, arrows, titles, and short descriptions.
- The page follows the existing mobile-first luxury design.
- The customer bottom navigation highlights More when the More page is open.

### Future checks

- Wishlist must open the actual saved products.
- Live Deals must lead to a real deal or offer experience. Do not imply that discounts exist if none are configured.
- WhatsApp must use a verified shop contact number and a valid link.
- The More tab must never redirect to the homepage unintentionally.

---

# 9. Latest Production Incident — 26 October 2026

This was the last major issue before today's confirmation that the website is working properly.

## Symptoms

In the deployed production website:

- The admin Product Catalog opened the customer-facing Shop.
- Unexpected or old catalog data appeared.
- Product API requests returned HTTP 500.
- Product image requests returned HTTP 404.
- AI Studio preview and production behaved differently.

The browser screenshot showed multiple failed image requests under `/api/uploads/...` and a failing product API request.

## Files touched in the continuation session

The AI Studio session reported changes to these nine files:

1. `src/App.tsx`
2. `src/components/AppLayout.tsx`
3. `src/pages/Products.tsx`
4. `src/pages/AddProduct.tsx`
5. `src/pages/EditProduct.tsx`
6. `api/controlPlane/registry.ts`
7. `api/tenantDatabase/requestContext.ts`
8. `api/productRouter.ts`
9. `api/app.ts`

The exact implementation details and final diffs must be recovered from the current repository if we need to investigate further.

## Intended fixes

The work focused on:

- Separating admin and customer routes.
- Preserving `/` for Super Master login.
- Correcting product catalog navigation.
- Investigating tenant context and database selection.
- Fixing the product API.
- Restoring durable image retrieval.
- Verifying production configuration and Netlify routing.

### Current status

**The user confirmed on 27 October 2026 that the website is now working properly.**

We should treat the immediate incident as resolved from the user's perspective.

We should not claim to know the precise final root cause of every production error unless the latest AI Studio report, code diff, logs, or production verification confirms it.

Do not repeat the previous repair unnecessarily. If a similar problem returns, inspect the current code and logs first.

---

# 10. Netlify and Production Safety

The website is deployed through Netlify, with Cloudflare DNS and Neon PostgreSQL in the established architecture.

Before future production changes:

1. Identify the correct Netlify site.
2. Verify the Git repository and branch.
3. Confirm the latest code changes are present.
4. Check the build command and publish directory.
5. Confirm API functions and redirects.
6. Confirm the correct production environment variables.
7. Deploy only after the build and relevant tests pass.
8. Open the actual production domain.
9. Verify the affected feature on production.

Never assume a successful AI Studio preview means the deployed site is correct.

### Production safety rules

- Do not reset the database to fix a display issue.
- Do not delete catalog items to hide unexpected data.
- Do not overwrite production environment variables without checking their purpose.
- Do not expose secrets in logs or reports.
- Do not replace real product images with fake placeholders as a permanent fix.
- Do not change domain routing without confirming the intended tenant mapping.
- Preserve existing customer orders, product records, and tenant isolation.

---

# 11. Google AI Studio Workflow

Google AI Studio has repeatedly reached its usage quota during our work.

We have switched Gmail accounts to continue in new sessions.

### Important session rules

Switching Gmail provides a new session or quota opportunity; it does not guarantee that all previous code changes are present.

At the start of a new session:

1. Open the existing project or connect the correct repository.
2. Verify the latest changes and branch.
3. Provide the relevant continuation notes.
4. Ask Gemini to inspect before editing.
5. Give one clearly scoped task.
6. Request actual tests and a build.
7. Review the change summary.
8. Deploy and verify the real production behavior.

If the task is interrupted, preserve the action history, current Git state, remaining errors, and the exact next step.

Avoid asking Gemini to rewrite large portions of the application for a small UI change.

---

# 12. Recommended Next Development Roadmap

Since the website is working, the next phase should improve reliability and complete the customer experience rather than immediately changing core infrastructure.

## Phase 1 — Baseline and backup

Before making new changes:

- Confirm the current production website works.
- Check the latest Git commit and working tree.
- Ensure the recent fixes are committed or otherwise safely preserved.
- Record the deployed Netlify version.
- Test the admin login, customer Shop, product details, wishlist, More page, and Bag.

Do not create unnecessary backup copies of secrets or production database credentials.

## Phase 2 — Customer shopping flow

Verify the complete journey:

`Home → Shop → Product Details → Variant Selection → Bag → Checkout → Order Confirmation`

Check that:

- Prices and totals are correct.
- Required variants are selected.
- Images are correct.
- Quantity changes work.
- Items are not duplicated unintentionally.
- Orders persist in the intended tenant database.
- Customer navigation remains correct.

Fix any confirmed problems one at a time.

## Phase 3 — Wishlist and More

Verify that wishlist actions work consistently from product cards and product detail pages.

Then confirm the More page's three cards:

- Wishlist.
- Live Deals.
- WhatsApp support.

Improve persistence or functionality only where needed.

## Phase 4 — Admin product management

Verify:

- Add Fragrance.
- Edit Fragrance.
- Primary image upload.
- Additional gallery images.
- Variant images and pricing.
- Product activation and visibility.
- Inventory and stock.
- Category assignment.

Ensure every saved change appears correctly on the customer storefront.

## Phase 5 — Checkout and order management

Once the product flow is stable, inspect:

- Cart persistence.
- Checkout validation.
- Order creation.
- Order detail pages.
- Invoices.
- Customer order history.
- Payment integration and payment-status handling.
- Delivery configuration.

Treat payment and order processing as sensitive functionality. Do not simulate a successful real payment in production.

## Phase 6 — SaaS platform expansion

After Website A remains stable, continue the broader platform roadmap:

- Tenant onboarding.
- Custom-domain onboarding.
- Tenant-specific database provisioning.
- Migration management.
- Shop-owner accounts.
- Staff permissions.
- Subscription management.
- Platform monitoring and audit logs.
- Tenant isolation tests.

Each tenant must be independently configurable and protected.

---

# 13. How to Resume Our Next Session

At the beginning of the next conversation, share these notes or simply say:

**“Mentor, continue The Fragrance Store — House of Brands using the continuation notes. The production website is currently working. First help me verify the current project state, then continue with the next feature without breaking the existing deployment.”**

We will then:

1. Confirm the latest project state.
2. Ask what feature you want to upgrade next if it is not already specified.
3. Inspect the relevant code and current behavior.
4. Generate a precise Google AI Studio prompt.
5. Review Gemini's implementation report.
6. Test the feature.
7. Deploy safely when appropriate.

---

# Final Project Status

The project has progressed from initial storefront design into a functioning multi-tenant SaaS application with tenant database configuration, customer shopping pages, admin product management, fragrance image handling, wishlist functionality, custom-domain routing, and Netlify deployment.

The most recent production routing/API/image incident is reported resolved by the user.

**Next priority:** Preserve the working version, establish a verified baseline, and continue the next customer or admin feature in small, testable steps.

These notes provide the starting context for our next session. We should update them as new changes are implemented and verified.
