# THE FRAGRANCE STORE — HOUSE OF BRANDS
## Master Project Handover & Continuation Notes

**Document purpose:** Complete project reference for future development sessions  
**Project owner:** Sohail  
**Development platform:** Google AI Studio  
**Repository:** `sohail-24/the-fragrance-store`  
**Branch:** `main`  
**Project workspace:** `the-fragrance-store`  
**Workspace/Applet ID:** `83291497-a3a9-4091-9462-fe9b68ef0910`  
**Project status:** Luxury storefront implemented; hero refinement and production-readiness work remain.

---

# 1. PROJECT OVERVIEW

The Fragrance Store — House of Brands is a mobile-first perfume e-commerce website being developed for Sohail's friend, who owns a fragrance shop in Hyderabad.

The physical store's signage reads:

**The Fragrance Store — House of Brands**

The original inspiration is the existing physical shop and a luxury fragrance shopping experience similar to premium perfume retailers.

The goal is to build a polished, professional e-commerce platform that can eventually be demonstrated to the shop owner and potentially used for the real business.

## Business objectives

- Display perfumes from multiple fragrance houses.
- Allow customers to discover and search for fragrances.
- Organize products by fragrance category.
- Show product images, sizes, descriptions and prices.
- Support shopping bags, checkout and order tracking.
- Provide a secure administration dashboard for managing products, stock and orders.
- Deliver a premium experience on mobile phones.
- Prepare the application for a dedicated database and production deployment.

## Core design philosophy

**Mobile first, premium appearance, reliable functionality.**

Most customers are expected to visit the store using their phones. Design and test the mobile experience before polishing desktop layouts.

The site should feel like a luxury fragrance boutique, not a generic shopping template and not a restaurant application.

---

# 2. PROJECT ISOLATION AND SAFETY

This project originated from an existing Tex's Chicken & Burgers application.

The fragrance storefront was created as a separate Google AI Studio workspace and a separate GitHub repository.

## Project identity

- Original restaurant repository: `sohail-24/texs-shop`
- New fragrance repository: `sohail-24/the-fragrance-store`
- Fragrance branch: `main`

The AI Studio inspection reported that the new workspace was isolated from the original restaurant workspace.

However, repository isolation and database isolation are two different things. Always verify database configuration independently.

## Mandatory safety rules

1. Never modify the original Tex's Chicken & Burgers repository.
2. Never connect the fragrance application to the restaurant's live Neon database.
3. Never drop tables, truncate data, wipe records or reset a database without explicit approval.
4. Never overwrite environment secrets or print credentials in logs.
5. Never modify payment, authentication or checkout logic during an unrelated design-only task.
6. Never publish or deploy without explicit approval.
7. Make focused changes, test them and report the result before starting the next phase.

The fragrance project must have its own dedicated Neon PostgreSQL project or an explicitly isolated database.

---

# 3. TECHNOLOGY STACK AND ARCHITECTURE

The initial technical audit reported the following stack.

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript |
| Build tooling | Vite 7 |
| Styling | Tailwind CSS 3.4 |
| UI components | Shadcn/Radix primitives |
| Icons | Lucide React |
| Notifications | Sonner |
| Routing | React Router 7 |
| Backend | Hono 4 |
| API communication | tRPC 11 |
| Serialization | SuperJSON |
| Database | PostgreSQL on Neon |
| ORM | Drizzle ORM |
| Database driver | Neon-compatible PostgreSQL driver |
| Image persistence | PostgreSQL binary storage through `product_images` |
| Testing | Vitest and existing project tests |
| Version control | GitHub |
| AI-assisted development | Google AI Studio |

The project includes a frontend and backend API. It is not just a static React website.

## Important application entry points

