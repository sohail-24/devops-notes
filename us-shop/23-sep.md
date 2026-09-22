Absolutely, Mentor. We covered **a lot today**, especially the complete customer order flow + Neon persistence + Admin order management. Below is a **master continuity note** you can keep and give to me/Codex/AI Studio next time so we can continue without explaining everything again.

# Tex’s Chicken & Burgers — MASTER PROJECT NOTES

### Last updated: 23 September 2026, around 12:09 AM IST

---

## 1. PROJECT IDENTITY

**Real brand:**

> Tex’s Chicken & Burgers

**Tagline:**

> Worth Every Bite

**Important:**

* Shah’s Halal was only a testing name.
* AM Fruits / FreshFlow are legacy origins.
* Do **not** bring back Shah’s Halal, AM Fruits, FreshFlow, fruit products, or fruit categories.
* Customer-facing application must remain Tex’s Chicken & Burgers.

### Local project

```text
/Users/sohal/Downloads/testing-project/shop
```

User prefers working with the **local project folder**, especially for large repository tasks.

---

# 2. CURRENT ARCHITECTURE

### Customer side

```text
/
Home
 ↓
/products
Products / categories
 ↓
/cart
Cart
 ↓
/info
Phone number
 ↓
/payment
Payment selection
 ↓
/bill
Final order bill
```

### Admin side

```text
/admin/login
      ↓
Admin dashboard
      ↓
/orders
Admin Orders
```

Customers are **guests**.

There is no customer login flow.

Admin authentication remains separate.

---

# 3. DATABASE

The application now uses:

```text
Neon PostgreSQL
+
Drizzle ORM
```

The Neon database and existing schema/migrations must be preserved.

### Do NOT:

* Drop the Neon database.
* Reset the schema.
* Drop existing tables.
* Recreate the database.
* Create a second order system.
* Create duplicate order tables.
* Bring back legacy fruit data.
* Delete the existing product/inventory architecture.

---

# 4. NEON CLEANUP COMPLETED

The old database data was cleaned.

### Removed legacy companies

Old fruit wholesale companies and Shah's Halal company were removed.

The main company is now:

```text
Tex’s Chicken & Burgers
```

Company ID:

```text
1
```

---

# 5. CURRENT TEX'S CATEGORIES

The active restaurant categories were cleaned to:

```text
Platters
Burgers & Sandwiches
Party Wings
Sides
Drinks
Catering
```

Legacy:

```text
Gyros
```

was removed/deactivated.

Old descriptions referring to things like:

* falafel
* pakora
* baklava
* hummus
* old halal-cart food

were cleaned from the active restaurant catalog.

---

# 6. CURRENT PRODUCTS

The current real Tex's products we have been working with are:

```text
French Fries
Mac N'Cheese
Mashed Potato
Fire Roasted Corn
Coleslaw
```

Existing inventory records were preserved.

Do not randomly create fake products or synthetic product images.

---

# 7. IMPORTANT IMAGE STORAGE WORK

We discovered the original problem:

Before Neon was connected, the application could show FreshFlow fruit images from the local mock database.

After Neon was connected, some product images disappeared because the database contained image URLs but the physical uploaded files were not persistent.

### Solution implemented

A dedicated Neon PostgreSQL table was created:

```text
product_images
```

It stores the actual image binary data using PostgreSQL `bytea`.

It also stores information such as:

```text
filename
MIME type
file size
product linkage
created timestamp
```

### Upload architecture

When an image is uploaded:

```text
Image
 ↓
POST /api/products/upload
 ↓
Neon product_images
 +
local filesystem cache
```

When an image is requested:

```text
/api/uploads/:filename
 ↓
Check local file
 ↓
If missing
 ↓
Read image from Neon product_images
 ↓
Serve image
```

This means uploaded images should survive local container/environment resets.

### Verification already done

A simulated reset was performed:

* image existed
* local file was removed
* application requested the image
* image was retrieved from PostgreSQL
* response returned HTTP 200
* binary content was verified

French Fries and Mac N'Cheese were verified as durable.

### Important

The remaining real images should be uploaded through the normal application/admin upload flow.

Do **not** fabricate UUID filenames manually.

---

