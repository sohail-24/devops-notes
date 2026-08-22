Sohail Studio — Development Checkpoint / Continuation Notes

Date: 22-Aug-2026
Project: Sohail Studio
Repository: /Users/sohal/Downloads/testing-project/sohail-studio
Real test project: /Users/sohal/Downloads/projects/full-stack_chatApp

Purpose of this note:
Continue development tomorrow without re-explaining today's investigation, architecture decisions, evidence rules, or test results.

1. Current Project Goal

Sohail Studio is being developed as a local-first DevOps AI Control Plane.

Current focus:
Dockerize operation.

Desired architecture:

REAL FILESYSTEM
→ Deep Inspector
→ Evidence
→ Project Intelligence
→ Neon PostgreSQL
→ Dockerize Context Builder
→ focused evidence
→ devops-qwen
→ deterministic engineering validation
→ Docker artifact generation

Important principle:
Ollama proposes engineering decisions. It does NOT have final authority.
Deterministic validation is the final safety/evidence boundary.

2. Critical Decision: Option A

We explicitly chose Option A:

STRICT EVIDENCE-BOUND DOCKERIZATION.

Rule:
If an exact required fact is not supported by repository/project evidence, Dockerize must return NEEDS_EVIDENCE.

Do NOT infer missing facts.
Do NOT use defaults.
Do NOT allow Ollama to invent runtime versions, ports, commands, or other Docker configuration.

This decision must remain unchanged.

3. Real Test Project

Real project:

/Users/sohal/Downloads/projects/full-stack_chatApp

IMPORTANT:
Do not modify this project during tests except for the intentional .nvmrc change already made.

Current intentional project change:

full-stack_chatApp/.nvmrc

Contents:

20

No Dockerfiles or Compose files have been intentionally created in the real project.

4. Ollama Model

Local Ollama model:

devops-qwen

Also present:

devops-qwen

Both currently point to the same underlying Qwen3 4B Q4_K_M model digest.

Verified model characteristics:

Architecture: qwen3

Parameters: 4.0B

Quantization: Q4_K_M

Context supported by running server: 16384 in current Dockerize testing

Capabilities include completion, tools, thinking

System prompt identifies it as a DevOps AI Control Plane Agent

Temperature configured very low for deterministic behavior

Ollama endpoint:

http://127.0.0.1:11434

The local model is working.

Important Qwen3 observation:
Thinking can consume the response channel. Docker decision requests have used think where appropriate.

5. Important Root Cause Previously Found

Original Dockerize failure:

"Docker decision requires evidence:
No focused Project Intelligence provided from local repository."

Root cause:
OllamaProvider._build_chat_payload() was dropping GenerationRequest.prompt whenever a system prompt existed.

Therefore Ollama received system instructions but not the focused Docker evidence.

This was fixed.

After the fix:

focused context reached Ollama

Ollama returned JSON

deterministic validation became the next boundary

6. Project Intelligence / Neon

Neon is the persistence source of truth.

DATABASE_URL is configured and available in the current development environment.

Verified:

Shell:
DATABASE_URL = YES

Python:
DATABASE_URL = YES

Neon health:
database connected

The real API path is working.

Example endpoint:

GET /api/agent/context?target=/Users/sohal/Downloads/projects/full-stack_chatApp

The API now returns populated Project Intelligence.

7. Runtime Evidence Fix

Problem:
Deep Inspector extracted .nvmrc into project-level intelligence.runtimes but component dictionaries did not contain runtime data.

Then Neon hydration also failed to restore runtime fields into components.

Fix:

Deep Inspector now carries runtime evidence into component data.

Neon hydration restores runtime information.

Current live runtime evidence:

backend:
Node.js 20
source: .nvmrc
confidence: high

frontend:
Node.js 20
source: .nvmrc
confidence: high

Strict runtime rules:

Allowed:

exact 20

exact 20.15.3

exact v20.15.3

Rejected:

20.x



=20

"v14 or higher"

machine Node version

dependency versions

LLM-invented versions

defaults such as node

Node base image must match the exact supported runtime evidence.

Example:
Node.js 20 can authorize node:20 or evidence-supported variants such as node:20-alpine under the current rules.

A model proposal such as node:20.15.3-alpine is rejected when evidence only says 20.

8. README Runtime Rule

Real README contains:

Node.js v14 or higher

This is retained as evidence but is NOT authoritative enough to select an exact Node base image.

