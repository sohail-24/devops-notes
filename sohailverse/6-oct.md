Absolutely, Mentor. This should be your **single master checkpoint for SohailVerse**. Next time, you can paste this one note into a new session and say **“Mentor, continue from these notes”** instead of explaining the whole portfolio again.

# SOHAILVERSE — MASTER PROJECT CHECKPOINT
**Last updated:** 06 October 2026  
**Project:** SohailVerse v2.0  
**Purpose:** Personal portfolio + project showcase + DevOps laboratory + Cinema + Timeline + Admin CMS  
**Current status:** Active development / production portfolio  
**Main workflow:** Small feature → inspect → implement → test → build → verify → next feature

---

# 1. PROJECT IDENTITY

**SohailVerse** is Sohail's personal portfolio and technical ecosystem.

It is not just a normal resume website. It combines:

- Personal portfolio
- Professional profile
- Projects showcase
- DevOps laboratory
- Technical notes/resources
- Video masterclasses
- Cinema section
- Timeline / About
- Admin CMS / Console
- Project documentation
- Resume/PDF system
- Media management

The project should feel like a **personal technical operating system / digital portfolio**, rather than a basic static portfolio.

---

# 2. TECHNOLOGY STACK

Current architecture:

- **React**
- **TypeScript**
- **Vite**
- **React Router**
- **Cloudflare Pages**
- **Cloudflare Pages Functions**
- **Neon PostgreSQL**
- **Drizzle ORM**
- `/api/*` backend/API routes
- Responsive desktop/tablet/mobile UI

Database:

- Neon PostgreSQL
- Drizzle ORM
- Project data stored persistently
- Rich project content is stored inside the project's database content structure / JSON

Deployment:

- Cloudflare Pages
- Production deployment connected to GitHub
- Repository: SohailVerse project repository
- Cloudflare production domain currently uses the SohailVerse Pages deployment.

---

# 3. IMPORTANT DEVELOPMENT PHILOSOPHY

This is extremely important for future work.

## Always work in small upgrades

Do **NOT** ask AI Studio to make huge changes across the whole project.

Preferred process:

```text
1. Identify ONE feature/problem
2. Inspect existing implementation
3. Trace the actual data flow
4. Change only required files
5. Build
6. Test the feature
7. Verify desktop + mobile
8. Verify existing functionality
9. Only then start the next feature
```

AI Studio prompts should be:

- Small
- Specific
- Explicit
- Limited in scope
- Clear about files
- Clear about what must NOT change
- Clear acceptance criteria

Avoid broad prompts such as:

> "Upgrade the entire project."

Instead:

> "Fix only the video playback in ProjectInformationPage.tsx. Do not modify gallery layout."

---

# 4. LOCAL PROJECT

SohailVerse local project path:

```text
/Users/sohal/Downloads/testing-project/sohailverse
```

For larger/local repository work, **Codex** is preferred when practical.

Google AI Studio is useful for small focused modifications, especially when working directly in the AI Studio project.

---

# 5. MAIN ROUTES

Core routes:

```text
/
├── Mission Control / Home
│
├── /projects
│   └── /projects/:id
│
├── /devops
│   └── /devops/:id
│
├── /cinema
│
├── /timeline
│   └── /about
│
├── /dashboard
│
└── /admin
    └── /console
```

---

# 6. DOMAIN SEPARATION — VERY IMPORTANT

SohailVerse has strict separation between **Projects** and **DevOps**.

## Projects

`/projects`

Contains:

- Portfolio projects
- Project overview
- Project screenshots
- Project videos
- README/PDF documentation
- Architecture diagrams
- External links
- Live project links
- Project-specific media

## DevOps

`/devops`

Contains:

- DevOps resources
- Notes
- Networking
- AWS
- DevOps
- Learn & Test
- Technical videos
- PDFs
- Technical resources

### NEVER mix them accidentally.

A DevOps note/video/resource should not randomly appear inside Projects.

A Project's screenshots/videos/docs should not be injected into DevOps.

If a future feature causes data leakage between these areas, fix the **data pipeline/source**, not by hiding things with CSS.

