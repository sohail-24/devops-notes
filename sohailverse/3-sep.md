
# SohailVerse v2.0 — Homepage Redesign Checkpoint

**Date:** 4 September 2026
**Current phase:** Homepage `/` visual redesign
**Tool/workflow:** Google AI Studio → Gemini 3.7 Flash
**Status:** Hero + mobile Projects section refined; **desktop Projects section is next**

---

## 1. Core rule for the entire redesign

The most important rule going forward:

> **Every change must consider both phone and desktop unless I explicitly say “mobile only” or “desktop only”.**

We learned during the hero redesign that creating separate mobile/desktop image implementations caused unnecessary problems.

Therefore:

* Prefer one shared implementation where possible.
* Use responsive CSS/layout rather than duplicated components.
* If a section genuinely needs different mobile/desktop behavior, scope the difference explicitly.
* Never break the already-approved mobile design while improving desktop.
* Preserve backend/API/database functionality.
* Preserve existing routes and verified project links.
* Do not invent project information or technology data.

---

# 2. HERO SECTION — COMPLETED

## Previous problem

The hero originally had separate:

```text
hero-mobile-master.jpg
hero-desktop-master.jpg
```

and the implementation had separate mobile and desktop layouts.

This created inconsistencies.

Git investigation showed that `hero-mobile-master.jpg` had existed historically but was later deleted.

The current design direction is now:

```text
ONE MASTER HERO IMAGE
        ↓
/hero-master.jpg
        ↓
Responsive across phone + desktop
```

---

# 3. Current Hero Design

The hero image is now shared across viewports.

The text is **not baked into the image**.

Instead, the browser renders animated HTML text over the photograph.

Current hero text:

```text
HEY, I'M SOHAIL 👋

I BUILD.
I AUTOMATE.
I CREATE IMPACT.|
```

The text:

* appears over the left side of the photograph
* uses staggered entrance animation
* fades/slides in
* has the lime accent on `I CREATE IMPACT.`
* has a blinking cursor
* uses a dark gradient behind the text for readability

This was an important improvement because the text is now real HTML rather than part of the image.

---

# 4. Mobile Hero — APPROVED / DO NOT CHANGE

The mobile hero is currently considered good.

Important mobile behavior:

### Hero

```text
[Navbar]

[PHOTO]
   animated text overlay

[description]

[I WORK WITH]
← animated tools marquee

[Explore My Universe] [Know My Journey]

[SCROLL TO EXPLORE]
```

### Mobile tools

The tools move:

```text
RIGHT → LEFT
```

and the speed was deliberately slowed because the original animation was too fast.

Tools include the technologies/tools learned throughout the project, including:

```text
AWS
Docker
Kubernetes
Terraform
GitHub
Python
Terminal
Helm
GitHub Actions
Jenkins
GitOps
Ansible
Prometheus
Grafana
CloudWatch
Linux
PostgreSQL
MongoDB
Redis
Ollama
...
```

The marquee must not create page-level horizontal scrolling.

---

# 5. Desktop Hero — COMPLETED

Desktop hero also uses the same master image.

Desktop changes completed:

* animated text overlay
* left-side text positioning
* readable dark gradient
* two-line explanation
* tool icons
* responsive tool marquee when necessary
* animated:

```text
SCROLL TO EXPLORE
```

The scroll cue was added because users need to understand that more content exists below the hero.

---

# 6. PROJECTS SECTION — ADDED

After:

```text
SCROLL TO EXPLORE
```

we introduced:

```text
PROJECTS I'M BUILDING 🚀
```

This section exists for both phone and desktop.

The project section contains a horizontal project rail/carousel.

Current canonical project records include:

```text
Sohail-Shop
Sohail Studio
Fresh Flow
Wedding Page
New Chapter Loading...
```

---

# 7. Projects Carousel Behavior

The carousel has:

### Right arrow

Moves toward hidden projects.

### Left arrow

Allows moving back.

### Mobile

Supports:

* touch swipe
* horizontal scrolling inside the carousel
* CSS snap behavior
* two cards visible at once
* partial next-card preview

### Important

There must be:

```text
NO PAGE-LEVEL HORIZONTAL SCROLL
```

Only the project rail itself may scroll horizontally.

---

# 8. MOBILE PROJECT CARDS — PERFECT / FREEZE

This is extremely important.

The mobile project cards have gone through several iterations.

The current mobile version is considered **perfect**.

### DO NOT redesign mobile cards during desktop work.

Current mobile card structure:

```text
┌─────────────────────────┐
│ [icon] Project Name     │
│              [STATUS]   │
│                         │
│ Project Category        │
│                         │
│ Short description...    │
│                         │
│    Explore Project ↗    │
└─────────────────────────┘
```

The important hierarchy is:

```text
Project Icon + Project Name
          ↓
Project Status
          ↓
Project Information / Category
          ↓
Short Project Description
          ↓
Explore Project ↗
```

---

# 9. Mobile Project Status Mapping

Current semantic mapping:

| Existing meaning | Display        |
| ---------------- | -------------- |
| Production Ready | **DEPLOYABLE** |
| Running / Live   | **ACTIVE**     |
| In Development   | **ONGOING**    |
| Coming Soon      | **UPCOMING**   |

Color language remains:

```text
DEPLOYABLE → lime
ACTIVE     → emerald
ONGOING    → cyan
UPCOMING   → purple
```

---

# 10. Mobile Project Elements Removed

The following are intentionally removed from mobile:

```text
01
02
03
...
```

Also removed:

```text
React
Node.js
Stripe
etc.
```

and other technology chips.

Also removed:

```text
Production Deployed
```

The mobile card should remain compact and readable.

Bottom action:

```text
Explore Project ↗
```

Only.

---

# 11. Mobile “View All Projects”

At the bottom of the mobile project carousel:

```text
View all projects in DevOps Forge →
```

It was deliberately made smaller/compact.

Keep it that way.

---

# 12. DESKTOP PROJECT SECTION — NEXT TASK

This is where we stopped today.

The current desktop project cards still have older elements that need refinement.

Current desktop screenshot still shows things like:

```text
01
02
03
```

and:

```text
Production Deployed
```

These need to go.

---

# 13. Desktop Changes Required Next

### Remove project numbers

Remove:

```text
01
02
03
...
```

from desktop project cards.

### Remove deployment footer text

Remove:

```text
Production Deployed
```

and equivalent old deployment footer labels.

### Move status to header

Desktop card should have:

```text
[PROJECT ICON] [PROJECT NAME]              [STATUS]
```

The status should be at the **top-right**.

Example:

```text
┌────────────────────────────────────────────┐
│ [icon] Sohail-Shop             [DEPLOYABLE]│
│                                            │
│ Production-Grade E-Commerce...             │
│                                            │
│ Description...                             │
│                                            │
│ [Kubernetes] [AWS EKS] [Terraform] [...]  │
│                                            │
│                         Explore Project ↗   │
└────────────────────────────────────────────┘
```

---

# 14. Desktop — What Must Stay

Unlike mobile, desktop should retain:

### Technology chips

For example:

```text
Kubernetes
AWS EKS
Terraform
Docker
React
TypeScript
Tailwind CSS
...
```

depending on the authentic existing project data.

### Project descriptions

Keep the actual existing descriptions.

### Categories/taglines

Keep them.

### Project links

Keep the existing verified routes.

### Carousel functionality

Keep:

* arrows
* project navigation
* existing interaction
* responsive behavior

---

# 15. Desktop Status

Use the same semantic status system:

```text
Production Ready → DEPLOYABLE
Running / Live   → ACTIVE
In Development   → ONGOING
Coming Soon      → UPCOMING
```

Status should be visually obvious but not overpower the project name.

---

# 16. Desktop Design Goal

The desktop section should feel like:

```text
PROJECTS I'M BUILDING 🚀

┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ icon Name    │ │ icon Name    │ │ icon Name    │
│       STATUS │ │       STATUS │ │       STATUS │
│              │ │              │ │              │
│ category     │ │ category     │ │ category     │
│ description  │ │ description  │ │ description  │
│              │ │              │ │              │
│ tech chips   │ │ tech chips   │ │ tech chips   │
│              │ │              │ │              │
│ Explore ↗    │ │ Explore ↗    │ │ Explore ↗    │
└──────────────┘ └──────────────┘ └──────────────┘
```

Clean, professional, dark, neon-accented, but not overloaded.

---

# 17. Important AI Studio Workflow

When continuing in Google AI Studio, don't simply say:

> “Change the desktop project cards.”

Give Gemini explicit scope.

The prompt should say:

```text
DESKTOP ONLY.

MOBILE PROJECT CARDS ARE ALREADY APPROVED.
DO NOT MODIFY MOBILE.
```

Then tell it exactly what to inspect/change.

Also tell AI Studio:

> Inspect the existing implementation and make the code changes directly. Do not merely describe the solution.

This has worked well in this session.

---

# 18. Visual Design Reference

