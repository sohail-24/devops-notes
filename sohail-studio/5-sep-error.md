
---

# 1. Where We Started

We discovered that the newer AI Studio changes had moved the project away from the state we wanted.

The important Git history was:

```text
4eaa783  ← AI Studio changes we rejected
ea55240  ← AI Studio changes we rejected
0a77e5e  ← Node 22 declaration
504876b
dd3f45d  ← Python/FastAPI → Node.js/Express migration
af3ef9c  ← Runtime evidence
e334074
9ab723c
7cd9226  ← OUR RECOVERY BASELINE
```

We determined that **`7cd9226` is the correct recovery point**.

Important correction:

> `7cd9226` is NOT just a documentation commit.

It contains the major Python → Node.js migration.

It removed the old Python backend architecture and established the Node/Express architecture.

---

# 2. Why We Created a Recovery Branch

We did **not** want to experiment directly on `main`.

So we created:

```bash
git switch -c recovery-7cd9226
git push -u origin recovery-7cd9226
```

Therefore:

```text
GitHub
│
├── main                    ← newer history, DON'T TOUCH
│
└── recovery-7cd9226        ← SAFE BASELINE
                              │
                              └── 7cd9226
```

This is extremely important.

### Our rule from now on

**Never experiment directly on `main`.**

Our working flow should be:

```text
recovery-7cd9226
       ↓
make controlled changes
       ↓
test
       ↓
review diff
       ↓
commit
       ↓
push recovery branch
       ↓
only later decide what goes to main
```

---

# 3. What Was Wrong Before Restoration

At the recovered `7cd9226` state, the UI was saying:

```text
Ollama
devops-qwen:v1
```

but the Node server was actually doing something different.

The old Node Chat path was roughly:

```text
Browser
   ↓
/ws/chat
   ↓
Gemini
   ↓
gemini-2.5-flash
```

and if Gemini wasn't available, it could fall back to a static/local mentor response.

That violated our architecture.

We specifically did **not** want:

```text
Chat
 ↓
Gemini
 ↓
cloud
```

or:

```text
Chat
 ↓
hardcoded answer
```

We wanted:

```text
Chat
 ↓
Control Plane
 ↓
real local evidence
 ↓
Ollama
 ↓
devops-qwen:v1
```

---

# 4. The Old Python Control Plane Was Our Reference

We inspected the architecture that existed before the migration.

The historical Control Plane had seven read-only tools:

```text
1. local_time
2. workspace_pwd
3. workspace_ls
4. project_files
5. docker_read
6. git_read
7. kubernetes_read
```

The important thing is:

**We are NOT restoring Python.**

We are restoring the **behavior**, not the old Python architecture.

So:

```text
OLD
Python ControlPlane
        ↓
FastAPI
```

becomes:

```text
NEW
TypeScript ControlPlane
        ↓
Node / Express
```

---

# 5. What AI Studio Just Implemented

According to the AI Studio report, it changed five files.

### Created

```text
core/control_plane.ts
core/ollama_output.ts
test_control_plane.ts
```

### Modified

```text
server.ts
test_runtime_evidence.ts
```

That is a controlled scope.

---

# 6. New Control Plane Architecture

This is the most important part.

The intended architecture is:

```text
                 USER
                   │
                   ▼
             Sohail Studio UI
                   │
                   │ /ws/chat
                   ▼
            Node / Express
                   │
                   ▼
          ┌──────────────────┐
          │   Control Plane  │
          │                  │
          │ READ ONLY ONLY   │
          └──────────────────┘
             │    │    │
      ┌──────┴────┴────┴───────┐
      │                         │
      ▼                         ▼
 local_time              project_files
 workspace_pwd           docker_read
 workspace_ls            git_read
                         kubernetes_read
      │
      ▼
LOCAL FACTUAL EVIDENCE
      │
      ▼
Ollama HTTP API
      │
      ▼
devops-qwen:v1
      │
      ▼
stream response
      │
      ▼
Browser
```

This is what we wanted.

---

# 7. Control Plane's Most Important Rule

The Control Plane is **not an agent that executes whatever the AI asks.**

It is an evidence layer.

For example:

User:

> What is today's date?

Control Plane:

```text
local_time
```

gets the actual system clock.

Then:

```text
date = 2026-09-15
time = ...
day = Tuesday
timezone = ...
```

gets supplied to Ollama.

So the model doesn't need to guess.

---

