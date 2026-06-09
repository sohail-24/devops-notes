# SOHAILVERSE - PROJECT NOTES

# DATE: 09 June 2026

# STATUS: SUCCESSFUL WORK SESSION

==================================================
PROJECT OVERVIEW
================

Goal:
Build SohailVerse as a real cloud-powered personal platform using:

* React + TypeScript Frontend
* Cloudflare Workers API
* Cloudflare D1 Database
* Cloudflare Hosting
* Personal Domain Integration (future)

Architecture:

React Frontend
↓
Cloudflare Worker API
↓
Cloudflare D1 Database

==================================================
FRONTEND WORK COMPLETED
=======================

1. Dashboard Page

Created Mission Control Dashboard.

Features:

* Mission Status Card
* Progress Percentage (72%)
* Progress Bar
* Active Missions
* Current Focus
* Universe Metrics
* Future Mission Section
* System Status Section

Status:
COMPLETED

---

2. Cinema Page

Originally:
Hardcoded movie data.

Converted to:
Database-driven page.

Added:

useState()
useEffect()
fetch()

API:

https://sohailverse-api.sohailkhan88008.workers.dev/api/movies

Movies loaded from D1 Database:

* Interstellar
* John Wick
* Top Gun Maverick

Issue faced:

CORS Error

Solution:

Added CORS headers in Worker.

Status:
COMPLETED

---

3. Timeline Page

Originally:
Hardcoded events array.

Converted to:
Database-driven page.

Added:

useState()
useEffect()
fetch()

API:

https://sohailverse-api.sohailkhan88008.workers.dev/api/travel

Travel data loaded from D1 Database.

Current Data:

Saudi Arabia

* Riyadh
* A journey that expanded my perspective and confidence

India

* Hyderabad
* My hometown and starting point of my journey

Status:
COMPLETED

==================================================
CLOUDFLARE WORK COMPLETED
=========================

Worker Name:

sohailverse-api

Status:
WORKING

---

Worker Endpoints

1.

GET /api/health

Returns:

{
"status": "online",
"project": "SohailVerse",
"version": "1.0"
}

---

2.

GET /api/movies

Returns movie data from D1.

Status:
WORKING

---

3.

GET /api/travel

Returns travel data from D1.

Status:
WORKING

==================================================
D1 DATABASE WORK COMPLETED
==========================

Database Name:

sohailverse-db

Status:
CONNECTED TO WORKER

Binding Name:

DB

Status:
WORKING

==================================================
MOVIES TABLE
============

Table:

movies

Columns:

* id
* title
* genre
* rating

Current Data:

1. Interstellar
   Genre: Sci-Fi
   Rating: 9.0

2. John Wick
   Genre: Action
   Rating: 8.5

3. Top Gun Maverick
   Genre: Action
   Rating: 8.8

Status:
WORKING

==================================================
TRAVEL TABLE
============

Table:

travel_posts

Columns:

* id
* country
* city
* description

Current Data:

1.

Country: Saudi Arabia
City: Riyadh

Description:
A journey that expanded my perspective and confidence

2.

Country: India
City: Hyderabad

Description:
My hometown and starting point of my journey

Status:
WORKING

==================================================
IMPORTANT ISSUE FIXES
=====================

Issue 1

Cinema page showed nothing.

Reason:

CORS blocked frontend requests.

Solution:

Added:

Access-Control-Allow-Origin

headers inside Worker.

---

Issue 2

Timeline page became white.

Reason:

useState() and useEffect() were outside component.

Wrong:

const [travels, setTravels] = useState([]);

Correct:

export default function TimelinePage() {

const [travels, setTravels] = useState([]);

}

Status:
FIXED

==================================================
CURRENT WORKING APIS
====================

Health:

https://sohailverse-api.sohailkhan88008.workers.dev/api/health

Movies:

https://sohailverse-api.sohailkhan88008.workers.dev/api/movies

Travel:

https://sohailverse-api.sohailkhan88008.workers.dev/api/travel

==================================================
CURRENT PROJECT STATUS
======================

Dashboard
COMPLETED

Timeline
CONNECTED TO D1

Cinema
CONNECTED TO D1

Cloudflare Worker
WORKING

Cloudflare D1
WORKING

API Layer
WORKING

React Fetch
WORKING

Database Connectivity
WORKING

==================================================
NEXT SESSION PLAN
=================

STEP 1

Convert Academy Page to D1 Database.

Create:

academy_posts

Store:

* AWS
* Linux
* Docker
* Git
* Kubernetes
* Cloudflare
* DevOps Learning Notes

==================================================

STEP 2

Create API:

/api/academy

==================================================

STEP 3

Connect Academy Page

Academy Page
↓
Worker API
↓
D1 Database

==================================================

STEP 4 (BIG UPGRADE)

Create Admin Dashboard.

Features:

* Add Movie
* Add Travel Post
* Add Academy Skill

Forms write directly to D1 Database.

This turns SohailVerse into a mini CMS.

==================================================

# LONG TERM VISION

SohailVerse V2

Frontend:
React + TypeScript

Backend:
Cloudflare Workers

Database:
Cloudflare D1

Storage:
Cloudflare R2 (future)

Authentication:
Future

Admin Panel:
Future

Custom Domain:
sohaildevops.site

Goal:

A personal cloud platform that showcases:

* Travel
* Learning
* Movies
* DevOps Journey
* Projects
* Portfolio
* Cloud Engineering Skills

==================================================
END OF NOTES
============
