
# Sohail Studio — Development Checkpoint

**Date:** 20-Aug-2026
**Project:** Sohail Studio
**Project path:**

```text
/Users/sohal/Downloads/testing-project/sohail-studio
```

---

# 1. Project Goal

**Sohail Studio** is a local-first AI engineering workspace.

The final product has only **two main modes**:

```text
Sohail Studio
│
├── Chat
│
└── Terminal
```

The goal is to make Sohail Studio a serious local DevOps engineering workspace, not a demo UI.

---

# 2. CHAT — COMPLETE

Chat was the first major part of the project.

## Phase 1 — Chat Foundation ✅

Chat uses:

```text
Ollama
└── devops-qwen:latest
```

Normal flow:

```text
User
 ↓
Sohail Studio Chat
 ↓
Ollama
 ↓
devops-qwen:latest
 ↓
Answer
```

Chat and Terminal are separated.

Chat **does not have arbitrary shell access**.

---

# 3. CHAT — CONTROL PLANE COMPLETE

## Phase 2 — AI Control Plane ✅

We added a read-only Control Plane so Chat can answer questions about the local environment safely.

Examples:

```text
pwd
ls
local time/date
project files
Docker read-only state
Git read-only state
Kubernetes read-only state
```

Architecture:

```text
User
 ↓
Chat
 ↓
Does this need local information?
 ↓
Control Plane
 ↓
Approved read-only tool
 ↓
Result
 ↓
Ollama / devops-qwen:latest
 ↓
Answer
```

Important security rule:

```text
Chat ≠ Terminal
```

Chat cannot execute arbitrary commands such as:

```text
rm -rf
mkdir
docker run
docker stop
git commit
git reset
kubectl apply
```

Only the real Terminal provides shell execution.

**Do NOT modify Chat now.**

Chat Phase 1 + Phase 2 are considered complete.

---

# 4. TERMINAL — MAIN PRODUCT WORK

The main current development is Terminal.

Terminal has two engines:

```text
Terminal
│
├── Raw PTY
│   └── real zsh
│
└── Sohail-Agent
    └── DevOps engineering CLI
```

This separation is extremely important.

---

# 5. RAW PTY

Raw PTY provides the real local shell.

Architecture:

```text
Browser
 ↓
WebSocket
 ↓
Real local PTY
 ↓
zsh
 ↓
Real terminal
```

User can use normal commands.

Example:

```text
pwd
ls
cd
docker
kubectl
git
```

Raw PTY should remain a real shell.

### Known UI issue

Previously some PTY output appeared incorrectly aligned / split left and right because terminal escape sequences/output rendering were not handled perfectly.

This should eventually be polished.

Do **not** confuse this with Sohail-Agent.

---

# 6. SOHAIL-AGENT — PRODUCT PURPOSE

Sohail-Agent is **NOT another LLM chat mode**.

This is one of our most important design rules.

### Never describe it as:

```text
Sohail-Agent = AI Chat
```

Instead:

```text
Sohail-Agent = local DevOps engineering CLI
```

It is an existing engineering CLI located inside the project.

It provides commands such as:

```text
inspect
dockerize
k8s
cicd
docs
interview
plan
plan-v2
bootstrap
stack
specification
blueprint
all
```

Current CLI help confirmed:

```text
sohail-agent --help
```

shows these commands.

---

# 7. SOHAIL-AGENT TERMINAL — FIRST IMPLEMENTATION

We integrated Sohail-Agent into the Terminal UI.

Current top-level options:

```text
Inspect
Dockerize
Kubernetes
CI/CD
Plan
Blueprint
```

The UI also has a live execution area:

```text
Sohail-Agent Terminal
```

The intention is:

```text
Top
 ↓
Choose engineering operation

Bottom
 ↓
Live Sohail-Agent execution/output
```

This architecture is now working.

---

# 8. IMPORTANT CHANGE — GUIDED WORKFLOW

Initially the design was too simple:

```text
click Dockerize
 ↓
run command
 ↓
done
```

We changed the design.

The correct design is:

```text
Inspect
 ↓
Understand repository
 ↓
Build Project Context
 ↓
Ask user what they want
 ↓
Collect required options
 ↓
Generate
 ↓
Show live output
```

