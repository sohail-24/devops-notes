🔥 **MENTOR NOTES — KUBERNETES MIGRATION DAY (Django E-commerce → K8s)**
Author: Mohammed Sohail
Cluster: kubeadm (1 control-plane + workers)
CNI: Calico
Storage: local-path-provisioner
Status: 🚧 Media not served (expected) → Fix tomorrow with NGINX Ingress

---

# 📌 WHAT WE COMPLETED TODAY

---

# 1️⃣ Docker → Kubernetes Migration

You moved from:

EC2 + Docker Compose + Nginx
⬇
Kubernetes (kubeadm cluster)

This is a MAJOR step.

---

# 2️⃣ Image Build & Registry

You:

✔ Built image → `sohail28/django-ecommerce:k8s-v8`
✔ Pushed to Docker Hub
✔ Updated deployment image
✔ Rolling restart successful

This confirms:

* Image pipeline working
* Registry integration working
* Cluster pulling images correctly

---

# 3️⃣ Namespace Setup

Created:

```
namespace: ecommerce
```

All workloads isolated properly.

Good production habit.

---

# 4️⃣ Redis Deployment

✔ Redis deployed
✔ Running stable
✔ Service working
✔ Django connected via:

```
REDIS_URL=redis://redis:6379/0
```

Networking inside cluster works.

---

# 5️⃣ PostgreSQL StatefulSet

✔ Installed local-path storage
✔ PVC created
✔ StatefulSet running
✔ Service working
✔ DB connected via:

```
postgres://postgres:postgres@postgres:5432/django_ecommerce
```

Important learning:

* PVC Pending until StorageClass installed
* WaitForFirstConsumer behavior
* RWO limitations

Excellent debugging today.

---

# 6️⃣ Django Deployment

Final working version:

```yaml
replicas: 1
```

Why 1?
Because:

```
ReadWriteOnce volume (RWO)
```

Cannot mount to multiple pods.

You correctly reduced replicas.

✔ Resource limits added
✔ Gunicorn running
✔ collectstatic working
✔ migrate running on startup
✔ ClusterIP service working

---

# 7️⃣ Media Storage (BIG LEARNING)

You:

✔ Created `django-media-pvc`
✔ Mounted at `/app/media`
✔ Verified volume works
✔ Verified file persistence
✔ Created test.txt
✔ Uploaded images

BUT…

---

# 8️⃣ WHY MEDIA STILL NOT WORKING

Root cause:

```
Gunicorn does NOT serve media files.
```

Django `static()` helper works only with:

```
runserver
```

Not with:

```
gunicorn
```

So your request:

```
/media/products/2026/03/black.jpeg
```

Returns 404.

Because:

Gunicorn only serves WSGI app.
Not filesystem static content.

---

# 🧠 IMPORTANT ARCHITECTURE UNDERSTANDING

Right now:

User
↓
Ingress
↓
Django (Gunicorn)
↓
Django app

There is NO static file server in front.

Production architecture requires:

User
↓
Ingress (NGINX)
↓
NGINX handles:
/static
/media
↓
Proxy other requests to Django

This is how real production works.

---

# 🚧 CURRENT ISSUE SUMMARY

| Component    | Status           |
| ------------ | ---------------- |
| Django       | ✅ Working        |
| Redis        | ✅ Working        |
| Postgres     | ✅ Working        |
| PVC          | ✅ Bound          |
| Media Files  | ❌ Not served     |
| Static Files | ✅ via WhiteNoise |
| Ingress      | Installed        |
| ArgoCD       | Not yet          |

---

# 🔥 WHAT WE FIX TOMORROW

You chose:

> ✅ Use NGINX Ingress to serve /media

Good choice. Production mindset.

---

# 🚀 TOMORROW PLAN (CLEAR EXECUTION PATH)

---

## Step 1 — Modify Ingress

We will:

* Keep django service as backend
* Configure NGINX to serve `/media` from volume

But Ingress alone cannot access pod filesystem.

So we need:

---

## Step 2 — Proper Production Setup

Two options:

### Option A (Learning Mode – Simple)

Run separate NGINX deployment:

* Mount same PVC
* Serve /media directly
* Proxy / to Django

### Option B (Cleaner Architecture)

Use:

* NGINX Ingress
* Django only app logic
* External object storage (S3)

Since you're learning Kubernetes infra:

We will do Option A.

---

# 📌 WHAT WE WILL CREATE TOMORROW

1. nginx-deployment.yaml
2. nginx-service.yaml
3. Update ingress.yaml

NGINX config:

```
location /media/ {
    alias /app/media/;
}
location / {
    proxy_pass http://django;
}
```

---

# 🧠 CONCEPT YOU LEARNED TODAY (VERY IMPORTANT)

### 1️⃣ RWO Volume Limitation

Scaling with file storage requires:

* RWX storage
* Or S3
* Or NFS
* Or separate file server

---

### 2️⃣ Gunicorn vs Runserver

| Server    | Static | Media |
| --------- | ------ | ----- |
| runserver | Yes    | Yes   |
| gunicorn  | No     | No    |
| nginx     | Yes    | Yes   |

---

### 3️⃣ Why Production Needs Reverse Proxy

App servers should NOT serve static files.

That is NGINX job.

---

### 4️⃣ Pod OOM (Exit Code 137)

You experienced:

```
CrashLoopBackOff
```

Learned:

* Always set resource limits.

---

# 🏗 CURRENT ARCHITECTURE

Cluster
│
├── Django Deployment (1 replica)
│
├── Postgres StatefulSet
│
├── Redis Deployment
│
├── Media PVC (local-path)
│
├── Ingress Controller (NGINX)
│
└── ClusterIP Services

This is already production-like architecture.

---

# 🎯 TOMORROW OBJECTIVES

1️⃣ Fix media with NGINX deployment
2️⃣ Clean up Postgres extra PVC (postgres-pvc pending)
3️⃣ Confirm domain routing works
4️⃣ Make architecture production-grade
5️⃣ Move to ArgoCD GitOps

---

# 🚀 AFTER MEDIA FIX

We move to:

### ArgoCD

Flow will become:

GitHub → ArgoCD → Cluster auto deploy

You push code → cluster updates.

That is real DevOps.

---

# 🏆 WHERE YOU STAND NOW

You are no longer learning Docker.

You are:

Building a real Kubernetes production stack.

Most beginners never reach this level.

---

# 📍 TOMORROW START POINT

We start directly with:

👉 Create NGINX deployment to serve media
👉 Update ingress
👉 Test with curl
👉 Confirm browser loads images

Then:

🔥 ArgoCD installation.

---

Rest now.

Tomorrow we complete infra layer.

Mentor proud today.
