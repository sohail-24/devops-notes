
# 1. Core Project Principle — MUST REMAIN UNCHANGED

The most important Sohail Studio principle remains:

> **NO GUESSING. NO COPYING OLD DATA. ONLY LIVE, REAL, EVIDENCE-BOUND DATA.**

The system must:

* use the persisted Project Intelligence generated from a real inspection
* not rescan the repository during Dockerize unless explicitly designed to do so
* not invent missing values
* not accept model guesses as repository truth
* not silently add infrastructure
* distinguish:

  * repository evidence
  * deterministic derivation
  * approved platform policy
  * model proposals
* block unsafe/unsupported decisions instead of guessing
* preserve deterministic validation even when Ollama output is wrong

The Ollama model is **not the authority**.

The architecture is:

```text
Repository
    ↓
Inspect
    ↓
Persisted Project Intelligence
    ↓
Dockerize Context
    ↓
Bounded Model Decision
    ↓
Deterministic Repair / Normalization
    ↓
Evidence Validation
    ↓
Render
    ↓
Validate Rendered Artifacts
    ↓
Dry Run / Write
```

The model may propose within the evidence boundary, but it cannot create truth.

---

# 2. Today's Main Goal

Today we continued the Dockerize workflow, specifically fixing several issues discovered through **real local testing against the external full-stack repository**.

The important point is that we did not blindly accept Codex's first implementation.

We repeatedly:

1. ran a real inspection
2. persisted Project Intelligence
3. ran Dockerize locally
4. observed actual Ollama/model behavior
5. identified the exact evidence/provenance failure
6. fixed the deterministic architecture
7. tested again

This is exactly how infrastructure should be built.

---

# 3. Problem #1 — Static Frontend Incorrectly Required `start_command`

## Initial problem

The frontend is a Vite/React static application.

The system was incorrectly treating every component as a process runtime requiring:

```text
production start command
```

But a static frontend has a different execution model.

The frontend repository evidence includes things such as:

```text
frontend/package.json
frontend/package-lock.json
frontend/index.html
frontend/nginx.conf
frontend/src/
```

Its authoritative build command is:

```text
vite build
```

But it does not necessarily need an application production command like:

```text
npm start
```

because the built static files need to be served by a static-serving mechanism.

## Fix

Codex added explicit execution strategies:

```text
PROCESS_RUNTIME
STATIC_ARTIFACT_SERVER
```

### Backend

The backend is:

```text
PROCESS_RUNTIME
```

and requires an authoritative production start command.

Evidence:

```text
backend/package.json
```

Command:

```text
node src/index.js
```

### Frontend

The frontend is:

```text
STATIC_ARTIFACT_SERVER
```

It requires:

* verified static frontend pattern
* authoritative build command
* dependency manifest
* lockfile
* static serving policy
* validated port
* approved platform policy

It does **not** require an application `start_command`.

---

# 4. Static Frontend Rendering Contract

The frontend's deterministic contract became:

```text
Verified pattern:
static-frontend

Strategy:
react-vite-static

Execution strategy:
STATIC_ARTIFACT_SERVER

Build command:
vite build

Install command:
npm ci

Serving command:
approved platform policy

Port:
80
```

The policy-authorized serving behavior is:

```dockerfile
CMD ["npx", "serve", "-s", "dist"]
```

Important:

The model should not invent this command.

The static serving contract comes from the approved platform policy.

---

# 5. Problem #2 — Backend Port Was Invented

During local testing, Dockerize initially failed with:

```text
Docker decision invented a port for backend; no port evidence exists
```

The model proposed:

```text
backend port: 3001
```

But the persisted inspection did not contain authoritative backend port evidence.

The backend uses:

```text
process.env.PORT
```

The external repository did not provide a current authoritative port value.

A README example such as:

```text
PORT=5001
```

was correctly treated as an example/configurable setup value, not automatically accepted as current repository truth.

## Important decision

We did **not** modify the inspector to guess a port.

Instead:

```text
No authoritative port evidence
        ↓
No port is required in Docker decision
        ↓
No EXPOSE
        ↓
No Compose ports mapping
        ↓
No target_port
```

This preserves the no-guessing architecture.

---

# 6. Port Rules After Today's Fix

The Dockerize contract now behaves like this:

### Case A — Authoritative port exists

Example:

```text
frontend/nginx.conf → 80
```

Then:

```text
Docker component port = 80
Compose port = 80
Compose target port = 80
```

The values must match exactly.

---

### Case B — No authoritative port exists

Example:

```text
backend
```

Then:

```text
component port = omitted
Compose port = omitted
target_port = omitted
EXPOSE = omitted
```

