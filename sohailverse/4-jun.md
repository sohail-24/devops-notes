# SOHAILVERSE PROJECT - MASTER NOTES (04 June 2026)

**Project Name:** SohailVerse
**Owner:** Mohammed Sohail
**Domain:** sohaildevops.site
**Goal:** Build a full-stack movie + travel platform using Cloudflare services with a modern React frontend and serverless backend.

---

# 1. PROJECT ARCHITECTURE

## Frontend

* React
* TypeScript
* React Router
* GSAP Animations
* Responsive UI
* Hosted on Cloudflare Pages

## Backend

* Cloudflare Workers
* REST API

## Database

* Cloudflare D1 (SQLite based serverless database)

## Image Storage

* Cloudflare R2 (Optional)

## Hosting

* Cloudflare Pages

## Domain

* sohaildevops.site

---

# 2. FINAL TARGET ARCHITECTURE

```text
Users
   |
   v
sohaildevops.site
   |
   v
Cloudflare Pages
   |
   v
React Frontend
   |
   v
Cloudflare Worker APIs
   |
   +----------+
   |          |
   v          v
Cloudflare   Cloudflare
D1 DB        R2 Storage
```

---

# 3. CURRENT WEBSITE PAGES

## Home Page

Purpose:

* Landing page
* Hero section
* Introduction to SohailVerse

Features:

* GSAP animations
* Modern UI
* Navigation menu

---

## Movies Page

Purpose:

* Display movie collection

Future Features:

* Movie cards
* Search movies
* Categories
* Movie details

---

## Movie Detail Page

Purpose:

* Show individual movie information

Future Features:

* Movie poster
* Description
* Rating
* Trailer link
* Genres

---

## Travel Page

Purpose:

* Travel experiences

Future Features:

* Country pages
* Travel gallery
* Travel blogs

---

# 4. TECHNOLOGY STACK DECISION

We finalized:

### Frontend

```text
React + TypeScript
```

Reason:

* Industry standard
* Easy deployment
* Fast development

---

### Backend

```text
Cloudflare Workers
```

Reason:

* No server management
* Fast
* Cheap
* Scalable

---

### Database

```text
Cloudflare D1
```

Reason:

* Serverless
* Managed by Cloudflare
* Works directly with Workers

---

### Storage

```text
Cloudflare R2
```

Purpose:

* Movie posters
* Travel images

Currently:

* Optional
* Can be added later

---

# 5. PROBLEMS WE SOLVED TODAY

---

## Problem 1

### Website Not Loading Properly

Symptoms:

* Site was not rendering correctly
* React routing issues suspected

Investigation:

* Checked React routes
* Verified page structure

Files involved:

```tsx
src/App.tsx
```

Routes found:

```tsx
HomePage
MoviesPage
MovieDetailPage
TravelPage
```

Result:

* Routing structure verified

---

## Problem 2

### Frontend Deployment Validation

We confirmed:

* React application builds correctly
* Pages load correctly
* Navigation working

Result:

✅ Website operational

---

## Problem 3

### Architecture Planning

Before:

No finalized architecture.

After:

Finalized stack:

```text
React
Cloudflare Pages
Cloudflare Workers
Cloudflare D1
Cloudflare R2
```

---

## Problem 4

### Future Scalability Concerns

Decision:

Avoid:

* EC2
* Complex Kubernetes
* Docker deployment

For this project.

Reason:

Cloudflare stack is:

* Simpler
* Faster
* Lower maintenance
* Good portfolio project

---

# 6. WHAT IS WORKING NOW

Current Status:

### Frontend

✅ React application

✅ Routing

✅ Pages loading

✅ Domain connected

✅ Website accessible

---

### Domain

✅ sohaildevops.site working

---

### Cloudflare

✅ Hosting setup functioning

---

# 7. DATABASE PLAN

Future D1 Tables

---

## Movies Table

```sql
movies
```

Fields:

```text
id
title
description
poster_url
release_year
genre
rating
created_at
```

---

## Travel Table

```sql
travel_posts
```

Fields:

```text
id
country
city
description
image_url
visit_date
created_at
```

---

## Users Table

```sql
users
```

Fields:

```text
id
name
email
role
created_at
```

---

# 8. WORKER API PLAN

Future APIs

---

## Movies

```text
GET /api/movies
```

Get all movies

---

```text
GET /api/movies/:id
```

Get movie details

---

```text
POST /api/movies
```

Add movie

---

```text
DELETE /api/movies/:id
```

Delete movie

---

## Travel

```text
GET /api/travel
```

Get travel posts

---

```text
POST /api/travel
```

Create travel post

---

# 9. R2 STORAGE PLAN

Purpose:

Store:

* Movie posters
* Travel photos

Example:

```text
movie-posters/
travel-images/
```

Workflow:

```text
Upload Image
      |
      v
Cloudflare R2
      |
      v
Store URL in D1
      |
      v
Display in React
```

---

# 10. DEPLOYMENT FLOW

```text
GitHub Push
      |
      v
Cloudflare Pages
      |
      v
Automatic Build
      |
      v
Production Deployment
```

---

# 11. WHY THIS PROJECT IS GOOD FOR DEVOPS PORTFOLIO

Shows:

### Frontend Skills

* React
* TypeScript
* Routing

---

### Cloud Skills

* Cloudflare Pages
* Cloudflare Workers
* D1
* R2

---

### DevOps Skills

* Git
* GitHub
* CI/CD
* DNS
* Domain Management
* Cloud Hosting

---

### Full Stack Skills

* Frontend
* Backend
* Database
* Storage

---

# 12. TOMORROW'S PLAN

## Phase 1

Backend Setup

Tasks:

```text
Create Cloudflare Worker
Create API Routes
Test API
Connect Frontend
```

---

## Phase 2

D1 Database

Tasks:

```text
Create D1 Database
Create Tables
Connect Worker
Insert Sample Data
```

---

## Phase 3

Movies Module

Tasks:

```text
Movie Listing
Movie Detail Page
Fetch From API
Dynamic Rendering
```

---

## Phase 4

Travel Module

Tasks:

```text
Travel Posts
Travel Detail Page
Images
API Integration
```

---

## Phase 5

Admin Features

Tasks:

```text
Add Movie
Delete Movie
Add Travel Post
Manage Content
```

---

# PROJECT STATUS SUMMARY

```text
Project Name:
SohailVerse

Frontend:
✅ React + TypeScript

Backend:
⏳ Cloudflare Workers

Database:
⏳ Cloudflare D1

Storage:
⏳ Cloudflare R2

Hosting:
✅ Cloudflare Pages

Domain:
✅ sohaildevops.site

Routing:
✅ Working

Website:
✅ Working

Next Step:
Create Cloudflare Worker API
```

### Interview Explanation (2-Minute Version)

> "SohailVerse is my full-stack portfolio project built using React, Cloudflare Pages, Cloudflare Workers, and Cloudflare D1. The frontend is developed with React and TypeScript and deployed on Cloudflare Pages. The backend is planned using Cloudflare Workers for serverless APIs, while Cloudflare D1 will store movie and travel data. The domain is sohaildevops.site. Through this project I am demonstrating frontend development, backend API development, cloud hosting, DNS management, CI/CD using GitHub, and serverless architecture on Cloudflare."
