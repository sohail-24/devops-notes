

### Important branding history

The project originally came from:

```text
FreshFlow
   ↓
AM Fruits
   ↓
Shah’s Halal  ← testing only
   ↓
Tex’s Chicken & Burgers  ← REAL BRAND
```

### IMPORTANT

Never bring back:

```text
Shah’s Halal
AM Fruits
FreshFlow
```

for customer-facing branding.

The real logo is:

```text
/public/branding/logo.png
```

The real brand must remain:

```text
Tex’s Chicken & Burgers
Worth Every Bite
```

---

# 2. PROJECT LOCATION / WORKFLOW

For larger repository work, the preferred local project is:

```text
/Users/sohal/Downloads/testing-project/shop
```

The user prefers:

```text
LOCAL PROJECT
↓
DIRECT CODE INSPECTION
↓
TARGETED CHANGES
↓
ACTUAL PREVIEW VERIFICATION
```

rather than giving a GitHub URL for large repository work.

Google AI Studio is currently being used for UI/application changes.

---

# 3. APPLICATION PURPOSE

The application has been transformed from the old wholesale FreshFlow application into a **restaurant storefront**.

Customer-facing experience:

```text
Home
Categories
Products
Product Details
Cart
About
```

Admin functionality still exists for managing:

```text
Products
Categories
Inventory
Business
Orders
```

The old FreshFlow wholesale/customer functionality is **preserved but hidden/deactivated**, not intentionally deleted.

---

# 4. ADMIN AUTHENTICATION

Current intended authentication:

```text
/admin/login
```

Admin-only authentication is active.

Customers should NOT receive the old FreshFlow customer-login experience.

Admin configuration includes:

```text
ADMIN_EMAIL
ADMIN_PASSWORD
JWT_ACCESS_SECRET
JWT_REFRESH_SECRET
DATABASE_URL
```

The business relationship has already been fixed so the application resolves to:

```text
Tex’s Chicken & Burgers
```

Business:

```text
Name: Tex’s Chicken & Burgers
Tagline: Worth Every Bite
Slug: texs-chicken-and-burgers
Logo: /branding/logo.png
Type: supplier
Status: active / verified
```

Admin business relationship and inventory functionality were previously verified.

---

# 5. SIDEBAR / CATEGORY STRUCTURE

The customer sidebar currently uses the real Tex’s branding.

Required categories:

```text
🍽️ All Products
🍛 Platters
🍗 Party Wings
🍟 Sides
🥤 Drinks
🍱 Catering
```

### IMPORTANT

Do NOT remove or rename these category icons/names unless specifically requested.

The sidebar should continue using the real Tex’s logo and branding.

---

# 6. PRODUCT IMAGE SYSTEM — WORKING

This was an important issue we fixed.

Initially:

```text
Admin uploads image
        ↓
image saved
        ↓
customer page did not show it
```

The image pipeline was investigated and fixed.

### Fixes included

1. Image upload authentication

`AddProduct.tsx` and `EditProduct.tsx` were updated so upload requests include the required admin credentials/session information.

2. Image fallback

The product queries now resolve images from available product image fields, including:

```text
products.image
products.images
```

3. Local upload paths

Supported paths were added for local product uploads such as:

```text
/api/uploads/
/uploads/products/
```

4. Customer visibility

Products must satisfy the appropriate active/marketplace/inventory visibility requirements.

5. Image rendering

Customer product cards/detail pages now properly display uploaded product images.

### Confirmed

The user explicitly confirmed:

> “yes its work!”

A new product such as French Fries was successfully showing its uploaded image on the customer storefront.

### DO NOT BREAK THIS

Future changes must not unnecessarily modify:

```text
AddProduct image upload
EditProduct image upload
product image queries
customer image rendering
inventory visibility
```

---

# 7. MULTIPLE PRODUCT OPTIONS / PRICES — WORKING

Another major feature was implemented.

The requirement was:

```text
ONE PRODUCT
   ↓
MULTIPLE OPTIONS
   ↓
EACH OPTION HAS ITS OWN PRICE
   ↓
SAME PRODUCT IMAGE
```

Example:

```text
Signature Chicken

2 PC       $9.49 Meal
           $5.49 Only

3 PC       $10.49 Meal
           $7.49 Only

4 PC       $11.49 Meal
           $8.49 Only
```

Other examples:

```text
Chicken Sandwich
├── Classic
├── Deluxe
└── Grilled
```

and:

```text
Chicken Tenders
├── 3 PC
└── 5 PC
```

The system was implemented across product management, product details, cart, and related APIs.

### Important behavior

Customer:

```text
Product
   ↓
Select option
   ↓
Correct price
   ↓
Add to cart
```

The cart preserves the selected option and price.

Different configurations can exist as separate cart items.

### Confirmed

User explicitly said:

> “yes its work!”

### DO NOT TOUCH THIS SYSTEM

Unless specifically requested, do not modify the working:

```text
ProductOptionsEditor
AddProduct
EditProduct
ProductDetail
Cart
product queries
cart queries
product API
order API
guest cart
```

---

# 8. TODAY'S MAIN WORK — ABOUT PAGE

Today's main focus was the **About page**.

The old About page contained incorrect/placeholder content such as:

```text
platters
gyros
wraps
falafel over rice
```

and referenced broken/nonexistent images.

We replaced the concept with a real Tex’s Chicken & Burgers story.

---

# 9. VERIFIED TEX’S STORY CONTENT

The About page now has the correct business story based on the information already researched.

Important facts:

### NYC origin

Tex’s roots go back to the:

```text
late 1980s
```

with NYC roots involving:

```text
Bronx
Harlem
Brooklyn
```

### Mission

The story focuses on providing accessible, affordable halal American comfort food.

### 2016

The brand was formally unified under:

```text
Texas Chicken & Burgers
```

in 2016.

The modern identity evolved toward:

```text
Tex’s
```

### Current footprint

The current official About content references:

```text
55+ locations
```

across the East Coast.

### Name

The “Tex’s” story connects the brand's southern-style crispy breading with its NYC halal identity.

### Brand tagline

```text
Worth Every Bite
```

---

# 10. FOOD QUALITY INFORMATION

Verified information used for the About page includes:

```text
100% Certified Halal
Never Frozen
Fresh ingredients
No artificial preservatives/chemicals
No pink slime / ammonia-treated fillers
```

The wording should remain factual and should not become exaggerated marketing claims.

---

# 11. MENU CONTENT

The About page can reference real menu categories such as:

```text
Signature Chicken
Smash Burgers
Chicken Sandwiches
Tenders
Fiery Wings
Sides
Honey Biscuits
Desserts
```

Real menu examples were researched earlier.

Do not invent menu items just to fill empty sections.

---

# 12. TEX’S REWARDS

The official Rewards system was also researched.

The program is called:

```text
Tex’s Rewards
```

Customers earn:

```text
Spurs
```

The important concept:

```text
Spend
 ↓
Earn Spurs
 ↓
Rewards
```

The earlier About redesign incorrectly presented Rewards as large:

```text
Tier 1
Bronze

Tier 2
Silver

Tier 3
Gold
```

cards.

### USER DOES NOT WANT THESE BOXES.

They must be removed from the About page.

Rewards should instead be represented in a simple visual format such as:

```text
EARN
  ↓
SPURS
  ↓
LEVEL UP
  ↓
REDEEM
```

No giant Bronze/Silver/Gold cards.

---

# 13. FIRST ABOUT REDESIGN

AI Studio created a very large redesign.

It added:

```text
About.tsx
BurgerExplodeAnimation.tsx
About.test.ts
```

The proposed page contained:

```text
Hero
↓
Born in New York
↓
Beginning
↓
Craft
↓
2016
↓
Then → Now
↓
Why Tex’s?
↓
Quality
↓
Menu
↓
Rewards
↓
Final CTA
```

It also added a burger animation.

---

# 14. PROBLEM WITH THE FIRST ABOUT REDESIGN

The user did **not** like the result.

Main problems:

### Problem 1 — Too much dark green

The page looked like:

```text
dark green
dark green
dark green
cards
dark green
```

User wants:

> **FULL PAGE WHITE**

---

### Problem 2 — Cartoon burger

The burger animation looked like:

```text
cartoon bun
cartoon cheese
cartoon patty
cartoon vegetables
```

User explicitly does NOT want this.

The user wants:

> **REAL BURGER IMAGE**

---

### Problem 3 — Wrong layout

The proposed split layout:

```text
┌──────────────┬──────────────┐
│    TEXT      │    IMAGE     │
└──────────────┴──────────────┘
```

was NOT what the user meant.

This was an important misunderstanding.

---

# 15. EXACT ABOUT PAGE DESIGN USER WANTS NOW

This is the most important part of today's notes.

## A. ENTIRE PAGE MUST BE WHITE