# 8. Your Screenshot Proves One Important Thing

You asked:

> `find sms folder`

The Chat responded that it checked the workspace and:

> there is no `sms` folder present.

This is exactly the behavior we want.

It should NOT say:

```text
I think your SMS folder is here:
/Users/.../sms
```

It should NOT hallucinate.

Instead:

```text
inspect actual workspace
        ↓
no sms folder
        ↓
tell user factual result
```

That's the **evidence-bound philosophy** of Sohail Studio.

---

# 9. Local Time Is Now Dynamic

AI Studio reports:

```text
local_time
```

uses:

```text
new Date()
```

instead of a hardcoded date.

Your screenshot shows:

```text
Tuesday, September 15, 2026
13:20
UTC+05:30
Calcutta time
```

This is a very good validation.

Previously we had seen stale/static responses such as:

```text
October 26, 2023
```

That problem is now addressed by the Control Plane.

---

# 10. Chat Model

The intended Chat model is:

```text
devops-qwen:v1
```

This is important.

### Chat

```text
devops-qwen:v1
```

### Sohail-Agent

```text
devops-qwen:latest
```

Keep these separate.

```text
                 SOHAIL STUDIO

       ┌─────────────────────────┐
       │          CHAT           │
       │                         │
       │   Control Plane         │
       │          ↓              │
       │   devops-qwen:v1        │
       └─────────────────────────┘


       ┌─────────────────────────┐
       │      SOHAIL-AGENT       │
       │                         │
       │   Agent workflows       │
       │          ↓              │
       │   devops-qwen:latest    │
       └─────────────────────────┘
```

Do **not** merge these models.

---

# 11. Ollama Connection

The intended endpoint is:

```text
http://localhost:11434
```

Chat calls:

```text
/api/chat
```

So the real flow on your Mac is:

```text
Safari
   ↓
localhost:3000
   ↓
Node server
   ↓
localhost:11434
   ↓
Ollama
   ↓
devops-qwen:v1
```

This is completely local.

---

# 12. Very Important: AI Studio Sandbox vs Your Mac

AI Studio correctly reported something important.

Its cloud/sandbox environment **cannot prove that your Mac's Ollama is working**.

It tested:

```text
AI Studio Sandbox
        ↓
localhost:11434
```

and Ollama wasn't there.

That is expected.

Your actual machine is:

```text
Your Mac
   ↓
localhost:11434
   ↓
Ollama
   ↓
devops-qwen:v1
```

We already separately verified that your Mac's Ollama is healthy.

Therefore:

### AI Studio can verify code architecture.

### Your Mac must verify real Ollama connectivity.

This distinction is important for our engineering evidence.

---

# 13. Read-Only Safety

The Control Plane must remain **READ ONLY**.

It can inspect:

```text
pwd
files
directories
Docker status
Git status
Git branch
Git log
Kubernetes configuration
local time
```

It must NOT allow Chat to perform:

```text
rm
mv
cp
mkdir
touch
write
delete

git commit
git push
git checkout

docker build
docker run
docker rm

kubectl apply
kubectl delete

npm install
```

etc.

---

# 14. Chat Must Never Become a Shell

This is a critical architecture boundary.

We do NOT want:

```text
User
 ↓
LLM
 ↓
"run this command"
 ↓
shell
```

That would make Chat dangerous.

Instead:

```text
User
 ↓
Control Plane
 ↓
approved read-only tool
 ↓
factual evidence
 ↓
LLM
 ↓
text response
```

The **Terminal** remains the place where actual commands can be executed.

---

# 15. Terminal Must Stay Separate

Current architecture:

```text
CHAT
 └── Control Plane
      └── Read-only
           └── Ollama

TERMINAL
 └── PTY
      └── Real shell
           └── command execution
```

Do not merge these.

The AI Studio report explicitly says Terminal remains untouched.

Good.

---

# 16. Dockerize Is NOT Our Current Task

This is extremely important.

We previously discovered that Dockerize had a dangerous problem:

```text
Target runtime: Node.js 22
node:22-alpine
```

was hardcoded.

That violated our:

> **NO GUESSING**

rule.

We decided Dockerize needs to become:

```text
Evidence
   ↓
Inspector
   ↓
Dockerize
   ↓
only use verified information
```

If required evidence is missing:

```text
NEEDS_EVIDENCE
```

Not:

```text
Node 22
node:22-alpine
port 3000
```