# 8. OFFLINE MOCK DATABASE

The old `mockDb.ts` contained FreshFlow fruit data.

That was cleaned.

The mock fallback was changed to Tex’s Chicken & Burgers data so that offline/fallback mode doesn't suddenly display:

```text
Valencia Oranges
Organic Navel Oranges
Citrus
Tropical
Berries
etc.
```

---

# 9. PHONE NUMBER SYSTEM

We changed the customer phone system from India to USA.

### Current format

```text
+1
```

Example:

```text
+1 9121969239
```

The old Indian validation such as:

```text
Indian mobile numbers must start with 6, 7, 8, or 9
```

was removed.

US +1 phone validation/normalization was implemented.

### `/info`

The customer sees:

```text
Almost there!

Enter your phone number to continue with your order.

PHONE NUMBER

+1 | ____________

Continue →
```

The sentence:

> We'll use this number to send order confirmations and delivery updates.

was removed.

---

# 10. CUSTOMER ORDER FLOW

This is now the intended flow:

```text
Cart
 ↓
/info
 ↓
Enter phone number
 ↓
Continue
 ↓
/payment
 ↓
Select Pay at Counter
 ↓
/bill
```

---

# 11. `/payment` PAGE

The payment page was created specifically for the order flow.

It displays the order ticket:

```text
T 2390
```

The letter was changed from:

```text
K
```

to:

```text
T
```

The last four digits remain from the customer's phone number.

Example:

```text
T 2390
T 9239
T 5743
```

### Payment options

Two side-by-side boxes:

```text
┌─────────────────┐ ┌──────────────────────┐
│ PAY AT COUNTER  │ │ MORE OPTIONS         │
│ Available       │ │ COMING SOON          │
└─────────────────┘ └──────────────────────┘
```

### Important current `/payment` behavior

The following were removed:

```text
Continue
Back to Customer Info
```

They must **not** be restored.

A:

```text
← Back to Home Page
```

option was added at the bottom of the payment card.

---

# 12. `/bill` PAGE

`/bill` is the final customer order bill.

It displays:

```text
ORDER TICKET

T 9239
```

Then the selected order items.

Example:

```text
Mac N'Cheese       x1       $3.25

TOTAL                       $3.25

PAYMENT
Pay at Counter
```

The page was redesigned from a plain page into a restaurant-style order ticket.

### `/bill` contains:

* Order ticket
* T + last four digits
* Selected items
* Quantities
* Item prices
* Total
* Payment method
* Order received state

### Navigation

A:

```text
← Back to Home Page
```

was added.

There should be:

* no Continue
* no unnecessary Back buttons
* no checkout navigation

The bill is intended to be the final customer order receipt/view.

---

# 13. CART BEHAVIOR AFTER ORDER

When the customer places an order:

```text
Current cart
     ↓
Order snapshot created
     ↓
Cart becomes empty
     ↓
Placed order remains available separately
```

This is important because the customer must be able to place another order later without mixing it with the previous order.

---

# 14. MULTIPLE ORDERS

This was an important requirement.

Example:

### First order

At:

```text
10:00 PM
```

Customer orders:

```text
Mac N'Cheese
```

Ticket:

```text
T 2390
```

Then five minutes later:

### Second order

Customer orders:

```text
French Fries
```

Ticket:

```text
T 2390
```

Both orders must remain separate.

The system must **never overwrite the first order with the second order**.

---

# 15. CUSTOMER "VIEW ORDER" FEATURE

After an order is placed, the Home page shows:

```text
View Order
```

near the Tex’s Chicken & Burgers header.

Example:

```text
Tex's Chicken & Burgers        [ View Order ]
Worth Every Bite
```

### Visibility

The customer-side View Order feature is limited to:

```text
30 minutes
```

from the order creation time.

After 30 minutes, the customer-side View Order option disappears.

### Multiple active orders

If one active order exists:

```text
View Order
```

If multiple active orders exist:

```text
View Orders (2)
```

etc.

The customer can select the specific order and open its `/bill`.

---

# 16. VERY IMPORTANT: ADMIN 30-MINUTE RULE

We explicitly separated customer visibility from Admin history.

### Customer:

```text
30-minute View Order visibility
```

