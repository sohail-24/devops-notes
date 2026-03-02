# 🚀 Django E-Commerce GitOps + Helm Migration — Continuation Notes

Author: Mohammed Sohail
Cluster: kubeadm (3-node)
GitOps: ArgoCD
CI/CD: GitHub Actions
Architecture: Two-Repo GitOps
Date: 03 March 2026

---

# 📌 CURRENT STABLE STATE (Before Helm Migration)

## ✅ Infrastructure Status

* Kubernetes cluster running (kubeadm)
* Ingress NGINX working
* PostgreSQL StatefulSet running
* Redis Deployment running
* PVC storage working
* Django Deployment running
* NGINX media pod running
* ArgoCD installed and healthy
* Auto Sync enabled
* Prune enabled
* Self Heal enabled

ArgoCD Status:

* Sync: Synced
* Health: Healthy
* Revision: 7d62f69
* Image Tag: SHA-based (943e8c8)

---

# 🏗 Two-Repo Architecture (WORKING)

## Repo 1: Application Repo

django_ecommerce

Contains:

* Django source code
* Dockerfile
* GitHub Actions workflow
* No Kubernetes manifests anymore

CI Flow:

1. Push to main
2. Build Docker image with SHA tag
3. Push image to DockerHub
4. Clone infra repo
5. Update image tag in infra repo
6. Push infra repo

---

## Repo 2: Infrastructure Repo

django_ecommerce_infra

Previously contained:

* django.yaml
* postgres.yaml
* redis.yaml
* ingress.yaml
* pvc.yaml
* namespace.yaml
* nginx config

ArgoCD watches THIS repo only.

---

# 🔥 What We Started Today — Helm Migration

We began converting infra repo from raw YAML → Helm chart.

New Structure:

django_ecommerce_infra/
charts/
django-ecommerce/
Chart.yaml
values.yaml
templates/
deployment.yaml

---

# ✅ What We Successfully Did

1. Created Helm chart:
   helm create django-ecommerce

2. Removed default templates.

3. Converted django.yaml → templates/deployment.yaml

4. Parameterized:

   * image.repository
   * image.tag
   * image.pullPolicy
   * replicaCount
   * service.port
   * resources
   * env variables

5. Added:

   * revisionHistoryLimit
   * readinessProbe
   * livenessProbe

6. Updated values.yaml with:

   * image settings
   * service config
   * resource limits
   * env variables

---

# ❌ Current Issue (Where We Stopped)

Helm template rendering error:

YAML parse error:
mapping values are not allowed in this context

Root cause:
Indentation issue in deployment.yaml under:

resources:
{{ toYaml .Values.resources | indent 12 }}

We must use:

{{- toYaml .Values.resources | nindent 12 }}

Helm indentation is strict. This is normal during Helm migration.

Cluster is still stable because ArgoCD is still using previous YAML commit.
Helm version has NOT yet been applied.

So production is SAFE.

---

# 🎯 Tomorrow's Plan (Step-by-Step)

## Phase 1 — Fix Helm Template Rendering

1. Fix indentation using:
   nindent instead of indent

2. Run:
   helm template test charts/django-ecommerce

3. Ensure output renders valid Kubernetes YAML.

---

## Phase 2 — Complete Helm Conversion (Django Only)

Once template renders successfully:

* Commit Helm chart

* Push infra repo

* Update ArgoCD application source:
  path: charts/django-ecommerce
  helm:
  valueFiles:
  - values.yaml

* Let ArgoCD sync Helm chart instead of raw YAML.

Verify:

* Deployment recreated
* Pod running
* App healthy

---

## Phase 3 — Convert Remaining Resources to Helm

After Django works via Helm:

Convert one by one:

1. Service (already inside file)
2. Ingress
3. PVC
4. Redis
5. Postgres
6. ConfigMap (nginx-media)

Do NOT migrate everything at once.

---

# 🧠 Architecture Evolution

Before:
Raw Kubernetes YAML GitOps

Now moving to:
Helm + GitOps + SHA immutable images

Future Direction:

* Environment folders (dev/stage/prod)
* Secrets via Kubernetes Secret
* HPA autoscaling
* Monitoring stack (Prometheus + Grafana)
* Sealed Secrets or External Secrets

---

# 🏆 Skills Achieved So Far

You now understand:

* kubeadm cluster setup
* Ingress routing
* StatefulSet with PVC
* GitOps workflow
* ArgoCD sync engine
* SHA-based image tagging
* Two-repo production architecture
* CI pushing to infra repo
* Immutable deployments
* Helm templating fundamentals
* Helm indentation debugging

This is already mid-level DevOps capability.

---

# ⚠️ Important Reminder for Tomorrow

Cluster is stable.
Do NOT delete namespace.
Do NOT modify ArgoCD yet.
Fix Helm locally first using helm template.
Only when rendering works → update ArgoCD.

---

# 🎯 Goal for Tomorrow

By end of session:

Django running fully via Helm chart
ArgoCD managing Helm release
Infra repo fully Helm-based

After that:
We move to environment-based structure.

---

# 📌 Final State Tonight

Cluster: Healthy
GitOps: Working
Helm: 80% migration complete
Blocking issue: YAML indentation in Helm template

---

END OF NOTES — Continue from Helm template fix.