- `index.html` — HTML document and metadata.
- `metadata.json` — Application metadata.
- `src/main.tsx` — Client entry point.
- `src/App.tsx` — Application routing and composition.
- `src/index.css` — Global styling and theme.
- `tailwind.config.js` — Tailwind theme configuration.
- `api/boot.ts` — Backend initialization and API setup.
- `api/queries/connection.ts` — Database connection configuration.
- `db/schema.ts` — Database schema.
- `db/relations.ts` — Database relations.
- `src/components/AppLayout.tsx` — Shared application layout.
- `src/components/CustomerBottomNav.tsx` — Customer navigation.
- `src/pages/LandingPage.tsx` — Homepage and current hero implementation.
- `src/pages/Products.tsx` — Product catalog.
- `src/pages/ProductDetail.tsx` — Product details.
- `src/pages/Cart.tsx` — Shopping bag/cart.
- `src/pages/About.tsx` — Brand story and fragrance guide.
- `src/pages/Dashboard.tsx` — Admin dashboard.
- `src/pages/Inventory.tsx` — Inventory management.
- `src/pages/Orders.tsx` — Order administration.
- `src/pages/AddProduct.tsx` — Product creation.
- `src/pages/EditProduct.tsx` — Product editing.
- `src/components/ProductOptionsEditor.tsx` — Product options editor.
- `src/lib/productOptionsPresets.ts` — Product option presets.

These paths were identified in the audit and previous AI Studio reports. Before editing, inspect the current repository because subsequent changes may have altered individual files.

---

# 4. DATABASE AND SECRETS STATUS

A previous read-only inspection of the new workspace reported:

- `DATABASE_URL` was not set in the application runtime.
- No local `.env` file was present.
- The application fell back to `mockDbInstance` in `api/queries/mockDb.ts`.
- No external database queries were occurring during that inspection.
- No migrations or SQL operations were executed by the inspection.

Sohail subsequently reported adding a new Neon PostgreSQL URL and admin-related secrets in AI Studio. However, the earlier inspection does not prove that those secrets are available to the current runtime.

**Current requirement: verify the runtime connection before performing any database work.**

Expected secret names discussed in the project:

- `DATABASE_URL`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `JWT_ACCESS_SECRET`
- `JWT_REFRESH_SECRET`
- `GEMINI_API_KEY`

Additional payment secrets may be required if online payments are enabled.

Never paste the actual secret values into ChatGPT or include them in a generated prompt.

## Database verification checklist

Before Phase 3 database work:

1. Verify that `DATABASE_URL` is available to the runtime.
2. Inspect only the parsed hostname and database name, never the password or full connection string.
3. Confirm the endpoint belongs to the dedicated fragrance Neon project.
4. Confirm the database is not the restaurant database.
5. Inspect the existing schema and migration strategy.
6. Create a backup or suitable recovery point before destructive schema changes.
7. Use controlled migrations and verify the resulting schema.

Do not assume that creating a new repository automatically creates a new database.

---

# 5. BRAND IDENTITY AND DESIGN SYSTEM

## Brand identity

- Brand: The Fragrance Store
- Secondary identity: House of Brands
- Tagline: Discover Your Signature Scent.
- Design personality: Luxurious, editorial, sophisticated and modern.

## Color palette

| Purpose | Color |
|---|---|
| Obsidian black | `#111111` |
| Deep charcoal | `#1B1B1B` |
| Warm ivory | `#FDFBF7` |
| Champagne gold | `#C5A059` |
| Light champagne | `#E0C895` |
| Warm border | `#E4E0D8` |

Use the black and gold palette for the primary luxury storefront, with ivory or warm white for product cards when it improves readability.

## Typography

- Headings: Cormorant Garamond, editorial serif.
- Body and interface: Plus Jakarta Sans, clean sans-serif.
- Use clear hierarchy, restrained letter spacing and readable mobile typography.

## Branding rules

- Use the actual store identity consistently.
- Preserve the KTK crest/monogram artwork where appropriate.
- Keep the wordmark legible at small mobile widths.
- Do not use restaurant names, food imagery or restaurant slogans.
- Do not invent claims such as guaranteed authenticity, free gifts or discounts unless the business confirms them.

---

# 6. COMPLETED WORK — PHASE 2

The initial branding foundation was implemented in Google AI Studio.

## Files reported as modified

- `index.html`
- `metadata.json`
- `tailwind.config.js`
- `src/index.css`
- `src/components/AppLayout.tsx`
- `src/components/CustomerBottomNav.tsx`
- `src/pages/LandingPage.tsx`
- `src/pages/About.tsx`
- `src/pages/Products.tsx`
- `src/pages/Cart.tsx`

Several local fragrance SVG assets were also created.

