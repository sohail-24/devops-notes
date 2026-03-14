# DevOps Platform Project – Work Summary (Terraform + EKS + ArgoCD + Django)

## Date

Project work completed today on building and fixing a fully automated DevOps platform.

---

# 1. Project Goal

The goal of this project is to build a **production-style DevOps platform** that can:

• Provision infrastructure automatically
• Deploy applications using GitOps
• Run a scalable Kubernetes application
• Destroy infrastructure cleanly without manual steps

The entire infrastructure lifecycle must be controlled by **Terraform**.

---

# 2. Final Architecture

Infrastructure is divided into three layers:

## Layer 1 — Infrastructure (Terraform)

Terraform provisions the AWS infrastructure.

Resources created:

• VPC
• Public Subnets
• Private Subnets
• Internet Gateway
• NAT Gateway
• Route Tables
• EKS Cluster
• Node Group
• IAM Roles and Policies
• OIDC Provider (IRSA)
• S3 Bucket for Django Media Storage

Terraform commands used:

terraform init
terraform plan
terraform apply
terraform destroy

---

## Layer 2 — Kubernetes Platform

After EKS cluster creation, the Kubernetes platform is configured.

Components installed:

AWS Load Balancer Controller
ArgoCD (GitOps tool)

These were installed using **Helm via Terraform**.

Purpose:

• AWS Load Balancer Controller → creates AWS ALB from Kubernetes Ingress
• ArgoCD → manages application deployment from GitHub

---

## Layer 3 — Application Layer

Application deployed is a **Django Ecommerce Application**.

Application stack:

Django Application
PostgreSQL Database (StatefulSet)
Redis Cache
Persistent Volume Claim (PVC)
Horizontal Pod Autoscaler (HPA)
Ingress for external traffic
Service Accounts
Secrets for credentials

Additional Kubernetes resources:

Deployment
ReplicaSet
Pod
Service
Job (django-migrate)
PodDisruptionBudget

---

# 3. GitOps Deployment Flow

Application deployment uses **GitOps with ArgoCD**.

Flow:

Developer pushes code to GitHub
↓
ArgoCD detects Git changes
↓
ArgoCD synchronizes Kubernetes manifests
↓
Kubernetes deploys the application automatically

This removes manual deployment commands.

---

# 4. Infrastructure Automation

The infrastructure lifecycle works as follows.

Create infrastructure:

terraform apply

This creates:

VPC
EKS cluster
Node group
IAM roles
ArgoCD
Load Balancer Controller

Application deployment then happens automatically via ArgoCD.

---

# 5. Major Problem We Faced

Earlier Terraform destroy required manual cleanup.

Problems included:

Manual terraform state rm commands
Manual IAM role deletion
Manual OIDC provider deletion
Manual ALB cleanup
Helm resources blocking Terraform destroy

This caused infrastructure to become inconsistent.

---

# 6. Fix Implemented Today

We refactored Terraform architecture to remove manual steps.

Key fixes:

Moved IAM resources to a dedicated module
Imported existing resources into Terraform state
Fixed dependency ordering between modules
Ensured Helm releases uninstall correctly
Corrected OIDC provider management
Removed duplicate resource definitions

Commands used to fix state issues:

terraform state rm
terraform import

Example:

terraform import module.iam.aws_iam_openid_connect_provider.oidc <OIDC ARN>

After importing resources, Terraform fully controlled the infrastructure.

---

# 7. Successful Terraform Destroy

After fixes we ran:

terraform destroy -auto-approve

Terraform destroyed all resources successfully.

Resources removed automatically:

S3 bucket
IAM roles
OIDC provider
ArgoCD Helm release
AWS Load Balancer Controller
EKS node group
EKS cluster
NAT Gateway
Subnets
Route tables
Internet Gateway
VPC

Final output:

Destroy complete! Resources: 39 destroyed.

Running destroy again shows:

No changes. No objects need to be destroyed.

This confirms Terraform state is clean.

---

# 8. ArgoCD Application Health

Before destroying the cluster the application status was:

Application Health: Healthy
Sync Status: Synced

Running components:

Django Deployment
Redis Deployment
Postgres StatefulSet
Migration Job
Horizontal Pod Autoscaler
Ingress
Services
Secrets
ServiceAccount

This confirmed the GitOps deployment pipeline was working correctly.

---

# 9. Final DevOps Architecture

Developer
↓
GitHub Repository
↓
ArgoCD (GitOps)
↓
Kubernetes (EKS Cluster)
↓
Django Application
↓
Redis + PostgreSQL
↓
AWS Load Balancer
↓
Internet Users

Infrastructure managed by:

Terraform
↓
AWS
• VPC
• EKS
• IAM
• Networking

---

# 10. Key DevOps Concepts Demonstrated

Infrastructure as Code (Terraform)
GitOps Deployment (ArgoCD)
Container Orchestration (Kubernetes)
Horizontal Pod Autoscaling
Persistent Storage (PVC)
Cloud Networking (VPC architecture)
IAM security with IRSA
Infrastructure lifecycle automation

---

# 11. Current Status

Infrastructure: Destroyed successfully
Terraform state: Clean
Application: Previously deployed successfully via GitOps
Automation: Fully working

The platform can now be recreated at any time using:

terraform apply

---

# 12. Next Improvements (Future Work)

Planned improvements for production-level platform:

Terraform Remote State (S3 + DynamoDB)
Domain + TLS using cert-manager
CI pipeline using GitHub Actions
Docker image build and push to ECR
Monitoring stack (Prometheus + Grafana)

---

# End of Work Summary

DevOps Platform built using Terraform + EKS + ArgoCD + Django.
