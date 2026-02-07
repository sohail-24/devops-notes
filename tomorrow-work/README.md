# 🚀 GitHub Dashboard – Production & CI/CD Notes (Checkpoint)

## 1️⃣ Why we created the **github-dashboard** repo (very important)

This repo is **NOT just a UI project**.

It is a **DevOps flagship project** used to demonstrate:

* Real backend (FastAPI)
* Real frontend (React + Vite + Nginx)
* Docker & Docker Compose
* Internal container networking
* Environment-based configuration
* GitHub Actions CI
* Docker Hub image registry
* Release-based workflows (tags)
* Production thinking (no hardcoded IPs)

👉 **Purpose**:
To show **how a real application moves from code → image → deployment**, not just how a webpage looks.

---

## 2️⃣ Architecture we finalized (current state)

### 🔹 Runtime Architecture (Docker)

* **Frontend**

  * React + Vite
  * Built once, served by **Nginx**
  * Calls backend using internal DNS: `http://backend:8000`

* **Backend**

  * FastAPI
  * Exposes `/health`, `/version`, `/github/repos`
  * Uses GitHub public API
  * No frontend IP dependency

* **Docker Compose**

  * Creates an **internal Docker network**
  * Services talk via service names:

    * frontend → backend:8000
  * Only frontend exposes port `80` to public

This is **production-correct design**.

---

## 3️⃣ Why we stopped using public IPs inside code

Earlier:

* Frontend → `http://<AWS_PUBLIC_IP>:8000`
* Backend CORS → public IP

Problems:

* Breaks when IP changes
* Not portable
* Not cloud-native
* Not Kubernetes-ready

Now:

* Frontend → `http://backend:8000`
* Backend CORS → domain / localhost / nginx

✅ This works in:

* Docker
* Docker Compose
* CI
* Kubernetes
* Any cloud

---

## 4️⃣ docker-compose strategy (important concept)

We intentionally moved to:

```yaml
services:
  backend:
    build: ./backend

  frontend:
    build: ./frontend
```

### Why?

* GitHub = **source of truth**
* Anyone can clone repo and run:

  ```
  docker-compose up --build
  ```
* No dependency on local images
* CI and local environments behave the same

This is **professional DevOps practice**.

---

## 5️⃣ CI (Continuous Integration) – what we implemented

### ✅ Backend GitHub Actions

* Trigger: Git tag (`vX.Y.Z`)
* Steps:

  * Checkout code
  * Login to Docker Hub
  * Build backend image
  * Tag image with version + `latest`
  * Push to Docker Hub

### ✅ Frontend GitHub Actions

* Same logic
* Builds Nginx-based frontend image
* Pushes versioned image

### 🔐 Secrets used

* `DOCKERHUB_USERNAME`
* `DOCKERHUB_TOKEN`

Stored securely in:

```
Repo → Settings → Actions → Secrets
```

---

## 6️⃣ What CI is doing vs what CD is NOT doing (yet)

### CI (DONE ✅)

* Build images
* Push images
* Version control via tags
* Reproducible builds

### CD (NOT done yet ❌)

* Auto deploy to AWS
* Auto restart containers
* Kubernetes rollout
* ArgoCD sync

👉 This is **intentional**.
We are stopping at the **correct checkpoint**.

---

## 7️⃣ Why GitHub “does not show graphs or UI”

GitHub UI only shows:

* Code
* Commits
* Actions
* Packages

It does **NOT** run your frontend.

To show UI:

* App must be deployed (AWS / K8s / Pages)
* Or linked from README / Portfolio

So **github-dashboard repo is backend infrastructure proof**, not a hosted site by default.

---

## 8️⃣ Why this repo is VERY valuable for interviews

You can confidently say:

> “I built a full-stack app and designed the complete CI pipeline using GitHub Actions, Docker, versioned releases, and production-grade networking. The same setup is Kubernetes-ready.”

This repo proves:

* Docker
* CI/CD
* Cloud readiness
* DevOps mindset

---

## 9️⃣ Important decision made about Codex / AI tools

* ❌ We will NOT dump everything (k8s, ansible, argocd) at once
* ❌ No “magic auto-generated mega repo”

Why?

* Recruiters want **clear evolution**
* Tools must be introduced **step by step**
* Each layer must be explainable

We will **extend this repo gradually**, not replace it.

---

## 🔜 10️⃣ Where we STOPPED & where we will CONTINUE

### We STOPPED at:

* CI complete (backend + frontend)
* docker-compose stable
* Clean GitHub repo
* Images building correctly

### We will CONTINUE from:

➡️ **CD phase**

Next steps (future):

1. Auto deploy on AWS via SSH OR Ansible
2. Convert docker-compose → Kubernetes manifests
3. Introduce ArgoCD (GitOps)
4. Make this repo truly “production-grade”

---

## 🧠 Mentor Final Summary

* This repo is **NOT useless**
* It is a **foundation**
* CI is DONE
* Architecture is CORRECT
* Next is **GitOps & Kubernetes**

👉 **Tomorrow we start directly from CD / Kubernetes without repeating anything.**

---

✅ Correct way (conceptually, not a prompt)

You should use Codex in stages, like this:

Give repo link

Ask it to ONLY add Kubernetes manifests

Review

Then ask for ArgoCD GitOps

Review

Then ask for Ansible for infra

Review
