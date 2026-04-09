Perfect — **that means local Terraform is your stable control plane now**, not GitHub Actions.

That is actually the **right decision for your current stage** because your infra has:

* EKS
* ALB
* IRSA
* ArgoCD
* EBS CSI
* S3 backend
* destroy dependencies

And this setup is **too state-sensitive** to blindly trust CI/CD until cleanup logic is fully mature.

So below are your **full detailed mentor notes for today** — written so next time you can just paste this and continue.

---

# 📘 DEVOPS NOTES — TODAY FULL SUMMARY

## Project: `terraform-eks-platform`

## Goal: Production-style AWS EKS infra using Terraform + S3 backend + GitHub Actions + ArgoCD

---

# 1) 🎯 WHAT WE ACHIEVED TODAY

Today we moved your project from:

```text
"basic terraform + one workflow"
```

to:

```text
"real infra lifecycle with remote state, deploy workflow, destroy workflow, and local recovery strategy"
```

That is a **big DevOps upgrade**.

---

# 2) ✅ BIG DECISION WE MADE

## We decided:

# 👉 **Terraform execution should work from LOCAL first**

and

# 👉 **GitHub Actions should be secondary / automation layer**

This was the correct call.

### Why?

Because your project contains resources that are very sensitive during create/destroy:

* EKS cluster
* EKS node group
* Auto Scaling Group
* Launch templates
* OIDC provider
* ALB controller
* ArgoCD
* S3 backend
* DynamoDB lock table
* Kubernetes cleanup hooks

If any one of these gets partially created/deleted, GitHub Actions can leave you in a broken “half-managed” state.

So your new safe strategy is:

```text
LOCAL = source of recovery / truth
GITHUB ACTIONS = automation layer
```

👉 This is actually how many engineers debug real infra.

---

# 3) ✅ S3 BACKEND WAS ADDED (VERY IMPORTANT)

You correctly understood that:

> before running Terraform in CI/CD, we must use remote backend

So we added:

## `backend.tf`

```hcl
terraform {
  backend "s3" {
    bucket         = "sohail-terraform-state-2026-001"
    key            = "terraform-eks-platform/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
```

---

## Why this is important

Without backend:

* `terraform.tfstate` stays only local
* GitHub runner cannot know your infra state
* destroy/apply becomes unsafe
* team collaboration becomes impossible

With backend:

* Terraform state is stored in **S3**
* state locking is handled by **DynamoDB**
* local + GitHub can use same state safely

👉 This is **industry standard**.

---

# 4) ✅ YOU CREATED BACKEND INFRA CORRECTLY

You used the correct AWS CLI commands:

## S3 bucket

```bash
aws s3 mb s3://sohail-terraform-state-2026-001 --region ap-south-1
```

## DynamoDB lock table

```bash
aws dynamodb create-table \
--table-name terraform-lock \
--attribute-definitions AttributeName=LockID,AttributeType=S \
--key-schema AttributeName=LockID,KeyType=HASH \
--billing-mode PAY_PER_REQUEST
```

---

## Important learning

You asked:

> “mentor, why so many commands? in kubeadm we used only this”

### Answer:

Because **those two commands are enough** to create backend infra.

What created complexity was **not backend creation**.

The complexity came from:

* stale locks
* partial destroy
* GitHub runner failure
* AWS resource dependencies
* EKS node group timing

So backend setup itself was simple.
The hard part was **infra lifecycle management**.

---

# 5) ✅ OLD `infra.yml` WAS REMOVED (GOOD DECISION)

You had this old file:

```yaml
.github/workflows/infra.yml
```

It was too simple and risky because it did:

* terraform init
* terraform apply
* kubeconfig
* ArgoCD install
* app deploy

all in one straight line **without enough protection**.

---

## Problems with old `infra.yml`

### ❌ No concurrency control

Could allow multiple runs to fight over state.

### ❌ No proper plan/apply discipline

Too easy to break infra.

### ❌ No wait handling

EKS and node groups need time.

### ❌ No cleanup intelligence

Destroy path would fail often.

### ❌ Not production-safe for EKS lifecycle

So removing it was correct.

---

# 6) ✅ WE SPLIT WORKFLOWS INTO TWO CLEAN FILES

Now your repo uses:

```text
.github/workflows/deploy.yml
.github/workflows/destroy.yml
```

This is much cleaner and more production-style.

---

# 7) ✅ GITHUB AUTH ISSUE WAS SOLVED

You got this error:

```text
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed
```

---

## Root cause

GitHub **does not allow password-based push anymore**.

So for pushing code from local machine, you need:

* Personal Access Token (PAT), or
* SSH auth

---

## Important learning

You asked:

> “do I need to add Git token in GitHub Actions secrets?”

### Correct answer:

# ❌ NO — not for normal repo checkout

Because inside GitHub Actions:

```yaml
uses: actions/checkout@v4
```

already uses GitHub’s built-in token.

So:

## You need PAT only for:

* local machine `git push`
* manual Git auth from terminal

## You do NOT need PAT for:

* normal GitHub Actions checkout
* Terraform AWS access
* AWS infra provisioning

---

# 8) ✅ AWS SECRETS LOGIC BECAME CLEAR

You correctly understood that GitHub Actions needs:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

because GitHub runner has **no access to your local AWS login**.

---

## This was the correct setup

In repo secrets:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

Optional:

* `AWS_REGION`

---

## Important learning

### GitHub Actions needs AWS creds because:

it must talk to AWS APIs.

### GitHub Actions does NOT need Git PAT because:

it already has built-in GitHub auth for repo checkout.

That distinction is very important.

---

# 9) ✅ EKS MODULE WAS UPGRADED

Today you significantly improved:

```text
modules/eks/main.tf
modules/eks/variables.tf
root main.tf
```

This was one of the most important technical improvements of the day.

---

# 10) ✅ WE ADDED NODE CONFIGURATION PROPERLY

You wanted kubeadm-style control like this:

```hcl
root_block_device {
  volume_size = 20
}
```

And you were absolutely right to want the same control for EKS nodes.

So we added node-level config through variables:

## In `modules/eks/variables.tf`

```hcl
variable "node_instance_type" {
  description = "EC2 instance type for EKS worker nodes"
  type        = string
  default     = "t2.medium"
}

variable "desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "node_disk_size" {
  description = "Disk size (GB) for EKS worker nodes"
  type        = number
  default     = 20
}
```

---

# 11) ✅ ROOT `main.tf` NOW OVERRIDES NODE SETTINGS

You configured:

```hcl
module "eks" {
  source = "./modules/eks"

  cluster_name       = "${var.project_name}-eks"
  vpc_id             = module.vpc.vpc_id
  private_subnets    = module.vpc.private_subnets
  node_instance_type = "t2.medium"
  desired_size       = 4
  node_disk_size     = 20

  depends_on = [
    module.vpc
  ]
}
```

---

## Why values appear in “two places”

You asked:

> “why are we using this in two different places?”

Example:

```hcl
node_instance_type = "t2.medium"
desired_size       = 2
node_disk_size     = 20
```

### Correct explanation:

## In `variables.tf`

These are **default values**.

## In root `main.tf`

These are **actual chosen values for this environment**.

So:

```text
variables.tf = fallback/defaults
main.tf      = real deployment choice
```

This is correct Terraform design.

---

# 12) ✅ INSTANCE TYPE WAS CORRECTED TO `t2.medium`

You noticed that AWS console was showing `t2.medium` and not the earlier suggested type.

So you standardized on:

```hcl
node_instance_type = "t2.medium"
```

That was a practical and correct choice for your account/region behavior.

---

# 13) ✅ NODE COUNT WAS INCREASED FROM 2 → 4

You checked this file:

```hcl
variable "desired_size" {
  default = 2
}
```

and asked whether it should be 4.

### Final answer:

Yes, for your current test + workload structure, using:

```hcl
desired_size = 4
```

in root `main.tf` was reasonable.

---

## Result

AWS console showed:

* Desired size = 4
* Min size = 2
* Max size = 6

That confirmed your node group config was applying.

---

# 14) ❌ BIG PROBLEM WE FACED: NODE GROUP “CREATING” / LOOP ISSUE

This was one of the most important debugging sessions.

You saw:

* node group stuck in **Creating**
* Auto Scaling Group weird behavior
* one EC2 instance staying alive
* repeated node group conflicts
* launch template issues
* stale AWS infra during recreate/destroy

---

## Root cause

Your EKS node group configuration was too complex / too fragile when using:

* custom launch template
* custom AMI lookup
* AWS-managed node group lifecycle
* repeated destroy/apply during failures

This caused AWS lifecycle mismatch.

---

## Real-world lesson

> EKS Managed Node Groups do NOT like over-engineered launch template setups unless really needed.

That’s why today’s best decision was:

# 👉 simplify EKS node group

This was exactly the right DevOps call.

---

# 15) ✅ WE MOVED TOWARD SIMPLER, SAFER NODE GROUP DESIGN

Instead of heavy launch-template based node creation, the better approach is:

```hcl
resource "aws_eks_node_group" "nodes" {
  instance_types = [var.node_instance_type]
  disk_size      = var.node_disk_size
  ami_type       = "AL2_x86_64"
}
```

This is much safer than overcomplicating launch templates for your current project stage.

