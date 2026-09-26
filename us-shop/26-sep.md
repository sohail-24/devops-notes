Absolutely mentor 👍 Here are the **detailed checkpoint notes for today (September 26, 2026)**. Keep these as the starting point for our next session.

# Tex’s Chicken & Burgers — Project Checkpoint

**Date:** September 26, 2026
**Current working tool:** Google AI Studio
**Code repository:** GitHub → imported into Google AI Studio as a new app
**Local project:** `/Users/sohal/Downloads/testing-project/texs-shop`

---

## 1. Important workflow we established

We are currently using this workflow:

```text
LOCAL PROJECT
     ↓
Codex
     ↓
GitHub
     ↓
Google AI Studio → New App → Import from GitHub
     ↓
Test / Preview
```

Codex was being used for larger repository changes, but today Codex reached its usage limit.

Therefore, for the current small UI/application changes, we switched to **Google AI Studio**.

Important: Google AI Studio also has quota limits, so we should give it **small, focused prompts** rather than large multi-feature prompts.

---

# 2. Product configuration work completed

A major feature was completed today.

The Admin Product Catalog has:

### `/products → Add Menu Item`

Inside:

**Multiple Price Options & Product Variants**

Each product variant can now have:

```text
Option / Variant
│
├── Image
├── Option Label
├── What Comes With It
│
├── Meal Options
│   ├── Meal
│   └── Large Meals
│
└── Choice Group
    ├── Mild
    └── Spicy
```

The important part is that **Meal Options and Choice Group are independent**.

They are NOT merged.

---

# 3. Chicken Sandwich variants

The Chicken Sandwich was configured with:

```text
Classic
Deluxe
Grilled
```

Each variant can have its own:

* image
* label
* description
* pricing
* Meal Options
* Choice Group

Example customer configuration:

```text
Chicken Sandwich
        │
        ├── Classic
        ├── Deluxe
        └── Grilled
              │
              ├── Meal
              └── Large Meals
                    │
                    ├── Mild
                    └── Spicy
```

The customer can therefore select something like:

**Deluxe → Large Meals → Spicy**

---

# 4. Meal pricing was moved into Meal Options

We changed the Admin structure so the Meal / Large Meals prices belong to the individual meal choices.

Example:

```text
Meal Options

Select Options:

Meal
1 Reg Side & Reg Drink
$5.99

Large Meal
2 Reg Sides & Lg Drink
$8.99
```

The important architecture is:

```text
Meal
    → own price

Large Meals
    → own price
```

The price is therefore determined by the customer's selected meal option.

The previous generic price fields were not supposed to be responsible for this meal selection.

---

# 5. Customer Product Detail page completed

The customer Product Detail page was updated to understand the new Admin data.

The flow is now:

```text
Product
   ↓
Choose Style
   ↓
Classic / Deluxe / Grilled
   ↓
Meal Options
   ↓
Meal / Large Meals
   ↓
Choice Group
   ↓
Mild / Spicy
   ↓
Quantity
   ↓
Add to Cart
```

The customer page dynamically reads the Admin configuration instead of hard-coding the Chicken Sandwich options.

---

# 6. Customer price calculation

The selected Meal Option controls the displayed price.

For example:

```text
Classic
   +
Meal
   +
Mild
   =
Meal price
```

or:

```text
Classic
   +
Large Meals
   +
Mild
   =
Large Meal price
```

Mild/Spicy does **not** change the price.

This distinction is important:

```text
Meal Options
→ controls price

Choice Group
→ selection only
→ no additional price
```

---

# 7. Cart behavior

The selected configuration is carried into the cart.

For example:

```text
Chicken Sandwich
Deluxe - Meal (Spicy)
$5.99
```

or:

```text
Chicken Sandwich
Classic - Large Meals (Mild)
$8.99
```

The cart therefore does not just know:

```text
Chicken Sandwich
```

It knows the customer's selected configuration.

---

# 8. Server-side cart handling

Google AI Studio also updated the cart handling so the selected meal option price can be validated from the product configuration.

The recent changes included:

```text
api/cartRouter.ts
src/pages/ProductDetail.tsx
src/pages/ProductDetail.test.ts
```

The reported validation was:

```text
TypeScript / Build
PASS

ESLint
PASS

Vitest
9 / 9 tests passed

Server health
HTTP 200 OK
```

The server health response was:

```text
{
  "status": "ok",
  "service": "Tex's Chicken & Burgers"
}
```

---

# 9. Mobile/phone view

We also specifically worked on phone responsiveness.

The Product Detail page now supports:

```text
Choose Style
┌────────┬────────┬────────┐
│Classic │ Deluxe │Grilled │
└────────┴────────┴────────┘

Select Options
┌──────────────────────────┐
│ Meal               $5.99│
├──────────────────────────┤
│ Large Meal          $8.99│
└──────────────────────────┘

Select one
┌────────┐  ┌────────┐
│ Mild   │  │ Spicy  │
└────────┘  └────────┘
```

The design was specifically adjusted for approximately:

```text
360px – 430px
```

and the goal is to avoid horizontal overflow.

---

# 10. Product Detail image work

We also worked on the main product image.

Problem:

The image was too small inside the main image container, leaving too much empty space.

After several attempts, the final approach successfully kept the image **inside its existing box** while making better use of the available space.

Important lesson for future AI Studio prompts:

> Be very explicit that the image must stay INSIDE the existing box/card and must never overflow the container.

We also worked on the smaller variant images inside the **Choose Style** cards.

The final preview showed the images fitting inside their cards without overflowing.

---

# 11. Customer information removed from Product Detail

