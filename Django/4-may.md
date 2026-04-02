Perfect.
This will be your **structured detailed notes** so tomorrow you can continue directly from Terraform without re-explaining everything.

I’m writing this like a technical project log.

---

# 🚀 Django E-Commerce – Production Kubernetes Project Notes

---

# 1️⃣ Cluster Setup (kubeadm Based)

### Infrastructure

* Kubernetes cluster built using **kubeadm**
* 1 Control Plane node
* 2 Worker nodes
* Calico CNI for networking
* NGINX Ingress Controller installed
* metrics-server installed (required for HPA)
* Local-path storage class used

### Why kubeadm?

* Full control over cluster behavior
* Understand scheduling, networking, eviction
* Simulates on-prem production cluster

---

# 2️⃣ Application Containerization

### Repository Structure

Two repositories:

1. `django_ecommerce` → Application repo
2. `django_ecommerce_infra` → Infrastructure (Helm, K8s manifests)

### Docker

* Built production-ready Django image
* Gunicorn used as WSGI server
* Static files collected in container
* Tagged using commit SHA
* Pushed to Docker Hub

Image pattern:

```
sohail28/django-ecommerce:<short-sha>
```

Immutable image strategy used.

---

# 3️⃣ Helm Chart Architecture

Converted raw YAML into structured Helm chart.

### Chart Includes:

* Deployment
* Service
* Ingress
* PersistentVolumeClaim (media)
* PostgreSQL StatefulSet
* Redis Deployment
* HPA
* PodDisruptionBudget
* Secret
* Migration Job

### values.yaml Controls:

* Image repository
* Image tag
* Resource limits
* Environment variables
* Replica count

Helm enables:

* Parameterized deployments
* Rollbacks
* Versioned infrastructure
* Clean GitOps integration

---

# 4️⃣ CI Pipeline (GitHub Actions)

CI Workflow:

1. Checkout code
2. Build Docker image
3. Tag with short commit SHA
4. Push to Docker Hub
5. Clone infra repo
6. Update Helm image tag
7. Commit & push

Result:

* Every commit = new immutable image
* Infra repo updated automatically
* No manual image change

CI is connected to CD via GitOps.

---

# 5️⃣ GitOps with ArgoCD

ArgoCD monitors `django_ecommerce_infra` repo.

When CI updates image tag:

* Argo detects change
* Auto-sync triggers
* Deployment updates
* Rolling update happens

No manual kubectl apply used.

Argo shows:

* Application tree
* ReplicaSets history
* Health status
* Sync history
* Job execution

---

# 6️⃣ Rolling Update Verification

Observed:

* New ReplicaSet created on each image update
* Old ReplicaSet retained (revision history)
* Pods transitioned:

  * Running → Terminating
  * New pods → Ready
* Zero downtime confirmed

Replica revisions tracked:

Rev 1 → Initial
Rev 2 → Fix
Rev 3 → Image update
Rev 4 → Host fix
Rev 5 → Stable
Rev 6+ → Hardened

---

# 7️⃣ Real Production Debugging – ALLOWED_HOSTS Issue

Problem:

* Pods restarting
* Health checks returning HTTP 400
* Argo showed Degraded

Root Cause:

* Django blocked Kubernetes health probes
* Probes use internal Pod IP as Host header
* Hardcoded ALLOWED_HOSTS in prod.py overrode env vars

Fix:

* Removed hardcoded ALLOWED_HOSTS
* Used `env.list("ALLOWED_HOSTS")`
* Passed correct values via Helm
* Added startupProbe

Result:

* No restart loop
* Probes return HTTP 200
* App Healthy

This was real multi-layer debugging.

---

# 8️⃣ Secret Management (Production Improvement)

Moved:

* SECRET_KEY
* DATABASE_URL
* REDIS_URL

From values.yaml → Kubernetes Secret

Created:

```
templates/secret.yaml
```

Used:

```
envFrom:
  - secretRef:
      name: django-secret
```

Now:

* Sensitive values not in Deployment
* Separation of config & secrets
* Cleaner Helm structure

---

# 9️⃣ Migration Job Pattern

Removed migrations from Deployment container.

Old pattern:

```
migrate && collectstatic && gunicorn
```

New pattern:

* Created Kubernetes Job
* Used ArgoCD sync-wave -1
* Job runs before Deployment rollout

Benefits:

* No DB locks during scaling
* Safe rolling updates
* Production-grade execution order

---

# 🔟 HPA (Horizontal Pod Autoscaler)

Created HPA:

* CPU-based scaling
* Min replicas: 1
* Max replicas: 5
* Target utilization: 70%

Verified:

* CPU spike triggered scaling
* Replica count adjusted automatically

metrics-server required and working.

---

# 1️⃣1️⃣ PodDisruptionBudget (PDB)

Created:

```
minAvailable: 1
```

Purpose:

* Prevent full outage during node drain
* Maintain availability during maintenance

Verified via:

```
kubectl get pdb
kubectl describe pdb
```

---

# 1️⃣2️⃣ Startup Probe

Added startupProbe:

```
failureThreshold: 30
periodSeconds: 5
```

Purpose:

* Allow slow boot without premature liveness failure
* Clean container lifecycle
* Prevent CrashLoopBackOff during heavy startup

Verified via `kubectl describe pod`.

---

# 1️⃣3️⃣ Final Architecture

```
GitHub Code Repo
        ↓
GitHub Actions CI
        ↓
Docker Hub (immutable image)
        ↓
Infra Repo updated
        ↓
ArgoCD Auto Sync
        ↓
Helm Chart renders
        ↓
Kubernetes Deployment
        ↓
Rolling Update
        ↓
Healthy Application
```

---

# 1️⃣4️⃣ What You Achieved Technically

You now understand:

* Kubernetes scheduling
* ReplicaSets
* Rolling updates
* Health probes
* Pod lifecycle
* HPA scaling
* GitOps
* Helm templating
* Secret management
* Migration job orchestration
* Production debugging
* Immutable image strategy
* Argo sync waves

This is full production-grade deployment pipeline.

---

# 📌 Where We Stop Today

Cluster state:

* Healthy
* Synced
* HPA working
* PDB active
* Secret injected
* Migration job pattern working
* Replica revisions preserved

No instability.

---

# 🚀 Tomorrow – Terraform Phase

Tomorrow we start:

### Terraform + AWS EKS

We will:

1. Design VPC (public/private subnets)
2. Create EKS cluster
3. Create managed node groups
4. Configure IAM roles
5. Install ArgoCD on EKS
6. Deploy same Helm app
7. Use real LoadBalancer (no NodePort)
8. Enable HTTPS

We will move from self-managed cluster → cloud production architecture.

---

You are not restarting from zero tomorrow.

You are upgrading architecture level.

Rest well.

Tomorrow we move to Infrastructure as Code.
