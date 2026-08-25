
# Sohail Studio — Development Checkpoint

**Date:** 24–25 August 2026
**Current project:** `/Users/sohal/Downloads/testing-project/sohail-studio`
**Test repository:** `/Users/sohal/Downloads/projects/full-stack_chatApp`
**Coding assistant:** **Codex, continuing in the same session**

---

# 1. Overall Project Goal

Sohail Studio is a **local-first AI engineering workspace**.

The core design principle is:

> **Do not let the AI guess project facts. Inspect the real repository, collect evidence, persist verified intelligence, and use AI only within that evidence-bound context.**

The target architecture is:

```text
Real Repository
      ↓
Deterministic Inspection
      ↓
Evidence Collection
      ↓
Project Intelligence
      ↓
PostgreSQL Persistence
      ↓
Stored Inspection Snapshot
      ↓
User Chooses Engineering Operation
      ↓
Ollama devops-qwen:latest
      ↓
Structured Decision
      ↓
Deterministic Validation
      ↓
Artifact Generation
```

The system should aim for very high correctness by combining:

* deterministic repository inspection
* evidence-bound workflows
* persisted project intelligence
* explicit user choices
* local Ollama intelligence
* strict validation
* controlled failure states such as `NEEDS_EVIDENCE`

The system should **not silently invent missing technical facts**.

---

# 2. Important Architecture Principle Established

## Inspection happens once

The repository should be deeply inspected once.

That inspection produces a persisted **Project Intelligence snapshot** containing things such as:

* project path
* inspection run ID
* inspection timestamp
* components
* backend/frontend detection
* runtimes
* languages
* frameworks
* package managers
* databases
* ports
* services
* Docker evidence
* Kubernetes evidence
* CI/CD evidence
* verified engineering patterns
* confidence levels
* evidence files/signals

This intelligence is stored in PostgreSQL.

Then later operations should reuse:

```text
Persisted Project Intelligence
```

rather than scanning the repository again.

This is a very important architecture decision.

---

# 3. What Was Fixed Today — Inspection Lifecycle

There was previously a bug where completed inspection runs could reconnect and effectively replay/retrigger lifecycle behavior.

## Root cause

After completion:

```text
handleAgentRunEvent()
```

fetched intelligence and called:

```text
render()
```

but the completed `agentRunId` was retained.

When the WebSocket closed, the dashboard could reconnect to the same completed run and replay events.

## Codex fixed this

The new lifecycle is intended to be:

```text
Click Inspect
    ↓
Create ONE inspection run
    ↓
Connect ONCE
    ↓
Stream terminal output
    ↓
Inspection completes
    ↓
Mark run terminal
    ↓
Fetch persisted intelligence ONCE
    ↓
Render Project Intelligence
    ↓
STOP
```

Completed or error runs should not automatically reconnect or restart.

Other protections added:

* terminal run-state guards
* duplicate completion events ignored
* duplicate in-flight run creation prevented
* explicit `Re-inspect project`
* post-inspection workflow does not show normal Inspect as an operation

The endpoint:

```text
GET /api/agent/intelligence
```

was confirmed to be read-only.

It should **never create an inspection run**.

---

# 4. Dashboard Redesign

We improved the dashboard because the previous design had too many cards and boxes and did not feel like a real production engineering system.

The current direction is:

* cleaner
* fewer unnecessary boxes
* more hierarchy
* more important information visible
* production engineering dashboard feeling
* evidence-oriented rather than decorative

The dashboard now displays persisted intelligence such as:

## Project Intelligence

* project name
* project path
* inspection timestamp
* PostgreSQL snapshot status
* inspection status

## Project Architecture

Examples from the current test project:

```text
backend
Express · Node.js 20 · npm

frontend
React · Node.js 20 · npm

MongoDB
Detected database
```

## Technology Stack

Grouped more cleanly:

* Languages
* Runtimes
* Frameworks
* Platform / tooling

Example:

```text
Languages:
CSS, HTML, JavaScript, Node.js

Runtime:
Node.js 20

Frameworks:
Express, Next.js, React, Vite

Platform:
npm, Kubernetes, Jenkins
```

## Deployment Status

