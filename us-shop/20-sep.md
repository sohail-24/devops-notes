
---

# 1. PROJECT IDENTITY

The original project was **FreshFlow / AM Fruits**, but it is being transformed into:

```text
SHAH'S HALAL

Fresh Food · Pure Taste
```

The application has both:

```text
CUSTOMER STOREFRONT
        +
ADMIN MANAGEMENT
```

The goal is to make the application behave like a real restaurant storefront where the Admin panel controls the actual customer-facing data.

---

# 2. DEVELOPMENT WORKFLOW WE ARE USING

## Google AI Studio

AI Studio was used for:

* UI redesign
* Shah's Halal branding
* category page redesign
* product page redesign
* admin product catalog redesign
* restaurant food data conversion
* initial data synchronization work

However, AI Studio recently hit:

```text
Request timeout
Quota exceeded
Unexpected error
```

So we moved the larger repository/data-flow tasks to **Codex**.

## Codex

For larger repository tasks we now use:

```text
Codex
+
LOCAL PROJECT
+
DIRECT REPOSITORY INSPECTION
```

We do **NOT** give Codex the GitHub repository URL.

Always use:

```bash
cd /Users/sohal/Downloads/testing-project/shop
```

This is now our preferred workflow for this project.

---

# 3. IMPORTANT DEVELOPMENT RULE

The user prefers:

```text
SMALL CHANGE
↓
INSPECT
↓
TEST
↓
CHECK DIFF
↓
COMMIT
↓
NEXT CHANGE
```

Avoid:

```text
BIG REWRITE
BIG REFACTOR
UNRELATED CLEANUP
```

Do not allow AI Studio/Codex to redesign unrelated parts of the application.

---

# 4. IMPORTANT AUTHENTICATION RULE

Authentication is already working.

Do NOT casually modify:

```text
api/auth-router.ts
api/auth/admin-session.ts
```

Also don't change:

* JWT
* admin login
* session handling
* admin password handling
* authentication architecture

The recent `a2f078a` commit already contained authentication-related changes, so future tasks should treat the current authentication implementation as the baseline.

---

# 5. IMPORTANT LEGACY ARCHITECTURE RULE

This project came from:

```text
FreshFlow / AM Fruits
```

There are still legacy wholesale/business fields and architecture.

We decided:

```text
KEEP LEGACY BACKEND WHERE NECESSARY
BUT
HIDE/ADAPT OLD WHOLESALE UI
```

Do not perform unnecessary database migrations.

Do not delete legacy columns just because Shah's Halal doesn't use them.

---

# 6. SHAH'S HALAL CUSTOMER UI WORK COMPLETED

## Mobile category sidebar

Implemented:

```text
28% sidebar
72% shopping area
```

Permanent sidebar.

No hamburger/drawer behavior.

Gradient:

```text
#0F5132
   ↓
#062E1F
   ↓
#0F5132
```

Categories include:

```text
All Products
Platters
Gyros
Burgers
Party Wings
Rice Bowls
Sandwiches
Salads
Sides
Beverages
Desserts
```

---

# 7. MOBILE PRODUCT CARDS

Implemented:

```text
2 products per row
```

Compact cards containing:

* image
* product name
* Shah's Halal Food
* selling price
* original price where available
* rating
* Certified Halal
* quantity control
* Add button

---

# 8. MOBILE BOTTOM NAVIGATION

Implemented:

```text
Home
Categories
Cart
Login/Profile
```

Customer mobile navigation is fixed at the bottom.

Cart badge uses live count.

Categories navigation was changed to route to:

```text
/products
```

rather than only scrolling the homepage.

---

# 9. HOME PAGE

The home page received a restaurant-style hero redesign.

Current concept:

```text
DELICIOUS HALAL FOOD

Fresh restaurant imagery

100% HALAL

ORDER NOW →
```

The existing sidebar and shopping structure were preserved.

---

# 10. `/products` PAGE

We redesigned `/products` to act as a food-category browsing destination.

Current concept:

```text
SHAH'S HALAL

Search

FOOD CATEGORIES
Choose what you're craving

┌───────────────┬───────────────┐
│   PLATTERS    │    GYROS      │
├───────────────┼───────────────┤
│   BURGERS     │ PARTY WINGS   │
├───────────────┼───────────────┤
│ RICE BOWLS    │ SANDWICHES    │
├───────────────┼───────────────┤
│   SALADS      │    SIDES      │
├───────────────┼───────────────┤
│  BEVERAGES    │   DESSERTS    │
└───────────────┴───────────────┘
```

Important:

We specifically wanted to avoid:

* one-column category layout
* three-column layout
* narrow cards
* huge blank space on the right

The category grid should use the available content width.

---

# 11. ADMIN PRODUCT CATALOG REDESIGN

The old Admin Product Catalog contained wholesale fruit concepts such as:

```text
Premium Alphonso Mango
Supplier
Warehouse
Barcode
Wholesale Selling Rules
Grade
Origin
Shelf Life
Packaging
Wholesale handling
```

We started converting this into restaurant terminology.

New direction:

```text
Dish Name
Menu Category
Food Image
Description
Price
Availability
Tags
Restaurant-specific information
```

The visual structure was intentionally preserved instead of completely redesigning the Admin UI.

---

# 12. REAL SHAH'S HALAL MENU RESEARCH

We researched the official Shah's Halal menu as reference.

Major menu concepts found include:

```text
Platters
Gyros
Burgers
Sandwiches
Party Wings
Fries
Sides
Desserts
Drinks
```

Example food items include:

```text
Chicken Over Rice
Shahwarma Over Rice
Beef and Lamb Over Rice
Combo Over Rice
Kofta Kabab Over Rice
Falafel Over Rice
Fish Over Rice

Chicken Gyro
Shahwarma Gyro
Beef & Lamb Gyro
Combo Gyro
Kofta Gyro
Falafel Gyro
Fish Gyro

Cheeseburger
Double Cheeseburger
Chicken Sandwich
Spicy Chicken Sandwich
Fish Sandwich
Falafel Sandwich

Party Wings

Fries
Pakora Chips
Loaded Chips

Chicken Nuggets
Hot Wings
Hummus
Baklava
Pita

Drinks
```

Prices should come from the application's database rather than blindly hardcoding official menu prices because restaurant pricing can vary by location.

---

# 13. IMPORTANT DATA-SYNC PROBLEM WE FOUND

This was the major functional issue.

Example:

Admin:

```text
Gyros
Inactive
```

But customer:

```text
Gyros
```

was still visible.

At first it looked like the Admin toggle wasn't working.

But Codex investigated the actual data flow.

---

# 14. ROOT CAUSE OF GYROS BUG

The actual problem was in:

```text
src/pages/LandingPage.tsx
```

The customer homepage had a **hardcoded category array**.

So it behaved like:

```text
LandingPage
    ↓
Hardcoded category list
    ↓
Gyros
```

while the database correctly knew:

```text
Gyros
isActive = false
```

Therefore:

```text
ADMIN
 ↓
DATABASE
 ↓
API

worked

BUT

CUSTOMER SIDEBAR
 ↓
hardcoded data

bypassed database
```

---

# 15. CATEGORY VISIBILITY FIX

Codex replaced the hardcoded customer category navigation with database-driven categories.

New architecture:

```text
ADMIN
   ↓
DATABASE
   ↓
category.list
   ↓
LandingPage
   ↓
ACTIVE CATEGORIES
   ↓
CUSTOMER
```

Category navigation now uses the actual database `categoryId`.

If a selected category becomes inactive, the storefront safely returns to:

```text
All Products
```

---

# 16. PRODUCT VISIBILITY FIX

The existing `api/queries/products.ts` already had an important buyer-side filter.

Customer product queries require appropriate conditions including:

```text
active product
+
marketplace visibility
+
active inventory
+
sufficient stock
+
active category
```

So we preserved this logic.

This means:

```text
Product inactive
        ↓
Customer cannot see it
```

and:

```text
Category inactive
        ↓
Products in category
        ↓
Customer cannot see them normally
```

---

# 17. PRICE SYNCHRONIZATION

We established the rule:

```text
ADMIN PRICE
    ↓
DATABASE
    ↓
product.list
    ↓
CUSTOMER
```

There should not be a separate hardcoded frontend price array.

Example:

```text
Admin
$12.99 → $13.99

Database
13.99

Customer
$13.99
```

---

# 18. ADD PRODUCT SYNCHRONIZATION

New products should follow:

```text
Admin creates product
        ↓
Database
        ↓
product.list
        ↓
Customer storefront
```

No manual frontend product-array editing should be required.

---

# 19. CODEX FIRST SYNC FIX

Codex changed:

```text
src/pages/LandingPage.tsx
api/queries/products.visibility.test.ts
src/pages/LandingPage.test.ts
vitest.config.ts
```

Tests were added for the data-driven behavior.

Validation:

```text
npm test
3 files
5 tests passed

npm run build
PASS

npm run lint
PASS
```

---

# 20. SECOND BUG — EDIT PRODUCT CATEGORY

After the data-sync fix, we found another issue.

Admin:

```text
Edit Menu Item
```

showed:

```text
Dish Name
Chicken Sandwich

Menu Category *
[ dropdown ]
```

But the category dropdown had no usable options.

Because:

```text
Menu Category *
```

is required, the product could not be saved.

---

# 21. IMAGE ERROR FOUND DURING EDIT PRODUCT

At the same time we saw:

```text
Product images must be uploaded files or HTTP(S) URLs.
```

This was treated as a **separate issue** from the empty category dropdown.

We instructed Codex:

* fix category data flow first
* don't redesign image handling
* don't build a new image system
* ensure an unchanged existing image doesn't unnecessarily prevent editing

---

# 22. CODEX SECOND FIX

Codex modified:

```text
api/productRouter.ts
api/productRouter.test.ts
src/pages/EditProduct.tsx
src/pages/EditProduct.test.ts
```

along with the previous files.

The final commit contains:

```text
8 files changed
148 insertions
53 deletions
```

Commit:

```text
2d251a6
fix: sync admin product and category data
```

---

# 23. CURRENT GIT CHECKPOINT

Current important commits:

```text
2d251a6 fix: sync admin product and category data
a2f078a refactor: update branding, improve stability, and fix filtering
7dec498 style: improve landing page UI and layout consistency
7a8afbd refactor(ui): update landing page layout and product catalog
```

At the time of the last check:

```text
working tree clean
```

and:

```text
main
ahead of origin/main by 1 commit
```

The new commit is:

```text
2d251a6
```

**Important:** We had not yet confirmed the final `git push origin main` after creating `2d251a6`. Tomorrow first check:

```bash
git status
git log --oneline -3
```

If it says:

```text
Your branch is ahead of 'origin/main' by 1 commit
```

then:

```bash
git push origin main
```

---

# 24. CURRENT LOCAL PATH

Always start Codex/local work here:

```bash
cd /Users/sohal/Downloads/testing-project/shop
```

Check:

```bash
pwd
```

Expected:

```text
/Users/sohal/Downloads/testing-project/shop
```

---

# 25. DEPENDENCY IMPORTANT NOTE

The current commit `a2f078a` showed:

```text
package-lock.json
```

being deleted.

Therefore:

### DO NOT automatically run:

```bash
npm install
```

because that may recreate `package-lock.json` and create a large unrelated change.

We already successfully ran:

```bash
npm test
```

with:

```text
3 test files passed
5 tests passed
```

So there was no need to run `npm install` at that point.

Also:

```text
metadata.json
```

does not need to be touched for this issue.

---

# 26. CURRENT TEST STATUS

The latest confirmed test result was:

```text
npm test

✓ src/pages/LandingPage.test.ts
✓ api/queries/products.visibility.test.ts
✓ api/services/orderNotification.test.ts

Test Files: 3 passed
Tests: 5 passed
```

Earlier Codex also confirmed:

```text
npm run build
PASS

npm run lint
PASS
```

After the second Edit Product changes, the final commit was created, but tomorrow we should run the complete validation again before any further work:

```bash
npm test
npm run build
npm run lint
```

---

# 27. CURRENT ADMIN → CUSTOMER ARCHITECTURE

This is now the key architecture we want:

```text
                    ADMIN
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
      CATEGORY                  PRODUCT
          │                       │
          │ activate/deactivate   │ activate/deactivate
          │                       │ price
          │                       │ add
          └───────────┬───────────┘
                      ↓
                   DATABASE
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
     category.list            product.list
          │                       │
          └───────────┬───────────┘
                      ↓
                CUSTOMER SHOP
```