This is now the main direction of Sohail-Agent.

---

# 9. SHARED PROJECT CONTEXT

We instructed Codex to create/use a shared understanding of the repository.

Conceptually:

```text
ProjectContext
│
├── project path
├── project type
├── components
├── languages
├── frameworks
├── runtimes
├── build systems
├── package managers
├── ports
├── source directories
├── Docker information
├── Docker Compose information
├── Kubernetes information
├── CI/CD information
└── important files
```

The goal:

```text
Inspect
   ↓
Project Context
   ↓
Dockerize
Kubernetes
CI/CD
Plan
Blueprint
```

Instead of every generator independently guessing the project.

---

# 10. INSPECT WORKFLOW

Inspect should become the foundation.

For example, if a repository contains:

```text
frontend/
backend/
docker-compose.yml
Jenkinsfile
k8s/
```

Sohail-Agent should understand that this is a multi-component project.

It should not assume:

```text
one repository = one Dockerfile
```

After Inspect, the UI should continue asking:

```text
What would you like to do next?

Dockerize
Kubernetes
CI/CD
```

The top operation buttons should **remain visible**.

---

# 11. DOCKERIZE WORKFLOW

Dockerize is now guided.

For a project containing:

```text
frontend
backend
```

the UI should ask:

```text
What should be Dockerized?

○ Frontend
○ Backend
● Frontend + Backend
```

Then:

```text
Do you want Docker Compose?

○ Yes
○ No
```

If an existing Compose file exists:

```text
Existing docker-compose.yml detected.

○ Keep existing
○ Analyze existing
○ Improve existing
○ Generate new
```

This prevents blindly overwriting real project files.

---

# 12. REAL REPOSITORY TEST

We tested against a real Git repository:

```text
full-stack_chatApp
```

Path:

```text
/Users/sohal/Downloads/projects/full-stack_chatApp
```

Repository structure:

```text
full-stack_chatApp/
├── backend/
├── frontend/
├── k8s/
├── package.json
├── docker-compose.yml
├── Jenkinsfile
├── README.md
└── LICENSE
```

This was cloned directly from Git.

---

# 13. IMPORTANT TEST — DELETE FILES FIRST

To prove Sohail-Agent can really generate files, we deliberately deleted:

```text
frontend/Dockerfile
backend/Dockerfile
docker-compose.yml
```

Then we asked Sohail-Agent to Dockerize the project.

This was important because we did **not** want to simply copy existing files.

---

# 14. CURRENT DOCKER GENERATION RESULT

Sohail-Agent successfully regenerated:

```text
frontend/Dockerfile
backend/Dockerfile
docker-compose.yml
```

The dashboard showed:

```text
Generating Docker configuration...

Detected stack: node

Wrote backend/Dockerfile
Wrote backend/.dockerignore

Wrote frontend/Dockerfile
Wrote frontend/.dockerignore

Wrote docker-compose.yml

Completed — exit code 0
```

This proves the basic generation workflow works.

---

# 15. BUT WE FOUND AN IMPORTANT PROBLEM

The generated configuration is **not yet production-quality**.

Latest generated backend Dockerfile contained:

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "start"]
```

But generated Compose contained:

```yaml
backend:
  build: ./backend
  ports:
    - "3000:3000"
```

So we have:

```text
Dockerfile:
5173

Compose:
3000:3000
```

That is inconsistent.

This is now one of the **first things to fix tomorrow**.

---

# 16. WHY THIS MATTERS

We don't want:

```text
Node project
 ↓
generic Docker template
 ↓
random port
```

We want:

```text
Repository
 ↓
Inspect package.json
 ↓
Inspect source
 ↓
Inspect configuration
 ↓
Determine actual start command
 ↓
Determine actual runtime port
 ↓
Generate Dockerfile
 ↓
Generate Compose using SAME information
```

The generated artifacts must agree with each other.

---

# 17. NODE VERSION ALSO NEEDS VERIFICATION

The generated Dockerfiles selected:

```text
node:20-alpine
```

But the previous repository Dockerfiles used:

```text
node:18-alpine
```

Node 20 might be correct, but Sohail-Agent must have evidence for that decision.

Tomorrow we should determine:

```text
Where did Node 20 come from?
```

and make the detection logic evidence-based.

Potential evidence:

```text
package.json
.nvmrc
engines
README
package-lock.json
```

The agent should not randomly choose runtime versions.

---

# 18. DOCKER GENERATION PRINCIPLE

This is a permanent project rule:

> **The repository is the source of truth.**

Sohail-Agent should work when we do:

```text
git clone <real repository>
        ↓
