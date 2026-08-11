
# 1. Your 5-Minute Explanation 🎤

Use this when the interviewer says:

> **"Tell me about your project."**

### 0:00–0:45 — What is AM Fruits?

> "I built a B2B wholesale commerce platform called AM Fruits. Internally the project is called FreshFlow. The main goal is to help wholesale businesses manage their product catalog, inventory, orders and procurement while also providing a buyer-facing marketplace.
>
> It's not just a basic ecommerce application. I designed it more like a wholesale ERP combined with a marketplace."

Then explain the two sides:

```text
Business Owner
     ↓
ERP Workspace

Buyer
     ↓
Marketplace
```

---

### 0:45–1:30 — Technology Stack

> "For the frontend I used React 19 with TypeScript and Vite. React Router handles routing, and Tailwind with shadcn-style components handles the UI.
>
> For data fetching I used tRPC with TanStack Query.
>
> The backend is Node.js using Hono and tRPC. I use Zod for validation and Drizzle ORM with PostgreSQL for database access."

Then:

```text
Frontend
React + TypeScript + Vite

        ↓ tRPC

Backend
Node.js + Hono + tRPC

        ↓ Drizzle ORM

Database
PostgreSQL
```

---

### 1:30–2:20 — Architecture / Deployment

This is your strongest DevOps section.

> "For deployment, I containerized the application using Docker Compose. I separated the system into an Nginx container, application container and PostgreSQL container."

Explain:

```text
Internet
   ↓
Cloudflare / DNS
   ↓
Nginx
   ↓
React + API
   ↓
Hono/tRPC
   ↓
PostgreSQL
```

Then explain Nginx:

> "Nginx is the public entry point. It handles HTTPS termination, serves the React SPA, reverse proxies `/api` requests to the Node application, and provides security headers, gzip compression and API rate limiting."

Then health checks:

```text
Nginx → /nginx-health

App → /health

PostgreSQL → pg_isready
```

This is a **very good DevOps answer**.

---

### 2:20–3:10 — Security & Authentication

> "Authentication supports email/password and mobile OTP. Successful authentication creates HTTP-only access and refresh cookies. Access and refresh tokens are rotated."

Then role-based access:

```text
Admin
  ↓
Platform Admin

Owner email
  ↓
Business Owner

Everyone else
  ↓
Buyer
```

And importantly:

> "I didn't rely only on frontend hiding. Owner-only operations are also protected at the backend through authorization middleware."

That last sentence is important in an interview.

---

### 3:10–4:15 — Razorpay

This is your strongest recent engineering story.

> "I integrated Razorpay for checkout and then performed a production-hardening pass."

Explain the flow:

```text
Buyer
 ↓
Checkout
 ↓
Backend creates Razorpay Order
 ↓
Razorpay Checkout
 ↓
Payment
 ↓
Razorpay response
 ↓
Backend signature verification
 ↓
Order creation
 ↓
PostgreSQL
```

Then your engineering improvements:

> "One issue I addressed was duplicate order creation. I added server-side idempotency using the Razorpay order ID."

> "I also implemented HMAC-SHA256 signature verification and used `crypto.timingSafeEqual` rather than normal string comparison."

> "On the frontend, I added payment-in-progress state so users cannot repeatedly submit checkout while the Razorpay modal is active."

Then clearly say:

> "The Razorpay integration is currently hardened and tested, but Live Mode is still pending. The next step is replacing the test credentials with production credentials and completing the production configuration."

**Don't say you have real payment working yet.** Your documentation explicitly says Live Mode is pending.

---

### 4:15–5:00 — What you learned / future

Finish with:

> "The biggest thing I learned from this project was that building the application is only one part. I also had to think about authentication, authorization, containerization, reverse proxying, HTTPS, health checks, payment security, idempotency and production readiness."

Then:

> "The next evolution would be CI/CD, durable object storage, stronger tenant isolation, Kubernetes deployment, additional staff roles, audit logging and more automated testing."