Shows:

* Docker
* Kubernetes
* CI/CD

based on repository evidence.

## Network

Typed evidence is preserved.

Example:

```text
backend
documented: 5001
application: 5001
service: 5001

frontend
application: 80
service: 80

mongodb
application: 27017
service: 27017
```

## Inspection Quality

Shows:

* files inspected
* evidence signals
* high confidence
* medium confidence
* low confidence

The current test repository showed approximately:

```text
74 files inspected
80 evidence signals
66 high confidence
14 medium confidence
0 low confidence
```

---

# 5. Post-Inspection Workflow

After successful inspection, the user should choose an engineering operation:

```text
Dockerize
Kubernetes
CI/CD
```

The system should not automatically re-inspect.

The current workflow is based on:

```text
Inspection
      ↓
Persist intelligence
      ↓
Choose operation
      ↓
Reuse same intelligence
```

---

# 6. Critical Decision: No Re-fetch / No Re-inspection for Operations

This was explicitly discussed and implemented as the intended architecture.

When the user has already inspected a project:

```text
Inspection Run ID
        ↓
Persisted PostgreSQL Intelligence
```

Then:

```text
Dockerize
Kubernetes
CI/CD
```

should reuse the stored snapshot.

They should **not**:

* start another complete repository inspection
* create another inspection run
* invoke `DeepInspector`
* recollect all evidence
* re-fetch/reprocess the project unnecessarily

The system should only use the persisted intelligence.

Example:

```text
Inspect project once
       ↓
Store intelligence
       ↓
Dockerize
       ↓
Reuse intelligence
       ↓
Kubernetes
       ↓
Reuse intelligence
       ↓
CI/CD
       ↓
Reuse intelligence
```

Only an explicit:

```text
Re-inspect
```

should create a new inspection snapshot.

---

# 7. Dockerize Workflow — Major Work Completed

Previously, clicking Dockerize immediately attempted generic generation.

That was changed.

Now the Dockerize UI should use the persisted Project Intelligence and ask the user what they actually want.

---

## Current Dockerize Planning UI

The system determines available components from the stored inspection.

For a project containing:

```text
backend
frontend
```

the UI can show:

```text
Backend Dockerfile
Frontend Dockerfile
Docker Compose
```

Each artifact has a state.

Examples:

```text
Missing → Generate
Existing → Keep
Existing → Upgrade
Skip
```

The user explicitly chooses what should happen.

---

# 8. Artifact Decision Rules

## If artifact is missing

Example:

```text
Backend Dockerfile
Status: Missing
```

The user can choose:

```text
Generate
Skip
```

---

## If artifact already exists

Example:

```text
Backend Dockerfile
Status: Existing
```

The system should default safely to:

```text
Keep
```

The user can explicitly choose:

```text
Keep
Upgrade
```

Upgrade must never happen automatically.

---

## Safety Rules

The implementation is intended to enforce:

```text
Generate
→ cannot overwrite an existing artifact

Upgrade
→ cannot target a missing artifact

Keep
→ leaves existing artifact unchanged

Skip
→ no artifact action
```

Existing files should never be overwritten accidentally.

---

# 9. Architecture-Aware Docker Questions

The desired behavior is:

## Backend-only project

Ask something like:

```text
Backend Dockerfile

Current status: Missing / Existing

What would you like to do?

Generate / Upgrade / Keep / Skip
```

Do not ask about frontend if no frontend component exists.

---

## Frontend + Backend project

Ask based on detected architecture:

```text
Backend Dockerfile
Generate / Upgrade / Keep / Skip

Frontend Dockerfile
Generate / Upgrade / Keep / Skip

Docker Compose
Generate / Upgrade / Keep / Skip
```

---

## Existing Docker configuration

The system should detect existing artifacts from stored intelligence and ask:

```text
Do you want to keep it or upgrade it?
```

The system must not automatically replace existing configuration.

---

# 10. Dockerize Uses Persisted Intelligence

The explicit Docker workflow is intended to use:

```text
inspection_run_id
        ↓
CLI bridge
        ↓
DockerAgent
        ↓
DockerContextBuilder
        ↓
PostgreSQL Project Intelligence Snapshot
```