---

# 7. PROJECTS SYSTEM

Projects are intentionally independent from DevOps.

Main routes:

```text
/projects
/projects/:id
```

A project detail page behaves like a **technical project dossier**.

It can contain:

- Project title
- Status
- Category
- Tagline
- Description
- Project gallery
- Videos
- README/documentation
- PDF documents
- Architecture diagrams
- External links
- Live application
- Other project metadata

Project detail data is loaded from the database and hydrated through the existing project data layer.

Important existing concepts:

```text
loadUnifiedProjects()
fetchProjectDetailsById()
```

Database project content is persisted in the project record's rich content/highlights structure.

---

# 8. ADMIN / CONSOLE

Admin route:

```text
/admin
```

The Admin Console is the CMS/control center for SohailVerse.

It manages:

### Projects

- Project metadata
- Project content
- Images
- Videos
- Documents
- PDFs
- Architecture
- Links
- Overview
- Tagline
- Hero/media

### Cinema

Cinema content management.

### DevOps

DevOps resources and technical content.

The admin system is authenticated.

---

# 9. PROJECT CONTENT MANAGER

The Project Content Manager is one of the most important parts of the current system.

It supports project content such as:

```text
Overview / Meta
Gallery
Video Sessions
Documents
Architecture
Links
```

The admin can configure project content without manually editing database records.

Project content is persisted through the existing project API/data system.

---

# 10. PROJECT IMAGE UPLOAD

Project gallery images support:

```text
Upload from Device
```

Images are stored persistently rather than being temporary browser-only files.

The admin can configure image slots and enable/disable content.

The project page then displays the configured images.

---

# 11. PROJECT VIDEO UPLOAD

Video upload was recently added.

Admin:

```text
/admin
→ Project
→ Manage Content
→ Video Sessions
→ Upload from Device
```

Supported direct video types include browser-compatible formats such as:

- MP4
- WebM
- MOV
- OGG
- other supported browser video formats

The project media pipeline supports persistent video storage.

Current architecture:

```text
Admin
 ↓
Upload from Device
 ↓
/api/project-media
 ↓
Neon PostgreSQL project_media
 ↓
/api/project-media/:id
 ↓
Project detail page
```

The API also supports HTTP range requests so videos can:

- Seek
- Scrub
- Stream smoothly
- Work on desktop/mobile

---

# 12. PROJECT VIDEO TYPES

The system now needs to support **both**:

### A. Uploaded/direct videos

Examples:

```text
/api/project-media/:id
.mp4
.webm
.mov
.ogg
```

These use HTML5:

```html
<video controls playsInline>
```

### B. External videos

Examples:

```text
YouTube
Vimeo
```

These use an appropriate iframe/embed source.

Important lesson from the recent work:

A YouTube watch URL cannot simply be treated as a direct HTML5 video.

Example:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

needs to resolve to an embed source such as:

```text
https://www.youtube.com/embed/VIDEO_ID
```

before being used in the iframe.

---

# 13. PROJECT GALLERY — CURRENT FINAL DESIGN

This was the major feature completed today.

The project detail page now has a unified top media gallery.

Desired structure:

```text
┌──────────────────────────────────────────┐
│                                          │
│              MAIN MEDIA BOX              │
│                                          │
│      Image / Image / Actual Video        │
│                                          │
└──────────────────────────────────────────┘

Project Gallery (3 items)

[ 1 Image ] [ 2 Image ] [ 🎬 3 Video ]
```

For a project with two images and one video:

```text
Image 1
Image 2
Video
```

are all part of **one gallery**.

---

# 14. PROJECT GALLERY BEHAVIOR

Gallery navigation:

```text
Image 1
   ↕
Image 2
   ↕
Video
   ↕
Image 1
```

Users can:

- Click image thumbnail
- Click video thumbnail
- Use left/right navigation arrows
- View image in the main media box
- View/play video in the same main media box

The video must NOT appear as a separate unrelated box below the gallery.

---

# 15. VIDEO PLAYBACK — CURRENT FINAL BEHAVIOR

When the third gallery item is selected:

```text
🎬 Video
```

the **actual video must appear inside the existing main gallery media box**.

If YouTube:

```text
YouTube embed player
```

If Vimeo:

```text
Vimeo embed player
```

If uploaded MP4:

```text
HTML5 video player
```

The user can then:

- Play
- Pause
- Seek
- Use video controls
- Fullscreen where supported

The video should not autoplay unless specifically requested in a future feature.

---

# 16. LOWER VIDEO SESSIONS SECTION

Important architectural decision:

The uploaded/gallery video should **NOT be duplicated** in the lower Video Sessions section.

The current behavior is:

```text
TOP PROJECT GALLERY
    ↓
Image 1
Image 2
Video
```

Then lower on the page:

```text
Video Sessions
```

should only contain **additional/external walkthrough sessions** that are not already represented in the top gallery.

This prevents:

```text
Same Video
↓
Top Gallery
↓
Again at bottom
```

---

# 17. VIDEO SESSION DATA

Project video sessions use project content data.

Conceptually:

```text
ProjectVideoSession
```

supports fields such as:

- id
- title
- video_url
- duration
- summary
- showInProjectGallery

`showInProjectGallery` was added to clearly identify videos that belong in the top gallery.

---

# 18. CURRENT PROJECT GALLERY MEDIA MODEL

The top gallery uses a unified media representation similar to:

```text
ProjectGalleryMediaItem
```

with:

```text
type: "image" | "video"
url
title
thumbnailUrl
duration
```

This allows images and videos to share the same gallery UI.

This architecture should be **reused** for future media features instead of creating a second gallery system.

---

# 19. IMPORTANT VIDEO DEBUGGING LESSON

During implementation, the gallery existed but the video displayed:

```text
Video unavailable
```

The root cause was not the gallery.

The issue was video source resolution.

The final fix was to inspect the actual:

```text
galleryVideoSession.video_url
```

and determine whether it was:

```text
YouTube
Vimeo
Direct/uploaded video
```

Then use the correct player.

This is an important future debugging principle:

> **Trace the actual data first. Do not blindly modify the UI.**

---

# 20. PROJECT MEDIA API

Current project media API:

```text
/api/project-media
/api/project-media/:id
```

The POST endpoint handles media uploads.

The GET endpoint serves stored media.

Video streaming supports:

```text
Accept-Ranges: bytes
```

and:

```text
HTTP 206 Partial Content
```

for range requests.

This is important for video seeking/scrubbing.

---

# 21. RESUME PAGE

Route:

```text
/resume
```

The resume page is already visually correct on the website.

Recent work focused on fixing the **download/print/mobile viewer**, without changing the actual resume content/design.

Files recently involved:

```text
scripts/generate-resume-pdf.ts
src/pages/ResumePage.tsx
```

---

# 22. RESUME PDF CURRENT STATE

Previously:

- Text became too small in downloaded PDF
- Print sometimes produced 3 pages
- Resume should remain approximately 2 pages

Recent changes:

- Increased PDF body text size
- Improved line height
- Improved section heading sizes
- Fixed print page-break handling
- Fixed A4 sizing
- Verified exactly 2 PDF pages
- Build succeeded

Current target:

```text
Resume PDF = exactly 2 pages
```

Do not unnecessarily redesign the resume.

---

# 23. RESUME MOBILE / TOUCH VIEWER

The resume viewer needed to work correctly on:

- Desktop
- Laptop
- Tablet
- Phone
- Touchscreen

Required behavior:

### Normal zoom

A4 page should be centered.

```text
[ dark space ][ A4 resume ][ dark space ]
```

### Zoomed

User must be able to pan:

```text
← left / right →
↑ up / down ↓
```

The document must not be clipped.

Touch scrolling/panning must work.

This was fixed by adjusting:

- Overflow behavior
- A4 scaler
- Transform origin
- Responsive stage sizing
- Horizontal/vertical scrolling

---

# 24. RESUME PDF BUILD

Current build pipeline includes PDF generation.

The build was verified successfully using the project build process.

Important:

Do not change resume PDF architecture unless there is a specific issue.

---

