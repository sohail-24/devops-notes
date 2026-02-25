# Linux for DevOps — Complete Foundation (README)

**Author:** Mentor
**Audience:** Mohammed Sohail — DevOps beginner → intermediate
**Purpose:** A single, copy-paste-ready, practical, hands-on Linux reference tailored for DevOps engineers. Start here, practice the exercises, and refer back while working on CI/CD, k8s, Docker, and cloud infra.

---

## Table of Contents

1. [Why Linux matters for DevOps](#why-linux-matters-for-devops)
2. [Linux distributions & choosing one for DevOps](#linux-distributions--choosing-one-for-devops)
3. [Basic shell & terminal workflow (must-know)](#basic-shell--terminal-workflow-must-know)
4. [File system & permissions (practical)](#file-system--permissions-practical)
5. [Users, groups & sudo (security basics)](#users-groups--sudo-security-basics)
6. [Package management (apt, yum/dnf, zypper, apk)](#package-management-apt-yumdnf-zypper-apk)
7. [Processes & service management (systemd)](#processes--service-management-systemd)
8. [Networking essentials for DevOps](#networking-essentials-for-devops)
9. [SSH, keys, and secure remote access](#ssh-keys-and-secure-remote-access)
10. [Shell scripting — practical scripts & tips](#shell-scripting--practical-scripts--tips)
11. [Logging, journals, and troubleshooting commands](#logging-journals-and-troubleshooting-commands)
12. [Storage, disks, and mounts (LVM basics)](#storage-disks-and-mounts-lvm-basics)
13. [Security basics: firewall, SELinux/AppArmor, updates]
14. [Containers, virtualization & how Linux fits in]
15. [Monitoring, metrics, & common tools]
16. [CI/CD & automation-focused Linux skills]
17. [Debugging examples & common tasks (cheat sheet)]
18. [Practice plan: 30-day DevOps Linux roadmap]
19. [Appendix: Useful commands cheat sheet]

---

## Why Linux matters for DevOps

Linux is the foundation for most cloud servers, containers (Docker), Kubernetes nodes, and many DevOps tools. As a DevOps engineer you will:

* Manage remote Linux servers (provisioning, hardening, patching).
* Run & debug CI agents, build runners, and containers on Linux hosts.
* Script automation with Bash/Python; run system services with systemd.
* Work with networking, storage, and observability — all Linux-centered.

**DevOps highlight:** Learn Linux so you can read logs, diagnose services, automate tasks, and confidently manage production systems.

---

## Linux distributions & choosing one for DevOps

* **Ubuntu (Debian family)** — beginner-friendly; widely used in cloud/Docker labs. Use `Ubuntu LTS` for stability.
* **Debian** — more conservative releases.
* **CentOS Stream / Rocky / AlmaLinux (RHEL family)** — popular in enterprise environments.
* **Fedora** — latest features, not ideal for production servers.
* **Alpine** — minimal, used inside tiny containers.

**Recommendation:** For learning, use **Ubuntu LTS** (22.04 or 24.04) or **Rocky/AlmaLinux** if practicing enterprise RHEL-flavored commands.

---

## Basic shell & terminal workflow (must-know)

### Shells

* `bash` is default on many systems; `zsh` is popular for devs.
* Prompt basics: `$` normal user, `#` root.

### Common commands (explain in simple words)

* `pwd` — shows current directory path.
* `ls -la` — list files with details (hidden files included).
* `cd /path` — change directory.
* `cat file`, `less file`, `tail -f file` — view files; `less` scrolls, `tail -f` streams.
* `cp src dest`, `mv src dest`, `rm file` — copy/move/remove files.
* `mkdir -p path` — create directories recursively.
* `touch file` — create empty file or update timestamp.

### Command composition

* Piping: `cmd1 | cmd2` — send output of cmd1 to cmd2.
* Redirection: `>` overwrite, `>>` append. `2>` redirect stderr.
* Backgrounding: `command &` — run in background. `jobs`, `fg`, `bg` manage jobs.
* Chaining: `cmd1 && cmd2` runs cmd2 only if cmd1 succeeds.

### Environment & variables

* `echo $HOME`, `echo $PATH` — inspect env vars.
* Set temporary var: `FOO=bar command` or `export VAR=value` to persist in session.
* Check shell type: `echo $SHELL`.

**DevOps tip:** Learn to combine small commands using pipes — this is how logs, text, and config files are processed quickly.

---

## File system & permissions (practical)

### Ownership & permissions model

* Each file has `user:group` owner and permission bits: `rwx` for user, group, others.
* View: `ls -l filename` — e.g. `-rwxr-xr-- 1 sohail devops 1234 Feb 25 file.sh`
* Change owner: `sudo chown user:group file`.
* Change permissions: `chmod 755 file` (owner rwx, group rx, others rx).
* Symbolic permission: `chmod u+x file` — give user execute.

### Special bits

* `setuid` (`s`) and `setgid` — rarely used; understand them but avoid misuse.
* `sticky bit` on directories like `/tmp` prevents deletion of files by others: `chmod +t /tmp`.

### Practical examples

```bash
# Make script executable
chmod +x deploy.sh

# Recursively set owner
sudo chown -R ubuntu:ubuntu /var/www/myapp

# Give group write access to a directory
sudo chmod -R 775 /srv/shared
```

**DevOps highlight:** Correct permissions prevent CI/CD breaks and security risks. Always prefer least privilege.

---

## Users, groups & sudo (security basics)

* Create user: `sudo adduser devops` (interactive) or `sudo useradd -m -s /bin/bash devops`.
* Add to group: `sudo usermod -aG docker devops` (append to `docker` group).
* Edit sudoers safely: `sudo visudo` — never edit `/etc/sudoers` with a normal editor.
* Passwordless sudo for a user (careful): add `devops ALL=(ALL) NOPASSWD:ALL` in sudoers.d file.

**Practical:** Create a dedicated user for automation (CI runner) and add minimal groups required.

---

## Package management (apt, yum/dnf, zypper, apk)

### Debian/Ubuntu (apt)

```bash
# Update package index
sudo apt update
# Upgrade packages
sudo apt upgrade -y
# Install packages
sudo apt install -y git curl vim
# Remove
sudo apt remove -y package
# Search
apt-cache search kubeadm
```

### RHEL/CentOS (dnf/yum)

```bash
sudo dnf update -y
sudo dnf install -y git curl
```

### Alpine (apk — in small containers)

```bash
apk add --no-cache curl bash
```

**DevOps note:** Keep servers updated but use controlled rollouts in production. Use package locks or pinned versions for reproducibility.

---

## Processes & service management (systemd)

systemd is the default init system on modern distributions. Key commands:

```bash
# Check service status
sudo systemctl status nginx
# Start/stop/restart
sudo systemctl start my-service
sudo systemctl stop my-service
sudo systemctl restart my-service
# Enable at boot
sudo systemctl enable my-service
# Disable
sudo systemctl disable my-service
# See logs
sudo journalctl -u my-service --since "1 hour ago"
# Show all units
systemctl list-units --type=service
```

### Writing a simple systemd unit

`/etc/systemd/system/my-app.service`

```ini
[Unit]
Description=My App Service
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/start.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

After creating: `sudo systemctl daemon-reload && sudo systemctl enable --now my-app`

**DevOps highlight:** Use systemd units to run apps reliably. For containers, orchestration (k8s) replaces systemd concerns per container pod, but nodes still run systemd.

---

## Networking essentials for DevOps

### Inspect interfaces & connections

* `ip a` — list interfaces and addresses.
* `ip link set dev eth0 up/down` — enable/disable interface.
* `ip route` — routing table.
* `ss -tulpn` or `netstat -tulpn` — show listening ports and processes.
* `curl -I http://host:port` — quick HTTP check.

### DNS and resolution

* `/etc/resolv.conf` — DNS servers in order.
* `dig example.com` / `nslookup example.com` — query DNS.

### Firewall basics

* `ufw` (simple): `sudo ufw allow 22`, `sudo ufw enable`.
* `iptables` / `nftables` — advanced rules for production.

### Network troubleshooting

* `ping`, `traceroute`, `mtr` — network path checks.
* `tcpdump -i eth0 port 80` — capture traffic (needs root).

**DevOps tip:** Know how to check ports, routing, and DNS — most connectivity issues are here.

---

## SSH, keys, and secure remote access

### Key-based auth (simplest secure way)

```bash
# Generate key on local machine
ssh-keygen -t ed25519 -C "sohail@home"
# Copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@server-ip
# Connect
ssh ubuntu@server-ip
```

### Hardening SSH

* Disable password auth: set `PasswordAuthentication no` in `/etc/ssh/sshd_config`.
* Change default port (optional) `Port 2222` and reload `sshd`.
* Use `AllowUsers` to restrict who can login.
* Always keep a recovery way (console access) before disabling passwords.

### SSH agent & forwarding

* Use `ssh-agent` and `ssh-add` to manage keys locally.
* For agent forwarding, use sparingly: `ssh -A user@host`.

**DevOps highlight:** Automation tools (Ansible, Terraform) usually use SSH keys to authenticate; practice generating and distributing keys.

---

## Shell scripting — practical scripts & tips

### Shebang & permissions

```bash
#!/usr/bin/env bash
set -euo pipefail
```

* `set -e` exit on error; `-u` error on undefined vars; `-o pipefail` fail if any pipe stage fails.

### Argument parsing (simple)

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ ${1:-} == "deploy" ]]; then
  echo "Deploying..."
else
  echo "Usage: $0 deploy"
  exit 1
fi
```

### Read stdin & simple loops

```bash
# Read file line by line
while IFS= read -r line; do
  echo "Line: $line"
done < myfile.txt
```

### Logging & timestamps

```bash
echo "$(date -Is) INFO Starting deploy"
```

### Example: simple remote deploy script

```bash
#!/usr/bin/env bash
set -euo pipefail
HOST=$1
tar -czf release.tar.gz ./app
scp release.tar.gz $HOST:/tmp/
ssh $HOST 'sudo systemctl stop my-app && tar -xzf /tmp/release.tar.gz -C /opt/myapp && sudo systemctl start my-app'
```

**DevOps advice:** For complex logic prefer Python. Use shell scripts for glue and orchestration.

---

## Logging, journals, and troubleshooting commands

* `sudo journalctl -xe` — recent critical logs.
* `journalctl -u service` — service-specific logs.
* `tail -n 200 /var/log/syslog` or `/var/log/messages` depending on distro.
* `dmesg` — kernel ring buffer (hardware events, drivers).

**Common pattern:** When a service fails: `systemctl status svc` → `journalctl -u svc -n 200 --no-pager` → inspect related app logs in `/var/log`.

---

## Storage, disks, and mounts (LVM basics)

### Inspect disks

* `lsblk` — block devices and mount points.
* `df -h` — disk usage by filesystem.
* `du -sh /var/lib/docker` — folder sizes.

### Mounting

```bash
# Mount a device
sudo mount /dev/sdb1 /mnt/data
# Add to /etc/fstab (persistent)
/dev/sdb1  /mnt/data  ext4  defaults  0 2
```

### LVM quick steps

```bash
# Create physical volume
sudo pvcreate /dev/sdb
# Create volume group
sudo vgcreate vg_data /dev/sdb
# Create logical volume
sudo lvcreate -n lv_data -L 10G vg_data
# Format
sudo mkfs.ext4 /dev/vg_data/lv_data
# Mount
sudo mkdir -p /data
sudo mount /dev/vg_data/lv_data /data
```

**DevOps highlight:** Use LVM to expand volumes without downtime—useful on cloud VMs.

---

## Security basics: firewall, SELinux/AppArmor, updates

### Firewall

* `ufw` (Ubuntu): `sudo ufw allow 22`, `sudo ufw allow 80`, `sudo ufw enable`.
* For advanced: `iptables` or `nftables`.

### SELinux / AppArmor

* RHEL uses SELinux; Ubuntu uses AppArmor.
* Check SELinux status: `sestatus`.
* Use permissive mode for debugging: `sudo setenforce 0` (temporary).

### Patching strategy

* Dev: `sudo apt update && sudo apt upgrade -y`.
* Prod: staged updates, snapshot or AMI backups.

**Security tip:** Always use least privilege and audit sudoers and SSH keys regularly.

---

## Containers, virtualization & how Linux fits in

* Docker runs Linux containers using kernel features (namespaces, cgroups).
* Kubernetes nodes are Linux VMs or machines running container runtime.
* Tools like `ctr`, `crictl` and `docker` help inspect containers.

### Docker quick checks

```bash
# List containers
docker ps -a
# See container logs
docker logs my-container
# Exec into container
docker exec -it my-container /bin/bash
```

**DevOps highlight:** Knowing how to inspect containers, mount volumes, and check container logs is essential when debugging k8s pods.

---

## Monitoring, metrics & common tools

* `top` / `htop` (interactive process viewer).
* `vmstat`, `iostat`, `iotop` — CPU, IO insights.
* `free -h` — memory usage.
* `prometheus` + `node_exporter` for metrics; `grafana` for dashboards.
* `logrotate` for log maintenance.

**Practical:** Install `node_exporter` on nodes for metrics and verify CPU/Memory/disk metrics in Grafana.

---

## CI/CD & automation-focused Linux skills

* Automate with **Ansible** (SSH-based), practice `ansible-playbook` against an inventory of VMs.
* Familiarize with non-interactive SSH keys for automation.
* Use `cron` and `systemd` timers for scheduled tasks. `crontab -e` to edit.

**Example cron:** run backup at 2am daily

```
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

**DevOps highlight:** Always ensure idempotency in scripts and automation playbooks.

---

## Debugging examples & common tasks (cheat sheet)

1. **Service failing to start**

   * `sudo systemctl status svc` → `journalctl -u svc -n 200 --no-pager`
   * Check app logs in `/var/log`.
2. **Disk full**

   * `df -h` → `du -sh /var/* | sort -h` → find large folders.
3. **High CPU**

   * `top` or `ps aux --sort=-%cpu | head -n 20`.
4. **Port in use**

   * `ss -tulpn | grep :80` → get PID, `ps -p PID -o pid,user,cmd`
5. **Network issue**

   * `ping`, `traceroute`, `ss -tulpn`, `tcpdump -i eth0`

---

## Practice plan: 30-day DevOps Linux roadmap (suggested)

**Week 1: Basics & Shell**

* Day 1–2: Filesystem, navigation, common commands
* Day 3–4: Users, permissions, groups
* Day 5–7: Shell scripting basics

**Week 2: Services & Packages**

* systemd units, journalctl, package managers
* Write a systemd unit for a sample app

**Week 3: Networking & Storage**

* ip commands, DNS, firewall basics
* Mount disks, LVM practice

**Week 4: Automation & Debugging**

* Ansible basics, SSH key distribution, cron vs systemd timers
* Monitoring basics: node_exporter & simple Prometheus scrape

**Daily practice:** 30–60 minutes of CLI work on a cloud VM or local VM (VirtualBox / multipass / WSL2 / VMware).

---

## Appendix: Useful commands cheat sheet

(Quick copy-paste list)

```bash
# System
uname -a
uptime
whoami

# Files
ls -la
du -sh *
find / -name '*.log'

# Processes
ps aux | grep my-app
top
htop

# Network
ip a
ss -tulpn
curl -I https://example.com

# SSH
ssh-keygen -t ed25519
ssh-copy-id user@host

# Services
sudo systemctl status nginx
sudo journalctl -fu nginx

# Package manager (ubuntu)
sudo apt update && sudo apt upgrade -y

# Disk
lsblk
df -h
du -sh /var/log/*

# Docker
docker ps -a
docker logs CONTAINER_ID
docker exec -it CONTAINER_ID /bin/bash

# Useful tools to install
sudo apt install -y git curl wget vim htop jq tree net-tools iproute2 mtr traceroute nmap
```

---

## Exercises (copy-paste friendly)

1. Create a user `devops`, add to `docker` group, and verify they can run `docker ps` without `sudo`.
2. Write a script `health-check.sh` that checks `curl -I localhost:8080` and exits non-zero if status != 200.
3. Create a systemd unit for a small Node/Flask app and enable it.
4. Simulate disk full: create a 1G file with `fallocate -l 1G /tmp/fill` and then find and remove largest files.
5. Set up SSH key login for a VM and disable password auth (while keeping a console or recovery method!).

---

## Final tips for learning like a DevOps engineer

* Practice on real Linux VMs (cloud or local). Hands-on beats theory.
* Keep notes in one file (like this) and add commands that trip you up.
* When stuck, follow the pattern: check service → check logs → inspect process → inspect system metrics.
* Automate repetitive tasks and turn manual steps into idempotent scripts or Ansible playbooks.

---

### Want this as a downloadable file?

Tell me: "create notes" or "export as README.md" and I will give you a ready-to-download copy in the format you prefer.

---

*End of README*