---

## Why this is better

### Safer create

AWS manages the worker AMI lifecycle.

### Safer destroy

Fewer dangling launch template dependencies.

### Cleaner Terraform

Less infra drift.

### Better for beginners + portfolio

Looks production-clean without unnecessary risk.

---

# 16) ✅ SSM POLICY WAS ADDED TO NODE ROLE

You added:

```hcl
resource "aws_iam_role_policy_attachment" "node_ssm_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
```

---

## Why this is useful

This gives you future flexibility for:

* node debugging
* Systems Manager access
* better ops troubleshooting

That is a **good real-world addition**.

---

# 17) ❌ BIG PROBLEM WE FACED: TERRAFORM STATE LOCK

This was your main blocker for a while.

You got errors like:

```text
Error acquiring the state lock
ConditionalCheckFailedException
ResourceNotFoundException
```

and also:

```text
NodeGroup already exists
OIDC provider already exists
```

---

# 18) 🧠 WHAT REALLY HAPPENED

This is the exact story:

### First:

Terraform/GitHub Actions started a run.

### Then:

That run partially created or partially deleted infra.

### Then:

The run failed or got interrupted.

### Result:

Terraform left a **stale lock** in DynamoDB.

That means Terraform believed:

> “someone is still modifying infra”

even though the runner was dead.

---

# 19) ✅ YOU LEARNED HOW TO DEBUG TERRAFORM LOCKS

This is a very valuable DevOps lesson.

You saw lock data like:

```text
LockID:
sohail-terraform-state-2026-001/terraform-eks-platform/terraform.tfstate
```

and:

```text
terraform.tfstate-md5
```

inside DynamoDB.

---

## Important learning

### Delete this:

```text
terraform.tfstate
```

### Usually keep / ignore:

```text
terraform.tfstate-md5
```

unless specifically needed

---

## Best recovery method

Instead of deleting table repeatedly, the cleaner fix is:

```bash
terraform force-unlock <LOCK_ID>
```

That is the correct Terraform way.

---

# 20) ❌ BIG PROBLEM WE FACED: MANUAL AWS DELETE CAUSED LOOP

You manually deleted some resources in AWS Console, such as:

* EC2
* Auto Scaling Group
* maybe parts of node infra

This caused Terraform confusion.

---

## Why it caused trouble

Because now:

```text
AWS actual state ≠ Terraform state
```

Terraform thought some resources still existed,
while AWS had already removed them.

That caused errors like:

```text
NodeGroup already exists
OIDC provider already exists
```

and repeated replacement loops.

---

# 21) 🔥 BIG LESSON OF THE DAY

# ❌ Never mix:

* Terraform-managed infra
* manual AWS deletion

unless it is emergency recovery.

---

## Correct rule now

### If Terraform created it:

👉 Terraform should delete it.

### Manual delete only when:

* resource is stuck forever
* destroy is blocked
* recovery is impossible otherwise

This is one of the biggest professional lessons from today.

---

# 22) ✅ YOU SUCCESSFULLY RECOVERED INFRA LOCALLY

This is very important.

At the end, you confirmed:

# ✅ “running on local works”

That means:

* your backend is working
* your state is usable
* your Terraform structure is recoverable
* your AWS credentials are correct locally

That is a **huge win**.

---

# 23) ❌ WHY GITHUB ACTIONS IS STILL NOT FULLY TRUSTWORTHY YET

GitHub Actions is not fully stable yet for this infra because of:

* timing issues
* EKS long create/destroy time
* AWS eventual consistency
* ALB cleanup delay
* OIDC conflicts
* node group cleanup delays
* stale lock risk

So the mature strategy now is:

---

# 24) ✅ NEW OPERATING MODEL (VERY IMPORTANT)

## Use LOCAL for:

* `terraform init`
* `terraform plan`
* `terraform apply`
* `terraform destroy`
* recovery
* cleanup
* debugging

## Use GITHUB ACTIONS later for:

* stable deploy automation
* controlled CI/CD
* non-destructive runs
* plan visibility

---

# 25) ✅ YOUR S3 MODULE IS IN GOOD SHAPE

You showed:

```hcl
resource "aws_s3_bucket" "django_media" {
  bucket = var.bucket_name
  force_destroy = true
}
```

and added:

* ownership controls
* versioning
* public access block
* bucket policy
* lifecycle

This is pretty solid for your current project stage.

---

## Why `force_destroy = true` matters

Without it:

Terraform destroy will fail if bucket has files.

With it:

Terraform can remove the bucket even if objects exist.

👉 Very important for destroy reliability.

---

# 26) ⚠️ ONE THING TO REMEMBER ABOUT S3

Your current bucket policy allows public read:

```hcl
Action = ["s3:GetObject"]
Principal = "*"
```

That is okay for:

* media/static style project usage

But later in production, you may move to:

* private bucket
* CloudFront
* signed access

So for now it is fine, but not final-enterprise secure.

---

# 27) ✅ EBS CSI POLICY FILE IS PRESENT

You confirmed your repo contains:

```text
ebs-csi-policy.json
```

That means your EBS CSI direction is still intact.

This is important because your architecture still needs storage support for:

* Postgres PVC
* EBS-backed storage
* future persistent workloads

---

# 28) ⚠️ WHY VPC / NETWORK RESOURCES SOMETIMES REMAIN

You asked:

> “mentor why VPC still exists?”

### Correct reason:

AWS networking resources often delete **last**, not first.

Especially if any of these still exist:

* ENI
* Security Group
* Route Table association
* NAT Gateway
* Internet Gateway
* EIP
* Load Balancer
* Subnet dependencies

So when VPC remains, it usually means:

> “something inside it is still attached”

That is normal AWS behavior.

---

# 29) 🧠 TODAY’S MOST IMPORTANT TECHNICAL LESSONS

Here are the **big mentor takeaways** from today:

---

## 🔥 Lesson 1 — Remote state is mandatory

For real Terraform infra:

```text
S3 + DynamoDB backend is not optional
```

---

## 🔥 Lesson 2 — Local first, CI second

For sensitive infra like EKS:

```text
local stability first
automation second
```

---

## 🔥 Lesson 3 — Don’t manually delete Terraform infra

Unless absolutely necessary.

---

## 🔥 Lesson 4 — Simpler EKS node group is better

Do not overcomplicate managed node groups too early.

---

## 🔥 Lesson 5 — State lock is normal

Terraform lock problems are not “failure”, they are part of real infra work.

---

## 🔥 Lesson 6 — AWS deletes slowly

Destroying EKS/VPC infra is not instant.

---

# 30) 🧱 CURRENT PROJECT STATUS (END OF TODAY)

## Repo:

`terraform-eks-platform`

## Infra components in project:

* VPC
* EKS
* Node Group
* ALB Controller
* ArgoCD
* S3 Media Bucket
* IAM / IRSA
* EBS CSI
* Destroy cleanup hook

---

## GitHub workflows:

* `deploy.yml`
* `destroy.yml`

---

## Backend:

* S3 state bucket
* DynamoDB lock table

---

## Operational truth:

# ✅ Local Terraform is currently your reliable execution path

---

# 31) 🚀 WHAT TO DO NEXT TIME (VERY CLEAR)

When you come back, we should NOT randomly continue.

We should continue in this exact order:

---

# 🔜 NEXT SESSION PLAN

## STEP 1 — Clean and finalize EKS module

Goal:

* stable create
* stable destroy
* no node group loop
* no launch template mess

---

## STEP 2 — Finalize `deploy.yml`

Goal:

* production-safe workflow
* waiting logic
* retries
* concurrency
* idempotent ArgoCD install

---

## STEP 3 — Finalize `destroy.yml`

Goal:

* safe cleanup
* avoid stuck node group
* avoid VPC leftovers
* improve destroy order

---

## STEP 4 — Test full clean lifecycle

### Test sequence:

```bash
terraform apply -auto-approve
terraform destroy -auto-approve
terraform apply -auto-approve
terraform destroy -auto-approve
```

👉 If this works cleanly twice,
your infra becomes **resume-worthy strong**.

---

# 32) 📌 YOUR SAFE COMMANDS NOW

## For deploy:

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

## For destroy:

```bash
terraform destroy -auto-approve
```

## If lock happens:

```bash
terraform force-unlock <LOCK_ID>
```

---

# 33) 🧠 FINAL MENTOR ASSESSMENT

Today was not “just error fixing”.

Today you learned **real DevOps engineering pain points**:

* Terraform backend
* remote state
* locking
* AWS cleanup timing
* EKS node group lifecycle
* GitHub Actions limits
* infra recovery
* drift between AWS and Terraform

That is **real engineer growth**.

---

# 34) 🏁 WHERE WE STOP TODAY

## Final stop state:

# ✅ Local Terraform works

# ✅ Backend exists

# ✅ Repo is upgraded

# ⚠️ Workflows still need hardening

# ⚠️ EKS module still needs final production cleanup

# ⚠️ Destroy path still needs stabilization

---

# 🔥 NEXT TIME JUST SAY THIS:

## 👉 **"mentor continue from terraform-eks-platform stabilize phase"**

Then I’ll continue from exactly here without needing full re-explanation.

---

If you want, I can also give you now a **clean “single-file copy-paste notes version”** for your personal DevOps notes folder.