The important rule is:

> Explicit Dockerize must use the completed inspection snapshot.

No new inspection should happen.

---

# 11. Ollama Is Now Part of Docker Generation

This was the next major change.

The user explicitly wanted Ollama:

```text
devops-qwen:latest
```

to actually participate in generating the requested Docker artifacts.

The intended model workflow is:

```text
Persisted Verified Intelligence
        +
Selected User Artifact Plan
        ↓
Bounded Docker Context
        ↓
Ollama devops-qwen:latest
        ↓
Structured Docker Decision
        ↓
Deterministic Validation
        ↓
Deterministic Renderer
        ↓
Dockerfile / Compose artifacts
```

Ollama should not receive unlimited raw repository content.

It should receive the verified context, such as:

* selected backend/frontend components
* runtime evidence
* package manager
* commands
* ports
* services
* Docker evidence
* selected artifact plan
* persisted project intelligence

Then it returns a structured decision.

---

# 12. Important Failure We Hit

The first Dockerize attempt failed because Ollama returned invalid structured data.

Specifically:

```text
reason
```

was empty.

The schema required:

```text
reason = non-empty string
```

The strict validation correctly rejected it.

The failure looked like:

```text
Dockerize failed: Ollama returned an invalid Docker decision schema:
reason must be a non-empty string
```

This was actually a good sign architecturally because the system did not silently continue with malformed AI output.

---

# 13. Codex Added One Bounded Ollama Repair Attempt

Codex then added exactly one repair attempt.

The intended behavior is:

```text
Call Ollama
     ↓
Validate response

If valid:
    continue

If invalid:
    send validation error back
    reuse original stored context
    ask Ollama once to repair
    validate again
```

Important restrictions:

The repair must:

* reuse the same persisted inspection snapshot
* reuse the same context
* not rescan the repository
* not acquire new evidence
* not start a new inspection run

If the repaired output is still invalid:

```text
FAIL CLEARLY
```

This keeps the system bounded and deterministic.

---

# 14. Current Failure State — Where We Stopped

After the repair implementation, the system still produced a controlled failure.

The terminal showed:

```text
Using persisted Project Intelligence
Selected Docker artifacts:
backend Dockerfile (generate),
frontend Dockerfile (generate),
Docker Compose (generate)

Asking devops-qwen:latest for a bounded Docker decision

Docker context:
full-stack_chatApp
root /Users/sohal/Downloads/projects/full-stack_chatApp
selected backend, frontend
components 2
evidence 46
model devops-qwen:latest
```

Then:

```text
Dockerize evidence acquisition not started:
the explicit plan is bound to the persisted inspection snapshot
```

And then the important error:

```text
Dockerize decision requires evidence:
Ollama returned Docker components different from the selected evidence
```

Result:

```text
[NEEDS_EVIDENCE - controlled outcome]
```

So this is the **current exact stopping point**.

---

# 15. What Needs Investigation Tomorrow

The current failure is:

> Ollama returned components different from the components selected by the user/persisted evidence.

We need to investigate the actual Ollama response.

The first priority is to understand exactly what:

```text
devops-qwen:latest
```

returned.

We should not guess.

Codex should inspect:

1. the exact bounded context sent to Ollama
2. the exact selected plan
3. the exact model response
4. the normalized parsed response
5. why the returned components differ from selected evidence
6. whether the prompt/schema is too ambiguous
7. whether component naming normalization is too strict
8. whether the model is adding/removing components
9. whether a deterministic mapping layer is needed

---

# 16. Important Design Decision for Tomorrow

The user wants Ollama to genuinely generate the requested Docker configuration.

However:

> Ollama must not be allowed to change the verified project scope.

For example, if the user selected:

```text
backend
frontend
docker-compose
```

and persisted intelligence confirms:

```text
backend
frontend
```

then Ollama should not decide:

```text
Only backend
```

or:

```text
backend + database + nginx + something else
```

unless those things are explicitly supported by the selected evidence and architecture rules.

A better architecture may be:

```text
User Selection
      +
Persisted Verified Component IDs
      ↓
LOCKED GENERATION SCOPE
      ↓
Ollama generates configuration decisions
      ↓
Deterministic validator checks:
- only allowed components
- all required selected components represented
- ports match evidence
- commands match evidence
- runtime assumptions supported
      ↓
Renderer generates files
```

The AI should decide **how to configure**, not **what the verified project contains**.

This distinction is important.

---

# 17. Suggested Investigation / Fix Direction

Tomorrow, ask Codex to inspect the current implementation before changing anything.

Potential robust approach:

## A. Log the structured model response safely

During development/testing, show:

```text
Selected components:
["backend", "frontend"]

Model components:
[...]
```

This will immediately show the mismatch.

---

## B. Normalize component identity

If the model returns:

```text
backend-service
```

but the persisted component ID is:

```text
backend
```

we need to determine whether that is:

* an invalid hallucination
* or a naming alias that can safely map to verified evidence

Do not automatically accept arbitrary aliases.

---

## C. Lock artifact scope before Ollama

The model prompt should clearly state:

```text
The selected components are immutable:
backend
frontend

You MUST NOT:
- remove a selected component
- add a new component
- rename component identifiers
- change the selected artifact scope

Return decisions only for these exact components.
```

---

## D. Use deterministic artifact targets

Potential structure:

```json
{
  "selected_components": [
    "backend",
    "frontend"
  ],
  "artifact_plan": {
    "backend_dockerfile": "generate",
    "frontend_dockerfile": "generate",
    "compose": "generate"
  }
}
```

Ollama should fill in configuration details, not redefine:

```text
selected_components
```

Potentially the deterministic system should own component IDs completely and Ollama should only return:

```text
build strategy
base image recommendation
install strategy
build command
runtime command
port mapping
compose service configuration
reason
```

Then component identity is not generated by AI at all.

This may be the strongest architecture.

---

# 18. Long-Term Dockerize Architecture Goal

The desired architecture is approximately:

```text
                  PROJECT INSPECTION
                         │
                         ▼
             Persisted Project Intelligence
                         │
                         │
                         ▼
                 User clicks Dockerize
                         │
                         ▼
                Docker Planning Screen
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           Backend    Frontend    Compose
           Generate    Upgrade    Generate
                         │
                         ▼
                 Immutable Plan
                         │
                         ▼
            Verified Docker Context Builder
                         │
                         ▼
             Ollama devops-qwen:latest
                         │
                         ▼
            Structured Configuration Decision
                         │
                         ▼
              Deterministic Validation
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           Valid      Invalid    Missing Evidence
              │          │          │
              ▼          ▼          ▼
           Render     One Repair  NEEDS_EVIDENCE
              │
              ▼
       Write Selected Artifacts
              │
              ▼
       Validate Generated Files
```

---

# 19. Important Files Recently Changed

The Docker planning work changed:

```text
dashboard/app.js
dashboard/styles.css
backend/main.py
core/cli_bridge.py
sohail_agent_cli/main.py
sohail_agent_cli/agents/docker_agent.py
sohail_agent_cli/dockerize/context_builder.py
sohail_agent_cli/dockerize/validation.py
```

The Ollama repair/fix work additionally changed:

```text
sohail_agent_cli/dockerize/decision.py
sohail_agent_cli/agents/docker_agent.py
sohail_agent_cli/dockerize/context_builder.py
tests/test_dockerize_workflow.py
```

Tests also changed:

```text
tests/test_terminal_workflow.py
tests/test_dockerize_workflow.py
```

---

# 20. Test Status at End of Session

Earlier focused test status:

```text
18 passed
```

After lifecycle/dashboard work:

```text
269 passed, 1 unrelated failure
```

After Docker planning:

```text
55 focused tests passed
```

After Ollama bounded repair work:

```text
58 focused tests passed
```

Full suite at the end of the reported Codex work:

```text
282 passed, 1 failed
```

The remaining failure was described as an existing environment-sensitive database health test.

Cause reported:

The repository `.env` still provides database configuration, so the health test can report:

```text
connected
```

even after only:

```text
DATABASE_URL
```

is unset.

This failure should not be casually ignored forever. Tomorrow or later, it should be verified and either:

* fixed properly, or
* confirmed as an existing unrelated test/environment issue.

---

# 21. Current UI State

The current UI now works approximately like:

```text
Project Intelligence
        ↓
Dockerize / Kubernetes / CI/CD
        ↓
Dockerize selected
        ↓
Dockerize Planning
        ↓
Backend Dockerfile:
Generate / Keep / Upgrade / Skip

Frontend Dockerfile:
Generate / Keep / Upgrade / Skip

Docker Compose:
Generate / Keep / Upgrade / Skip
        ↓
Continue
        ↓
Sohail-Agent Terminal
        ↓
Use persisted intelligence
        ↓
Ask Ollama
        ↓
Validate
        ↓
Generate
```

The UI behavior is largely correct.

The current blocker is in the **Ollama structured decision/component consistency layer**, not the basic dashboard workflow.

---

# 22. What NOT to Do Tomorrow

Do not let Codex:

* redesign the entire architecture without inspection
* remove evidence-bound validation
* make Ollama unrestricted
* add a new repository inspection during Dockerize
* silently accept mismatched components
* silently generate unsupported Docker assumptions
* replace deterministic validation with “trust the model”
* add lots of unnecessary UI boxes/options
* rewrite unrelated parts of the project
* change Kubernetes/CI-CD workflows unnecessarily

Keep the fix focused.

---

# 23. Immediate Tomorrow Task

Tomorrow's first task should be:

> Inspect the current Dockerize Ollama response path and identify exactly why `devops-qwen:latest` returns Docker components different from the immutable selected evidence.

Before making a large fix, inspect:

```text
Selected artifact plan
Selected component IDs
Bounded Docker context
Ollama prompt
Raw Ollama response
Parsed structured decision
Validation mismatch
```

Then implement the smallest correct architectural fix.

---

# 24. Recommended Next Development Sequence

After Dockerize works end-to-end:

## Phase A — Complete Dockerize

1. Fix Ollama component mismatch.
2. Generate backend Dockerfile.
3. Generate frontend Dockerfile.
4. Generate Docker Compose.
5. Validate generated artifacts.
6. Show created/updated files clearly.
7. Verify files locally.
8. Test:

   * backend-only
   * frontend-only
   * full-stack
   * existing Dockerfile
   * existing compose
   * missing evidence
   * invalid Ollama output
   * repair output
   * dry run
   * upgrade path

---

## Phase B — Kubernetes

Use the same architecture:

```text
Persisted Project Intelligence
        ↓
Kubernetes Planning
        ↓
User chooses required manifests
        ↓
Immutable plan
        ↓
Ollama bounded context
        ↓
Structured decision
        ↓
Deterministic validation
        ↓
Generate manifests
```

Possible artifacts:

```text
Deployment
Service
Ingress
ConfigMap
Secret references
Namespace
```

But only ask for artifacts that make sense for the detected architecture.

---

## Phase C — CI/CD

Use persisted intelligence again.

Possible workflow:

```text
Project intelligence
      ↓
Detected platform / existing CI
      ↓
Ask user what they want
      ↓
Generate or upgrade workflow
      ↓
Validate against verified commands
```

Potentially:

```text
GitHub Actions
GitLab CI
Jenkins
```

based on evidence and user choice.

---

# 25. Long-Term Product Direction

The product should eventually feel like:

> A serious local AI engineering control plane.

Not:

> “Chatbot that writes Dockerfiles.”

The differentiator is:

```text
Verified Intelligence
+
Persistent Project Memory
+
Human Choice
+
Bounded Local AI
+
Deterministic Validation
```

The system should know:

```text
What was inspected?
What evidence supports it?
When was it inspected?
Which snapshot is being used?
What did the user ask to change?
What did the AI decide?
Why was it allowed?
What was generated?
What was validated?
```

That traceability is a major strength of Sohail Studio.

---

continue from:

> **Dockerize planning and persisted intelligence are working. Ollama `devops-qwen:latest` is being called with bounded stored context, but the generated structured Docker decision fails because the model returns components different from the immutable selected evidence. Investigate the exact raw response and validation path first, then fix component scope locking/normalization without allowing reinspection or weakening evidence-bound validation.**