Sohail-Agent Inspect
        ↓
understand repository
        ↓
ask user
        ↓
generate
```

The user should NOT need to paste:

```text
Dockerfile
docker-compose.yml
Jenkinsfile
Kubernetes YAML
```

into Chat.

---

# 19. KUBERNETES — NEXT MAJOR WORK

Kubernetes is not finished yet.

Current option:

```text
Kubernetes
```

should become a guided workflow.

For a full-stack project:

```text
Detected:

Frontend
Backend
```

Ask:

```text
What should be deployed?

☑ Frontend
☑ Backend
```

Then:

```text
Manifest organization

● Automatic / Recommended
○ Single manifest
○ Separate resource files
```

The user should not have to manually say:

```text
make exactly 7 YAML files
```

The agent should determine an appropriate structure from the project.

Possible resources:

```text
Deployment
Service
ConfigMap
Secret template
Ingress
HPA
```

But don't generate everything automatically.

Only generate what is justified.

---

# 20. CI/CD — NEXT MAJOR WORK

CI/CD is also not finished.

The repository may contain:

```text
Jenkinsfile
```

Sohail-Agent should detect it.

Then ask:

```text
Existing Jenkinsfile detected.

What would you like to do?

○ Analyze
○ Improve
○ Generate new
○ Keep unchanged
```

Potential platforms:

```text
Jenkins
GitHub Actions
Both
```

Pipeline stages should come from the actual project.

For example:

```text
Checkout
Frontend build
Backend build
Tests
Docker build
Docker push
Deployment
```

But:

**Do not automatically push images or deploy.**

Those should require explicit user selection.

---

# 21. PLAN

Plan remains an existing Sohail-Agent capability.

It should eventually become a guided GUI workflow around the existing CLI.

Do not replace the existing planning engine.

---

# 22. BLUEPRINT

Blueprint also remains an existing capability.

It should use:

```text
planning package
+
specification package
```

when required.

If prerequisites are missing, the UI should explain what is missing rather than inventing information.

---

# 23. SOHAIL-AGENT CONSOLE

We also wanted the bottom panel to become useful as an actual Sohail-Agent console.

Important distinction:

```text
Raw PTY
↓
real zsh
↓
arbitrary commands
```

versus:

```text
Sohail-Agent Terminal
↓
existing sohail-agent CLI
```

The Sohail-Agent console should not become another unrestricted shell.

Example:

```text
sohail-agent --help
```

or:

```text
sohail-agent inspect /Users/sohal/Downloads/projects/full-stack_chatApp
```

should execute through the real existing CLI and stream:

```text
stdout
stderr
progress
completion
errors
```

---

# 24. CURRENT TERMINAL UI DESIGN

The intended design:

```text
TERMINAL
│
├── Raw PTY
│
└── Sohail-Agent
    │
    ├── Inspect
    ├── Dockerize
    ├── Kubernetes
    ├── CI/CD
    ├── Plan
    └── Blueprint
         │
         ↓
    Operation Workspace
         │
         ↓
    Questions / Choices
         │
         ↓
    Confirmation
         │
         ↓
    Live Sohail-Agent Terminal
```

The top buttons stay visible.

The middle changes depending on the selected operation.

The bottom remains the live execution/output area.

---

# 25. CHAT MUST NOT BE TOUCHED

Tomorrow, do not start modifying Chat.

Chat is:

```text
Phase 1 ✅
Phase 2 ✅
```

Current Chat:

```text
devops-qwen:latest
```

through Ollama.

Current Chat safety and Control Plane are already implemented.

Our current development target is:

```text
Terminal → Sohail-Agent
```

---

# 26. CODEX RULES WE ESTABLISHED

Because Codex limits are important, every future Codex prompt should explicitly say:

```text
START IMPLEMENTATION DIRECTLY.

Do not generate a planning report.

