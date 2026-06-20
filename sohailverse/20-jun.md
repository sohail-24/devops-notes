# SohailVerse — Mentor Notes

## Date: 20 June 2026

## Project: SohailShop Case Study Page (DevOps Portfolio)

---

# Today's Goal

Transform SohailShop from a normal project page into a premium DevOps case study that looks like a real engineering portfolio.

Reference inspiration:

* AWS Architecture style layouts
* Kubernetes journey pages
* Engineering case studies
* Production portfolio showcases

---

# Major Changes Completed Today

---

## 1. Fixed Lucide React Issues

### Problem

Build was failing because:

```tsx
Github
```

and

```tsx
GitHub
```

do not exist in newer lucide-react versions.

Build error:

```bash
Module '"lucide-react"' has no exported member 'Github'
```

---

### Solution

Replaced GitHub icons with:

```tsx
Code2
```

and other supported icons.

Example:

```tsx
import { Code2 } from "lucide-react";
```

---

### Result

```bash
npm run build
```

successfully completed.

---

# 2. Rebuilt ProjectLinks

File:

```bash
src/components/projects/ProjectLinks.tsx
```

---

### Before

Simple placeholder.

```tsx
ProjectLinks
```

---

### After

Created production-style repository section.

Contains:

### Kubeadm Stack

```text
django_ecommerce
devops-ecommerce-kubeadm
devops-ecommerce-platform
```

---

### EKS Stack

```text
django_ecommerce
django_ecommerce_infra
terraform-eks-platform
```

---

### Features

* Repository cards
* Hover effects
* External links
* Recruiter-friendly layout
* GitHub URLs visible

---

# 3. Rebuilt TechnologyArsenal

File:

```bash
src/components/projects/TechnologyArsenal.tsx
```

---

Created stack showcase.

Sections:

---

### Application Layer

```text
Django 5
Python 3.12
Gunicorn
WhiteNoise
```

---

### Data Layer

```text
PostgreSQL
Redis
Persistence
Caching
```

---

### Cloud & Kubernetes

```text
AWS EC2
AWS EKS
Kubeadm
EBS
S3
```

---

### Automation & Delivery

```text
Terraform
GitHub Actions
ArgoCD
Helm
GitOps
```

---

### Source Control

```text
GitHub
Multi Repo Architecture
Versioned Releases
```

---

### Security & Operations

```text
IAM
IRSA
EBS CSI
Least Privilege
```

---

# 4. Rebuilt ArchitectureDiagram

File:

```bash
src/components/projects/ArchitectureDiagram.tsx
```

---

This became the biggest section of the page.

---

## New Section

```text
Engineering Journey
Dual Deployment Architecture
```

---

### Added Summary Metrics

```text
6 Repositories
200+ Git Commits
2 Kubernetes Platforms
Ready Production Architecture
```

---

## Flow 1

### Kubeadm on AWS EC2

```text
Code Repository
Build & Push
Helm Charts
GitOps
Kubeadm Cluster
Data Layer
```

---

## Flow 2

### AWS EKS

```text
Code Repository
Build & Push
Helm Charts
GitOps
AWS EKS
Data & Services
```

---

### Visual Improvements

* Better cards
* Better hierarchy
* Cleaner spacing
* Production theme
* Cyan / Purple separation

---

# 5. Created InfrastructureBlueprint

File:

```bash
src/components/projects/InfrastructureBlueprint.tsx
```

---

Purpose:

Move this content OUT of ArchitectureDiagram:

```text
Infrastructure Layer
GitHub Repositories
```

---

Reason:

ArchitectureDiagram was becoming too large.

Splitting improves:

* readability
* maintainability
* design quality

---

Current status:

```tsx
export default function InfrastructureBlueprint() {
  return (
    <section>
      <h2>Infrastructure Blueprint</h2>
    </section>
  );
}
```

Placeholder only.

Needs implementation tomorrow.

---

# 6. Updated ProjectDetailPage

File:

```bash
src/pages/ProjectDetailPage.tsx
```

---

Current order:

```tsx
<ProjectHero />

<ProjectMetrics />

<MissionOverview />

<ArchitectureDiagram />

<TechnologyArsenal />

<InfrastructureBlueprint />

<ProductionIncidents />

<LessonsLearned />

<MissionAssets />

<ProjectLinks />

<ProjectGallery />
```

---

# Current SohailShop Page Status

## Finished

### Hero

```text
Mission Dossier
```

---

### Metrics

```text
Repositories
Commits
Platforms
Status
```

---

### Mission Overview

Working

---

### Dual Deployment Architecture

Working

---

### Technology Arsenal

Working

---

### Project Links

Working

---

### Footer

Working

---

# Needs Work

---

## InfrastructureBlueprint

Status:

```text
Not built
```

Priority:

★★★★★

---

## ProjectGallery

Status:

```text
Currently shows:
ProjectGallery
```

Priority:

★★★★★

---

## ProductionIncidents

Status:

Basic

Priority:

★★★★☆

---

## LessonsLearned

Status:

Basic

Priority:

★★★★☆

---

## MissionAssets

Status:

Good

Can improve later.

Priority:

★★☆☆☆

---

# Tomorrow's Plan

---

## STEP 1

Build

```bash
src/components/projects/InfrastructureBlueprint.tsx
```

Goal:

Create visual cloud architecture.

---

### Kubeadm Side

```text
Terraform
↓
AWS VPC
↓
EC2 Master
↓
Worker Nodes
↓
EBS
```

---

### EKS Side

```text
Terraform
↓
AWS EKS
↓
Managed Node Groups
↓
EBS CSI
↓
S3
```

---

## STEP 2

Build

```bash
src/components/projects/ProjectGallery.tsx
```

Need real screenshots.

---

Suggested screenshots:

### Kubeadm

```text
kubectl get nodes
```

---

### EKS

```text
AWS EKS Console
```

---

### ArgoCD

```text
Applications
Sync Status
```

---

### GitHub Actions

```text
Successful CI/CD
```

---

### Grafana

```text
Cluster Metrics
```

---

### Terraform

```text
Apply Output
```

---

## STEP 3

Upgrade

```bash
src/components/projects/ProductionIncidents.tsx
```

Create incident cards.

Examples:

```text
Pending Pods
Storage Issue
Docker Pull Failure
ArgoCD OutOfSync
```

---

## STEP 4

Upgrade

```bash
src/components/projects/LessonsLearned.tsx
```

Split into:

### Kubeadm Learnings

and

### EKS Learnings

---

## STEP 5

Polish ArchitectureDiagram

Add:

```text
Code → Build → Helm → GitOps → Cluster → Data
```

visual pipeline arrows.

---

# Files I Need Before We Start Tomorrow

Please have these ready:

### 1.

```bash
src/components/projects/InfrastructureBlueprint.tsx
```

---

### 2.

```bash
src/components/projects/ProjectGallery.tsx
```

---

### 3.

```bash
src/components/projects/ProductionIncidents.tsx
```

---

### 4.

```bash
src/components/projects/LessonsLearned.tsx
```

---

### 5.

Optional screenshots folder

```bash
public/images/projects/sohailshop/
```

Add any screenshots you have:

```text
kubeadm.png
eks.png
argocd.png
github-actions.png
grafana.png
terraform.png
```

---

# Project Health

### Build Status

```bash
npm run build
```

✅ Successful

---

### Design Status

```text
Hero                ✅
Metrics             ✅
Mission Overview    ✅
Architecture        ✅
Technology Arsenal  ✅
Project Links       ✅
Footer              ✅

Infrastructure      ⏳
Gallery             ⏳
Incidents           ⏳
Lessons             ⏳
```

---

# End State Goal

When SohailShop is finished, it should look like:

```text
A Senior DevOps Engineer Case Study

NOT

A student project page.
```

Current progress is roughly **75–80% complete**. Tomorrow's work is mainly about adding visual proof (gallery), architecture depth (Infrastructure Blueprint), and engineering storytelling (Incidents + Lessons Learned).