That's your **5-minute answer**.

---

# 2. Your 10-Minute Explanation 🎤

If the interviewer says:

> **"Explain the project in detail."**

Use the 5-minute explanation above, then expand into these sections.

## A. Business Problem

Explain:

```text
Wholesale business
        ↓
Product catalog
        ↓
Inventory
        ↓
Buyer orders
        ↓
Payment
        ↓
Delivery
        ↓
Reports
```

The important distinction:

> "The system is designed around wholesale procurement rather than consumer ecommerce."

That is a strong domain explanation.

---

# B. Frontend Architecture

Explain:

```text
src/
├── pages/
├── components/
├── hooks/
├── providers/
└── lib/
```

Then:

> "`App.tsx` controls route composition. `AppLayout` provides the authenticated shell. Pages are role-aware so the owner gets ERP functionality while buyers get procurement functionality."

Mention:

* React 19
* TypeScript
* Vite
* React Router
* Tailwind
* shadcn-style components
* Lucide
* tRPC
* TanStack Query

---

# C. Backend Architecture

Explain separation of concerns:

```text
Router
  ↓
Validation / Authorization
  ↓
Query Layer
  ↓
Drizzle ORM
  ↓
PostgreSQL
```

Your important statement:

> "I separated router responsibilities from database query functions. Routers handle validation and authorization, while query functions handle persistence."

That's a good software architecture answer.

---

# D. Database

You don't need to memorize every table.

Understand the major domains:

```text
Users
 ↓
Companies

Products
 ↓
Categories
 ↓
Inventory

Buyer
 ↓
Cart
 ↓
Orders
 ↓
Order Items
 ↓
Invoices
```

And:

```text
Products
 ↓
Supplier

Inventory
 ↓
Warehouse
 ↓
Stock Movements
```

Know these relationships.

---

# E. Docker

Your deployment:

```text
docker-compose.yml

├── nginx
├── app
└── db
```

Explain why:

> "I separated the public reverse proxy, application runtime and database into independent containers so each service has a clear responsibility."

Then:

```text
nginx:stable
node:22-slim
postgres:15-alpine
```

Volumes:

```text
pgdata
product_uploads
```

Network:

```text
freshflow-network
```

---

# F. Nginx

Know these very well:

### Port 80

```text
HTTP
 ↓
301 redirect
 ↓
HTTPS
```

### Port 443

```text
HTTPS
 ↓
React SPA
```

### `/api/`

```text
Nginx
 ↓
app:3000
```

### `/api/uploads/`

```text
Nginx
 ↓
/app/uploads/products/
```

And:

> "The database isn't exposed publicly."

Very important.

---

# G. Razorpay Security

This deserves extra attention.

Know this sequence:

```text
Razorpay payment

      ↓

razorpay_order_id
razorpay_payment_id
razorpay_signature

      ↓

Backend

      ↓

HMAC-SHA256

      ↓

timingSafeEqual

      ↓

Valid?
  /     \
Yes      No
 ↓        ↓
Order    Reject
```

And duplicate protection:

```text
razorpayOrderId
       ↓
Check DB
       ↓
Already exists?
   /         \
 Yes          No
 ↓             ↓
Reject       Create
```

---

# 3. Most Important Points to Memorize ⭐

Don't memorize everything.

Memorize these **20 points**.

### Project

1. **AM Fruits = public brand; FreshFlow = internal project name.**
2. B2B wholesale marketplace + ERP.
3. Owner workspace + Buyer workspace.

### Frontend

4. React 19.
5. TypeScript + Vite.
6. React Router.
7. tRPC + TanStack Query.
8. Tailwind + shadcn-style components.

### Backend

9. Node.js + Hono + tRPC.
10. Zod validation.
11. Drizzle ORM.
12. PostgreSQL.

### Security

13. JWT access + refresh cookies.
14. HTTP-only cookies.
15. Role-based authorization.
16. Backend owner authorization — not just frontend hiding.

### Infrastructure