Do not generate an architecture report.

Do not run Git commands.

Do not run:
git status
git diff
git log
git branch
git show

Do not repeatedly inspect unrelated files.

Do not run the full test suite unless necessary.

Only run focused tests/commands.

Do not install unnecessary dependencies.

Do not modify unrelated code.
```

Codex should work directly.

---

# 27. NEXT SESSION — PHASE 4

Tomorrow we should start here:

## Phase 4 — Project-Aware Generation Accuracy

### Step 1 — Inspect current implementation

First understand the code Codex changed today.

Especially:

```text
core/
sohail_agent_cli/
backend/
dashboard/
```

Focus on:

```text
project context
inspect
dockerize
k8s
cicd
dashboard workflow
CLI execution
```

Do not touch Chat.

---

### Step 2 — Fix runtime detection

For Node projects, inspect:

```text
package.json
package-lock.json
.nvmrc
engines
README
source/configuration
```

Determine:

```text
Node version
package manager
build command
start command
port
framework
```

---

### Step 3 — Fix Docker/Compose consistency

The same detected context must drive:

```text
frontend/Dockerfile
backend/Dockerfile
docker-compose.yml
```

For example:

```text
Backend detected port
        ↓
Dockerfile EXPOSE
        ↓
Compose target port
        ↓
same value
```

No contradictions.

---

### Step 4 — Test another real project

Don't test only `full-stack_chatApp`.

Use another cloned project, preferably something different such as:

```text
Java/Maven
```

or:

```text
Django/Python
```

to prove the generator isn't hard-coded for Node.

---

### Step 5 — Kubernetes

After Docker generation is trustworthy:

```text
Kubernetes
 ↓
inspect shared ProjectContext
 ↓
ask frontend/backend
 ↓
ask manifest strategy
 ↓
generate
```

---

### Step 6 — CI/CD

Then:

```text
CI/CD
 ↓
detect Jenkins/GitHub Actions
 ↓
inspect existing pipeline
 ↓
ask user
 ↓
generate/improve
```

---

### Step 7 — Final Sohail-Agent integration

Eventually:

```text
Inspect
 ↓
Dockerize
 ↓
Kubernetes
 ↓
CI/CD
 ↓
Plan
 ↓
Blueprint
```

should feel like one coherent engineering system.

---

# 28. DEFINITION OF "REAL DEVOPS CLI"

Keep this principle for the whole project:

```text
NOT:

User tells agent what the project is
        ↓
Agent uses template
        ↓
Generate files
```

Instead:

```text
REAL:

Repository
    ↓
Inspection
    ↓
Evidence
    ↓
Project Context
    ↓
Engineering decisions
    ↓
User choices
    ↓
Generation
    ↓
Validation
```

That is the standard we should hold Sohail-Agent to.

---

# 29. CURRENT PROJECT STATUS

```text
Sohail Studio
│
├── Chat
│   ├── Phase 1 ✅
│   └── Phase 2 ✅
│
└── Terminal
    │
    ├── Raw PTY
    │   └── Real zsh ✅
    │
    └── Sohail-Agent
        ├── CLI integration ✅
        ├── Inspect ✅
        ├── Shared project context ✅
        ├── Guided Dockerize ✅
        ├── Docker generation 🟡
        ├── Kubernetes 🟡
        ├── CI/CD 🟡
        ├── Plan 🟡
        ├── Blueprint 🟡
        └── Interactive CLI console 🟡
```

### Overall milestone

**Approximately 50% of the Sohail-Agent/Terminal milestone is complete.**

The remaining 50% is primarily about **accuracy, guided workflows, Kubernetes/CI/CD, and final integration**, not rebuilding the foundation.

---

# 30. TOMORROW'S FIRST MESSAGE

Tomorrow you don't need to explain everything again.

Just tell me:

> **“Mentor, continue Sohail Studio from the 20-Aug checkpoint. Start Phase 4 — Project-Aware Generation Accuracy.”**

Then our first target will be:

```text
full-stack_chatApp
        ↓
Inspect actual project evidence
        ↓
Fix Node/runtime/port detection
        ↓
Fix Dockerfile + Compose consistency
        ↓
Test with another real repository
```

**That's exactly where we stop tonight.**