## Implemented changes

- Replaced restaurant branding with fragrance-store branding.
- Added luxury black, charcoal and champagne-gold theme tokens.
- Added serif and sans-serif typography.
- Reworked the homepage into a fragrance boutique.
- Added fragrance-oriented collection content.
- Replaced restaurant copy on the About page with fragrance education and brand storytelling.
- Updated product category wording.
- Updated cart styling while preserving existing cart behavior.
- Filtered restaurant products from customer-facing fragrance grids.
- Added an empty-catalog state while fragrance product records were unavailable.

The empty-catalog state was intentional: food products must not appear as perfumes.

---

# 7. COMPLETED WORK — PHASE 2.1

The storefront was upgraded to resemble a premium perfume retailer.

## Implemented features

### Mobile header

- Menu button.
- Store monogram and wordmark.
- Search control.
- Shopping bag icon.
- Live cart item count.
- Slide-out navigation drawer.

### Homepage campaigns

- Luxury fragrance hero.
- Campaign headline and description.
- Shop Now button.
- Carousel indicators.
- Perfume campaign artwork.

### Categories

- For Him.
- For Her.
- Unisex.
- Gift Sets.

Category cards use fragrance artwork and are intended to navigate to the corresponding catalog filters.

### Product cards

The reported product-card design includes:

- Product image.
- Fragrance name and brand.
- Concentration.
- Bottle size.
- Price.
- Optional compare-at price.
- Ratings and review counts.
- Add to Bag button.

These product details must eventually be backed by verified product records. Existing visual mock content must not be mistaken for confirmed inventory.

### Additional homepage sections

- Premium Brands showcase.
- Olfactory family guide.
- Store trust and service highlights.
- Newsletter signup interface.

Reported local assets include:

- `public/fragrance/store-logo.svg`
- `public/fragrance/hero-sauvage-million.svg`
- `public/fragrance/cat-for-him.svg`
- `public/fragrance/cat-for-her.svg`
- `public/fragrance/cat-unisex.svg`
- `public/fragrance/cat-gift-sets.svg`
- `public/fragrance/banner-brands.svg`
- `public/fragrance/sauvage-edp.svg`
- `public/fragrance/one-million.svg`
- `public/fragrance/bleu-chanel.svg`
- `public/fragrance/baccarat-540.svg`
- `public/fragrance/tom-ford-oud.svg`
- `public/fragrance/creed-aventus.svg`
- `public/fragrance/miss-dior.svg`
- `public/fragrance/jazz-club.svg`

Verify current asset paths before reusing them.

---

# 8. COMPLETED WORK — PHASE 2.4

The mobile header was refined into a single horizontal row.

## Required layout

```text
+----------------------------------------------------+
| [MENU] [LOGO + WORDMARK]       [SEARCH] [BAG (0)] |
+----------------------------------------------------+
```

## Behavior

- Menu opens the existing slide-out navigation.
- Logo and wordmark identify the shop.
- Flexible spacing keeps search and bag controls on the right.
- Search icon toggles the existing expandable search field.
- Shopping bag count reflects the existing cart state.
- Existing search and cart behavior must remain intact.

Only `src/pages/LandingPage.tsx` was reported as modified for this refinement.

---

# 9. COMPLETED WORK — PHASE 2.5

The hero announcement and presentation were refined.

## Announcement bar

The promotional strip containing:

`Complimentary Luxury Samples with Orders Over $100 • Verified Authentic Flacons`

was removed from the homepage.

Do not reintroduce it unless explicitly requested.

## Hero presentation

- Removed the border around the inner perfume artwork.
- Removed the separate nested image-card appearance.
- Removed the border around the eyebrow text.
- Retained the luxury dark background and gold typography.

## Three hero campaigns

**Campaign 1 — Signature Scent**

- Eyebrow: `LUXURY • ELEGANCE • EVERYDAY YOU`
- Headline: `Find Your Signature Scent`
- Image: `/fragrance/hero-sauvage-million.svg`
- CTA: Shop Now.

**Campaign 2 — Artisanal Extraits**

- Eyebrow: `NICHE & ARTISANAL • PRIVATE BLEND`
- Headline: `Haute Parfumerie & Artisanal Extraits`
- Image: `/fragrance/hero-fragrance.svg`
- CTA: Explore Niche.

