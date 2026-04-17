🚀 DEVOPS + BACKEND ENGINEERING PROJECT — DJANGO E-COMMERCE PLATFORM

🎤 INTRO (VERY STRONG — USE THIS)

I designed and built a production-grade Django e-commerce backend from scratch and then deployed it using DevOps practices across two Kubernetes environments: a self-managed kubeadm cluster on EC2 and a production-ready AWS EKS setup.

This project helped me understand both application design and infrastructure automation end-to-end.

------------------------------------------------------------

🧠 1. BACKEND ENGINEERING (IMPORTANT — THIS IS YOUR EDGE)

I didn’t use a tutorial project — I built the application myself as a modular monolith.

Key design decisions:

- Used Django 5 with modular architecture (accounts, products, orders, payments)
- Implemented custom user model (production requirement)
- Designed order lifecycle with snapshot-based system
- Built cart system with session + user support
- Prepared payment layer (Stripe-ready)

👉 I followed 12-factor principles:
- environment-based config
- PostgreSQL only (no SQLite)
- stateless design

📌 This is not just a project — it is production-minded backend design :contentReference[oaicite:0]{index=0}

------------------------------------------------------------

🐳 2. CONTAINERIZATION + EC2 DEPLOYMENT

Before Kubernetes, I deployed the app on EC2 using Docker and Nginx.

Architecture:

Internet → Nginx → Gunicorn → Django → PostgreSQL

Key learnings:
- Gunicorn cannot serve static/media
- Nginx handles reverse proxy
- Docker networking uses service names as hostnames

👉 I debugged real issues like Redis misconfiguration causing 500 errors :contentReference[oaicite:1]{index=1}

------------------------------------------------------------

☸️ 3. KUBERNETES (KUBEADM — DEEP LEARNING)

Then I moved to Kubernetes using kubeadm.

Cluster:
- 1 control plane + worker nodes
- Calico CNI
- local-path storage

Workloads:
- Django (Deployment)
- PostgreSQL (StatefulSet + PVC)
- Redis

👉 Major problem I solved:
Media files not loading

Root cause:
Gunicorn cannot serve media

Solution:
Designed NGINX-based architecture to serve media separately

👉 Learned:
- RWO volume limitations
- why reverse proxy is required
- storage behavior in Kubernetes :contentReference[oaicite:2]{index=2}

------------------------------------------------------------

🔄 4. GITOPS + CI/CD (REAL ENGINEERING LEVEL)

I implemented a two-repo GitOps architecture:

Repo 1:
Application code → builds Docker image

Repo 2:
Infrastructure → Kubernetes manifests / Helm

Flow:
Git Push →
GitHub Actions →
Build & Push Image →
Update Infra Repo →
ArgoCD Sync →
Cluster Deployment

👉 This ensures:
- immutable deployments
- Git as source of truth
- automated rollout

------------------------------------------------------------

📦 5. HELM MIGRATION (ADVANCED TOPIC)

I started migrating raw Kubernetes YAML to Helm charts.

- Parameterized image, resources, env
- Implemented liveness/readiness probes
- Debugged Helm YAML indentation issues

👉 Learned real Helm templating challenges

------------------------------------------------------------

☁️ 6. AWS EKS (PRODUCTION SETUP)

Then I implemented the same system on AWS EKS.

- Terraform for infrastructure
- EKS cluster + node group
- IAM roles (IRSA)
- ALB Ingress

Storage:
- PostgreSQL → EBS
- Media → S3

👉 Real issue solved:
S3 upload failing (500 error)

Root cause:
Bucket mismatch after AWS account change

Fix:
Updated environment + IAM role

👉 Also handled:
- IRSA vs access keys conflict
- CI/CD authentication failures

------------------------------------------------------------

🐞 7. REAL PROBLEMS (MY STRONGEST PART)

I solved multiple real-world issues:

- PVC Pending → CSI driver issue
- Media not loading → NGINX design fix
- S3 500 error → bucket mismatch
- Pipeline failures → Docker + Git auth
- Redis misconfiguration → container crash
- Helm YAML parsing errors

👉 These are not tutorial issues — these are real production debugging scenarios

------------------------------------------------------------

🏁 8. FINAL SYSTEM

- Fully automated deployment pipeline
- GitOps-based architecture
- Works on:
  - kubeadm (self-managed)
  - EKS (managed)

One push → deploy entire system  
One destroy → clean infrastructure  

------------------------------------------------------------

🎤 FINAL LINE (VERY POWERFUL)

This project helped me understand not just how to deploy applications, but how to design backend systems, automate infrastructure, and debug real production issues across Kubernetes, AWS, and CI/CD pipelines.
