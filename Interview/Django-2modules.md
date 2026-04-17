🚀 DEVOPS E-COMMERCE PLATFORM — INTERVIEW NOTES (FINAL)

🎤 PROJECT INTRODUCTION (VERY IMPORTANT)

I worked on a DevOps E-Commerce platform using Django, Docker, Kubernetes, Terraform, ArgoCD, and AWS.

The unique part of my project is that I implemented it in two different models:

1. kubeadm on EC2 → to understand Kubernetes internals deeply
2. AWS EKS → to build a production-grade managed Kubernetes architecture

This helped me understand both low-level cluster setup and real-world production deployment.

------------------------------------------------------------

🧱 1) KUBEADM ARCHITECTURE (FOUNDATION)

In the kubeadm setup:

- Terraform provisioned AWS infrastructure:
  - VPC, subnet, security groups, EC2 instances
  - S3 for media storage

- Kubernetes cluster:
  - 1 control plane
  - 2 worker nodes

- Installed:
  - containerd (runtime)
  - kubeadm, kubelet, kubectl
  - Calico (networking)

- Application deployed using:
  - Helm charts
  - ArgoCD (GitOps)

- Exposure:
  - NodePort (for testing)

👉 Key Learning:
This helped me understand how Kubernetes works internally:
control plane, node join, networking, debugging.

------------------------------------------------------------

☁️ 2) EKS ARCHITECTURE (PRODUCTION)

In the EKS setup:

- Terraform provisions:
  - VPC (public + private subnets)
  - EKS cluster + node group
  - IAM roles (IRSA)
  - S3 bucket

- Kubernetes:
  - Managed control plane (AWS)
  - Worker nodes (node group)
  - EBS CSI driver for storage

- Application:
  - Django (Deployment)
  - PostgreSQL (StatefulSet + PVC)
  - Redis (Deployment)

- Networking:
  - AWS ALB (Ingress)
  - Public access via LoadBalancer

👉 Key Difference:
EKS removes control plane management and provides a production-ready environment.

------------------------------------------------------------

⚙️ 3) CI/CD + GITOPS FLOW (MOST IMPORTANT)

Git Push →
GitHub Actions →
Docker Build & Push →
Update GitOps Repo →
ArgoCD Sync →
Kubernetes Deployment →
Application Live 🚀

👉 Git = source of truth
👉 ArgoCD handles deployment automatically

------------------------------------------------------------

📦 4) STORAGE DESIGN

- PostgreSQL → EBS (persistent storage)
- Media files → S3 (object storage)

👉 Used IRSA for secure S3 access (no access keys)

------------------------------------------------------------

🔐 5) SECURITY

- IAM roles for pods (IRSA)
- No hardcoded AWS credentials
- S3 with encryption + versioning

------------------------------------------------------------

🐞 6) REAL PROBLEMS I SOLVED (INTERVIEW GOLD)

1. PVC Pending Issue
→ Fixed using EBS CSI driver

2. CI/CD Failures
→ Docker token expired
→ GitHub PAT issue
→ Fixed pipeline authentication

3. S3 Upload 500 Error
→ Cause: wrong bucket name after AWS account change
→ Fix: updated env variable + IRSA

4. IRSA vs Access Keys Conflict
→ Fixed by removing access keys and using IAM role

5. kubeadm Learning Issues
→ NodePort exposure
→ Migration errors
→ Cluster networking debugging

------------------------------------------------------------

🏁 7) FINAL RESULT

- Fully automated deployment system
- One push → complete deployment
- One destroy → clean infrastructure
- Same app works on both:
  - self-managed Kubernetes (kubeadm)
  - managed Kubernetes (EKS)

------------------------------------------------------------

🎤 PERFECT INTERVIEW ANSWER (2 MIN)

I built a DevOps e-commerce platform using Django, Kubernetes, Terraform, ArgoCD, and GitHub Actions.

The unique part is I implemented it in two models: kubeadm on EC2 to understand Kubernetes internals, and AWS EKS for a production-grade managed setup.

In kubeadm, I manually created the cluster with one control plane and two worker nodes, installed Calico for networking, and exposed the app using NodePort.

In EKS, I used Terraform to provision infrastructure and deployed the app using Helm and ArgoCD with GitOps. The application is exposed via AWS ALB.

I also implemented CI/CD where GitHub Actions builds and pushes Docker images and ArgoCD automatically syncs deployments.

I used EBS for database storage and S3 for media storage using IAM roles.

One key issue I solved was an S3 upload failure caused by incorrect bucket configuration after switching AWS accounts, which I fixed by updating environment variables and IAM role setup.

This project helped me understand both Kubernetes internals and production-level deployment.

------------------------------------------------------------

🔥 KEY IMPRESSION LINE (USE THIS)

“What makes my project strong is that I didn’t just use EKS directly — I first built Kubernetes from scratch using kubeadm, then moved to EKS for production. That gave me both deep understanding and real-world deployment experience.”