Therefore:

README range does not authorize node:14

README range does not authorize node:20

README range does not authorize node:22

Exact runtime evidence must come from authoritative exact sources such as:

.nvmrc

package.json engines.node

existing Dockerfile runtime metadata

other explicitly supported exact runtime evidence

This rule must remain strict.

9. Kubernetes Port Evidence Fix

Next problem:
Frontend Docker decision proposed port 80, but deterministic validation initially rejected it because frontend application-port evidence was missing.

Real project evidence:

Frontend:
k8s/frontend-deployment.yml
containerPort: 80

k8s/frontend-service.yml
port: 80
targetPort: 80

Backend:
k8s/backend-deployment.yml
containerPort: 5001

k8s/backend-service.yml
port: 5001
targetPort: 5001

Fix:
Deep Inspector now:

extracts Kubernetes containerPort as container evidence

promotes it to application evidence only when the same component's Service has a matching targetPort

keeps unmatched Service ports service-only

This avoids blindly treating every Kubernetes Service port as an application port.

Current live evidence:

backend:
application port: 5001
source: k8s/backend-deployment.yml

frontend:
application port: 80
source: k8s/frontend-deployment.yml

Matching Service ports are retained separately.

README/application-port conflicts remain protected.

10. Current Real Project Components

Backend package:

backend/package.json

Important scripts:

dev: nodemon src/index.js

start: node src/index.js

Backend runtime:
Node.js 20

Backend application port:
5001

Backend source:
backend/src/index.js
contains:
server.listen(PORT)

README contains:
PORT=5001

Frontend package:

frontend/package.json

Scripts:

dev: vite

build: vite build

lint: eslint .

preview: vite preview

Frontend runtime:
Node.js 20

Frontend application port:
80

Frontend Kubernetes evidence:
containerPort: 80

11. Command Evidence Fix

Current problem:
The validator originally only accepted a Docker start command if it matched a script named "start".

Frontend package.json does NOT have a "start" script.

It has:

preview: vite preview

Backend does have:

start: node src/index.js

Root package.json has:
start: npm run start --prefix backend
build: npm install --prefix backend && npm install --prefix frontend && npm run build --prefix frontend

The frontend command evidence is correctly extracted, persisted, restored, and included in focused Docker context.

Fix implemented:
Docker start validation now accepts:

exact component start script command
OR

exact component preview script command when no start script exists
including existing package-manager form such as:
npm run preview

Arbitrary commands remain rejected.
Dev commands remain rejected.

Therefore:
frontend "vite preview" is evidence-backed.
frontend "vite" is NOT an acceptable Docker production start command.

12. Most Recent Real Dockerize Result

Latest live focused Docker context:

Selected components:

backend

frontend

Evidence items:
46

Model:
devops-qwen

Focused command evidence:

backend:
start → node src/index.js

frontend:
dev → vite
build → vite build
lint → eslint .
preview → vite preview

Runtime:
backend → Node.js 20
frontend → Node.js 20

Ports:
backend → 5001
frontend → 80

Latest Ollama response was schema-valid and returned:

status: ready

Relevant model decisions:
backend:
start_command: node src/index.js
port: 5001

frontend:
start_command: vite
port: 80

The frontend command is WRONG for Dockerize because "vite" is the development command.

Deterministic validation correctly rejected it:

Docker decision invented start command for frontend

This is currently the correct safe outcome.

A regression test confirms that if Ollama proposes the exact evidence-backed:
vite preview

the validator accepts it.

13. Current Test Status

Latest full test result:

217 passed

Focused Inspector/Dockerize tests:
48 passed

Dockerize workflow tests:
30 passed

Ruff:

focused non-line-length checks passed

default Ruff still reports pre-existing E501 line-length violations in legacy files

Do not treat the pre-existing E501 issues as a Dockerize regression unless the changed code introduces them.

14. Important Previous Test Counts

Useful historical progression:

Original baseline: 187 tests

After initial provider/evidence work: 199

Runtime/port evidence work: 203

Strict runtime enforcement: 206

README runtime evidence refinement: 211

Runtime handoff fix: 212

Kubernetes port evidence fix: 215

Frontend preview command fix: 217

This progression is useful for detecting accidental regressions.

15. Files Changed Across Today's Work

Latest/current implementation changes included:

sohail_agent_cli/providers/base_provider.py
sohail_agent_cli/providers/ollama_provider.py
sohail_agent_cli/dockerize/context_builder.py
sohail_agent_cli/dockerize/decision.py
sohail_agent_cli/inspection/deep_inspector.py
core/storage/project_intelligence.py

Tests updated:

tests/sohail_agent_cli/providers/test_ollama_provider.py
tests/test_dockerize_workflow.py
tests/test_deep_inspector.py

Documentation:
DOCUMENTATION.md

Some files may have been changed in separate commits during the day's work. Use git log/status before making further changes.

16. Git Status / Latest Commit Context

Today the user committed and pushed a set of strict runtime evidence changes.

Commit:
d3de9ef

Message:
"Ruff focuset test pass"

It was pushed to origin/main.

Earlier push:
6c36418

Current repository should be checked with:

git status
git log --oneline -10

Do not assume the working tree is clean without checking.

17. Current Architecture Safety Rules

These MUST remain:

No evidence = NEEDS_EVIDENCE.

No fake Project Intelligence.

No fallback to raw inspection summaries for Dockerize.

No Ollama inference for missing facts.

No invented runtime versions.

No invented ports.

No invented commands.

No destructive command generation.

Preserve project isolation.

Neon remains persistence source of truth.

Docker artifact generation occurs only after deterministic validation succeeds.

Model output must follow strict JSON contract.

Accepted statuses are only:
ready
NEEDS_EVIDENCE

Required decision structure includes:
status
reason
components
compose

Validation must reject arbitrary success/error payloads.

Selected components must match evidence-selected components exactly.

README documentation alone cannot authorize unsupported exact runtime or application port.

Machine-local runtime versions are not project evidence.

Dependency versions are not runtime evidence.

Service ports alone are not application-port evidence.

Kubernetes containerPort + matching Service targetPort can establish application-port evidence for the same component.

Frontend dev command must not be treated as production Docker start command.

Evidence-backed preview command may be accepted when no start script exists.

18. What We Are NOT Going To Do

Do NOT solve the current frontend issue by:

allowing "vite" blindly

treating every npm script as a valid Docker start command

making "dev" acceptable

hardcoding "vite preview"

telling Ollama to always output "vite preview"

bypassing deterministic validation

accepting model output simply because status=ready

using node

using an inferred Node version

inventing port 80

modifying full-stack_chatApp Docker files just to make the test pass

replacing Neon with SQLite

weakening evidence rules

The model is currently making an unsupported proposal.
The validator is correctly stopping it.

19. Immediate Next Task Tomorrow

Primary task:

Investigate WHY devops-qwen prefers:

frontend start_command = vite

instead of the evidence-backed:

frontend start_command = vite preview

Do NOT immediately change validation.

First trace:

focused Project Intelligence
→ prompt construction
→ Ollama system prompt
→ Ollama user prompt
→ JSON response

Determine whether:

the prompt does not clearly distinguish dev/build/preview/start

the model is over-weighting "dev"

the Docker decision schema lacks enough semantic instruction

the context ordering causes the model to choose dev

the command contract should explicitly state Docker runtime command selection

a different evidence representation is needed

The deterministic validator is already protecting the system.

Potential correct future solution:
Improve the decision prompt/contract so the model understands:

For Docker start_command:

Prefer exact "start" script.

If no "start" script exists, use exact "preview" script when appropriate for the component.

Never use "dev" as a production Docker start command unless explicitly supported by evidence and policy.

Never invent commands.

But this should be implemented only after inspecting the current prompt and tests.

20. Next Validation Goal

The next milestone is NOT simply "make Ollama return ready."

The milestone is:

A real end-to-end Dockerize request where:

Inspect reads the real repository.

Project Intelligence is persisted to Neon.

/api/agent/context returns:
backend Node 20, port 5001, command evidence
frontend Node 20, port 80, command evidence

Dockerize retrieves the same persisted intelligence.

Focused evidence is correct.

Ollama proposes only evidence-supported decisions.

Deterministic validation accepts the complete decision.

Dockerfiles/Compose are generated.

Generated artifacts contain only evidence-supported values.

The real project is modified only by the intended generated artifacts.

Tests remain green.

No safety/evidence boundary is weakened.

21. Real API Workflow Already Verified

Uvicorn command:

uvicorn backend.main --reload

Expected server:
http://127.0.0.1:8000

Important API endpoints:
GET /api/agent/context
POST /api/agent/runs

