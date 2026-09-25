
# TEX’S CHICKEN & BURGERS — PROJECT CHECKPOINT

**Date:** September 25, 2026
**Project:** `texs-shop`
**Local project:** `/Users/sohal/Downloads/testing-project/shop`
**Brand:** **TEX’S CHICKEN & BURGERS**
**Tagline:** **Worth Every Bite**

---

# 1. Project identity — IMPORTANT

This is now the **Tex’s Chicken & Burgers restaurant storefront**.

Do **NOT** bring back or reintroduce:

* Shah’s Halal
* AM Fruits
* FreshFlow
* fruit products
* fruit categories
* old wholesale functionality into the customer UI

The old FreshFlow functionality may remain in the codebase as legacy/hidden functionality, but the active customer-facing brand is **Tex’s Chicken & Burgers**.

---

# 2. Main application architecture

Current customer flow:

```text
/
   ↓
/products
   ↓
/cart
   ↓
/info
   ↓
/payment
   ↓
/bill
```

Admin:

```text
/admin/login
      ↓
/admin/products
/admin/categories
/admin/inventory
/admin/orders
...
```

Database:

```text
Neon PostgreSQL
      ↓
Drizzle ORM
```

Do not create duplicate database systems.

---

# 3. Important product/variant system

The project already has a working **Multiple Price Options & Product Variants** system.

Admin currently has:

```text
Multiple Price Options & Product Variants

Option #1
Option #2
Option #3
...
```

Each variant/option can already contain things such as:

```text
Option Label
What Comes With It
Primary Price
Combo Meal Price
Only Price
Image
```

The existing architecture should always be reused.

### Existing variant behavior

* First variant image acts as the default product image.
* Variant image changes when customer selects another variant.
* Variant price changes with selected variant.
* Variant `What Comes With It` changes with selected variant.
* Existing product option functionality is already working.
* Do NOT break this.

---

# 4. What we worked on today — Home advertisement

We finalized the Home page advertisement design.

The correct design is:

```text
┌──────────────────────────────────────┐
│                                      │
│      FULL PRODUCT IMAGE              │
│                                      │
│  TODAY'S SPECIAL                     │
│  Worth Every Bite                    │
│  Fresh favorites made for you.       │
│  [ VIEW SPECIALS → ]                 │
│                                      │
└──────────────────────────────────────┘
```

### Final advertisement requirements

It must be:

* ONE single advertisement box.
* One full product image.
* Image fills the entire advertisement.
* Text directly overlays the image.
* No left/right split.
* No separate text panel.
* No inner image box.
* No divider.
* Image should remain sharp.
* Image should not be blurred.
* Image should not be distorted.

### Exact text

```text
TODAY'S SPECIAL
Worth Every Bite
Fresh favorites made for you.
VIEW SPECIALS →
```

The first three products are used dynamically.

The advertisement rotates between the first 3 products, one at a time.

The active advertisement can navigate to the active product's detail page.

### Typography adjustment

We then reduced:

```text
TODAY'S SPECIAL
Worth Every Bite
VIEW SPECIALS →
```

slightly.

The advertisement height was also reduced slightly.

Current intended state:

* advertisement height = already adjusted
* those three texts = slightly smaller
* `Fresh favorites made for you.` stays as it was
* layout must not be redesigned

---

# 5. Product-detail mobile zoom bug

We found a problem where the **Chicken Sandwich product detail page** was becoming horizontally zoomed/cropped on mobile.

Root cause was related to responsive width/overflow behavior, especially long option/title content.

AI Studio made a system-wide responsive fix.

It included things such as:

```text
min-w-0
w-full
responsive grid/flex sizing
break-words
overflow-x-hidden
```

The goal was:

```text
Mobile viewport
┌────────────────────────┐
│ Product image          │
│                        │
│ Sandwich               │
│                    $8  │
│                        │
│ Select Option          │
│ ┌────────────────────┐ │
│ │ Option             │ │
│ └────────────────────┘ │
└────────────────────────┘
```

instead of content being wider than the viewport.

### Important

Do not undo this responsive fix.

Future product detail changes must preserve:

* no horizontal overflow
* no mobile zoom/cropping
* long product names must work
* variant descriptions must work
* option cards must fit
* prices must fit

