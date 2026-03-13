# DevOps Project Notes – Django E-commerce on AWS EKS (GitOps)

Author: Mohammed Sohail
Project: Production-style Django E-commerce Platform
Stack: Terraform + AWS EKS + Helm + ArgoCD + GitHub Actions + DockerHub

---

# 1. Project Goal

Build a **production-grade Kubernetes deployment** for a Django e-commerce application using modern DevOps practices:

* Infrastructure as Code (Terraform)
* GitOps (ArgoCD)
* CI/CD (GitHub Actions)
* Containerization (Docker)
* Kubernetes orchestration (EKS)
* Cloud storage (S3 – next step)

---

# 2. Current Architecture (After Today)

System architecture now:

AWS ALB
↓
Kubernetes Ingress
↓
Service (django)
↓
Django Deployment
↓
Pods

Additional services:

Django
├── PostgreSQL (StatefulSet + EBS volume)
└── Redis (Deployment)

---

# 3. Infrastructure Layer (Terraform)

Repository:
terraform-eks-platform

Terraform created:

VPC

* CIDR: 10.0.0.0/16

Subnets

* public-1
* public-2
* private-1
* private-2

Networking

* Internet Gateway
* NAT Gateway
* Route tables

EKS Cluster

* Name: aws_eks-eks
* Version: 1.35

Node Group

* Instance: t3.micro
* Desired nodes: 15
* Min: 5
* Max: 16

IAM Roles

* EKS cluster role
* Node role
* OIDC provider

ALB Controller

* Installed using Helm
* IRSA configured

---

# 4. Application CI/CD Pipeline

Repository: django_ecommerce

CI/CD Tool: GitHub Actions

Workflow:
.github/workflows/ci.yml

Pipeline steps:

1. Checkout code
2. Setup Docker Buildx
3. Login to DockerHub
4. Build Docker image
5. Tag image using commit SHA
6. Push image to DockerHub
7. Update Helm values.yaml in infra repo
8. Push commit → triggers ArgoCD deployment

Docker image example:

sohail28/django-ecommerce:abc1234
sohail28/django-ecommerce:latest

---

# 5. GitOps Deployment (ArgoCD)

Repository:
django_ecommerce_infra

Helm Chart Structure:

charts/django-ecommerce/

Contains:

Chart.yaml
values.yaml

templates/

deployment.yaml
ingress.yaml
postgres.yaml
redis.yaml
migration-job.yaml
hpa.yaml
pdb.yaml
secret.yaml

---

# 6. Important Fix Done Today

Originally architecture used:

Django
↓
EBS volume (RWO)
↓
nginx media server

Problem:

EBS StorageClass = RWO (ReadWriteOnce)

Meaning:
Only ONE pod can attach the volume.

Error seen:

Multi-Attach error for volume

So nginx-media pod was stuck in:

ContainerCreating

---

# 7. Solution Implemented

We removed the entire nginx + PVC architecture.

Deleted files:

templates/nginx.yaml
templates/pvc.yaml

Removed from deployment:

volumeMounts
volumes
persistentVolumeClaim

Updated ingress:

Old:

backend:
service:
name: nginx-media

New:

backend:
service:
name: django

---

# 8. ArgoCD GitOps Behavior

After pushing changes:

git add .
git commit
git push

ArgoCD performed:

Pruned resources:

nginx-media deployment
nginx-media service
nginx-media configmap
django-media-pvc

Current status:

Application Health: Progressing
Sync Status: OutOfSync → Syncing

Reason:

PVC still deleting.

Message:

waiting for deletion of PersistentVolumeClaim django-media-pvc

This is normal because AWS must detach the EBS volume first.

---

# 9. Current Kubernetes State

Pods running:

django
postgres
redis

Job completed:

django-migrate

PVC:

postgres-storage-postgres-0 → Bound
django-media-pvc → Terminating

---

# 10. Current System Architecture

Final architecture today:

ALB
↓
Ingress
↓
Service (django)
↓
Django Pod

Django
├── PostgreSQL StatefulSet
└── Redis

No nginx.

No EBS media volume.

---

# 11. Why This Change Is Important

Old architecture problems:

EBS volume cannot attach to multiple pods
Scaling issues
Multi-attach errors

New architecture benefits:

Simpler design
Better scaling
Production ready

Next step will introduce **S3 for media storage**.

---

# 12. Next Architecture (Tomorrow)

Tomorrow we implement:

Django
↓
AWS S3 (media storage)

Final architecture will become:

ALB
↓
Ingress
↓
Django
↓
S3

Benefits:

Unlimited storage
Highly scalable
No multi-attach issues
Industry standard architecture

---

# 13. Tomorrow's Work Plan

We will create a Terraform module.

Folder structure:

terraform-eks-platform

modules/

s3/

main.tf
variables.tf
outputs.tf

---

# 14. What the S3 Module Will Do

Create S3 bucket for media files.

Example:

sohail-django-media-bucket

Terraform will create:

S3 bucket
Bucket policy
Versioning
Public access configuration

Later we will also add:

IAM role for Django pods
IRSA configuration
django-storages integration

---

# 15. Future Improvements After S3

Planned improvements:

1. CloudFront CDN for media
2. HTTPS using ACM
3. Production settings.py
4. Logging and monitoring
5. Prometheus + Grafana
6. Loki log aggregation
7. Argo Rollouts (blue/green deployment)
8. KEDA autoscaling

---

# 16. Final Status of Project Today

Infrastructure: Completed
EKS Cluster: Running
GitOps: Working
CI/CD: Working
Application: Running
Architecture: Cleaned

Next step:

S3 Media Storage

---

# END OF NOTES