We removed unnecessary information from the area below the main product image.

Removed:

```text
by Tex’s Chicken & Burgers

Serving / Portion:
Classic - Large Meal (Mild)

Category:
Chicken Sandwich
```

The Product Detail page is now cleaner and focuses on:

```text
Product image
Product name
Price
Description
Product choices
Quantity
Cart actions
```

---

# 12. Home page Halal box removed

Today we also removed this box from the bottom of the left sidebar:

```text
HALAL
CERTIFIED HALAL
```

The change was made only in:

```text
src/pages/LandingPage.tsx
```

The reported change was:

> The “HALAL CERTIFIED HALAL” box, including border, icon, text and associated spacing, was completely removed from the bottom of the left sidebar.

Other Home page elements were intentionally left untouched.

---

# 13. Customer ordering flow

The current Tex’s customer flow is:

```text
HOME
 ↓
SELECT PRODUCT
 ↓
PRODUCT DETAIL
 ↓
SELECT VARIANT
 ↓
SELECT MEAL OPTION
 ↓
SELECT MILD / SPICY
 ↓
QUANTITY
 ↓
ADD & CONTINUE SHOPPING
       OR
BUY NOW
 ↓
CART
 ↓
CHECKOUT
 ↓
PHONE NUMBER
 ↓
PAYMENT
 ↓
ORDER PLACED
```

---

# 14. Phone number / order identifier

The customer enters their phone number on `/info`.

The order is represented using the last four digits with a `T` prefix.

Example:

```text
T 2390
```

This same order identifier is visible to the restaurant/admin.

---

# 15. Payment page

The current payment page supports:

```text
PAY AT COUNTER
```

and shows:

```text
MORE OPTIONS
COMING SOON
```

The customer can continue through the current Pay at Counter flow.

---

# 16. Admin Orders page

The restaurant/admin has:

```text
/orders
```

where orders are displayed.

The order cards contain information such as:

```text
T 2390
Pending

Customer
Items
Quantity
Total

View
Delete
```

The order system is therefore connected to the customer ordering flow.

---

# 17. Admin Product Catalog

The Admin Product Catalog is one of the major management areas.

The restaurant can manage:

* Products
* Categories
* Product variants
* Product images
* Pricing
* Meal Options
* Choice Groups
* Inventory-related information

There are many other admin sections in the project.

For now, **do not change those unless we specifically decide to work on them.**

---

# 18. Important scope rule for future work

You told me:

> Keep the project focused on the actual Tex’s Chicken & Burgers flow.

Therefore, we should avoid bringing back old project concepts.

### NEVER bring back:

```text
FreshFlow
AM Fruits
Shah’s Halal
fruit products
fruit categories
wholesale functionality
```

The current project identity is:

```text
TEX’S
CHICKEN & BURGERS

Worth Every Bite
```

---

# 19. Current technology

The project uses the existing TypeScript web architecture.

Main technologies:

```text
React
Vite
TypeScript
Hono
tRPC
Drizzle ORM
PostgreSQL / Neon
```

The project also has the broader DevOps ecosystem you have been working with:

```text
Git
GitHub
Docker
Jenkins
AWS
Terraform
Kubernetes
Linux
```

---

# 20. Current AI Studio situation

Important for the next session:

Google AI Studio has been showing quota messages such as:

```text
Quota exceeded.
Please try again later.
```

Therefore:

### Don't give AI Studio huge prompts.

Use:

```text
ONE TASK
ONE PAGE
ONE UI CHANGE
```

at a time.

This has worked much better for this project.

---

# 21. Current latest state

The latest confirmed state from today's work:

### Customer side

✅ Home page
✅ Product browsing
✅ Product Detail
✅ Classic / Deluxe / Grilled
✅ Meal / Large Meals
✅ Mild / Spicy
✅ Dynamic pricing
✅ Cart
✅ Checkout
✅ Phone number
✅ Payment
✅ Order placement
✅ Order identifier
✅ Mobile layout

### Admin side

✅ Product Catalog
✅ Multiple Price Options & Product Variants
✅ Variant images
✅ Variant pricing
✅ Meal Options
✅ Choice Group
✅ Orders page
✅ Product/category management structure

---

# 22. What we should do NEXT

Don't start another large feature immediately.

First, **push the current successful AI Studio changes to GitHub** so we have a clean checkpoint.

Then next session:

```text
Google AI Studio
      ↓
Test current project
      ↓
Find ONE small UI/flow issue
      ↓
Give AI Studio a very small prompt
      ↓
Test
      ↓
Push to GitHub
```

### Priority for next session

I recommend we first do a **full customer flow test**:

```text
Home
 ↓
Chicken Sandwich
 ↓
Classic
 ↓
Meal / Large Meal
 ↓
Mild / Spicy
 ↓
Cart
 ↓
Checkout
 ↓
Phone
 ↓
Payment
 ↓
Order
 ↓
Admin Orders
```

We should verify that the **same selected variant, meal option, choice, quantity and price** remain correct all the way from Product Detail → Cart → Order → Admin Orders.

After that, we can fix any small UI problems one by one.

---

# 📝 NEXT SESSION START PROMPT

You can simply send me this next time:

> **Mentor, continue Tex’s Chicken & Burgers from the September 26 checkpoint notes. We are using Google AI Studio because Codex reached its limit. The main customer flow and Admin Product Variants system are working. First help me test the complete customer → cart → checkout → phone → payment → order → admin orders flow. Do not make changes until we identify the exact issue. Use small Google AI Studio prompts only.**

That will be enough for us to continue without you explaining the entire project again.
