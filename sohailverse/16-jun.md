# SohailVerse v2 - Project Notes

## Project Overview

SohailVerse is my personal digital ecosystem built with:

* React + TypeScript
* Cloudflare Pages
* Cloudflare Workers
* Cloudflare D1 Database
* Custom CMS (Admin Panel)
* Dynamic APIs

Goal:

Build a fully dynamic personal platform where all content is managed through Admin CMS and stored in D1.

---

# Current Architecture

Frontend:

* Mission Control
* Atlas
* Cinema
* Academy
* DevOps
* Timeline
* Dashboard
* Admin

Backend:

Cloudflare Worker API

Database:

Cloudflare D1

---

# Database Tables

## movies

Used by:

* Cinema Page

Fields:

* id
* title
* genre
* rating

API:

* GET /api/movies
* POST /api/movies
* DELETE /api/movies/:id

---

## academy_posts

Used by:

* Academy Page

Fields:

* id
* skill
* category
* level

API:

* GET /api/academy
* POST /api/academy
* DELETE /api/academy/:id

---

## devops_posts

Used by:

* DevOps Page

Fields:

* id
* title
* category
* description

API:

* GET /api/devops
* POST /api/devops
* DELETE /api/devops/:id

---

## timeline_posts

Used by:

* Timeline Page

Fields:

* id
* title
* category
* description

API:

* GET /api/timeline
* POST /api/timeline
* DELETE /api/timeline/:id

---

## atlas_posts

Used by:

* Atlas Page

Fields:

* id
* country
* status
* year
* highlight

API:

* GET /api/atlas
* POST /api/atlas
* DELETE /api/atlas/:id

---

# Travel System Status

Old system:

travel_posts

Fields:

* country
* city
* description

Reason removed:

Atlas became a better replacement.

Travel data was duplicated.

Travel page no longer exists.

Current decision:

Travel Manager removed from Admin.

Travel API removed from Worker.

Travel table may remain in D1 as backup.

Do not build future features on travel_posts.

Use atlas_posts instead.

---

# Admin CMS Status

Current CMS Modules:

1. Movie Manager
2. Academy Manager
3. DevOps Manager
4. Timeline Manager
5. Atlas Manager

Removed:

* Travel Manager

Admin is now aligned with actual website pages.

---

# Worker Status

Worker routes active:

* /api/health
* /api/movies
* /api/academy
* /api/devops
* /api/timeline
* /api/atlas

Removed:

* /api/travel

---

# Atlas System

Status: Dynamic

Atlas page should load from:

GET /api/atlas

Admin writes to:

POST /api/atlas

Admin deletes from:

DELETE /api/atlas/:id

Atlas is now source of truth for:

* Visited countries
* Planned countries
* Travel milestones
* Future destinations

---

# Timeline System

Status: Dynamic

Timeline page should load from:

GET /api/timeline

Admin controls all timeline entries.

No hardcoded timeline events should remain.

---

# Immediate Next Tasks

## Priority 1

Convert Atlas page fully dynamic.

Current:

Hardcoded countries.

Target:

Fetch from /api/atlas.

---

## Priority 2

Convert Timeline page fully dynamic.

Current:

Partially hardcoded.

Target:

Fetch from /api/timeline.

---

## Priority 3

Dashboard

Build statistics page:

* Movies count
* Skills count
* DevOps projects count
* Timeline events count
* Countries count

---

## Priority 4

Authentication

Current:

Password stored in frontend.

Problem:

Visible in source code.

Target:

Move authentication to Worker.

Create secure login system.

---

## Priority 5

Admin Refactor

Create reusable CMS component:

CMSManager

Use for:

* Movies
* Academy
* DevOps
* Timeline
* Atlas

This will reduce Admin.tsx size significantly.

---

# Future Vision

SohailVerse v3

Add:

* Blog CMS
* Certifications CMS
* Resume CMS
* Achievement System
* Public API
* Analytics Dashboard
* User Authentication
* Dark/Light Theme Toggle
* Search Engine

Goal:

Turn SohailVerse into a complete personal operating system.
