
---

# FreshFlow - Cloud Deployment Notes

## Phase 13 - Multi-Cloud Evaluation (Completed)

---

# Goal

Find a cloud platform to host **FreshFlow** in production with:

* Docker
* Docker Compose
* Nginx
* PostgreSQL
* Custom Domain
* HTTPS
* Lowest possible cost

---

# Cloud Platforms Evaluated

---

# 1. Oracle Cloud Infrastructure (OCI)

## Goal

Use Oracle Always Free ARM VM.

### Account

* ✅ Oracle Free Tier account created.
* ✅ Home Region: India South (Hyderabad)
* ✅ One subscribed region only.

---

## Instance Configuration

### Shape

```
VM.Standard.A1.Flex
```

Resources

```
1 OCPU
6 GB RAM
Always Free
```

---

## SSH

* ✅ SSH key pair generated.
* ✅ Private key downloaded.
* ✅ SSH configuration verified.

---

## Networking

* ✅ VCN created.
* ✅ Public IP enabled.
* ✅ Internet Gateway configured.
* ✅ Security rules configured.

---

## Errors

### Error

```
Out of capacity for shape VM.Standard.A1.Flex
```

Meaning

Oracle had no available ARM servers.

---

### Availability Domain

Available

```
AD-1
```

Unavailable

```
AD-2
AD-3
```

Our tenancy only provides AD-1.

---

## Region

Available

```
India South (Hyderabad)
```

Mumbai cannot be added to this tenancy.

---

## AMD Instance

Available

```
VM.Standard.E2.1.Micro
```

Resources

```
1 GB RAM
```

Decision

Too small for FreshFlow production.

---

## Oracle Final Result

Tried:

* Yesterday evening
* Today early morning
* Today morning again

Result

```
Out of capacity
```

Conclusion

The issue is Oracle infrastructure capacity, not our configuration.

---

# Oracle Decision

Stop spending more time on Oracle.

---

# 2. Google Cloud Platform (GCP)

## Goal

Evaluate Google Compute Engine.

---

## Project

```
FreshFlow
```

---

## Machine Configuration

Machine Series

```
E2
```

Machine Type

```
e2-small
```

Resources

```
2 vCPU
2 GB RAM
```

---

## Operating System

```
Debian GNU/Linux 13
```

Boot Disk

```
Balanced Persistent Disk
```

Size

```
10 GB
```

---

## Configuration Completed

### Machine

* ✅ Name configured
* ✅ Region selected
* ✅ Zone automatic

---

### Storage

* ✅ Debian selected
* ✅ 10 GB disk
* ✅ Balanced disk

---

### Data Protection

Selected

```
No Backups
```

---

### Networking

Enabled

```
HTTP
HTTPS
```

Kept default

* Public IPv4
* Premium Network
* Default VPC

---

### Observability

Left default.

---

### Security

Kept default configuration.

---

### Advanced

Kept default configuration.

---

## Estimated Cost

Google estimated approximately

```
US$15.89/month
```

Important

This VM uses **trial credits** from the free trial account.

---

## Google Final Result

Google VM creation works.

However:

* It is not an Always Free VM for our required configuration.
* It consumes trial credits.
* After the trial ends, charges apply if the VM continues running.

---

# Google Decision

Suitable for:

* Learning
* Practice
* Short-term testing

Not selected as the long-term host for FreshFlow.

---

# Multi-Cloud Comparison

| Platform     | Result                                     | Decision              |
| ------------ | ------------------------------------------ | --------------------- |
| Oracle Cloud | Capacity unavailable                       | ❌ Skip                |
| Google Cloud | Uses trial credits                         | ❌ Skip for production |
| AWS          | Stable learning and deployment environment | ✅ Next choice         |

---

# Final Decision

FreshFlow will continue on:

# AWS

Reason

* Familiar platform from previous projects.
* Stable VM availability.
* Strong DevOps ecosystem.
* Ideal for Docker, Nginx, PostgreSQL, GitHub Actions, and future Kubernetes migration.

---

# Deployment Plan

## Phase 14

Deploy FreshFlow on AWS.

Steps

1. Create EC2 instance.
2. Connect using SSH.
3. Install Docker.
4. Install Docker Compose.
5. Clone FreshFlow repository.
6. Configure `.env`.
7. Run:

```bash
docker compose up -d --build
```

8. Verify application.
9. Configure Nginx.
10. Point:

```
amfruits.sohaildevops.site
```

11. Install HTTPS (Let's Encrypt).
12. Test production deployment.
13. Monitor logs.
14. Create deployment documentation.

---

# Long-Term Infrastructure Roadmap

```
Local Development
        │
        ▼
Docker Compose
        │
        ▼
AWS EC2
        │
        ▼
Production Deployment
        │
        ▼
HTTPS + Custom Domain
        │
        ▼
CI/CD (GitHub Actions)
        │
        ▼
Monitoring
        │
        ▼
Kubernetes (Future)
```