---

# 6. Left customer sidebar fix

We also fixed the customer Home page's left green sidebar.

### Previous problem

The sidebar was stretching vertically according to the product grid.

It looked like:

```text
Sidebar
│
│ categories
│
│
│
│
│
│
│
│
│
│
│
└────────────
```

and became extremely tall when the product list grew.

### Intended architecture

```text
┌──────────────┬──────────────────────┐
│ LOGO         │                      │
│ TEX'S        │       PRODUCTS       │
│              │                      │
│ All Products │      products        │
│ Burgers      │      products        │
│ Sides        │      products        │
│ Beverages    │      products        │
│ ...          │      products        │
│              │         ↓            │
│ categories   │      scrolling       │
│ can scroll   │                      │
│              │                      │
│ Good Food    │                      │
│ Brings Good │                      │
│ People       │                      │
└──────────────┴──────────────────────┘
```

The sidebar should:

* stay within the viewport
* not stretch to product-grid height
* have its own category scrolling if needed
* keep branding at top
* keep slogan/footer at bottom
* stay above mobile bottom navigation

AI Studio reported this was fixed successfully.

---

# 7. Admin Product Catalog — current task

This is the **most important unfinished task**.

We are working on:

```text
Admin
 ↓
/products
 ↓
Add Menu Item
 ↓
Multiple Price Options & Product Variants
```

The existing screen looks approximately like:

```text
Multiple Price Options & Product Variants

Option #1

[ image ]

Option Label
What Comes With It

Primary Price
Combo Meal Price
Only Price
```

---

# 8. What we originally asked for

Initially we thought about adding:

```text
[Mild] [Spicy]
```

as Quick Presets.

AI Studio added:

```text
Quick Presets:

[ Signature ]
[ Wings ]
[ Sandwiches ]
[ Tenders ]
[ Meal vs Only ]
[ Mild ]
[ Spicy ]
```

But we realized this is **NOT what we actually want**.

### IMPORTANT

Mild and Spicy should **NOT be Quick Presets**.

The Quick Preset implementation should not be expanded further.

---

# 9. Actual desired Mild / Spicy feature

What we really want is a **customer-selectable choice**.

Admin should eventually be able to configure something like:

```text
Option #1

Option Label:
Spice Level

Choices:

[ Mild ]    [ Spicy ]
```

Customer should then see:

```text
Spice Level

┌──────────────┐  ┌──────────────┐
│     Mild     │  │    Spicy     │
└──────────────┘  └──────────────┘
```

Customer selects **one**.

Example:

```text
Spice Level

[ Mild ] [ Spicy ]
   ↑
 selected
```

The selected choice should travel with the product selection into:

```text
Cart
 ↓
Checkout
 ↓
Bill
 ↓
Order
```

---

# 10. Desired future architecture for Choices

We specifically want this to be reusable.

Not hard-coded only for:

```text
Mild
Spicy
```

It should eventually support:

```text
[ Regular ] [ Mild ] [ Spicy ]
```

or:

```text
[ Small ] [ Medium ] [ Large ]
```

or another choice group.

But **we should implement the smallest possible version first**.

---

# 11. Last AI Studio task status

We gave AI Studio a prompt to add an optional:

```text
Choices
```

field to the existing option structure.

The goal was:

```text
Option #1

Option Label: Spice Level

Choices:
[ Mild ] [ Spicy ]
```

and then customer selection.

AI Studio started changing files.

The GitHub panel showed these modified files:

```text
src/components/ProductOptionsEditor.tsx
src/index.css
src/pages/LandingPage.tsx
src/lib/productOptionsPresets.test.ts
```

Then AI Studio showed:

```text
Quota exceeded. Please try again later.
```

So the task **did not clearly complete**.

---

# 12. Last verification attempt

We told AI Studio:

```text
Do not change any code.

Only verify whether the Choices feature was actually completed.

Do not edit.
Do not push to GitHub.
```

But AI Studio again ended with:

```text
Quota exceeded
```

It only showed:

```text
Built
```

It did NOT provide a proper verification result.

Therefore:

### Current status of Choices feature

**UNKNOWN / NOT VERIFIED**

Do NOT assume it works.

Do NOT push those changes to GitHub until we know what is actually implemented.

