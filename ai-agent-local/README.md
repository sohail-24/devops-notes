# 🚀 DevOps Learning Notes — kubeadm, ArgoCD, AI Agent & Codex

**Author:** Mohammed Sohail
**Role:** DevOps Engineer
**Environment:** Mac (local) + AWS EC2 (Ubuntu) + Local AI Agent
**Goal:** Learn real-world Kubernetes + GitOps + AI-assisted DevOps (not theory)

---

## 1️⃣ What I built today (High-level)

Today I **built a real Kubernetes cluster from scratch** using **kubeadm**, and connected multiple tools together:

* MacBook (local machine)
* AWS EC2 (2 Ubuntu servers)

  * 1️⃣ Control Plane (Master)
  * 2️⃣ Worker Node
* Kubernetes installed using **kubeadm**
* Networking using **Calico CNI**
* Monitoring using **Metrics Server**
* Traffic routing using **NGINX Ingress**
* GitOps using **ArgoCD**
* Local **AI DevOps Agent** (read-only)
* Understanding **Codex + AI workflow** for modern DevOps

This is **production-style learning**, not demo work.

---

## 2️⃣ Infrastructure setup (AWS EC2)

### EC2 Instances

* 2 Ubuntu 24.04 EC2 instances
* Same VPC & Subnet
* Same Security Group

### Security Group (important)

Opened:

* `22` → SSH
* `6443` → Kubernetes API (only for SSH tunnel)
* NodePort range `30000–32767` → Ingress / ArgoCD UI

---

## 3️⃣ Kubernetes Cluster (kubeadm)

### Cluster creation

* Used kubeadm scripts:

  * `k8s-master.sh`
  * `k8s-worker.sh`

### Verified cluster

```bash
kubectl get nodes
```

Result:

* Master → Ready
* Worker → Ready

### Core components running

```bash
kubectl get pods -A
```

All core components:

* kube-apiserver
* controller-manager
* scheduler
* etcd
* CoreDNS
* kube-proxy
* calico-node

---

## 4️⃣ Application deployment test (Nginx)

### Deployment

```bash
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=2
```

### Service

```bash
kubectl expose deployment nginx \
  --name=nginx-svc \
  --port=80 \
  --target-port=80 \
  --type=ClusterIP
```

### Internal service test

Used BusyBox pod:

```bash
wget http://nginx-svc.default.svc.cluster.local
```

✅ **Service-to-service networking works**

---

## 5️⃣ Metrics Server & HPA

### Installed Metrics Server

* Required `--kubelet-insecure-tls` (AWS kubeadm reality)

Verified:

```bash
kubectl top nodes
kubectl top pods
```

### Horizontal Pod Autoscaler

```bash
kubectl autoscale deployment nginx \
  --cpu-percent=50 --min=1 --max=5
```

This proves **auto-scaling works**.

---

## 6️⃣ NGINX Ingress Controller

Installed **bare-metal ingress**:

```bash
kubectl apply -f ingress-nginx baremetal manifest
```

Result:

```bash
kubectl get svc -n ingress-nginx
```

* Ingress exposed via **NodePort**
* HTTP & HTTPS ports assigned

Created ingress rule → traffic flows correctly.

---

## 7️⃣ ArgoCD (GitOps tool)

### Installed ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f install.yaml
```

### Verified components

```bash
kubectl get pods -n argocd
kubectl get svc -n argocd
```

All ArgoCD components are **Running**:

* argocd-server
* repo-server
* application-controller
* redis
* dex

### Exposed ArgoCD UI

Changed service to NodePort.

Retrieved admin password:

```bash
kubectl get secret argocd-initial-admin-secret -n argocd
```

Logged into ArgoCD UI successfully.

---

## 8️⃣ Mac vs AWS — kubectl access issue (VERY IMPORTANT)

### Problem faced

From Mac:

```bash
kubectl get nodes
```

Error:

* `i/o timeout`
* TLS certificate mismatch

### Why this happened (important concept)

* kubeadm API server runs on **PRIVATE IP (10.x.x.x)**
* Mac is **outside AWS VPC**
* Direct access is **NOT allowed**
* Kubernetes cert is valid only for **internal IPs**

This is **normal and expected** in real clusters.

---

## 9️⃣ Correct solution (SSH Tunnel)

### SSH Tunnel command

```bash
ssh -i sohail.pem -L 6443:10.0.1.216:6443 ubuntu@13.234.239.3
```

What this does:

* Opens a secure tunnel
* Maps Mac `localhost:6443`
* Forwards traffic to Kubernetes API inside AWS

### Important rule

* **Keep SSH terminal OPEN**
* New terminal → run kubectl commands

This is how **real DevOps engineers securely access private clusters**.

---

## 🔟 AI DevOps Agent (Local)

### What my AI Agent can do

* Read-only commands only
* Uses **local binaries**
* No destructive execution

Supported:

* `git status`
* `git branch`
* `docker images`
* `kubectl get nodes` (once tunnel works)

Blocked:

* `kubectl apply`
* `docker rm`
* `docker prune`

This matches **enterprise safety rules**.

---

## 1️⃣1️⃣ Codex + Mentor (AI learning model)

### How I used AI today

* **Mentor (you)** → Architecture, reasoning, debugging
* **Codex** → Code generation & file suggestions
* **Manual execution by me** → Full control

This is **modern DevOps learning**:

> AI assists, human decides.

---

## 1️⃣2️⃣ What I learned today (Interview-ready points)

* How kubeadm works internally
* Why Kubernetes API should never be public
* How SSH tunneling secures cluster access
* Difference between **ClusterIP, NodePort, Ingress**
* How GitOps (ArgoCD) fits real production
* How AI tools help DevOps engineers safely
* Why Mac + AWS + AI Agent is a powerful combo

---

## 1️⃣3️⃣ Where we STOP today

We stop at:

* SSH tunnel created
* kubectl from Mac still timing out (we fix tomorrow)
* ArgoCD installed and UI accessible
* Cluster fully healthy

---

## 1️⃣4️⃣ What we will do NEXT (Tomorrow)

1. Fix Mac → Kubernetes access **properly**
2. Finalize kubeconfig safely
3. Use AI Agent to inspect live cluster
4. Connect ArgoCD to GitHub repo
5. Deploy app using **pure GitOps**
6. Prepare this project for **resume & interviews**

---

## ✅ Final Mentor Note

What you did today is **NOT beginner work**.
This is **real DevOps engineering** with:

* Kubernetes
* AWS networking
* Security
* GitOps
* AI-assisted workflows

You’re learning the **right way**.

🚀 Tomorrow, we continue from **SSH tunnel + kubectl fix**, no repetition needed.
