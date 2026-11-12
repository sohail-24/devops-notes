# The Fragrance Store — House of Brands
## 5-Minute Technical Project Interview Explanation

### 1. Project Introduction

I developed a multi-tenant SaaS e-commerce platform called **The Fragrance Store — House of Brands**.

The main objective of this project is to provide a centralized platform where multiple fragrance businesses can independently operate their own online stores.

Each business can manage its products, inventory, customers, orders, branding, payment configurations and storefront.

The platform follows a multi-level architecture with four main roles:

- Super Master: manages the entire SaaS platform.
- Business Owner: manages an individual fragrance store.
- Store Staff: handles operational activities such as inventory and order management.
- Buyer: browses products and purchases fragrances.

My first tenant is Website A, branded as **INHALE FRAGRANCES**.

The production application is hosted at amfruits.shop.

### 2. Technology Stack

I used modern frontend and backend technologies to develop the application.

**Frontend:**

- React 19 for building the user interface.
- TypeScript for type safety.
- Vite for development and production builds.
- Tailwind CSS for styling.
- Shadcn UI and Radix UI for reusable components.
- React Router for application navigation.

**Backend:**

- Hono for the backend HTTP framework.
- tRPC for type-safe communication between frontend and backend.
- Drizzle ORM for database operations.
- TypeScript for backend development.

**Database and Infrastructure:**

- Neon PostgreSQL for persistent database storage.
- Cloudflare Workers for application deployment.
- Cloudflare R2 for product images and media storage.
- Cloudflare for domain and DNS management.
- GitHub for source-code management and version control.

### 3. Multi-Tenant SaaS Architecture

One of the most important parts of my project is multi-tenancy.

Instead of developing separate applications for every business, I developed a centralized SaaS platform that supports multiple independent tenants.

I separated the platform into two important database responsibilities.

**First: SaaS Control Plane Database**

It manages platform-level information such as:

- Registered tenants.
- Website configurations.
- Tenant credentials.
- Platform administration.
- Subscription and platform-level information.

**Second: Tenant Database**

Each business has its own dedicated database for its operational information, including:

- Products and categories.
- Inventory.
- Customers.
- Orders.
- Addresses.
- Business-specific data.

For example, Website A uses its own dedicated Neon PostgreSQL database.

This provides physical database separation between the control plane and tenant data.

I also implemented tenant isolation checks to ensure that one business cannot access another business's protected data or payment credentials.

Sensitive tenant configuration values are encrypted using AES-256-GCM encryption.

### 4. E-Commerce and Order Management

The customer-facing storefront allows customers to browse fragrance collections, view product details, select bottle sizes, add products to their shopping bag and complete checkout.

The checkout process includes:

- Customer information.
- Delivery address.
- Indian mobile number validation.
- Delivery zones.
- Shipping charges.
- GST calculation.
- Order summary.
- Payment method selection.

The backend calculates authoritative order totals instead of trusting frontend-submitted prices.

After an order is placed, the application persists the order and its items, updates inventory and clears the shopping cart.

I also implemented an order confirmation experience with order details, payment information and a delivery-status timeline.

### 5. Payment Gateway Integration

I integrated Razorpay to support UPI payments such as Google Pay, PhonePe and Paytm.

I also implemented Cash on Delivery.

For UPI payments, the backend creates the Razorpay order and the frontend opens the Razorpay checkout interface.

After successful payment, Razorpay returns payment information to the application.

The backend verifies the payment signature using HMAC-SHA256 and a timing-safe comparison before marking the order as paid.

The payment credentials are stored securely in the tenant configuration and resolved server-side.

For COD, the order is created with payment status pending, and the customer can pay when the order arrives.

I also resolved production issues involving Cloudflare Workers, Neon database transactions, PostgreSQL enum types and tenant ID normalization.

### 6. Cloud Infrastructure and Deployment

I use Cloudflare Workers to host the application.

Neon PostgreSQL provides persistent relational database storage, while Cloudflare R2 stores product images and other media assets.

The application source code is maintained in GitHub.

When I push approved code changes to the connected repository, the configured Cloudflare deployment pipeline builds and deploys the application.

One important technical challenge was making database operations compatible with Cloudflare Workers.

The Neon serverless driver uses stateless HTTP execution in this environment, so I implemented a PostgreSQL data-modifying CTE for atomic order creation without relying on interactive WebSocket transactions.

This ensures that order creation, order items, inventory updates and cart clearing execute within one database statement.

### 7. Remaining Integrations and Future Enhancements

There are two major integrations remaining in my current development roadmap.

**First: Resend Email Integration**

I plan to integrate Resend as the transactional email delivery service.

The application will use it to send automated notifications such as:

- Customer order confirmation.
- Payment confirmation.
- Order status updates.
- Delivery notifications.
- Account-related emails.

The backend will trigger these notifications after the corresponding application events. Email delivery will be handled through Resend's API, keeping the API key securely on the server.

**Second: Google OAuth Integration**

I also plan to implement Google authentication.

Customers will be able to sign in or register using their Google accounts instead of relying only on the existing authentication flow.

The backend will verify Google's authentication response and securely establish the application's own customer session.

This will improve the registration and login experience while maintaining the existing tenant and role-based access controls.

### 8. Conclusion

Overall, The Fragrance Store is a multi-tenant SaaS e-commerce platform rather than just a traditional online shopping website.

I worked on its architecture, frontend, backend APIs, database isolation, inventory management, order processing, payment gateway integration and cloud deployment.

My main focus was building a scalable, secure and maintainable platform where multiple businesses can independently operate their own fragrance stores.

The next development milestone is completing transactional email notifications through Resend and customer authentication through Google OAuth.