# 25. PACKAGE MANAGER / CLOUDFLARE ISSUE

A recent Cloudflare deployment failed because an old:

```text
bun.lock
```

was present.

Cloudflare detected:

```text
bun@1.2.15
```

and attempted:

```text
bun install --frozen-lockfile
```

but the lockfile used an unsupported old version:

```text
lockfileVersion: 2
```

This produced:

```text
UnknownLockfileVersion
```

The project was subsequently migrated toward npm/package-lock handling.

Recent AI Studio output confirmed:

- `bun.lock` removed
- `package-lock.json` generated
- npm build verified successfully

Future deployment issue diagnosis should check:

```text
package.json
package-lock.json
bun.lock
Cloudflare build settings
```

before assuming application code is broken.

---

# 26. CLOUDflare DEPLOYMENT

Production deployment:

```text
Cloudflare Pages
```

Connected to GitHub.

The production pipeline has previously successfully deployed commits.

When deployment fails, inspect:

```text
1. Clone
2. Package manager detection
3. Dependency installation
4. Build command
5. Functions
6. Deploy
```

Do not immediately change application code if the failure occurs during dependency installation.

---

# 27. DATABASE

Primary persistent database:

```text
Neon PostgreSQL
```

ORM:

```text
Drizzle
```

Important project data is persisted in Neon.

The project CMS should not rely on temporary browser state for permanent content.

Recent video work confirmed the project media pipeline stores uploaded media persistently.

---

# 28. PROJECT DATA CACHING

Project details use caching/data-loading helpers.

Recent bug:

The public project page could show stale project content because the data loader was not forcing a refresh.

The solution included:

```text
forceRefresh: true
```

where required and cache invalidation after admin content changes.

Future CMS bugs should consider:

```text
Database persistence
↓
API response
↓
cache
↓
frontend state
↓
render
```

rather than assuming the UI alone is wrong.

---

# 29. ADMIN CONTENT SAVE FLOW

General flow:

```text
Admin
 ↓
Edit Content
 ↓
Local form state
 ↓
Save All Changes
 ↓
API
 ↓
Neon PostgreSQL
 ↓
Cache invalidation
 ↓
Public Project Page
 ↓
Fresh project data
```

If something saves in Admin but does not appear publicly, inspect this entire pipeline.

---

# 30. DEVOPS LABORATORY

DevOps section:

```text
/devops
```

Current pillars include:

- Notes
- Networking
- AWS
- DevOps
- Learn & Test

The project also supports technical learning resources such as:

- PDFs
- Videos
- Notes
- Technical resources

Recent admin work added/expanded media upload functionality for DevOps resources as well.

---

# 31. DEVOPS NOTES

Admin Console supports DevOps resource management.

The user previously requested:

```text
Upload from Device
```

for notes/resources.

This follows the same general persistent-media philosophy.

Do not mix these resources with Project content.

---

# 32. CINEMA

Route:

```text
/cinema
```

Cinema is another independent domain in SohailVerse.

It should remain isolated from:

- Projects
- DevOps

---

# 33. TIMELINE / ABOUT

Routes:

```text
/timeline
/about
```

This area contains the personal/professional timeline and CV/resume-related content.

Recent work included updating the Curriculum Vitae/resume box sizing.

The timeline/about design should remain visually consistent with the overall SohailVerse identity.

---

# 34. DESIGN LANGUAGE

Overall design direction:

- Dark
- Technical
- Futuristic
- Minimal
- Cyan/green accent
- Terminal/engineering aesthetic
- Responsive
- Professional
- Strong visual hierarchy

The UI should feel like:

```text
Personal OS
+
DevOps Lab
+
Technical Portfolio
```

rather than a generic corporate template.

---

# 35. MOBILE-FIRST CONSIDERATION

Every future feature must be tested on:

```text
Desktop
Laptop
Tablet
Phone
Touchscreen
```

Especially important for:

- Galleries
- Video players
- Admin modals
- PDF viewers
- Navigation
- Horizontal scrolling
- Upload controls

Avoid introducing:

```text
horizontal page overflow
```

unless it is intentionally required for something such as a zoomed document.