unless those are actually supported by repository evidence.

---

# 17. AI Studio Says Dockerize Was Untouched

The new AI Studio report says:

```text
Dockerize: Unchanged
Inspector: Unchanged
Terminal: Unchanged
Sessions: Unchanged
Sohail-Agent: Unchanged
```

That is what we requested.

So **do not start changing Dockerize now**.

We finish the Chat restoration first.

---

# 18. Tests AI Studio Added

AI Studio reports Control Plane tests for:

```text
local_time
workspace_pwd
workspace_ls
project_files
missing file handling

Chat model
Sohail-Agent model
Ollama URL
Ollama override
transport
Gemini absence
static fallback absence
Ollama error handling

shell safety
docker read-only
git read-only
kubernetes read-only

multi-tool routing
Ollama output cleaning
```

That is a strong test scope.

It reports:

```text
ALL AI CONTROL PLANE & OLLAMA TESTS PASSED
Exit Code: 0
```

And:

```text
npm run lint
PASS
```

And:

```text
npm run build
PASS
```

---

# 19. BUT — One Thing We Must Verify

This is the important Mentor warning.

AI Studio's report says:

```text
Current Sohail Studio repository declares engines.node = 22
```

and:

```text
DOCKERIZE TEST A
Current repository selects node:22
```

But our chosen recovery point was:

```text
7cd9226
```

and we intentionally rolled back the later:

```text
0a77e5e
chore: specify Node.js 22 in package.json
```

So I do **not** want us to blindly accept that statement.

This may be because AI Studio's workspace started from a different `main` state.

Therefore:

> **AI Studio's report is not automatically the same as the state of your local `recovery-7cd9226` branch.**

This is exactly why we created the recovery branch.

---

# 20. AI Studio Only Having `main` Is Not a Problem

You said:

> AI Studio only has main branch.

That's okay.

AI Studio's branch view and your local Git repository are not something we should treat as the same working state.

Our safe structure is:

```text
GitHub
│
├── main
│
└── recovery-7cd9226
       ↑
       │
       OUR SAFE DEVELOPMENT BASELINE
```

AI Studio:

```text
AI Studio
└── main
```

We can use AI Studio as a **code-editing assistant**, but our Git repository remains the source of truth.

### Rule:

**Never let AI Studio's `main` state override our recovery branch without reviewing the diff.**

---

# 21. What We Should Do With AI Studio's Changes

Do NOT:

```text
git add .
git commit
git push main
```

Do NOT overwrite the recovery branch blindly.

Instead:

```text
AI Studio changes
       ↓
bring changed files into local recovery branch
       ↓
git diff
       ↓
inspect every change
       ↓
test
       ↓
real Mac Ollama test
       ↓
commit
       ↓
push recovery-7cd9226
```

The expected changed files are:

```text
core/control_plane.ts
core/ollama_output.ts
server.ts
test_control_plane.ts
test_runtime_evidence.ts
```

We should verify that **only the intended changes** are present.

---

# 22. Current Phase

I would officially mark us here:

## 🟢 Phase 1 — Node.js Foundation

**COMPLETE**

```text
Python/FastAPI
       ↓
Node/TypeScript/Express
```

---

## 🟢 Phase 2 — Runtime Evidence

**COMPLETE / PRESERVED**

Inspector can identify runtime evidence.

No guessing.

---

## 🟢 Phase 3 — Recovery Baseline

**COMPLETE**

```text
7cd9226
```

protected by:

```text
recovery-7cd9226
```

---

## 🟡 Phase 4 — AI Control Plane Restoration

**IMPLEMENTED — NEEDS LOCAL VERIFICATION**

AI Studio has implemented:

```text
ControlPlane
Ollama integration
read-only tools
tests
```

Your screenshot gives us positive evidence that it is working.

But we still need to verify the exact code state against our recovery branch.

---

## ⏳ Phase 5 — Dockerize

**NOT STARTED / HOLD**

First finish Chat restoration.

---

## ⏳ Phase 6 — Kubernetes

**HOLD**

Do not touch yet.

---

## ⏳ Phase 7 — CI/CD

**HOLD**

Do not touch yet.

---

# 23. Our Next Immediate Step

We should NOT ask AI Studio to redesign anything.

We should NOT ask it to improve UI.

We should NOT touch Dockerize.

We should NOT touch Kubernetes.

We should NOT touch CI/CD.

### Next step is simply:

**Bring the AI Studio restoration into the local `recovery-7cd9226` branch and inspect the diff.**

Then we test.

---

# 24. Exact Next Verification Sequence

Once the files are in your local project, we will do:

```bash
git status
```

Then:

```bash
git diff --stat
```

Then:

```bash
git diff
```

We specifically inspect:

```text
core/control_plane.ts
core/ollama_output.ts
server.ts
test_control_plane.ts
test_runtime_evidence.ts
```

Then:

```bash
npm test
```

Then:

```bash
npm run lint
```

Then:

```bash
npm run build
```

Then start:

```bash
npm run dev
```

---

# 25. Then We Test Real Mac Ollama

Before browser testing:

```bash
ollama list
```

We need to confirm:

```text
devops-qwen:v1
devops-qwen:latest
```

Then the application:

```text
localhost:3000
        ↓
Node
        ↓
localhost:11434
        ↓
Ollama
```

Then test Chat with small factual questions.

### Test 1

```text
What is today's date?
```

Expected:

```text
September 15, 2026
```

with the actual current local time if requested.

### Test 2

```text
What is my current workspace path?
```

Expected actual project path.

### Test 3

```text
Find the sms folder
```

Expected factual result.

If it doesn't exist:

```text
File or directory 'sms' not found
```

### Test 4

```text
List the files in my workspace
```

Expected actual workspace evidence.

### Test 5

```text
What Git branch am I on?
```

Expected:

```text
recovery-7cd9226
```

if the server is running from that branch/worktree.

This is a very good test because it proves the Control Plane is reading the actual repository.

---

# 26. Final Architecture We Are Building

This is the architecture I want you to keep in your project notes:

```text
                    SOHAIL STUDIO
                         │
          ┌──────────────┴──────────────┐
          │                             │
        CHAT                         TERMINAL
          │                             │
          ▼                             ▼
   AI CONTROL PLANE                   PTY
          │                             │
          │ READ ONLY                   │ REAL SHELL
          │                             │
     ┌────┴────────┐                    │
     │             │                    │
     ▼             ▼                    │
  Workspace     System                  │
  Evidence       Time                   │
     │                                  │
     └──────────────┐                   │
                    ▼                   │
              Ollama HTTP               │
                    │                   │
                    ▼                   │
             devops-qwen:v1             │
                    │                   │
                    ▼                   │
                 CHAT                   │
                                        │
                               Sohail-Agent
                                        │
                               devops-qwen:latest
```

---

# 27. The Golden Rules Going Forward

### Rule 1 — Git safety

```text
recovery branch first
main later
```

### Rule 2 — No guessing

If evidence isn't available:

```text
NEEDS_EVIDENCE
```

### Rule 3 — Chat is read-only

Chat cannot execute arbitrary commands.

### Rule 4 — Terminal is execution

Real shell operations belong in Terminal/approved agent workflows.

### Rule 5 — Local-first

Chat:

```text
Ollama → localhost
```

No Gemini.

No cloud fallback.

No fake response.

### Rule 6 — Two models remain separate

```text
Chat       → devops-qwen:v1
Sohail-Agent → devops-qwen:latest
```

### Rule 7 — AI Studio is not the source of truth

Your Git repository is.

AI Studio can modify code, but we review:

```text
git diff
```

before accepting it.

### Rule 8 — Don't touch unrelated systems

Until Chat restoration is completely verified:

```text
Dockerize      HOLD
Kubernetes     HOLD
CI/CD          HOLD
UI redesign    HOLD
Database       HOLD
```

---

# 🏁 Exact Position Right Now

```text
                    SOHAIL STUDIO
                         │
                         ▼
              ┌───────────────────┐
              │  Node/Express      │
              │     BASELINE       │
              └─────────┬─────────┘
                        │
                  7cd9226 SAFE
                        │
              recovery-7cd9226
                        │
                        ▼
             ┌────────────────────┐
             │ AI CONTROL PLANE   │
             │                    │
             │ 7 read-only tools  │
             └─────────┬──────────┘
                       │
                       ▼
                LOCAL OLLAMA
                       │
                       ▼
                devops-qwen:v1
                       │
                       ▼
                    CHAT
                       │
                       ▼
             🟡 LOCAL VERIFICATION
                       │
                       ▼
             ⏳ Dockerize later
                       │
                       ▼
             ⏳ Kubernetes later
                       │
                       ▼
             ⏳ CI/CD later
```