**Campaign 3 — Discovery Sets**

- Headline: `Curated Luxury Discovery Sets`
- Image: `/fragrance/discovery-set.svg`
- CTA: Discover Sets.

The campaign content should be checked against the current implementation before making further changes.

## Reported verification

Gemini reported:

- `src/pages/LandingPage.tsx` modified.
- `src/pages/LandingPage.test.ts` modified.
- Full test suite passed: 17 test files and 60/60 tests.
- Compilation succeeded.
- ESLint reported zero errors and zero warnings.

These are the reported results from that development run, not a guarantee that future modifications will also pass.

---

# 10. CURRENT TASK — PHASE 2.6

**Status: Prompt prepared; implementation completion has not yet been confirmed.**

The latest task is a focused improvement to the existing hero carousel.

## Change 1: Increase carousel interval

Current reported behavior: 3-second automatic rotation.

Required behavior: 5-second automatic rotation.

The intended interval is:

```typescript
5000
```

The carousel must continue to loop through exactly three campaigns.

## Change 2: Explicit headline line breaks

The required visual endings are:

```text
Campaign 1

Find Your
Signature
Scent
```

```text
Campaign 2

Haute Parfumerie &
Artisanal
Extraits
```

```text
Campaign 3

Curated Luxury
Discovery
Sets
```

Use explicit line breaks or separate block-level spans rather than relying on accidental wrapping.

Preserve the wording, serif typography and gold emphasis.

## Change 3: Increase perfume image prominence

Target approximately 60% visual emphasis for the image and 40% for the text. This is a design target, not a rigid width that must apply at every viewport.

```text
+----------------------------------------------------+
| TEXT — APPROX. 40% | IMAGE — APPROX. 60%           |
|                    |                               |
| Find Your          |     LARGE PERFUME BOTTLES     |
| Signature          |                               |
| Scent              |     CLEAR AND PROMINENT       |
|                    |                               |
| Description        |     NO INNER BORDER           |
| [ SHOP NOW ]       |     NO SEPARATE IMAGE CARD    |
+----------------------------------------------------+
```

The actual perfume bottles must become larger and more visible. Merely enlarging the empty container is not sufficient.

Preserve aspect ratios, prevent clipping and maintain readable text.

## Mobile test widths

Prioritize:

- 320px.
- 360px.
- 375px.
- 390px.
- 430px.

At narrower widths, the hero may grow vertically to preserve readability and image prominence.

## Phase 2.6 verification

After applying the prompt, check:

1. Rotation occurs every 5 seconds.
2. The third campaign returns to the first.
3. Headline line breaks are correct.
4. Images are noticeably larger.
5. The inner image frame stays removed.
6. The eyebrow remains borderless.
7. There is no horizontal overflow or overlap.
8. All CTAs remain functional.
9. Existing tests and the production build pass.

**Do not begin another homepage redesign until this phase has been inspected and approved.**

---

# 11. EXISTING SHOPPING AND ADMIN FEATURES

The initial audit reported a substantial e-commerce foundation that should be reused instead of rebuilt unnecessarily.

## Catalog

- Product listing.
- Product detail pages.
- Category filters.
- Search by product title, tags/notes and slug.
- Product options and pricing.
- Stock availability.
- Product image galleries.

## Shopping bag and orders

- Guest cart persistence through browser local storage.
- Authenticated cart operations.
- Existing order creation and status tracking.
- Order detail views.
- Guest checkout support.

Reported order statuses include:

- Pending.
- Confirmed.
- Packed.
- Ready for dispatch.
- Out for delivery.
- Delivered.
- Cancelled.

## Admin

- Dashboard with sales and order summaries.
- Inventory tracking.
- Low-stock alerts.
- Product creation and editing.
- Order administration.
- Existing authentication and role guards.

The existence of these modules does not mean every flow is production-ready for the fragrance business. They must be reviewed and tested as domain-specific requirements are implemented.

---

# 12. FRAGRANCE CATALOG — PLANNED DOMAIN MODEL

The initial audit recommended replacing restaurant-specific product concepts with fragrance-specific attributes.

## Proposed product fields