17. Docker Compose.
18. Nginx reverse proxy + HTTPS.
19. Cloudflare DNS.
20. Health checks + persistent volumes.

### Payment — VERY IMPORTANT

And separately memorize:

```text
Razorpay
HMAC-SHA256
timingSafeEqual
Idempotency
Duplicate order protection
Payment-in-progress state
```

---

# 4. Questions You MUST Be Able to Answer

These are your **high-priority interview questions**.

### Architecture

**Q: Explain your project architecture.**

You should be able to draw:

```text
User
 ↓
Cloudflare
 ↓
Nginx
 ↓
React
 ↓
Hono/tRPC
 ↓
Drizzle
 ↓
PostgreSQL
```

---

### DevOps

**Q: Why did you use Docker Compose?**

Answer:

> "To containerize and isolate the Nginx, application and database services while providing reproducible deployment and service networking."

---

### Nginx

**Q: Why Nginx?**

Answer:

> "As the public reverse proxy and TLS termination layer. It serves the SPA, proxies API traffic, provides security headers, compression and rate limiting."

---

### Security

**Q: Why HTTP-only cookies?**

> "To prevent JavaScript from directly accessing authentication tokens and reduce exposure to token theft through XSS."

---

### Authorization

**Q: Why hide owner controls on the frontend?**

Don't say only:

> "For security."

Say:

> "Frontend hiding improves UX, but it is not a security boundary. I also enforce owner authorization on backend procedures so a buyer cannot bypass the UI and directly call protected APIs."

🔥 **Very important answer.**

---

### Razorpay

**Q: How do you verify a Razorpay payment?**

You should answer:

> "The backend receives the Razorpay order ID, payment ID and signature. It generates the expected HMAC-SHA256 signature using the server-side Razorpay secret and compares it using `crypto.timingSafeEqual`. Only after successful verification do we proceed with order creation."

---

### Idempotency

**Q: How do you prevent duplicate orders?**

> "Before creating the application order, the backend checks whether the Razorpay order ID has already been processed. If it exists, the request is rejected instead of creating another order."

---

### Failure

**Q: What happens if payment fails?**

Explain:

```text
Payment failure
 ↓
No successful verification
 ↓
No duplicate order creation
 ↓
Frontend handles failure
 ↓
User can retry
```

---

# 5. Your Strongest Interview Story

If they ask:

> **"Tell me about a challenging problem you solved."**

Use Razorpay.

### STAR format

**Situation**

> "During payment integration, I identified that repeated payment callbacks or repeated user actions could potentially result in duplicate orders."

**Task**

> "I needed to make the payment flow reliable and secure enough for production."

**Action**

> "I implemented idempotency using the Razorpay order ID, added HMAC-SHA256 signature verification, changed signature comparison to `crypto.timingSafeEqual`, and added frontend payment-in-progress state."

**Result**

> "The payment flow became resistant to duplicate order creation and timing-based signature comparison issues. I verified the implementation with tests and a production build."

That's a **very strong fresher/entry-level DevOps/backend project answer**.

---

# 6. Your Mental Architecture Diagram

This is the one diagram I want you to remember:

```text
                       INTERNET
                           │
                           ▼
                    Cloudflare DNS
                           │
                           ▼
                    EC2 Ubuntu Server
                           │
                           ▼
                    Docker Compose
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
             NGINX                  APP
             :443                   :3000
                │                     │
        ┌───────┴───────┐             │
        │               │             │
      React            /api           │
        │               │             │
        └───────────────┴─────────────┘
                                │
                                ▼
                           Hono/tRPC
                                │
                          Zod + Auth
                                │
                          Drizzle ORM
                                │
                                ▼
                           PostgreSQL
                                │
                                ▼
                          Orders / Data

                         PAYMENT
                            │
                            ▼
                         Razorpay
                            │
                            ▼
                    Signature Verification
                            │
                            ▼
                         Order Create
```

If you can draw this on paper and explain every arrow, **you understand your project**.

---