---

# 13. Current safety status

The project preview/Home page was still loading correctly after the AI Studio attempts.

AI Studio showed:

```text
Built
```

So there was no obvious catastrophic build failure shown.

However:

```text
Built ≠ feature completed
```

We still need to verify the actual Choices implementation.

---

# 14. What we should do next time

### STEP 1 — Verify current code

First ask AI Studio something extremely small:

```text
Do not change any code.

Check whether the Choices feature is actually implemented.

Answer only:

YES — fully implemented

or

NO — not implemented

If NO, tell me only the exact missing file/function.

Do not edit anything.
Do not push to GitHub.
```

Because AI Studio has been hitting quota, **do not give it another huge implementation prompt immediately**.

---

# 15. If Choices is NOT implemented

Then we inspect the current code and make **one tiny change at a time**.

Likely sequence:

```text
STEP 1
Admin UI only
        ↓
Add Choices field
        ↓
Verify
        ↓
STEP 2
Save Choices in existing option JSON
        ↓
Verify
        ↓
STEP 3
Customer displays Choices
        ↓
Verify
        ↓
STEP 4
Customer can select one
        ↓
Verify
        ↓
STEP 5
Carry selection to cart/order
```

This is safer than asking AI Studio to do everything at once.

---

# 16. Very important AI Studio strategy

Because AI Studio has repeatedly shown:

```text
Quota exceeded
```

we should now use **small prompts**.

Avoid prompts like:

> "Build a complete reusable choice architecture across admin, customer, cart, order, database..."

Instead:

```text
Make ONE small change.

Only modify ProductOptionsEditor.tsx.

Do not touch anything else.

Build and verify.
```

Then move to the next step.

This will make debugging much easier.

---

# 17. Things already working — DO NOT BREAK

### Product variants

Working:

* Option #1
* Option #2
* Option #3
* variant prices
* combo price
* only price
* variant images
* first variant as default image
* variant image synchronization
* `What Comes With It`
* customer variant selection

### Product detail

Working:

* product name
* active price
* variant synchronization
* responsive layout
* mobile overflow fix

### Home

Working:

* left category sidebar
* product grid
* advertisement
* dynamic product advertisement rotation
* search
* categories
* cart
* mobile navigation

### Order flow

Working:

```text
Cart
 ↓
Phone
 ↓
Payment
 ↓
Bill
 ↓
Order
```

Ticket format:

```text
T + last 4 digits
```

---

# 18. Database safety rules

Do NOT:

* drop Neon database
* reset schema
* recreate products
* recreate categories
* create duplicate product systems
* create duplicate variant tables
* bring back old products
* resurrect IDs 61/65–73
* restore old FreshFlow/AM Fruits data

The database resurrection bug was already fixed.

The current active products were previously verified as:

```text
6 products
6 inventory records
```

and old products/images were removed.

---

# 19. Image persistence

Product images use the durable:

```text
product_images
```

architecture with PostgreSQL `bytea`.

Do NOT replace this with temporary/local-only image storage.

Variant images must continue using the existing durable image architecture.

---

# 20. Current design philosophy

For future changes, follow this rule:

> **Small change → verify → next small change.**

Especially with Google AI Studio.

And always tell AI Studio:

```text
Do not modify unrelated systems.
Reuse existing architecture.
Do not create duplicate systems.
Do not change the database unless absolutely necessary.
Run build/tests after the change.
```

---

# 21. Immediate next task

When we continue, the starting point should be:

```text
ADMIN /products
        ↓
Add Menu Item
        ↓
Multiple Price Options & Product Variants
        ↓
VERIFY CURRENT CHOICES IMPLEMENTATION
        ↓
If incomplete:
Add Choices in the smallest possible step
        ↓
Admin:
Spice Level
[Mild] [Spicy]
        ↓
Customer:
Spice Level
[Mild] [Spicy]
        ↓
Select ONE
        ↓
Cart
        ↓
Bill
        ↓
Order
```

### Current checkpoint

**We should NOT start another large implementation yet.**

First determine exactly what the previous AI Studio run left behind.

And mentor, **you don't need to explain the whole Tex’s project again next time**. This checkpoint plus the existing project context is enough for us to resume from the **Choices/Mild-Spicy task** directly.