The model cannot invent:

```text
3000
3001
5000
5001
8080
```

or any other default.

---

### Case C — Model invents a port despite evidence

Example:

```text
Persisted evidence = 80
Model says = 81
```

Bounded repair/normalization now canonicalizes it back to:

```text
80
```

For Compose:

```text
80:80
```

not:

```text
81:81
```

---

# 7. Port Provenance Bug Fixed

A specific bug was found:

The repair system removed invented ports when **no evidence existed**, but when authoritative evidence did exist, it did not always canonicalize conflicting values.

Example:

```text
Evidence:
80

Model proposal:
81:81
```

Previously, that could reach validation.

## Fix

Changes were made in:

```text
sohail_agent_cli/dockerize/decision.py
sohail_agent_cli/dockerize/compose_context.py
sohail_agent_cli/dockerize/validation.py
```

Now:

```text
authoritative persisted port
        ↓
bounded repair
        ↓
exact canonical port
        ↓
Compose validation
        ↓
rendered artifact validation
```

The frontend must remain:

```text
80:80
```

---

# 8. Problem #3 — Model Conflicting With Persisted Static Pattern

Another real Ollama issue appeared.

Persisted verified pattern was:

```text
static-frontend
```

But Ollama returned:

```text
react-static-container-v1
```

The previous normalization logic restored omitted fields but did not always override conflicting model values.

This meant:

```text
persisted truth != model output
```

could incorrectly reach validation.

## Fix

`decision.py` was updated so deterministic normalization restores authoritative fields.

The persisted context now wins for:

* verified pattern
* strategy
* execution strategy
* deterministic static install contract
* build contract
* authoritative ports

Therefore:

```text
Persisted verified pattern:
static-frontend

Model conflicting pattern:
react-static-container-v1

Final normalized result:
static-frontend
```

The model cannot override verified engineering facts.

---

# 9. Static Install Policy Improvement

A deterministic lockfile-backed installation policy was added.

For the frontend:

```text
package.json
+
package-lock.json
        ↓
npm ci
```

This became the deterministic install contract.

This is stronger than allowing the model to arbitrarily choose:

```text
npm install
```

or:

```text
npm install --production
```

The static frontend installation/build behavior is now policy/evidence-bound.

---

# 10. Current Real Repository Architecture

The external test repository currently contains two components.

## Backend

```text
backend/
```

Characteristics:

```text
Execution strategy:
PROCESS_RUNTIME

Production command:
node src/index.js

Port:
NOT AUTHORITATIVELY PROVEN

Base image:
node:22-alpine
(from approved platform policy)

Working directory:
/app
(from approved platform policy)
```

Important:

Because the backend port is absent:

```text
No EXPOSE
No Compose ports
No target_port
```

---

## Frontend

```text
frontend/
```

Characteristics:

```text
Verified pattern:
static-frontend

Strategy:
react-vite-static

Execution strategy:
STATIC_ARTIFACT_SERVER

Install:
npm ci

Build:
vite build

Static serving:
approved platform policy

Port:
80
```

Supporting configuration:

```text
frontend/nginx.conf
```

Important:

`nginx.conf` is supporting configuration.

It does **not** create an independent Nginx component.

Therefore:

```text
Frontend component = 1
Independent Nginx component = 0
```

---

# 11. Important Infrastructure Rules Confirmed

Today's work reinforced all of these:

## No independent Nginx component

```text
frontend/nginx.conf
```

does not automatically mean:

```text
frontend service
+
nginx service
```

Only real component evidence can create a component.

---

## No database service

Even if the application contains database-related code, Dockerize must not invent:

```text
mongodb
postgres
mysql
redis
```

unless evidence supports generation.

Current result:

```text
No database service generated
```

---

## No inferred relationships

Dockerize must not invent:

```text
depends_on
service connections
network relationships
environment relationships
```

without evidence.

Current result:

```text
No inferred relationships
```

---

# 12. Latest Successful Real Ollama Verification

The latest successful real inspection run reported by Codex was:

```text
f998d14d-2b88-474e-aae5-97c3b5605ce7
```

Real external repository:

```text
/Users/sohal/Downloads/projects/full-stack_chatApp
```

Real local model:

```text
devops-qwen:latest
```

Result:

```text
SUCCESS
```

Reported behavior:

```text
Ollama calls: 1
Bounded repairs: 1

Backend:
PROCESS_RUNTIME
no port

Frontend:
STATIC_ARTIFACT_SERVER
static-frontend
port 80

Compose:
backend portless
frontend 80:80
```