We generated a visual specification for the desktop project refinement.

The intended desktop header is:

```text
[Project Icon] [Project Name]                    [Project Status]
```

Status at top-right.

No numeric index.

No “Production Deployed”.

Technology chips remain on desktop.

Mobile remains unchanged.

---

# 19. Existing Important Project Data

Do not invent replacements.

Current known project concepts:

### Sohail-Shop

Production-grade e-commerce / multi-vendor platform.

### Sohail Studio

AI engineering / creative workspace.

### Fresh Flow

Fresh grocery delivery / essentials.

### Wedding Page

Digital celebration / wedding experience.

### New Chapter Loading...

Future/placeholder project.

The actual repository data should remain the source of truth.

---

# 20. Git / Asset History — Important Context

During troubleshooting we ran:

```bash
grep -RniE "hero-mobile-master|hero-desktop-master|sohail-hero-master|hero-mobile|hero.*jpg" src public --exclude-dir=node_modules
```

The component had references to:

```text
/hero-mobile-master.jpg
/hero-desktop-master.jpg
```

but the actual files were missing.

Git history showed:

```text
6d326f4 update background v1
ca87b87 update image
df29616 feat: enhance UI and integrate AI dependencies
```

`hero-mobile-master.jpg` was added historically, modified, then deleted.

There was also an accidental attempt to execute:

```text
/Users/sohal/Downloads/hero-mobile-master.jpg
```

which produced:

```text
zsh: permission denied
```

because it was an image file, not a command.

The latest design direction is now one canonical:

```text
/hero-master.jpg
```

But **next session should verify the actual repository state instead of assuming it**, because AI Studio has changed files since the earlier Git inspection.

---

# 21. Git Checkpoint

Earlier we reached:

```text
cc9f220 testing v1
```

and pushed it successfully.

At that point:

```text
main
ahead of origin/main by 1 commit
```

was pushed.

After that, Google AI Studio made additional changes.

Therefore, next session should first check:

```bash
git status
git log --oneline -5
```

and, if necessary:

```bash
git diff --stat
```

Do **not** assume the current Git state is identical to the earlier checkpoint.

---

# 22. Next Session — Exact Starting Point

Start with:

### Step 1

Verify repository:

```bash
git status
git log --oneline -5
```

### Step 2

Verify current hero asset:

```bash
find public -maxdepth 1 -type f | sort | grep -E "hero|photo"
```

### Step 3

Inspect current project component:

```bash
grep -Rni "Projects I'm Building\|PROJECTS I'M BUILDING\|Production Deployed" src
```

Then inspect the relevant component.

### Step 4

Continue **desktop Projects section only**.

Do NOT touch mobile.

---

# 23. After Desktop Projects Are Finished

We should then test:

### Desktop

* Chrome/Safari
* wide screen
* medium desktop
* project cards
* arrows
* links
* technology chips
* status placement
* no numbers
* no deployment footer

### Mobile

Confirm nothing was accidentally changed:

* hero
* hero animation
* tool marquee
* CTA row
* scroll cue
* project cards
* status
* swipe
* arrows
* two-card visibility

---

# 24. Future Homepage Roadmap

Once desktop Projects is approved:

```text
HOME
 │
 ├── Navbar                    ✅
 │
 ├── Cinematic Hero            ✅
 │
 ├── Scroll to Explore         ✅
 │
 ├── Projects I'm Building     🔄 Desktop refinement next
 │
 ├── Stats / Metrics           ⏭
 │
 ├── My Principles             ⏭
 │
 ├── What I Love To Do         ⏭
 │
 ├── Services / Capabilities   ⏭
 │
 ├── Other homepage sections   ⏭
 │
 └── Footer                    ⏭
```

The exact existing section order should be inspected from the repository rather than assumed.

---

# 25. Long-Term Engineering Rule

The homepage redesign is primarily a **frontend/design exercise**.

Do not accidentally modify:

```text
Backend
API
Database
Authentication
Existing routes
Existing project destinations
Other working pages
```

unless there is a real functional reason.

The goal is:

> **Make SohailVerse visually excellent without breaking the engineering foundation underneath it.**

---

## 🧠 One-line resume point for next session

> **“Continue SohailVerse v2.0 homepage redesign from the 4-Sep-2026 checkpoint: mobile Projects section is APPROVED/FROZEN; refine the DESKTOP Projects cards only by removing numeric labels and ‘Production Deployed’, moving the project status to the top-right beside the project name, while preserving authentic data, tech chips, links, carousel behavior, and all mobile behavior.”**