### Admin:

```text
PERMANENT order history
```

The Admin must **not** lose orders after 30 minutes.

An order expiring from the customer's View Order UI must **never delete the Neon order**.

---

# 17. ADMIN `/orders` — NOW WORKING

This was the major issue we fixed today.

Previously:

```text
/info → Continue
```

could create a customer-side order snapshot but it wasn't reliably appearing in Admin `/orders`.

That has now been connected to the existing database order system.

### Current flow

```text
Customer
  ↓
/info
  ↓
Enter phone
  ↓
Continue
  ↓
Existing orderRouter.create
  ↓
Neon PostgreSQL
  ↓
orders
+
order_items
  ↓
Admin /orders
```

The order now appears in Admin.

---

# 18. ADMIN ORDER INFORMATION

Admin `/orders` now displays information such as:

```text
T 5743
Pending
11:57 PM · Sep 22, 2026

$3.25

Pay at Counter
```

And order details include:

* T + last four digits
* customer/order information
* ordered products
* quantities
* prices
* total
* payment method
* order timestamp

---

# 19. ADMIN MULTIPLE ORDERS

Admin must preserve every order separately.

Example:

```text
T 2390
T 9239
T 5743
```

All remain in Admin order history.

Refreshing `/orders` must not remove them.

The customer's 30-minute visibility is completely separate.

---

# 20. ADMIN DELETE ORDER

We also added a Delete Order option.

Each order can be deleted individually.

Expected behavior:

```text
Delete
 ↓
"Delete this order?"
 ↓
Confirm
 ↓
Delete selected order
 +
associated order items
 ↓
Refresh order list
```

Deleting one order must not delete other orders.

---

# 21. ADMIN `/orders` MOBILE DESIGN

The Admin Orders page was changed to a two-column mobile layout.

Instead of:

```text
┌───────────────────┐
│ Order 1           │
└───────────────────┘

┌───────────────────┐
│ Order 2           │
└───────────────────┘
```

we now want:

```text
┌──────────────┐ ┌──────────────┐
│ T 5743       │ │ T 2390       │
│ Pending      │ │ Pending      │
│ $3.25        │ │ $6.50        │
│ Pay Counter  │ │ Pay Counter  │
│ Delete       │ │ Delete       │
└──────────────┘ └──────────────┘
```

This was confirmed working.

---

# 22. TESTING COMPLETED TODAY

AI Studio reported successful:

* ESLint
* TypeScript compilation
* production build
* test suites

The order creation → Admin `/orders` flow was verified working.

---

# 23. CURRENT CUSTOMER EXPERIENCE

The intended final customer journey is:

```text
                  HOME
                   │
                   ▼
               PRODUCTS
                   │
                   ▼
                  CART
                   │
                   ▼
                 /INFO
                   │
           Enter phone number
                   │
                Continue
                   │
                   ▼
               /PAYMENT
                   │
        ┌──────────┴──────────┐
        │                     │
 PAY AT COUNTER        MORE OPTIONS
   Available            Coming Soon
        │
        ▼
                /BILL
        │
        ├── Order Ticket
        ├── Items
        ├── Quantities
        ├── Total
        ├── Payment
        └── Back to Home
```

At the same time:

```text
/info
  │
  ▼
Neon PostgreSQL
  │
  ▼
Admin /orders
```

---

# 24. IMPORTANT THINGS NOT TO TOUCH

When continuing development, AI Studio/Codex must not unnecessarily modify:

```text
Neon schema
Database migrations
Product catalog
Inventory
Product image architecture
Cart logic
Admin authentication
/payment design
/bill design
/info phone validation
Customer 30-minute View Order behavior
```

Especially don't allow AI Studio to "clean up" unrelated architecture while doing a small UI change.

We have repeatedly used the instruction:

> Do not modify unrelated pages or systems.

Keep doing this.

---

# 25. CURRENT KNOWN UI CLEANUP

There are still some visible old/testing texts in the customer Home page that should eventually be cleaned.

For example, the screenshot still showed things such as:

```text
Fresh Halal Products
```

and an old banner containing:

```text
HALAL FOOD
DELICIOUS HALAL FOOD
```

These are leftovers from the old Shah's Halal testing design.

