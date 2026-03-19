# 🚀 DEVOPS ECOMMERCE PLATFORM – PROJECT NOTES

## 📌 DAY SUMMARY

Today we made a **major architecture decision**:
👉 Move from AWS EKS → Kubeadm-based Kubernetes setup

---

# ❗ WHY WE LEFT EKS

## Problems faced:

* AWS vCPU quota limits ❌
* Cannot create 15-node cluster ❌
* Resource constraints changed ❌
* Cluster creation failing ❌

## Decision:

👉 Instead of waiting for AWS quota → we changed approach

---

# ✅ WHY WE CHOSE KUBEADM

## Strong Reasons:

* Full control over Kubernetes cluster
* No AWS limitations (cost + quota)
* Matches real office environment (very important)
* Deep understanding of Kubernetes internals
* Better for interviews (hands-on knowledge)

## Interview Explanation:

👉 “Due to AWS quota and cost constraints, I moved to a kubeadm-based Kubernetes setup to gain deeper control and align with real-world on-prem environments.”

---

# 🏗️ FINAL ARCHITECTURE DESIGN

GitHub → GitHub Actions → Terraform → EC2 → Scripts → Kubernetes → ArgoCD → App

---

# 📁 PROJECT STRUCTURE

devops-ecommerce-platform/
├── terraform/
├── scripts/
│   ├── master.sh
│   ├── worker.sh
│   └── common.sh
├── k8s-bootstrap/
├── .github/workflows/
├── README.md
└── .gitignore

---

# 🔥 MASTER SCRIPT (FINAL VERSION)

```bash
#!/bin/bash
set -e

echo "🚀 MASTER SETUP STARTED"

apt update && apt upgrade -y

swapoff -a
sed -i '/ swap / s/^/#/' /etc/fstab

modprobe br_netfilter
echo br_netfilter >/etc/modules-load.d/br_netfilter.conf

cat <<EOF >/etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables=1
net.ipv4.ip_forward=1
EOF

sysctl --system

# Container runtime
apt install -y containerd docker.io
systemctl enable containerd docker
systemctl start containerd docker

# Kubernetes
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | \
gpg --dearmor -o /usr/share/keyrings/kubernetes-apt-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-apt-keyring.gpg] \
https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" \
>/etc/apt/sources.list.d/kubernetes.list

apt update
apt install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl

# Init cluster
kubeadm init --pod-network-cidr=192.168.0.0/16 | tee /root/init.log

# Configure kubectl
mkdir -p /home/ubuntu/.kube
cp /etc/kubernetes/admin.conf /home/ubuntu/.kube/config
chown ubuntu:ubuntu /home/ubuntu/.kube/config

export KUBECONFIG=/etc/kubernetes/admin.conf

# Install Calico
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.3/manifests/calico.yaml
sleep 30

# Generate join command
kubeadm token create --print-join-command > /home/ubuntu/join.sh
chmod +x /home/ubuntu/join.sh

# Install ArgoCD
kubectl create namespace argocd || true
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "✅ MASTER READY"
```

---

# 🔥 WORKER SCRIPT (FINAL VERSION)

```bash
#!/bin/bash
set -e

echo "🚀 WORKER SETUP STARTED"

apt update && apt upgrade -y

swapoff -a
sed -i '/ swap / s/^/#/' /etc/fstab

modprobe br_netfilter

cat <<EOF >/etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables=1
net.ipv4.ip_forward=1
EOF

sysctl --system

apt install -y containerd docker.io
systemctl enable containerd docker
systemctl start containerd docker

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | \
gpg --dearmor -o /usr/share/keyrings/kubernetes-apt-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-apt-keyring.gpg] \
https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" \
>/etc/apt/sources.list.d/kubernetes.list

apt update
apt install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl

# Join cluster
MASTER_IP="<MASTER_PRIVATE_IP>"

scp -o StrictHostKeyChecking=no ubuntu@$MASTER_IP:/home/ubuntu/join.sh /tmp/join.sh
chmod +x /tmp/join.sh
bash /tmp/join.sh

echo "✅ WORKER JOINED"
```

---

# 🔁 AUTOMATION FLOW

Master:

* Setup cluster
* Generate join.sh

Worker:

* Pull join.sh
* Join automatically

---

# 🚨 CURRENT STATUS

✅ Structure ready
✅ Scripts upgraded
✅ Automation logic designed

---

# 🚀 NEXT STEPS

## Step 1: Test scripts manually

* Run master.sh
* Run worker.sh
* Check: kubectl get nodes

## Step 2: Terraform

* Create EC2
* Pass scripts via user_data

## Step 3: GitHub Actions

* Automate Terraform

## Step 4: ArgoCD

* Connect Helm repo
* Enable auto sync

---

# 🎯 FINAL GOAL

👉 One Git push → Full infra + cluster + app deployment

---

# 🧠 KEY LEARNING

* GitHub Actions = trigger
* Terraform = infra
* Scripts = setup
* ArgoCD = deployment

---

👨‍💻 Mohammed Sohail
🚀 DevOps Engineer (in progress)
