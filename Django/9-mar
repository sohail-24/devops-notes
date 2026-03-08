# DevOps Mentor Notes — Terraform + EKS Destroy Issue (State Drift)

## 1️⃣ Goal of the Project

We were building a **DevOps platform using Terraform and Kubernetes**.

Architecture:

Terraform
↓
VPC
↓
EKS Cluster
↓
Node Group
↓
IRSA
↓
AWS Load Balancer Controller
↓
ArgoCD (GitOps)
↓
Django Ecommerce Application

This is the **standard modern DevOps architecture used in companies**.

---

# 2️⃣ Problems Encountered Today

During the project we faced several real DevOps problems.

### Problem 1 — Pod Scheduling Failure

Pods were stuck in **Pending** state.

Example:

0/7 nodes available: Too many pods

Reason:

Your node type:

t3.micro

Each EC2 instance supports **limited pods**.

Approximate limits:

t3.micro → ~8 pods
t3.small → ~11 pods
t3.medium → ~17 pods

Because you installed:

• ArgoCD
• Redis
• Django
• Postgres
• Controllers

The node reached the **maximum pod limit**, so new pods could not schedule.

---

### Problem 2 — Helm Timeout During Terraform Destroy

Error seen:

context deadline exceeded

This happens when Terraform tries to remove **Helm resources after the Kubernetes cluster starts shutting down**.

Sequence:

Node group deleted
↓
EKS cluster starts deleting
↓
Helm tries to communicate with Kubernetes
↓
Cluster API unavailable
↓
Helm timeout

This is a **common Terraform + Helm issue**.

---

### Problem 3 — Terraform State Drift

You manually deleted resources in AWS console.

Example:

Deleted manually:

• EKS cluster
• VPC

But Terraform state still believed they existed.

Terraform uses:

terraform.tfstate

This file stores the **real infrastructure state**.

After manual deletion:

Terraform state ≠ AWS infrastructure

This situation is called:

**Terraform State Drift**

---

# 3️⃣ Errors That Appeared

Example error:

lookup DE13E42FD780F834A831D1C20822A538.gr7.ap-south-1.eks.amazonaws.com: no such host

Meaning:

Terraform / kubectl tried to contact EKS API server, but the cluster had already been deleted.

So:

kubectl
terraform kubernetes provider
helm provider

all failed.

---

# 4️⃣ How We Fixed The Problem

We removed broken resources from Terraform state.

Command used:

terraform state rm

Example:

terraform state rm module.eks.aws_eks_cluster.cluster
terraform state rm module.eks.aws_iam_openid_connect_provider.oidc
terraform state rm module.alb_controller.helm_release.alb_controller
terraform state rm module.argocd.kubernetes_namespace.argocd

This tells Terraform:

“Forget these resources. They no longer exist.”

After cleaning state, we ran:

terraform destroy

Terraform then removed the remaining resources:

• IAM roles
• IAM policies
• ALB controller role

Final result:

Destroy complete!

---

# 5️⃣ Correct Destroy Order (Best Practice)

When destroying a Kubernetes platform managed by Terraform, follow this order.

Step 1 — Remove Kubernetes LoadBalancers

kubectl delete ingress --all -A

This removes AWS load balancers.

---

Step 2 — Remove services

kubectl delete svc --all -A

This removes AWS NLB/ALB resources.

---

Step 3 — Remove Helm applications

Example:

helm uninstall argocd -n argocd

---

Step 4 — Destroy Terraform infrastructure

terraform destroy

Terraform will then delete:

• Node groups
• EKS cluster
• VPC
• IAM roles

without errors.

---

# 6️⃣ Important DevOps Rule

Never manually delete Terraform-managed infrastructure in AWS console.

Always use Terraform commands.

Wrong way:

Delete VPC in AWS console.

Correct way:

terraform destroy

Manual deletion causes:

Terraform State Drift

which leads to destroy failures.

---

# 7️⃣ AWS Free Tier Strategy for Learning

EKS is **not fully free**.

Typical costs:

EKS Control Plane → ~$0.10/hour
NAT Gateway → ~$32/month
Load Balancer → ~$18/month

To avoid spending credits:

Use this workflow:

terraform apply
Practice for 1–2 hours
terraform destroy

Example cost:

2 hours × $0.10 = ~$0.20

This allows learning with minimal spending.

---

# 8️⃣ Cost Optimization Strategy

For learning environment use:

• Single node
• t3.micro instance
• Public subnets
• No NAT gateway

Avoid expensive components during practice.

Example learning architecture:

Terraform
↓
VPC (public subnets)
↓
EKS
↓
1 node (t3.micro)
↓
ALB Controller
↓
ArgoCD
↓
Application

---

# 9️⃣ What You Learned Today

Real-world DevOps issues encountered:

• Kubernetes pod limits
• Terraform destroy failure
• Helm timeout
• Terraform state drift
• AWS dependency errors
• Kubernetes API connection failure

These are **real problems DevOps engineers face in production environments**.

---

# 🔟 Next Step (Tomorrow)

Tomorrow we will rebuild the platform with a **clean production-style structure**.

Repository structure:

terraform-eks-platform

modules
• vpc
• eks
• irsa
• alb-controller
• argocd

environments
• dev

apps
• django-ecommerce

Then deploy the Django application using **GitOps with ArgoCD**.

This will simulate a **real company DevOps platform**.