The real brand is:

```text
Tex’s Chicken & Burgers
```

So these should eventually be replaced with Tex's actual restaurant branding/content.

**Do not bring back Shah's Halal as a brand.**

---

# 26. NEXT WORK — RECOMMENDED ORDER

Now that the **core ordering/database flow is working**, the next work should be done carefully rather than changing the architecture again.

### Next 1 — Complete Tex's branding cleanup

Search customer-facing pages for old:

```text
Shah's Halal
Fresh Halal
Halal Food
FreshFlow
AM Fruits
fruit names
old fruit descriptions
```

and remove/replace only where they are still visible.

Do not change database architecture.

---

### Next 2 — Test complete customer order flow

Test:

```text
Add product
 ↓
Cart
 ↓
Info
 ↓
+1 phone
 ↓
Continue
 ↓
Payment
 ↓
Pay at Counter
 ↓
Bill
 ↓
Home
 ↓
View Order
```

Then test:

```text
Order #1
 ↓
Order #2
 ↓
Home
 ↓
View Orders (2)
 ↓
Open each bill
```

---

### Next 3 — Test Admin

Verify:

```text
/info
 ↓
Continue
 ↓
Neon
 ↓
Admin /orders
```

Check:

* ticket
* items
* quantity
* prices
* total
* payment method
* timestamp

Then:

```text
Place second order
 ↓
Admin
 ↓
Both orders visible
```

Then:

```text
Delete one
 ↓
Only that order disappears
 ↓
Other order remains
```

---

### Next 4 — Test image persistence again

Because this was a major problem earlier, perform a real reset/reconnect test:

```text
Upload image
 ↓
Confirm image displays
 ↓
Disconnect/reconnect environment
 ↓
Reload application
 ↓
Image still displays
```

Do this for the actual uploaded Tex's images.

---

### Next 5 — Continue UI polish

After functionality is stable:

* Home page branding
* Product cards
* Category presentation
* About page
* Admin Inventory responsive design
* remaining image consistency
* spacing/layout cleanup

These should be handled **one focused change at a time**.

---

# 27. GOLDEN RULE FOR FUTURE AI STUDIO PROMPTS

Because AI Studio sometimes changes unrelated code, use this structure:

```text
Change ONLY [specific page/feature].

Do not modify:
[list unrelated systems]

Use the existing architecture.
Do not create duplicate systems/tables.
Do not change database schema unless explicitly requested.

After the change:
- build
- run tests
- verify the exact requested behavior.
```

This has worked much better for this project.

---

# 28. ONE-PARAGRAPH QUICK RESUME

If we start a new conversation, this is enough to immediately restore the project context:

> **We are building the Tex’s Chicken & Burgers restaurant storefront at `/Users/sohal/Downloads/testing-project/shop`. It uses Neon PostgreSQL + Drizzle, with guests ordering through `/ → /products → /cart → /info → /payment → /bill`, and Admin isolated at `/admin/login`. Product images are now durably stored in Neon through `product_images` so they survive environment resets. Legacy FreshFlow/AM Fruits/Shah’s Halal fruit data has been cleaned/deactivated. `/info` uses US `+1` phone numbers and creates a real Neon order when Continue is clicked. Customer tickets use `T + last four digits`. `/payment` has Pay at Counter and More Options Coming Soon, with Continue and Back to Customer Info removed; it has Back to Home. `/bill` is the final attractive order ticket with items, totals, payment method, and Back to Home. Customer View Order(s) remains visible for 30 minutes only and supports multiple active orders. Admin `/orders` permanently stores all orders, displays ticket/details/items/total/payment/time, supports multiple orders, has two-column mobile cards, and allows deleting individual orders. The key remaining work is branding cleanup of old Fresh Halal/Shah’s Halal text/images, thorough end-to-end order/image persistence testing, and then UI polish. Do not reset the Neon database, create duplicate order systems, restore legacy data, or modify unrelated pages when making focused changes.**

---

## Current checkpoint

**The most important milestone today:**
The application is no longer just showing a customer-side order snapshot. **`/info → Continue` is now connected to the real Neon order system, and the order appears in Admin `/orders`.** Multiple orders and Admin deletion are also working.