Not:

```text
green hero
green section
green card
green section
```

Instead:

```text
WHITE
WHITE
WHITE
WHITE
WHITE
WHITE
```

Green/gold can be used only as small accents.

---

# 16. HERO IMAGE REQUIREMENT

The user wants the **real burger photograph at the top**.

Not beside the text.

Not in a separate right column.

Not inside a small card.

The desired concept is:

```text
┌──────────────────────────────────┐
│                                  │
│       REAL BURGER PHOTO          │
│                                  │
│     TEX'S CHICKEN & BURGERS      │
│          Worth Every Bite        │
│                                  │
└──────────────────────────────────┘
```

The text should sit **over the burger background/image**.

This is the key misunderstanding from the previous prompt.

---

# 17. AFTER HERO

After the burger hero:

```text
              ↓
       COMPLETELY WHITE
              ↓
        ABOUT CONTENT
```

No dark green full-width blocks.

The content should feel like a clean premium restaurant editorial page.

---

# 18. BURGER ANIMATION REQUIREMENT

The user wants the burger state to react to scrolling.

Initial:

```text
ASSEMBLED
```

When scrolling DOWN:

```text
ASSEMBLED
     ↓
EXPLODED
```

When scrolling UP:

```text
EXPLODED
     ↑
ASSEMBLED
```

So:

```text
SCROLL DOWN = EXPLODE

SCROLL UP = ASSEMBLE
```

This should not simply be:

```text
page loads
↓
animation plays once
↓
finished
```

It must respond to scroll direction.

---

# 19. IMPORTANT BURGER VISUAL REQUIREMENT

The burger should be based on:

**REAL FOOD PHOTOGRAPHY**

Not:

```text
SVG cartoon
illustration
fake vector ingredients
cartoon patty
cartoon bun
```

If separate ingredient photos are unavailable, do not fabricate them.

A real burger photo can instead use:

```text
scale
crop
mask
parallax
position
opacity
layer reveal
```

to create a premium exploded effect.

---

# 20. SIDE-BY-SIDE REQUIREMENT — CLARIFICATION

The user DOES want some content to be visually side-by-side, but **not** as:

```text
TEXT | IMAGE
```

The earlier prompt misunderstood this.

The intended idea is more like **multiple content boxes/cards side-by-side** where appropriate.

For example:

```text
┌───────────────────┬───────────────────┐
│   BORN IN NYC     │   THE BEGINNING   │
└───────────────────┴───────────────────┘
```

or:

```text
┌───────────────────┬───────────────────┐
│      QUALITY      │      STORY        │
└───────────────────┴───────────────────┘
```

But the **hero is different**:

```text
REAL BURGER IMAGE
+
TEXT ON TOP
```

---

# 21. MOBILE REQUIREMENT

Phone view is very important.

Target:

```text
375px
390px
414px
```

Must have:

```text
No horizontal overflow
No clipped text
No overlapping elements
No huge empty spaces
Comfortable touch targets
Bottom navigation visible
Real burger remains visually strong
```

Cards can stack on mobile when needed.

---

# 22. BOTTOM NAVIGATION

Keep:

```text
Home
Categories
Cart
About
```

About should remain active when on `/about`.

Do not remove the bottom navigation.

---

# 23. WHAT HAPPENED WITH THE LATEST AI STUDIO ATTEMPT

We gave AI Studio a large redesign prompt.

It was too broad.

Then we tried a shorter prompt.

That also did not produce the intended visual result.

The latest screenshot showed the preview at:

```text
/
```

rather than the intended About page.

AI Studio also displayed:

```text
Quota exceeded. Please try again later.
```

So **do not assume the latest requested About changes were successfully implemented.**

This is important.

The last reliable implementation state is the previous About redesign, while the desired new white/real-photo design is still the target.

---

# 24. WHY WE SHOULD NOT KEEP SENDING HUGE PROMPTS

AI Studio is already working with a large codebase.

When we send a huge prompt containing:

```text
architecture
design
animations
testing
business story
responsive rules
many files
many requirements
```

Gemini can misunderstand the visual priority or spend too much time changing unrelated code.

### New strategy

We should upgrade the About page in **small controlled steps**.

For example:

```text
STEP 1
Fix ONLY About page background + hero.

STEP 2
Fix ONLY burger image/animation.

STEP 3
Fix ONLY content layout.

STEP 4
Remove Rewards Tier cards.

STEP 5
Mobile polish.

STEP 6
Final verification.
```