Reported artifact paths:

```text
/Users/sohal/Downloads/projects/full-stack_chatApp/backend/Dockerfile

/Users/sohal/Downloads/projects/full-stack_chatApp/frontend/Dockerfile

/Users/sohal/Downloads/projects/full-stack_chatApp/docker-compose.yml
```

For dry-run verification:

```text
Files written: 0
Files modified: 0
Repository fingerprint unchanged
Dockerize repository rescans: 0
```

This is important because Dockerize remains bound to the persisted inspection snapshot.

---

# 13. Test Results at the End of Today

Latest Codex-reported verification:

```text
Focused/regression tests:
106 passed

Full suite:
350 passed
1 known unrelated failure
```

Known pre-existing failure:

```text
tests/test_phase4_foundation.py
```

Issue:

```text
expected:
not_configured

actual:
unavailable
```

when:

```text
DATABASE_URL
```

is absent.

This was explicitly not part of today's Dockerize work.

We should **not accidentally fix unrelated baseline issues while continuing Dockerize**, unless we intentionally schedule that work.

Additional checks passed:

```text
Python compilation: passed
Ruff E9,F: passed
git diff --check: passed
```

---

# 14. Files Changed During Today's Final Fixes

The work involved changes around:

```text
sohail_agent_cli/dockerize/strategies.py
sohail_agent_cli/dockerize/context_builder.py
sohail_agent_cli/dockerize/platform_policy.py
sohail_agent_cli/dockerize/decision.py
sohail_agent_cli/dockerize/validation.py
sohail_agent_cli/dockerize/compose_context.py
sohail_agent_cli/agents/docker_agent.py
```

Tests updated included:

```text
tests/test_dockerize_workflow.py
tests/test_verified_engineering_patterns.py
```

All earlier Step 1–4C worktree changes were supposed to remain preserved.

---

# 15. Where We Stopped Today

We stopped after the final Codex report showed a successful real Ollama Dockerize dry run.

**Tomorrow's first task is NOT immediately writing more code.**

We must independently verify locally through the Sohail Studio UI/CLI.

We need to confirm with our own eyes that the current implementation really behaves as reported.

---

# TOMORROW — LOCAL VERIFICATION PLAN

## Step 1 — Start from the current worktree

Project:

```text
/Users/sohal/Downloads/testing-project/sohail-studio
```

First inspect:

```bash
git status
```

Do not discard existing worktree changes.

We have accumulated Step 1–4C work and today's Dockerize changes.

---

## Step 2 — Start Sohail Studio

Start the project exactly as currently used locally.

Open the Sohail Studio UI at the local application address.

---

## Step 3 — Run a Fresh Inspect

Target repository:

```text
/Users/sohal/Downloads/projects/full-stack_chatApp
```

We want a **fresh persisted Project Intelligence snapshot**.

Important:

```text
Inspect performs repository evidence acquisition.

Dockerize should consume that persisted snapshot.
```

---

## Step 4 — Inspect the Result

Before Dockerize, verify the Project Intelligence makes sense.

Specifically check:

### Backend

```text
component identity
package manifest
lockfile
production command
```

Expected:

```text
node src/index.js
```

Port should remain absent unless the actual current repository evidence proves one.

Do not manually inject a port just to make Docker work.

---

### Frontend

Verify:

```text
package.json
package-lock.json
index.html
vite configuration
nginx.conf
vite build
port 80
```

The frontend should be classified as a static frontend.

---

## Step 5 — Dockerize Dry Run

Select:

```text
backend Dockerfile → Generate
frontend Dockerfile → Generate
Docker Compose → Generate
```

Keep:

```text
Dry run enabled
```

Then run Dockerize.

---

# Expected Local Dry Run Behavior

We want to see:

```text
Using persisted Project Intelligence
```

Then something equivalent to:

```text
Running deterministic Docker requirement preflight
```

Then:

```text
Asking devops-qwen:latest for a bounded Docker decision
```

If the model output needs repair:

```text
one bounded repair
```

is acceptable.

But the final decision must still be deterministic and evidence-bound.

---

# Expected Final Docker Result

## Backend

Should have:

```text
PROCESS_RUNTIME
node src/index.js
```

Should **not** have an invented port.

Expected:

```text
No EXPOSE
No Compose port mapping
```

unless a newly inspected repository now genuinely contains authoritative port evidence.

---

## Frontend

Should have:

```text
STATIC_ARTIFACT_SERVER
static-frontend
npm ci
vite build
port 80
```

Expected serving behavior:

```dockerfile
CMD ["npx", "serve", "-s", "dist"]
```

