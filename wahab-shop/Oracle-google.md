
---

# FreshFlow - Cloud Deployment Notes

## Phase 13 - Oracle Cloud Attempt (Completed)

### Goal

Deploy FreshFlow on Oracle Cloud Always Free VM.

---

## Oracle Account

* ✅ Oracle Free Tier account created.
* ✅ Home Region: India South (Hyderabad)
* ✅ Only one subscribed region.
* ❌ Cannot subscribe to Mumbai.

---

## Instance Configuration

**Name**

```
FreshFlow
```

**OS**

```
Ubuntu 24.04 LTS
```

**Shape Tried**

```
VM.Standard.A1.Flex
```

Status:

```
Always Free
```

Resources:

```
1 OCPU
6 GB RAM
```

---

## SSH

* ✅ Generated SSH key pair.
* ✅ Downloaded private key successfully.
* ✅ SSH configuration was correct.

---

## Networking

* ✅ VCN created.
* ✅ Public IP enabled.
* ✅ Everything configured correctly.

---

## Errors Found

### Error 1

```
Out of capacity for shape VM.Standard.A1.Flex
```

Reason:

Oracle has no available A1 Flex servers in our Availability Domain.

---

### Error 2

Initially

```
No SSH Access
```

Reason:

Private key was not downloaded.

Fixed:

```
Downloaded SSH private key.
```

Not an issue anymore.

---

## Availability Domain

Our account only has

```
AD-1
```

Cannot change to

```
AD-2
AD-3
```

Oracle tenancy does not provide additional Availability Domains.

---

## Region

Only

```
India South (Hyderabad)
```

Available.

Mumbai cannot be subscribed because of Free Tier tenancy limitations.

---

## AMD Shapes

Available:

```
VM.Standard.E2.1.Micro
```

Always Free

But only

```
1 GB RAM
```

Not suitable for our long-term FreshFlow deployment.

---

# Final Decision

After trying:

* Yesterday evening (~5 PM)
* Today early morning (5–6 AM)
* Today again around 11 AM

Oracle still returned

```
Out of capacity
```

The issue is Oracle capacity, **not** our configuration.

---

# Decision

✅ Stop spending time on Oracle.

Switch to

# Google Cloud Platform (GCP)

Reason:

* Better chance of getting a VM without capacity issues.
* Reliable infrastructure.
* Excellent platform for learning DevOps.
* Suitable for Docker, Nginx, PostgreSQL, and FreshFlow.

---

# Next Session Plan

We will start directly with:

```
Google Cloud
```

Steps:

1. Create GCP account.
2. Create Ubuntu VM.
3. Install Docker.
4. Install Docker Compose.
5. Deploy FreshFlow.
6. Configure Nginx.
7. Connect:

   ```
   amfruits.sohaildevops.site
   ```
8. Configure HTTPS.
9. Complete production deployment.

---