Database must remain the source of truth.

---

# 28. CUSTOMER VS ADMIN ROUTING — IMPORTANT

During the Codex investigation we discovered that:

```text
/categories
```

is currently associated with the **protected Admin category-management route**.

The customer storefront is:

```text
/
```

and customer product browsing uses:

```text
/products
```

So tomorrow don't assume `/categories` is the public customer category page.

The customer category navigation is currently part of the landing/storefront experience.

---

# 29. CURRENT CUSTOMER CATEGORY RULE

```text
category.isActive = true
        ↓
Customer can see category

category.isActive = false
        ↓
Customer cannot see category
```

And:

```text
product active
+
category active
        ↓
customer can see product
```

---

# 30. NEXT TESTS — TOMORROW

Before any new feature, perform these real-world tests.

### Test A — Category OFF

Admin:

```text
Categories
→ Gyros
→ OFF
```

Customer:

```text
/
```

Expected:

```text
Gyros disappears
```

---

### Test B — Category ON

Admin:

```text
Gyros
→ ON
```

Customer:

```text
/
```

Expected:

```text
Gyros appears
```

---

### Test C — Product OFF

Admin:

```text
Product Catalog
→ Product
→ OFF
```

Customer:

```text
Product category
```

Expected:

```text
Product disappears
```

---

### Test D — Product ON

Admin:

```text
Product
→ ON
```

Expected:

```text
Product appears
```

---

### Test E — Price

Admin:

```text
12.99 → 13.99
```

Customer:

```text
13.99
```

---

### Test F — Add Product

Admin:

```text
Add Product
→ create active product
```

Customer:

```text
new product appears
```

---

### Test G — Edit Product Category

Admin:

```text
Edit Product
→ Menu Category
→ choose category
→ Save
```

Expected:

```text
category dropdown contains database categories
selected category persists
product relationship changes
```

---

# 31. IMPORTANT IMAGE TEST

Because the Edit Product page showed:

```text
Product images must be uploaded files or HTTP(S) URLs.
```

tomorrow specifically test:

```text
Open existing product
↓
Do NOT change image
↓
Change only category/name/price
↓
Save
```

If Save fails because of the existing image value, investigate that separately.

Don't redesign image handling unless necessary.

---

# 32. NEXT DEVELOPMENT ORDER

After testing, our likely order is:

```text
1. Verify Git push
        ↓
2. Run test/build/lint
        ↓
3. Test Admin category sync
        ↓
4. Test product activation
        ↓
5. Test price change
        ↓
6. Test Add Product
        ↓
7. Test Edit Product category
        ↓
8. Test existing image behavior
        ↓
9. Fix only remaining bugs
        ↓
10. New Git checkpoint
        ↓
11. Continue Admin Product Catalog improvements
```

---

# 33. WHAT NOT TO DO TOMORROW

Do NOT immediately:

```text
❌ redesign Admin
❌ redesign customer UI
❌ migrate database
❌ upgrade dependencies
❌ run npm audit fix --force
❌ recreate package-lock.json unnecessarily
❌ rewrite authentication
❌ create another category system
❌ hardcode categories
❌ hardcode product prices
❌ hardcode Gyros behavior
❌ reset to old commits
❌ revert a2f078a
```

---

# 34. OUR MAIN PRINCIPLE

From now on, for Shah's Halal:

```text
                  DATABASE
                     │
             SOURCE OF TRUTH
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
      ADMIN                    CUSTOMER
    manages                   displays
        │                         │
        └────── SAME DATA ────────┘
```

If Admin changes something, the customer should reflect that change through the database/API.

---

# 35. TOMORROW — START COMMAND

When you come back, just tell me:

> **Mentor, continue Shah's Halal from the 20 Sep checkpoint.**

We can start with:

```bash
cd /Users/sohal/Downloads/testing-project/shop

git status

git log --oneline -3
```

Then I'll know we're continuing from:

```text
2d251a6
fix: sync admin product and category data
```

and we can immediately continue testing/fixing without rebuilding the whole story.

**Checkpoint saved.**
