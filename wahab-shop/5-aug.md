
---

# FreshFlow Debugging Notes (05 Aug 2026)

## Project Stack

* Frontend: React 19 + TypeScript + Vite
* Backend: Hono + tRPC
* Database: PostgreSQL + Drizzle ORM
* Authentication: JWT + HTTP-only Cookies
* Deployment: Docker Compose + Nginx

---

# Problem 1 — Product Images Disappeared After Docker Rebuild

## Problem

Product images initially displayed correctly, but after rebuilding Docker containers:

* Images disappeared.
* Product cards showed placeholders.
* Browser Network tab returned:

```
GET /api/uploads/products/<uuid>.webp

404 Not Found
```

The image URL still existed in PostgreSQL, but the actual image file no longer existed.

---

## Investigation

We traced the complete flow:

```
React Add Product
        ↓
POST /api/uploads/products
        ↓
Hono Upload API
        ↓
writeFile()
        ↓
/app/uploads/products
        ↓
Save URL in PostgreSQL
```

We checked inside Docker:

```
docker exec -it freshflow-app sh
```

Then:

```
find /app -name "*.webp"
```

Result:

```
No files found
```

The upload directory itself didn't exist.

---

## Root Cause

The uploaded images were stored inside the container filesystem:

```
/app/uploads/products
```

Docker containers are ephemeral.

Whenever we executed:

```
docker compose up --build
```

the container was recreated.

PostgreSQL data survived because of the database volume.

Image files were deleted because no Docker volume existed for uploads.

Database:

```
image:
/api/uploads/products/abc.webp
```

File:

```
Deleted
```

Hence:

```
404 Not Found
```

---

## Solution

### Dockerfile

Created upload directory before switching to the non-root user:

```dockerfile
RUN mkdir -p /app/uploads/products
RUN chown -R appuser:appgroup /app
```

---

### docker-compose.yml

Added persistent volume:

```yaml
services:
  app:
    volumes:
      - product_uploads:/app/uploads

volumes:
  pgdata:
  product_uploads:
```

---

## Verification

Uploaded a new product image.

Verified inside container:

```
ls /app/uploads/products
```

Image existed.

Ran:

```
docker compose down
docker compose up
```

Image still existed.

Ran:

```
docker compose up --build
```

Image still existed.

Verified in:

* Brave
* Safari
* Atlas Browser

All browsers displayed images correctly.

---

## Interview Explanation

> We discovered uploaded product images were stored inside the application's writable container layer. Since Docker recreates containers during rebuilds, image files were lost while PostgreSQL still contained their paths. We solved this by introducing a persistent Docker named volume mounted at `/app/uploads`, allowing uploaded media to survive container recreation.

---

# Problem 2 — First Login Always Failed

## Problem

User visited:

```
/checkout
```

Redirected to:

```
/login?returnTo=/checkout
```

After entering valid credentials:

* Login API succeeded.
* Page redirected back to Login.
* Second login always worked.

---

## Investigation

We traced:

```
Login Page
      ↓
Login Mutation
      ↓
JWT Cookie
      ↓
React Query
      ↓
ProtectedRoute
```

Authentication itself worked.

JWT cookies were already created.

No issue with:

* JWT
* Cookies
* Docker
* Nginx

---

## Root Cause

React Query had cached:

```
auth.me = null
```

When login completed:

```
invalidate()
```

only marked the cache stale.

Navigation happened immediately.

ProtectedRoute still received:

```
auth.me = null
```

Therefore it redirected back to Login.

Only afterward did React Query refetch the authenticated user.

Second login succeeded because cache already contained the user.

---

## Solution

Instead of:

```ts
invalidate();

navigate(...)
```

we changed to:

```ts
await utils.auth.me.invalidate();

const user = await utils.auth.me.fetch();

navigate(...)
```

Now the authenticated user is loaded before routing.

---

## Verification

Tested:

```
/checkout
```

→ Login

→ First Login

Immediately entered Checkout.

No second login required.

---

## Interview Explanation

> The issue wasn't JWT generation but a React Query cache race condition. After login, the router navigated before the authenticated user state was refreshed, so ProtectedRoute still saw the stale anonymous cache. We solved it by explicitly fetching the authenticated user before navigation.

---

# Problem 3 — Wrong Supplier Phone Number

## Problem

Buyer Order page displayed:

```
Supplier Phone

+1 (555) 123-4567
```

Admin Profile showed:

```
9573692390
```

Address was correct.

Supplier name was correct.

Only phone number was wrong.

---

## Investigation

We traced:

```
Buyer Order Page
      ↓
tRPC
      ↓
Router
      ↓
Query
      ↓
Database
```

Found:

```
companies.phone
```

was being used.

It still contained seeded placeholder data.

---

## Root Cause

Admin Profile updates:

```
users.phone
```

Order Details read:

```
companies.phone
```

Two unrelated sources.

So changing the admin profile never affected orders.

---

## Solution

Order Details now loads:

```
Platform Admin
```

and maps:

```
supplierPhone = platformAdmin.phone
```

Removed placeholder value from future seed data.

---

## Verification

Updated admin phone.

Opened Buyer Order.

Phone immediately reflected the updated value.

---

## Interview Explanation

> We discovered a data consistency issue where different parts of the application read the supplier phone from different database tables. The admin profile updated the `users` table, while order details displayed the phone from seeded company data. We unified the data source so both screens read from the same authoritative value.

---

# Key Technical Concepts You Learned

* Docker named volumes
* Persistent vs ephemeral container storage
* File uploads inside Docker
* React Query cache invalidation
* Authentication race conditions
* HTTP-only JWT cookies
* ProtectedRoute behavior
* Full-stack debugging (Frontend → API → Database)
* Data consistency across related tables
* End-to-end request tracing
* Production-style root cause analysis

---

# What You Can Say in an Interview

> "During development of FreshFlow, I debugged several production-level issues. One was a Docker persistence problem where uploaded images disappeared after container recreation because they were stored inside the container filesystem instead of a persistent volume. Another was an authentication race condition caused by React Query caching anonymous user data, which required fetching the authenticated user before routing. I also resolved a data consistency issue by ensuring order details used the same authoritative source as the admin profile for supplier contact information. In each case, I traced the issue end-to-end—from the React UI through the tRPC API, backend queries, and PostgreSQL—to identify the real root cause rather than applying temporary fixes."

---

Mentor, today you didn't just "fix bugs." You solved **three real production engineering issues** by following the correct debugging process: reproduce the issue, trace the full request flow, identify the root cause, implement the minimal fix, and verify it end-to-end. Those experiences are exactly the kind that strengthen both your project and your interview discussions.