- Product name.
- Fragrance house or brand.
- Product slug.
- Description.
- Concentration.
- Olfactory family.
- Top notes.
- Heart notes.
- Base notes.
- Gender/category designation.
- Bottle size.
- Price.
- Compare-at price, when genuinely applicable.
- Stock quantity.
- Product images.
- Active/inactive status.

## Concentration options

- Eau de Toilette (EDT).
- Eau de Parfum (EDP).
- Extrait de Parfum.
- Pure Oil / Attar.

## Suggested volume options

- 6ml attar or roll-on, when available.
- 30ml.
- 50ml.
- 100ml.
- Sample vial or discovery set, where applicable.

Use only the sizes actually sold by the store.

## Proposed categories

1. Men's Fragrances.
2. Women's Fragrances.
3. Unisex & Niche.
4. Oud & Pure Attars.
5. Gift Sets & Discovery Collections.

## Olfactory families

- Woody & Earthy.
- Amber & Oriental.
- Fresh & Citrus.
- Floral & Solar.
- Gourmand, where appropriate.

Do not add fragrance attributes to the live database until the schema and migration strategy have been inspected.

---

# 13. NEXT DEVELOPMENT ROADMAP

Follow this order to reduce risk and avoid mixing unrelated changes.

## Phase 2.6 — Finish the hero

- Apply the 5-second carousel timing.
- Correct the headline line breaks.
- Enlarge the fragrance imagery.
- Test mobile layouts.
- Confirm tests and build.

## Phase 3 — Fragrance data model and catalog

- Inspect the existing Drizzle schema.
- Identify food-specific columns and assumptions.
- Define a backward-compatible fragrance data model.
- Introduce fragrance-specific fields and size variants.
- Plan migrations before executing them.
- Seed only clearly identified fragrance test records into the dedicated database.
- Verify product listing, search, filters and detail pages.

Do not destroy the existing schema simply because some fields were originally intended for food products.

## Phase 4 — Customer shopping experience

- Review category filtering.
- Improve product detail pages.
- Implement size selection.
- Display accurate stock and prices.
- Review cart persistence.
- Add shipping address collection.
- Define shipping methods and delivery rules.
- Improve order confirmation and tracking.

## Phase 5 — Checkout and payments

The existing audit reported Razorpay integration code, while the customer payment interface was still configured for pay-at-counter behavior.

Before enabling online payments:

- Inspect the current Razorpay implementation.
- Verify the required secrets and runtime configuration.
- Confirm order totals are calculated and validated on the server.
- Implement shipping and payment validation.
- Test payment success, failure and cancellation.
- Avoid storing card details.
- Keep payment credentials private.
- Do not enable real payment collection until the complete flow has been tested and approved.

## Phase 6 — Admin and inventory adaptation

- Add fragrance brand/house fields.
- Add concentration and olfactory-note fields.
- Support bottle-size variants and variant pricing.
- Review inventory and stock movement behavior.
- Review image management.
- Validate order management and cancellation behavior.
- Preserve secure admin access.

## Phase 7 — Image storage and performance

The original audit reported image binaries stored in PostgreSQL through `product_images`.

For a small initial catalog, this may be sufficient, depending on storage limits and performance. As the catalog grows, evaluate Cloudflare R2 or another object store.

Do not migrate image storage without assessing the current persistence implementation and creating a safe migration plan.

## Phase 8 — Production readiness

- Confirm the dedicated Neon database connection.
- Apply reviewed migrations.
- Verify environment secrets.
- Test all routes.
- Test mobile and desktop layouts.
- Review accessibility and keyboard interaction.
- Add loading, error and empty states.
- Review SEO metadata and structured data.
- Configure deployment and environment settings.
- Test a production build.
- Deploy only after explicit approval.

---

# 14. SEO AND DISCOVERABILITY

SEO was identified as a later improvement area.

Planned work:

- Unique titles and meta descriptions for the homepage, catalog, categories and product details.
- Canonical URLs.
- Open Graph metadata.
- Product structured data where accurate.
- Organization/store structured data.
- `robots.txt`.
- `sitemap.xml`.
- Search-friendly product URLs.
- Correct indexing and canonicalization.
- Google Search Console setup and sitemap submission.

