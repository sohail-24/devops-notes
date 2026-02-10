# 📘 Kubernetes on AWS (kubeadm) – Production-Style Build Notes

**Owner:** Mohammed Sohail
**Mentor-guided, clean rebuild approach**
**Status:** Phase 2 completed successfully
**Date stopped:** After all nodes became `Ready`

---

## 🎯 GOAL (Big Picture)

Build a **production-style Kubernetes cluster on AWS EC2 using kubeadm**, with:

* Clean IAM + IMDS setup (no hacks)
* External cloud provider (AWS CCM)
* Real LoadBalancer support
* Proper networking (Calico)
* Future-ready for Ingress, TLS, DNS, ArgoCD, GitOps

We intentionally **reset and rebuilt cleanly** to avoid hidden mistakes.

---

## 🧱 CLUSTER ARCHITECTURE

* **Region:** ap-south-1 (Mumbai)
* **Instances:** 3 EC2 (Ubuntu 24.04)

  * 1 × Control Plane
  * 2 × Worker Nodes
* **Instance type:** t3.small
* **Runtime:** containerd
* **Kubernetes:** v1.29.15
* **CNI:** Calico
* **Cloud:** AWS (External CCM – to be finalized next)

---

## ✅ PHASE 0 – CLEAN SLATE DECISION (IMPORTANT)

### Why we reset everything

* Earlier CCM attempts failed due to:

  * Mixed cloud-provider modes
  * IMDS confusion
  * Partial role attachment
* Production rule: **Never patch blindly → reset and rebuild clean**

### Action taken

* Terminated old EC2 instances
* Recreated **new EC2 instances with correct IAM & IMDS**
* Started from zero

✔️ **Correct engineering decision**

---

## ✅ PHASE 1 – EC2 + IAM (DONE)

### IAM Role

Attached to **ALL 3 instances**:

* EC2 permissions for:

  * DescribeInstances
  * LoadBalancers (future CCM)
  * Security Groups
  * Tags

### IMDS

* IMDS enabled (v2 supported)
* Instances can securely fetch metadata

### Important concept learned

> You *can* create 3 instances at once,
> but creating **one-by-one helps learning & debugging**.
> In production → use Launch Templates / Auto Scaling.

---

## ✅ PHASE 2 – OS + CONTAINER RUNTIME (DONE)

### Common setup on **ALL NODES**

#### 1. containerd installed & configured

* Generated default config:

  ```
  containerd config default > /etc/containerd/config.toml
  ```
* **Critical fix (production rule):**

  ```
  SystemdCgroup = true
  ```

#### 2. containerd service

* Restarted
* Enabled on boot
* Verified:

  ```
  systemctl status containerd
  ```

✔️ No crashes
✔️ Clean runtime

---

## ✅ PHASE 3 – KUBERNETES BINARIES (DONE)

Installed on **ALL NODES**:

* kubeadm
* kubelet
* kubectl

### Version pinning (VERY IMPORTANT)

```
apt-mark hold kubelet kubeadm kubectl
```

Why:

* Prevents accidental upgrades
* Keeps cluster stable

---

## ✅ PHASE 4 – CLUSTER RESET & INIT (CONTROL PLANE)

### Reset (clean state)

```
kubeadm reset -f
```

Manual awareness:

* CNI not removed automatically
* iptables not auto-reset (acceptable for now)

### kubeadm init

* Control plane initialized cleanly
* kubeconfig copied correctly

Result:

```
kubectl get nodes
→ control-plane = NotReady (expected)
```

---

## ✅ PHASE 5 – NETWORKING (CALICO) ✅ SUCCESS

### Applied Calico

```
kubectl apply -f calico.yaml
```

### Observed correctly

* calico-node DaemonSet
* calico-kube-controllers
* CoreDNS transitioned:

  ```
  Pending → ContainerCreating → Running
  ```

### Result

```
kubectl get nodes
→ control-plane = Ready
```

✔️ Networking fully functional

---

## ✅ PHASE 6 – WORKER NODES JOINED SUCCESSFULLY

* Worker nodes joined
* Initially `NotReady` (expected)
* After Calico:

  ```
  ip-10-0-1-177 → Ready
  ip-10-0-1-209 → Ready
  ```

### Final cluster state

```
kubectl get nodes -o wide
```

All nodes:

* STATUS: Ready
* Runtime: containerd
* Kubernetes: v1.29.15

✔️ **Perfect cluster base**

---

## 🧠 KEY LEARNINGS (VERY IMPORTANT)

1. **Never mix cloud-provider=aws and external**
2. **IMDS failure = IAM/metadata issue, not Kubernetes**
3. Resetting is not failure → it’s professional behavior
4. containerd + systemd cgroup is mandatory
5. Networking (CNI) controls node readiness
6. Build slowly = fewer production issues later

---

## 🧭 CURRENT STATE (STOP POINT)

✅ Cluster is UP
✅ Nodes are Ready
✅ Networking works
❌ Cloud Controller Manager not yet finalized
❌ No LoadBalancer yet
❌ No Ingress / TLS / DNS yet

---

## 🚀 WHAT WE WILL DO NEXT (PHASE 7+)

### Next immediate steps

1. **Proper AWS Cloud Controller Manager**

   * Correct manifest
   * Correct tags
   * External cloud provider only

2. Verify:

   ```
   Service type: LoadBalancer
   → AWS ELB created
   ```

3. Then:

   * NGINX Ingress Controller
   * Expose via LB (80/443)
   * cert-manager
   * DNS (Route53 / Cloudflare)
   * ArgoCD
   * GitOps structure

---

## 🧘‍♂️ MENTOR NOTE

You did **everything right** today:

* You stopped when confused
* You chose clean rebuild
* You followed production discipline

This is **real DevOps**, not copy-paste.

Tomorrow we **continue directly from Phase 7**.
You do **NOT** need to explain anything again.

---

**STOP POINT CONFIRMED ✅**
**READY TO CONTINUE TOMORROW 🚀**

— *Your mentor*
