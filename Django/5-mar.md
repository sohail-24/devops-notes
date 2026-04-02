# Terraform EKS Project – Work Notes (Day Progress)

Author: Mohammed Sohail
Project: Terraform EKS Kubernetes Infrastructure
Domain: sohaildevops.site
Region: ap-south-1 (Mumbai)
Cluster Name: django-eks-cluster

---

# 1. Project Goal

Build a **Production-style Kubernetes infrastructure on AWS using Terraform** and deploy applications using Kubernetes + AWS Load Balancer Controller.

Architecture target:

Internet
↓
AWS Application Load Balancer (ALB)
↓
Kubernetes Ingress
↓
Kubernetes Service
↓
Pods
↓
Worker Nodes (EC2) in Private Subnets
↓
EKS Cluster (Control Plane Managed by AWS)

---

# 2. Terraform Infrastructure Created

Project directory:

terraform-eks-project

Structure:

terraform-eks-project/
│
├── main.tf
├── variables.tf
├── terraform.tfvars
├── outputs.tf
├── providers.tf
├── terraform.tfstate
├── terraform.tfstate.backup
│
├── environments/
│
└── modules/
│
├── vpc/
│
└── eks/

---

# 3. VPC Infrastructure Created via Terraform

Components deployed:

VPC

Public Subnets
Used for:
• Load Balancer

Private Subnets
Used for:
• Kubernetes Worker Nodes

Internet Gateway

NAT Gateway

Route Tables

Public Route Table → Internet Gateway

Private Route Table → NAT Gateway

---

# 4. EKS Cluster Created via Terraform

Cluster name:

django-eks-cluster

Region:

ap-south-1

Kubernetes version:

1.35

Worker nodes:

2 nodes

Instance type:

t3.micro

Node group name:

django-eks-cluster-nodes

---

# 5. Verified Kubernetes Access

Command:

kubectl get namespaces

Result:

default
kube-system
kube-public
kube-node-lease

Cluster is working correctly.

---

# 6. Verified Cluster Services

Command:

kubectl get svc -A

Services running:

kubernetes
kube-dns
eks-extension-metrics-api

Cluster networking working properly.

---

# 7. Helm Installed

Command:

helm version

Result:

Helm v4.1.0

Helm will be used to install Kubernetes controllers.

---

# 8. Verified EKS OIDC Provider

Command:

aws eks describe-cluster 
--name django-eks-cluster 
--query "cluster.identity.oidc.issuer" 
--output text

Output:

https://oidc.eks.ap-south-1.amazonaws.com/id/xxxxxxxx

Purpose:

OIDC allows Kubernetes Service Accounts to assume IAM roles.

This is required for:

• AWS Load Balancer Controller
• Cluster Autoscaler
• EBS CSI Driver
• External DNS

This mechanism is called:

IRSA (IAM Roles for Service Accounts)

---

# 9. Created IAM Policy for ALB Controller

Downloaded IAM policy:

curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json

Created policy:

aws iam create-policy 
--policy-name AWSLoadBalancerControllerIAMPolicy 
--policy-document file://iam_policy.json

Policy ARN:

arn:aws:iam::111376855660:policy/AWSLoadBalancerControllerIAMPolicy

---

# 10. OIDC Provider Attached to Cluster

Command:

eksctl utils associate-iam-oidc-provider 
--region ap-south-1 
--cluster django-eks-cluster 
--approve

Result:

OIDC provider successfully created.

---

# 11. Created IAM Service Account

Command:

eksctl create iamserviceaccount 
--cluster=django-eks-cluster 
--namespace=kube-system 
--name=aws-load-balancer-controller 
--role-name AmazonEKSLoadBalancerControllerRole 
--attach-policy-arn arn:aws:iam::111376855660:policy/AWSLoadBalancerControllerIAMPolicy 
--approve

Result:

Service account created:

kube-system/aws-load-balancer-controller

IAM role attached successfully.

---

# 12. Installed AWS Load Balancer Controller

Helm repository added:

helm repo add eks https://aws.github.io/eks-charts

Repository updated:

helm repo update

Controller installed:

helm install aws-load-balancer-controller eks/aws-load-balancer-controller 
-n kube-system 
--set clusterName=django-eks-cluster 
--set serviceAccount.create=false 
--set serviceAccount.name=aws-load-balancer-controller

Purpose:

Allows Kubernetes to automatically create AWS ALB.

---

# 13. Verified EKS Cluster Status (AWS Console)

Cluster health:

Healthy

Node health issues:

0

Nodes running:

2 nodes

Instance type:

t3.micro

Node status:

Ready

---

# 14. Current Status of Project

Working components:

Terraform
VPC
Private Subnets
Public Subnets
NAT Gateway
EKS Cluster
Worker Nodes
kubectl access
Helm installed
IAM roles configured
AWS Load Balancer Controller installed

---

# 15. AWS Load Balancer Page

Currently:

0 Load Balancers

Reason:

No Kubernetes Ingress has been created yet.

ALB will appear automatically when Ingress is deployed.

---

# 16. Tomorrow's Work Plan

Next steps:

1. Verify AWS Load Balancer Controller Pods

Command:

kubectl get pods -n kube-system

Expected:

aws-load-balancer-controller running

---

2. Tag Subnets for ALB Controller

ALB Controller needs subnet tags.

Public subnets:

kubernetes.io/role/elb = 1

Private subnets:

kubernetes.io/role/internal-elb = 1

---

3. Deploy Test Application

Create:

Deployment

Example:

nginx deployment

---

4. Create Kubernetes Service

Service type:

ClusterIP

Purpose:

Expose pods inside cluster.

---

5. Create Kubernetes Ingress

Ingress will trigger:

AWS Load Balancer Controller

which automatically creates:

Application Load Balancer

---

6. Verify AWS ALB Creation

Check in AWS Console:

EC2 → Load Balancers

Expected result:

New ALB automatically created.

---

# 17. Final Architecture After Tomorrow

Internet
↓
AWS ALB
↓
Kubernetes Ingress
↓
Service
↓
Pods
↓
EC2 Worker Nodes (Private Subnets)

---

# 18. GitHub Project

Repository contains:

Terraform infrastructure
EKS cluster configuration
Future Kubernetes manifests

Used for:

Infrastructure as Code (IaC)

---

# End of Notes
