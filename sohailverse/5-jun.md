# SOHAILVERSE PROJECT - CURRENT STATUS NOTES

Date: 05 June 2026

## Project Overview

Project Name: SohailVerse

Purpose:
Personal portfolio and content platform combining:

* Movies Collection
* Travel Journals
* Learning Notes
* Blog
* Dashboard

Tech Stack:

Frontend:

* React
* TypeScript
* Tailwind CSS
* React Router

Animation:

* GSAP
* ScrollTrigger

Deployment Target:

* Cloudflare Pages

Future Backend:

* Cloudflare Workers

Future Database:

* Cloudflare D1

Domain:

* sohaildevops.site

---

# Current Homepage Structure

HomePage.tsx contains:

1. HeroSection
2. MovieCollectionSection
3. GenreSection
4. CuratedSection
5. FeaturedSection
6. TravelSection
7. LearningSection
8. QuoteSection
9. BlogHubSection
10. ContactSection

Most sections use:

* GSAP Timeline
* ScrollTrigger
* Pinning
* Scrubbing

Several sections are full-screen sections.

---

# Important Files

## src/App.tsx

Responsible for:

* Routes
* Global ScrollTrigger setup
* Global Snap System
* Navbar
* Footer

Important code:

gsap.registerPlugin(ScrollTrigger)

Contains:

setupGlobalSnap()

Purpose:

Automatically snap scroll position between pinned sections.

Current status:

Enabled.

Potential source of bug.

---

## src/pages/HomePage.tsx

Main homepage.

Contains all GSAP animations.

Important sections:

HeroSection
MovieCollectionSection
GenreSection
CuratedSection
FeaturedSection
TravelSection
LearningSection
QuoteSection

Many sections use:

pin: true

and

scrub: 0.6

---

## src/components/Navbar.tsx

Reviewed.

Navbar is NOT causing the issue.

Navbar contains:

* Desktop menu
* Mobile menu
* Scroll background effect
* Active route highlighting

No issue found.

---

# Main Problem We Are Debugging

Issue:

When navigating and scrolling:

* Animations break
* Homepage behaves incorrectly
* GSAP state becomes unstable
* Browser console shows DOM-related errors

Example:

Failed to execute 'removeChild'

and other animation-related issues.

---

# Things We Checked

## 1. GSAP Registration

Checked:

App.tsx

and

HomePage.tsx

Both contain:

gsap.registerPlugin(ScrollTrigger)

Result:

Not the problem.

---

## 2. Navbar

Reviewed entire Navbar.tsx.

Result:

Not the problem.

---

## 3. HeroSection Cleanup

Original code:

return () => {
ScrollTrigger.getAll().forEach((st) => st.kill());
ctx.revert();
};

Reason:

This kills ALL ScrollTriggers globally.

We suspected:

HeroSection unmount
↓
Kills all triggers
↓
Breaks other sections

Result:

Removing it did NOT completely solve issue.

Still under investigation.

---

## 4. HeroSection pinSpacing

Found:

pinSpacing: false

while

pin: true

was commented.

Potential GSAP conflict.

Tested.

Result:

Issue still exists.

---

## 5. Global Snap System

Located in:

App.tsx

Function:

setupGlobalSnap()

Creates:

snapTrigger

Uses:

ScrollTrigger.getAll()

Collects:

all pinned sections

Creates:

scroll snapping behavior

Suspected issue:

Snap system may conflict with route changes and pinned sections.

Status:

Needs further testing.

---

# Current Suspicious Areas

Most suspicious files now:

1. src/App.tsx
2. src/pages/HomePage.tsx
3. MoviesPage.tsx
4. ScrollToTop component (if exists)
5. Any custom route transition code

---

# Files Mentor Must Review Tomorrow

Before continuing tomorrow, provide:

1. src/App.tsx
2. src/pages/HomePage.tsx
3. src/pages/MoviesPage.tsx
4. ScrollToTop.tsx (if exists)
5. Browser console error screenshot
6. Exact error message after refresh

These are highest priority files.

---

# What We Learned Today

* Navbar is healthy.
* Routing appears mostly correct.
* GSAP plugin registration is correct.
* Multiple pinned sections exist.
* Global Snap system may be causing conflicts.
* HomePage contains many independent ScrollTriggers.
* Root cause has NOT yet been identified.

---

# Tomorrow's Goal

Step 1:
Review App.tsx again.

Step 2:
Review MoviesPage.tsx.

Step 3:
Check ScrollToTop implementation.

Step 4:
Capture exact browser console error.

Step 5:
Find the real source of removeChild / ScrollTrigger issue.

Step 6:
Stabilize homepage animations.

Goal:

Homepage animations work smoothly without breaking during navigation between routes.

END OF NOTES