---

# 36. ADMIN UI PRINCIPLE

Admin UI should be powerful but clean.

For upload features:

```text
Upload from Device
```

should be obvious.

Whenever possible, show:

- Preview
- File information
- Enabled/disabled state
- Replace
- Clear/delete
- Save All Changes

Do not create multiple confusing upload systems for the same type of content.

---

# 37. PROJECT MEDIA FUTURE EXTENSIONS

Because the project now has a unified media architecture, future media features should preferably extend:

```text
ProjectGalleryMediaItem
```

rather than creating a completely separate gallery.

Potential supported media concepts already emerging:

```text
Image
Video
```

If another media type is ever added, inspect the existing gallery/data architecture first.

---

# 38. IMPORTANT EXISTING PROJECT CONTENT

Some screenshots during development showed an older project such as:

```text
AM Fruits / Fresh Flow
```

This is existing project data/content used during testing and portfolio management.

Do not assume screenshots showing old project data mean the SohailVerse architecture should be rebuilt around that project.

The architecture is the important part.

---

# 39. WHAT NOT TO DO

Future AI Studio/Codex prompts should explicitly avoid:

### Do not:

- Rewrite the entire portfolio
- Refactor unrelated components
- Replace the database
- Replace Neon
- Replace Cloudflare
- Create unnecessary tables
- Create duplicate media systems
- Break Project/DevOps separation
- Change the resume design when fixing PDF mechanics
- Rebuild working gallery logic
- Duplicate videos
- Put uploaded gallery videos back into the lower Video Sessions section
- Change unrelated routes
- Modify unrelated admin pages
- Make large changes because of one small bug

---

# 40. CURRENT VERIFIED STATE — 06 OCTOBER 2026

### SohailVerse

```text
Core architecture             ✅
React + TypeScript + Vite     ✅
Cloudflare Pages              ✅
Pages Functions               ✅
Neon PostgreSQL               ✅
Drizzle ORM                   ✅
React Router                  ✅
Admin Console                 ✅
Projects CMS                  ✅
DevOps CMS                    ✅
Cinema                        ✅
Timeline/About                ✅
```

### Projects

```text
/projects                     ✅
/projects/:id                 ✅
Project gallery               ✅
Project images                ✅
Project documents             ✅
Project links                 ✅
Project architecture         ✅
Project videos                ✅
Video upload                  ✅
Persistent media              ✅
Top gallery video             ✅
YouTube playback              ✅
Video controls                ✅
No duplicate gallery video    ✅
```

### Resume

```text
/resume                       ✅
PDF generation                ✅
2-page PDF                    ✅
Readable PDF text             ✅
Print pagination              ✅
Mobile zoom                   ✅
Horizontal panning            ✅
Vertical panning              ✅
Centered A4 viewer            ✅
```

### Deployment/package

```text
Old bun.lock issue identified ✅
bun.lock removed              ✅
npm lockfile                  ✅
Local build                   ✅
TypeScript check              ✅
```

---

# 41. CURRENT PROJECT FILES THAT ARE IMPORTANT

Recent work has involved:

```text
src/pages/ProjectInformationPage.tsx

src/components/admin/ProjectContentManagerModal.tsx

src/lib/projectContent.ts

functions/api/project-media/index.ts

functions/api/project-media/[id].ts

vite.config.ts

src/pages/ResumePage.tsx

scripts/generate-resume-pdf.ts
```

Do not modify all of these for every future task.

First identify the smallest relevant file set.

---

# 42. FUTURE FEATURE WORKFLOW

When starting a new feature, use this exact process:

```text
SOHAILVERSE FEATURE WORKFLOW

1. Read this master checkpoint.

2. Identify the exact route/page.

3. Identify whether the feature belongs to:
   - Projects
   - DevOps
   - Cinema
   - Timeline
   - Admin
   - Resume

4. Inspect existing implementation.

5. Trace data:
   UI
   ↓
   state
   ↓
   API
   ↓
   database
   ↓
   API response
   ↓
   UI

6. Make ONE focused change.

7. Do not modify unrelated systems.

8. Run build.

9. Test desktop.

10. Test mobile.

11. Test existing functionality.

12. Only after verification start another feature.
```