A React single-page application can have discoverability limitations if all routes return the same initial HTML metadata. Inspect the deployed rendering and routing strategy before deciding whether static prerendering or another SEO approach is necessary.

Do not promise that Google will immediately index every page.

---

# 15. GOOGLE AI STUDIO DEVELOPMENT WORKFLOW

Sohail prefers to build in small, controlled steps.

Use this process for every future change:

1. Identify the single feature being upgraded.
2. Prepare a detailed prompt with the exact files, expected behavior and constraints.
3. Include an ASCII wireframe when layout or responsive behavior is involved.
4. Paste the prompt into the existing Google AI Studio conversation.
5. Wait for Gemini to finish.
6. Review its summary, files changed, build results and tests.
7. Inspect the actual mobile preview.
8. Check for regressions in related features.
9. Run the required tests and `npm run build`.
10. Approve or correct the result before starting the next feature.
11. Keep GitHub synchronized after reviewing the changes.
12. Deploy only when explicitly approved.

## Standard prompt rules

Every prompt should specify:

- Project name and repository.
- Current feature being changed.
- Exact desired outcome.
- ASCII wireframe, where useful.
- Mobile-first requirements.
- Files to inspect or modify.
- Existing behavior that must remain unchanged.
- Explicit prohibited changes.
- Verification steps.
- A requirement to report exact modified files and test results.
- A stop-and-wait instruction after the requested feature.

Avoid asking Gemini to redesign the entire application for a small improvement.

---

# 16. CURRENT HOMEPAGE STRUCTURE

The intended homepage contains these sections:

```text
+------------------------------------------------------+
| HEADER                                               |
| [MENU] [STORE LOGO + WORDMARK] [SEARCH] [BAG]       |
+------------------------------------------------------+
| HERO CAROUSEL — 3 CAMPAIGNS                         |
| Borderless editorial text + prominent perfume image |
| Automatic rotation: 5 seconds (Phase 2.6 target)     |
+------------------------------------------------------+
| SHOP BY CATEGORY                                     |
| For Him | For Her | Unisex | Gift Sets               |
+------------------------------------------------------+
| PREMIUM BRANDS UNDER ONE ROOF                        |
| Campaign image + Explore Brands                      |
+------------------------------------------------------+
| FEATURED FRAGRANCES                                   |
| Product cards + View All + Add to Bag                |
+------------------------------------------------------+
| OLFACTORY GUIDE                                      |
| Woody | Amber | Fresh | Floral                       |
+------------------------------------------------------+
| WHY SHOP WITH US?                                    |
| Authenticity | Premium Brands | Gifts | Assistance   |
+------------------------------------------------------+
| FOOTER                                                |
+------------------------------------------------------+
| FIXED MOBILE NAVIGATION                              |
| [HOME] [SHOP] [CATEGORIES] [CART] [ACCOUNT]          |
+------------------------------------------------------+
```

The homepage should prioritize the phone experience, with compact spacing, large product imagery, readable text and easy-to-tap controls.

---

# 17. FINAL CONTINUATION INSTRUCTIONS

When starting a new ChatGPT conversation, paste these notes and use the following message:

```text
Mentor, continue The Fragrance Store — House of Brands
project using the attached master handover notes.

We are building in Google AI Studio.

Repository:
sohail-24/the-fragrance-store

Workspace:
the-fragrance-store

Follow our mobile-first development approach.
Make one change at a time.
Use ASCII wireframes for UI changes.
Preserve the existing database, cart, checkout,
payment, authentication and admin functionality
unless I explicitly approve changing them.

Our current pending task is PHASE 2.6.

Review Gemini's latest output and verify that:
1. The hero carousel rotates every 5 seconds.
2. Signature Scent, Artisanal Extraits and
   Discovery Sets use the intended line breaks.
3. The perfume image is substantially larger,
   occupying approximately 60% of the hero's
   visual composition where responsive layout allows.
4. The hero remains borderless and mobile-friendly.

The Phase 2.6 prompt was prepared, but I have not yet
confirmed that Gemini implemented it.

Do not assume any unverified work is complete.
First establish the current state from the latest
AI Studio output. Then continue step by step.

Do not make unrelated changes or deploy anything
without my approval.
```

**End of master handover notes.**
