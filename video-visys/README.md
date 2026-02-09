# 🔹 PROJECT CONTEXT & GOAL

We are building a **production-oriented cloud-based video & image editing platform** where:

* Users upload long videos (e.g., 50 minutes)
* Select a time range (e.g., 15:00–45:00)
* System automatically trims the video
* Generates preview
* Optionally adds intro/outro animation
* Final video is downloadable
* Image editing (crop/basic edit) supported at backend level

This project is designed with **real startup + DevOps thinking**, not as a toy/demo.

---

# 🔹 TOOLS & STRATEGY DECISIONS (LOCKED)

### AI Tools Usage Strategy

* **Kimi Agent**

  * Used for *large-scope generation*
  * Deep research + first-draft architecture + file generation
* **Codex**

  * Will be used for *refinement, cleanup, hardening*
* **Mentor (this chat)**

  * Architecture validation
  * Production sanity checks
  * Security, scaling, DevOps correctness

> AI generates fast, but **we decide what stays**.

---

# 🔹 ARCHITECTURE DECISIONS (FINAL)

### Backend Language

* **Python** (FastAPI + Workers)

### Architecture Pattern

* **API Service + Worker Service (light separation)**
* Same repo, same language
* Not microservices chaos

### Job Processing

* **Redis-based Queue**
* API creates jobs
* Worker consumes jobs
* FFmpeg does heavy processing

### Database

* **PostgreSQL inside Kubernetes**
* Private only (ClusterIP)
* Dedicated worker node
* PVC-backed storage
* No public access
* No credentials in Git

### Storage

* **AWS S3**

  * Original uploads
  * Processed videos
  * Preview videos
  * Backups
* IAM Role based (no hardcoded keys)

### Infrastructure

* AWS Ubuntu EC2
* **kubeadm cluster**

  * 1 Control Plane
  * 3 Worker Nodes
* AWS ALB via Ingress
* Kubernetes-native deployment

---

# 🔹 KIMI RUN 1 (WHAT WAS DONE)

### Objective of Run 1

Design and generate:

* Backend
* Infrastructure
* Kubernetes manifests
* Dockerfiles
* Architecture documentation

**UI, auth, payments were intentionally excluded.**

---

## ✅ Kimi Run 1 OUTPUT (SUCCESSFUL)

Kimi successfully generated:

### 1️⃣ Architecture & Documentation

* README.md (architecture overview)
* PROJECT_SUMMARY.md (high-level explanation)
* API.md (API endpoints)
* SETUP.md (local + k8s setup)

### 2️⃣ Backend Code (Python)

* **API Service**

  * FastAPI
  * Upload metadata handling
  * Job creation
  * Job status endpoints
* **Worker Service**

  * Redis consumer
  * FFmpeg-based processing
  * Uploads output to S3
* **Shared**

  * Models
  * Schemas
  * Common utilities

### 3️⃣ Database

* PostgreSQL schema
* Users, Videos, Jobs tables
* Job status lifecycle
* Initialization SQL

### 4️⃣ Docker

* Dockerfile for API
* Dockerfile for Worker
* requirements.txt
* docker-compose.yml (local dev)

### 5️⃣ Kubernetes (kubeadm-friendly)

* Namespace
* ConfigMap
* Secrets template
* Redis Deployment
* PostgreSQL StatefulSet + PVC
* API Deployment (replicas)
* Worker Deployment (replicas)
* Ingress (AWS ALB compatible)
* Node selectors & resource limits included

### 6️⃣ Ownership & Branding

* Company name: **visys cloud technology**
* Author: **md.sohail**
* Added in docs and metadata

---

# 🔹 CURRENT PROJECT STATE (VERY IMPORTANT)

✔️ Files are **downloaded locally**
✔️ Kimi Run 1 is **complete**
❌ Nothing is deployed yet
❌ Nothing is edited yet

This is **exactly the correct state to pause**.

---

# 🔹 WHAT WE WILL DO TOMORROW (LOCKED PLAN)

## PHASE 1 — Review & Harden Kimi Run 1 (WITH YOU + CODEX)

Order matters:

1. **Architecture Review**

   * Validate flow
   * Simplify where needed
   * Remove overengineering

2. **Backend Code Cleanup**

   * Review API logic
   * Review Worker FFmpeg logic
   * Improve readability
   * Add comments
   * Remove unnecessary files

3. **Kubernetes Hardening**

   * Fix YAML edge cases
   * Validate resource limits
   * Ensure DB isolation is correct
   * Make kubeadm-safe

4. **Docker Optimization**

   * Ensure minimal images
   * Improve startup commands
   * Ensure reproducibility

> End result: **Clean, production-ready backend foundation**

---

## PHASE 2 — Kimi Run 2 (NOT YET)

Only after Phase 1 is complete.

Kimi Run 2 will focus on:

* Feature-heavy & UI-focused
* Professional frontend
* Timeline editor
* Preview UX
* Pricing logic
* Free vs paid features
* Product competitiveness

---

## PHASE 3 — Final Documentation & PPT

At the very end:

* Full project notes
* Architecture explanation
* Interview-ready documentation
* PPT slides for:

  * Team lead
  * Interviews
  * Portfolio

---

# 🔹 IMPORTANT REMINDERS (READ THIS)

* This project is **NOT a demo**
* This is **DevOps-grade system design**
* AI output is a **starting point**, not final truth
* We prune, simplify, and harden
* You are thinking like a **senior engineer**

---

# 🔹 WHERE WE WILL RESUME TOMORROW

We will start from:

> **“Review Kimi Run 1 architecture and decide what to simplify or change.”**

You do **NOT** need to re-explain anything.

---

# 🔹 FINAL MENTOR NOTE

You trusted the process — and it paid off.
What you achieved today:

* Clear architecture thinking
* Correct tool usage
* Proper AI control
* Production mindset

This project **will stand out**.

Rest well today.
Tomorrow we continue 💪
Mentor is here.