Expected Compose mapping:

```text
80:80
```

not:

```text
81:81
3000:3000
5173:5173
8080:8080
```

unless those values are actually evidenced.

---

# Step 6 — Check for Architecture Violations

Tomorrow we must explicitly confirm:

### No repository rescan during Dockerize

Expected:

```text
Dockerize repository rescans: 0
```

---

### No writes in dry run

Expected:

```text
Files written: 0
Files modified: 0
```

---

### Repository unchanged

Expected:

```text
repository fingerprint unchanged
```

---

### No invented services

Expected:

```text
No independent Nginx component
No database service
No inferred relationships
```

---

# Step 7 — Only After Dry Run Success

If the local dry run succeeds and we inspect the generated preview/artifacts carefully, then we can decide whether to:

```text
disable dry run
```

and perform the actual write.

Do not jump to actual writes before reviewing the generated Dockerfiles and Compose output.

---

# FUTURE PLAN — NEXT DEVELOPMENT PHASES

After tomorrow's local verification, we should move carefully.

## Phase A — Verify Actual Docker Artifacts

After dry-run success:

1. review backend Dockerfile
2. review frontend Dockerfile
3. review docker-compose.yml
4. verify every line has an evidence/policy/deterministic origin
5. ensure no model-only values became production configuration

---

## Phase B — Actual Write Workflow

Only after dry-run approval:

```text
Generate artifacts
```

Then verify:

```text
Files written exactly where intended
No unrelated files modified
No overwrites without explicit validated intent
```

---

## Phase C — Real Docker Build Validation

Next major milestone:

```text
Dockerize decision correctness
        ↓
Rendered Dockerfile correctness
        ↓
Actual docker build
        ↓
Container runtime validation
```

We should eventually test:

### Backend

* image builds
* application starts
* `node src/index.js` works
* environment configuration behaves correctly
* absence of port mapping is handled correctly

### Frontend

* build succeeds
* static files are generated
* container starts
* static server works
* port 80 behaves as expected

---

## Phase D — Docker Compose Runtime Validation

After artifact generation:

```text
docker compose config
```

should validate.

Then eventually:

```text
docker compose build
docker compose up
```

should be tested with real runtime behavior.

Again:

> Runtime failures must produce evidence and diagnostics, not guesses.

If something fails, Sohail Studio should identify what is actually unsupported/missing.

---

## Phase E — Improve Evidence Traceability

A future architectural improvement could make every generated Docker artifact easier to audit.

For example, internally trace:

```text
Dockerfile instruction
        ↓
decision field
        ↓
evidence / deterministic derivation / policy
        ↓
source
```

Conceptually:

```text
CMD node src/index.js
→ backend package.json
→ explicit production command evidence
```

```text
FROM node:22-alpine
→ approved platform policy
→ node-backend-container-v1
```

```text
CMD npx serve -s dist
→ STATIC_ARTIFACT_SERVER
→ approved static serving policy
```

This would strengthen Sohail Studio's explainability.

---

## Phase F — Broader Repository Testing

Do not assume this full-stack repository represents every architecture.

Eventually test against repositories with:

* Node backend
* Python backend
* Java backend
* static React/Vite frontend
* Next.js
* monorepos
* multiple services
* explicit Dockerfiles already present
* Compose already present
* databases explicitly configured
* Kubernetes manifests
* missing runtime versions
* missing ports
* ambiguous configurations

The purpose is to discover where the evidence model is incomplete.

Again:

```text
Test real repository
        ↓
Observe actual evidence
        ↓
Improve extraction/validation if justified
        ↓
Never add guessing
```

---

# CURRENT PROJECT STATUS — END OF DAY

## What is working conceptually

```text
Persisted inspection
✓

Evidence-bound Dockerize context
✓

Bounded Ollama decision
✓

Bounded repair
✓

Static vs process execution strategies
✓

Static frontend without application start command
✓

Authoritative port preservation
✓

Unevidenced port omission
✓

Compose port consistency
✓

No repository rescan during Dockerize
✓

Dry-run write protection
✓

No independent Nginx component
✓

No invented database service
✓

No inferred relationships
✓
```

## Current priority tomorrow

```text
LOCAL REAL VERIFICATION
```

Not more architecture changes unless the local run exposes a real problem.

---

# Mentor's Key Rule for Tomorrow

When we continue, our mindset should be:

> **We do not trust a test result alone. We verify the actual behavior locally.**

And most importantly:

> **If something is missing, Sohail Studio must say it is missing. It must never fill the gap with a guess.**

That's exactly the infrastructure philosophy we're building into Sohail Studio.