---

# 43. MASTER AI STUDIO PROMPT STYLE

For future AI Studio sessions, use this structure:

```text
Mentor task:

[ONE CLEAR FEATURE]

CURRENT STATE:
[what already works]

PROBLEM:
[exact problem]

GOAL:
[exact expected behavior]

FILES TO INSPECT:
[file names]

IMPORTANT:
- Do not change unrelated features.
- Reuse the existing architecture.
- Do not create duplicate systems.
- Preserve current UI unless specifically requested.
- Keep desktop/mobile behavior working.

IMPLEMENTATION:
[small focused instructions]

ACCEPTANCE TEST:
1. ...
2. ...
3. ...

BUILD:
npm run build

STOP after completing this task.
```

This style matches your preferred workflow and reduces AI Studio quota usage.

---

# 44. MASTER RULE FOR FUTURE AI

The most important instruction for future sessions:

> **Do not assume. Inspect the existing code and trace the real data flow first.**

This became especially important with the Project Gallery video work.

The UI appeared correct, but the actual problem was the video source/URL resolution.

So future debugging should follow:

```text
Symptom
 ↓
Inspect component
 ↓
Inspect state
 ↓
Inspect API
 ↓
Inspect database data
 ↓
Identify root cause
 ↓
Minimal fix
 ↓
Build
 ↓
Verify
```

---

# 45. CURRENT PROJECT PHILOSOPHY

SohailVerse should continue evolving as a **modular personal technical platform**.

The architecture should remain:

```text
                    SOHAILVERSE
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
   Portfolio          DevOps            Personal
       │                 │                 │
   Projects          Laboratory        Timeline
       │                 │                 │
   Project CMS       Notes             About
   Gallery           Videos            Resume
   Videos            PDFs
   Docs              Resources
   Links
       │
       └──────────────┐
                      │
                 Admin CMS
                      │
              Neon PostgreSQL
                      │
              Cloudflare Pages
```

---

# 46. MOST IMPORTANT CURRENT FEATURE: PROJECT MEDIA

The latest major upgrade is now:

```text
Admin
 ↓
Manage Project Content
 ↓
Video Sessions
 ↓
Upload from Device
 ↓
Persistent storage
 ↓
Project Gallery
 ↓
Image 1 | Image 2 | 🎬 Video
 ↓
Select Video
 ↓
Actual playable video
```

This is now the **reference implementation** for project video/gallery behavior.

Future changes should build on this rather than replacing it.

---

# 47. FINAL CHECKPOINT

### As of 06 October 2026:

**SohailVerse is in a stable feature-development state.**

The most recent work successfully completed:

1. Resume PDF readability improvement.
2. Resume PDF pagination fixed to 2 pages.
3. Resume mobile/touch zoom and 2D panning fixed.
4. Resume A4 viewer centering fixed.
5. Package manager/deployment lockfile issue resolved.
6. Admin Project Content Manager gained device video upload.
7. Project media API supports persistent video storage.
8. Video streaming supports range requests.
9. Project detail gallery supports images + video.
10. Video appears as the third gallery item.
11. Video uses the same main media box as images.
12. YouTube/external video playback was fixed.
13. Uploaded/direct video playback is supported.
14. Gallery navigation works:
   
```text
Image 1 ↔ Image 2 ↔ Video
```

15. Gallery video is not duplicated in the lower Video Sessions section.
16. Build/type checks have been successfully verified after the latest changes.

---

## 🚀 NEXT SESSION START PROMPT

When you open a new ChatGPT/AI Studio session, you can paste this entire note and simply say:

> **“Mentor, these are my latest SohailVerse master notes. Read them completely and use them as the project baseline. Do not ask me to explain the project again. I want to work on one small feature at a time. First inspect the existing implementation, then make only the requested change, preserve all working features, test desktop/mobile, and run the build before considering the task complete.”**

Then tell me the **one new feature** you want to work on.

This note can be your **SohailVerse Master Checkpoint v1.0**.