Agent run WebSocket:
/ws/agent-runs/<run_id>

Ollama:
http://127.0.0.1:11434

Useful checks:

DATABASE_URL:
printf 'Shell DATABASE_URL: '
[ -n "$DATABASE_URL" ] && echo YES || echo NO

Python:
.venv/bin/python -c 'import os; print("Python DATABASE_URL:", "YES" if os.getenv("DATABASE_URL") else "NO")'

Ollama:
curl -sS http://127.0.0.1:11434/api/tags | python -m json.tool

Loaded model:
curl -sS http://127.0.0.1:11434/api/ps | python -m json.tool

API context:
curl -sS 'http://127.0.0.1:8000/api/agent/context?target=/Users/sohal/Downloads/projects/full-stack_chatApp' | python -m json.tool

Remember:
URLs must be quoted in zsh because query strings and pasted markdown URLs can cause shell expansion problems.

22. Useful Real Project Evidence Commands

Runtime:

cd /Users/sohal/Downloads/projects/full-stack_chatApp

cat .nvmrc

Package scripts:

cat frontend/package.json
cat backend/package.json
cat package.json

Port evidence:

grep -RniE 
'PORT[=:]|port[=:]|listen(|EXPOSE|targetPort|containerPort|localhost:[0-9]+|127.0.0.1:[0-9]+' 
--exclude-dir=node_modules 
--exclude-dir=.git 
--exclude='package-lock.json' 
. 2>/dev/null | head -200

Kubernetes files:

find k8s -type f -maxdepth 3 -print

Do not use unquoted zsh wildcards such as deployment* unless quoted.

23. Future Development Plan

Phase A — Finish Dockerize evidence/decision path

Fix Ollama's selection of frontend Docker start command.

Keep deterministic validation strict.

Achieve real accepted end-to-end Docker decision.

Generate Dockerfile(s) and Compose only after validation.

Inspect generated artifacts for evidence correctness.

Add regression tests for the successful real path.

Phase B — Dockerize hardening

Multi-component project support.

More precise build/start command semantics.

Better service dependency mapping.

Environment variable evidence handling.

Build context validation.

Dockerfile safety validation.

Compose validation.

Artifact diff/preview before writing.

Preserve no-evidence failure behavior.

Phase C — Control Plane integration

Connect Inspect → Dockerize as explicit operations.

Show Project Intelligence/evidence in UI.

Show model proposal vs deterministic validation.

Show NEEDS_EVIDENCE reasons clearly.

Add operation/run history.

Preserve Chat and Terminal separation.

Phase D — Broader DevOps operations
Potential future operations:

Inspect

Dockerize

Kubernetes

CI/CD

Terraform

Helm

deployment analysis

health checks

Each operation must follow the same evidence-bound decision architecture.

Phase E — Production-quality safety

Strong project isolation.

Explicit workspace boundaries.

Write confirmation for artifact creation where required.

Destructive operation confirmation.

Full audit trail.

Deterministic validators before file writes.

Comprehensive regression suite.

No silent model inference.

24. Mentor Guidance for Tomorrow

Start tomorrow by reading this note first.

Then run:

cd /Users/sohal/Downloads/testing-project/sohail-studio

git status
git log --oneline -10

Then verify:

DATABASE_URL

Ollama

Uvicorn

current test count

Do NOT immediately modify code.

First inspect the current Docker decision prompt and the focused context sent to Ollama.

The current failure is useful evidence:
Ollama sees the frontend command set but still selects "vite".

Therefore the next investigation should focus on the MODEL DECISION CONTRACT/PROMPT, not the Inspector or Neon layers unless new evidence proves otherwise.

25. End-of-Day Status

Overall:

Project Intelligence: GREEN
Neon persistence: GREEN
Runtime evidence: GREEN
Port evidence: GREEN
Command extraction: GREEN
Command persistence/hydration: GREEN
Ollama connectivity: GREEN
JSON contract: GREEN
Deterministic validation: GREEN
Safety boundary: GREEN
Project isolation: GREEN
Full test suite: GREEN — 217 passed
Real Docker artifact generation: NOT YET SUCCESSFUL
Current blocker: Ollama selects frontend dev command "vite" instead of evidence-backed "vite preview"

This is a SAFE blocker, not an architecture failure.

STOP POINT:
Do not continue tonight.

Tomorrow resume from Section 19.