This will make debugging much easier.

---

# 25. WHAT MUST NOT BE TOUCHED

Future About work must NOT break:

```text
Product image upload
Product image display
Multiple product options
Multiple prices
Cart
Checkout
Admin authentication
Business relationship
Inventory
Product catalog
Category system
Bottom navigation
```

These systems are already working.

---

# 26. CURRENT PRIORITY

Our next priority is **NOT another giant About prompt**.

The next step should be:

```text
ABOUT PAGE
     ↓
INSPECT CURRENT CODE
     ↓
INSPECT CURRENT PREVIEW
     ↓
FIX HERO ONLY
```

The first change should establish the correct visual foundation:

```text
WHITE PAGE
     +
REAL BURGER IMAGE
     +
TEXT OVER BURGER IMAGE
```

Once that looks correct, we move to the scroll animation.

---

# 27. NEXT UPGRADE PLAN

## Phase 1 — Hero

Target:

```text
WHITE PAGE
        ↓
REAL BURGER PHOTO
        ↓
TEXT OVER PHOTO
        ↓
TEX'S LOGO
        ↓
Worth Every Bite
```

No cartoon.

No green full-page background.

---

## Phase 2 — Burger scroll

Implement:

```text
Initial → Assembled

Scroll ↓ → Exploded

Scroll ↑ → Assembled
```

Verify this manually in preview.

---

## Phase 3 — Content layout

Use clean white sections with selected content arranged in grids:

```text
┌────────────┬────────────┐
│   STORY    │   ORIGIN   │
├────────────┼────────────┤
│   CRAFT    │   QUALITY  │
└────────────┴────────────┘
```

Not text/image split everywhere.

---

## Phase 4 — Rewards

Remove:

```text
Bronze
Silver
Gold
```

large cards.

Use:

```text
EARN → LEVEL UP → REDEEM
```

---

## Phase 5 — Mobile

Check:

```text
375px
390px
414px
```

---

## Phase 6 — Final verification

Only after the visual design is correct:

```text
npm test
npm run lint
build
/about desktop
/about mobile
scroll down
scroll up
bottom nav
```

---

# 28. MASTER DESIGN RULE

If we ever need to explain the About page again, this is the **short version**:

```text
TEX'S ABOUT PAGE

FULL PAGE = WHITE

TOP:
REAL BURGER PHOTO AS BACKGROUND
TEXT + LOGO OVER THE BURGER

SCROLL:
ASSEMBLED → EXPLODED
EXPLODED → ASSEMBLED

REST OF PAGE:
WHITE
CLEAN
PREMIUM
CONTENT GRID
SIDE-BY-SIDE BOXES WHERE APPROPRIATE

REMOVE:
❌ Cartoon burger
❌ Dark green page
❌ Dark green sections
❌ Tier 1
❌ Tier 2
❌ Tier 3
❌ Text/Image split layout

KEEP:
✅ Tex's logo
✅ Tex's story
✅ Real business information
✅ Bottom navigation
✅ Product/cart/admin systems untouched
```

---

# 29. CURRENT CHECKPOINT

```text
┌─────────────────────────────────────────────┐
│       TEX'S CHICKEN & BURGERS              │
│           PROJECT CHECKPOINT                │
├─────────────────────────────────────────────┤
│ Branding              ✅                    │
│ Real logo             ✅                    │
│ Admin auth            ✅                    │
│ Business relation     ✅                    │
│ Product images        ✅ WORKING            │
│ Multiple options      ✅ WORKING            │
│ Multiple prices       ✅ WORKING            │
│ Cart                   ✅ PRESERVE          │
│ Inventory              ✅ PRESERVE          │
│ Categories             ✅ PRESERVE          │
│                                             │
│ About content         ✅ RESEARCHED         │
│ About redesign        ⚠️ STILL REFINING    │
│ Cartoon burger        ❌ REMOVE             │
│ Dark page             ❌ REMOVE             │
│ Real burger hero      🎯 NEXT              │
│ Scroll animation      🎯 NEXT               │
│ Rewards tiers         ❌ REMOVE             │
└─────────────────────────────────────────────┘
```

## Mentor's next starting point

When you come back again, you **do not need to explain the project**.

Just say something like:

> **“Mentor, continue from the Tex’s Chicken & Burgers September 21 checkpoint. Let's work on the About page.”**

Then we can immediately continue from:

**white page → real burger background hero → text over image → scroll animation → clean content layout → rewards cleanup.**
