# 📒 DevOps Mentor Notes — Terraform EKS + ArgoCD GitOps Platform

## 1️⃣ Project Goal

Build a **Production-Style GitOps Platform** on AWS using:

Terraform → AWS Infrastructure → EKS → IRSA → AWS Load Balancer Controller → ArgoCD → GitOps Deployments.

Goal Architecture:

Terraform
↓
AWS VPC (Public + Private Subnets)
↓
NAT Gateway + Internet Gateway
↓
EKS Cluster
↓
EKS Node Group (EC2 worker nodes)
↓
IRSA (IAM Roles for Service Accounts)
↓
AWS Load Balancer Controller
↓
ArgoCD installed via Helm (Terraform)
↓
Internet-facing AWS Network Load Balancer
↓
ArgoCD UI accessible from browser

---

# 2️⃣ Infrastructure Created by Terraform

Terraform created the following AWS resources automatically:

### VPC Infrastructure

* VPC (10.0.0.0/16)
* Public Subnet 1 (10.0.1.0/24)
* Public Subnet 2 (10.0.2.0/24)
* Private Subnet 1 (10.0.3.0/24)
* Private Subnet 2 (10.0.4.0/24)

### Internet Connectivity

* Internet Gateway
* NAT Gateway
* Elastic IP for NAT

### Routing

Public Route Table
→ Internet Gateway

Private Route Table
→ NAT Gateway

---

# 3️⃣ Kubernetes Infrastructure

Terraform created:

### EKS Cluster

Cluster name:
devops-platform-eks

Region:
ap-south-1

Version:
Kubernetes 1.35

Cluster Endpoint:
Public access enabled

---

### Node Group

Node group:
devops-platform-eks-nodes

Instance type:
t3.micro

Scaling:

min = 2
desired = 3 → later increased to 5
max = 8

Disk size:
20GB

---

# 4️⃣ IAM Roles Created

Terraform created IAM roles required by EKS.

### EKS Cluster Role

Policy attached:

AmazonEKSClusterPolicy

Allows EKS control plane to manage cluster.

---

### Node Group Role

Policies attached:

AmazonEKSWorkerNodePolicy
AmazonEKS_CNI_Policy
AmazonEC2ContainerRegistryReadOnly

Allows worker nodes to:

* run pods
* access container images
* manage networking

---

# 5️⃣ IRSA (IAM Role for Service Accounts)

IRSA allows Kubernetes pods to access AWS services securely.

Steps Terraform performed:

1. Created OIDC provider for EKS
2. Created IAM role
3. Allowed Kubernetes service account to assume that role

Service Account used:

aws-load-balancer-controller
namespace = kube-system

Role:

alb-controller-role

This allows pods to create:

* Load Balancers
* Target Groups
* Security Groups

---

# 6️⃣ AWS Load Balancer Controller

Installed using Terraform Helm provider.

Helm Chart:

aws-load-balancer-controller

Repository:

https://aws.github.io/eks-charts

Purpose:

Allows Kubernetes Services or Ingress to automatically create AWS Load Balancers.

Example flow:

Kubernetes Service
↓
AWS Load Balancer Controller
↓
AWS LoadBalancer created automatically

---

# 7️⃣ ArgoCD Installation (GitOps Tool)

Installed using Helm via Terraform.

Helm Chart:

argo-cd

Repository:

https://argoproj.github.io/argo-helm

Namespace created:

argocd

Command equivalent:

helm install argocd argo-cd

---

# 8️⃣ ArgoCD Configuration

To reduce resource usage on free tier nodes:

Disabled heavy components:

dex.enabled = false
notifications.enabled = false
applicationset.enabled = false

Service exposed using:

server.service.type = LoadBalancer

---

# 9️⃣ Fixing LoadBalancer Problem

Initially LoadBalancer was created as:

Internal NLB

So browser could not access it.

Solution:

Added service annotations.

Terraform Helm configuration:

server.service.annotations.service.beta.kubernetes.io/aws-load-balancer-scheme = internet-facing

server.service.annotations.service.beta.kubernetes.io/aws-load-balancer-type = nlb

Result:

Public AWS Network Load Balancer created.

---

# 🔟 Verifying ArgoCD Deployment

Check pods:

kubectl get pods -n argocd

Expected:

argocd-application-controller Running
argocd-server Running
argocd-repo-server Running
argocd-redis Running

---

Check service:

kubectl get svc -n argocd

Expected:

argocd-server
TYPE = LoadBalancer

Example:

k8s-argocd-argocdse-xxxxx.elb.ap-south-1.amazonaws.com

---

Check DNS:

nslookup <elb-url>

Should return public AWS IPs.

Example:

13.205.xxx.xxx
3.6.xxx.xxx

---

Verify using curl:

curl -vk https://<elb-url>

Expected:

HTTP/1.1 200 OK

Response contains HTML for ArgoCD UI.

---

# 1️⃣1️⃣ ArgoCD Login

URL:

https://<elb-url>

Username:

admin

Password command:

kubectl -n argocd get secret argocd-initial-admin-secret 
-o jsonpath="{.data.password}" | base64 -d

---

# 1️⃣2️⃣ Terraform Destroy

Used to delete infrastructure and avoid AWS billing.

Command:

terraform destroy

Terraform deletes:

VPC
Subnets
Internet Gateway
NAT Gateway
Route Tables
EKS Cluster
Node Group
IAM Roles
OIDC Provider
AWS Load Balancer Controller
ArgoCD
LoadBalancer

Destroy plan example:

Plan: 0 to add, 0 to change, 32 to destroy

---

# 1️⃣3️⃣ DevOps Infrastructure Lifecycle

Typical workflow:

terraform apply
test infrastructure
practice deployments
terraform destroy

Infrastructure is recreated anytime using:

terraform apply

---

# 1️⃣4️⃣ What Happens Tomorrow

When running:

terraform apply

Terraform will recreate automatically:

VPC
Subnets
NAT Gateway
EKS cluster
Node group
IAM roles
IRSA
AWS Load Balancer Controller
ArgoCD
LoadBalancer

No manual steps required.

---

# 1️⃣5️⃣ Next Step (Tomorrow)

Next tasks:

Login to ArgoCD

Connect GitHub repo

Create ArgoCD Application

Deploy Django application using GitOps.

Flow will be:

GitHub Repo
↓
ArgoCD watches repo
↓
ArgoCD syncs Kubernetes manifests
↓
Application deployed automatically

---

# 1️⃣6️⃣ Skills Practiced

Terraform Infrastructure as Code
AWS Networking
EKS Cluster Deployment
Kubernetes Node Groups
IAM Roles and Policies
IRSA (IAM Roles for Service Accounts)
Helm Deployment using Terraform
AWS Load Balancer Controller
ArgoCD GitOps Platform
LoadBalancer Networking Debugging
Infrastructure Lifecycle Management

