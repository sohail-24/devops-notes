

## 🎯 Main project goal

Build **Sohail Studio** as a local-first automation AI engineering system targeting approximately **99% correctness** through:

* deterministic validation
* repository evidence
* safe local workflows
* explicit evidence provenance
* bounded AI behavior
* human clarification when facts are missing

**AI must not guess and pretend guesses are facts.**

---

# Current architecture status

The Dockerize workflow now works through this pipeline:

```text
1. Inspect project
        ↓
2. Extract repository evidence
        ↓
3. Persist Project Intelligence to Neon
        ↓
4. Reload latest persisted snapshot
        ↓
5. Build Docker context
        ↓
6. Deterministic Docker preflight
        ↓
7. Missing evidence detected
        ↓
8. Create typed EvidenceGap
        ↓
9. Ollama analyzes the evidence gap
        ↓
10. Strict EvidenceAnalysis parsing
        ↓
11. Validate proposed repository targets safely
        ↓
12. DeepInspector performs bounded acquisition
        ↓
13. New deterministic evidence?
       │
       ├── YES → persist → rebuild context → retry once
       │
       └── NO
             ↓
14. Ask user for typed clarification
             ↓
15. Validate user answer
             ↓
16. Store separately as USER_PROVIDED_EVIDENCE
             ↓
17. Rebuild context
             ↓
18. Retry once
             ↓
19. Normal Docker decision
             ↓
20. Strict validation
             ↓
21. Generate artifacts only if valid
```

---

# What we successfully tested

## Repository inspection

Test project:

```text
/Users/sohal/Downloads/projects/full-stack_chatApp
```

Sohail Studio project:

```text
/Users/sohal/Downloads/testing-project/sohail-studio
```

Important:

⚠️ The system must remain **generic**.

It must work with:

* any valid project path
* any folder name
* different programming languages
* different frameworks

There must be **no hardcoding for `full-stack_chatApp`, React, Vite, Node, or any specific project**.

---

# The missing evidence

The frontend component does not contain enough trustworthy repository evidence for its **production Docker start command**.

The system correctly refused to assume:

```text
npm run dev
```

or:

```text
npm run preview
```

as a production Docker command.

Instead, it safely reached:

```text
NEEDS_CLARIFICATION
```

The GUI displayed:

> **evidence-backed production Docker runtime/start strategy**

Component:

```text
frontend
```

Reason:

> frontend lacks evidence-backed production start command; development and preview commands cannot be used as Docker start commands

Question:

> **What exact production start command should be used for component 'frontend'?**

---

# Current GUI state

The GUI successfully showed:

* clarification heading
* affected component
* reason for missing evidence
* text input
* Submit answer button

This is a **success**, not an error.

The workflow correctly reached the human-in-the-loop safety boundary.

---

# Very important: Do NOT enter “yes”

The current question expects an exact command.

Examples of the type of answer:

```text
npm start
```

or:

```text
node server.js
```

But tomorrow we **must not guess**.

We first need to determine:

1. Does the project already contain real production/deployment evidence that the inspector missed?
2. If not, does the user/project owner know the intended production command?
3. If a command is explicitly supplied by the user, test it as:

```text
USER_PROVIDED_EVIDENCE
```

It must never become:

```text
REPOSITORY_EVIDENCE
```

---

# Evidence provenance rules

The architecture now separates:

```text
REPOSITORY_EVIDENCE
```

Facts extracted from the actual project.

```text
USER_PROVIDED_EVIDENCE
```

Explicit information provided by the user.

```text
VERIFIED_INFERENCE
```

Deterministically derived facts.

```text
AI_ANALYSIS
```

Ollama suggestions and analysis.

## Critical rule

```text
AI_ANALYSIS ≠ accepted evidence
```

Ollama can suggest where to inspect.

Ollama cannot invent facts and close an evidence gap.

---

# Evidence acquisition status

The live workflow successfully did:

```text
Evidence analysis
→ partially valid response
→ 1 valid inspection target
→ 0 malformed targets rejected
→ deterministic validation
→ 1 safe target approved
→ acquisition started
→ deterministic inspection completed
→ no new deterministic evidence
→ Project Intelligence not refreshed
→ clarification required
```

This proves the bounded evidence-acquisition architecture is working.

---

# Latest clarification implementation

Codex implemented:

### Core clarification support

* `core/evidence/clarification.py`
* clarification contracts/models
* clarification IDs
* workflow metadata
* gap ID
* project root
* component
* requirement
* question
* answer type
* allowed/candidate values
* proposition
* evidence references
* status
* timestamp

### Docker policy

Current Docker clarification policy accepts only an appropriate exact production start command.

Rejected examples include:

* empty input
* `Yes`
* `No`
* shell-shaped unsafe input
* control characters
* oversized values

### Backend

Supports:

```text
clarification_required
```

and:

```text
/api/agent/runs/{run_id}/clarification
```

### GUI

Supports dynamic controls:

* text
* select
* yes/no

The control should depend on the missing fact.

### Retry safety

Maximum:

```text
ONE clarification retry per run
```

No infinite loops.

---

# Latest validation from Codex

Latest implementation report:

```text
Focused tests: 72 passed
Full dotenv-isolated suite: 259 passed
Normal suite: 258 passed
Existing dotenv-related failure: 1
```

The normal-suite failure is known environment interference, not introduced by this clarification feature.

Ruff:

* changed files passed applicable non-baseline checks
* existing repository style issues remain

---

# Safety guarantees still active

These must not be weakened:

* deterministic Docker preflight remains authoritative
* `NEEDS_EVIDENCE` remains controlled
* CLI controlled exit code:

```text
2
```

* no arbitrary paths
* no traversal
* no unsafe inspection targets
* no secret-bearing target inspection
* no AI-generated evidence accepted as fact
* no infinite retry loops
* no project-specific hardcoding
* no Docker artifacts without validated evidence

---

# What we do tomorrow

## Step 1 — Continue from current checkpoint

Do **not** rebuild or redesign the whole architecture.

We are here:

```text
Clarification displayed successfully
            ↓
NEXT
            ↓
Test valid clarification answer path
```

---

## Step 2 — Determine the correct production command

Before entering anything:

* inspect whether the project actually contains overlooked deployment evidence
* check deployment documentation/configuration/CI/hosting intent
* do not infer from framework alone

If no repository evidence exists, treat the command as explicitly user-provided.

---

## Step 3 — Test valid answer

The expected flow:

```text
User enters valid production command
        ↓
Backend validates it
        ↓
USER_PROVIDED_EVIDENCE persisted separately
        ↓
Reload/rebuild context
        ↓
One retry
        ↓
Docker preflight
        ↓
Evidence sufficient?
        ↓
Ollama normal Docker decision
        ↓
Strict decision validation
        ↓
Generate Dockerfile / artifacts only if valid
```

---

# Our next milestone

🎯 **End-to-end successful Docker generation with evidence provenance**

We want to prove:

```text
Repository evidence
+
explicit user-provided evidence
+
deterministic validation
+
bounded Ollama reasoning
=
validated Docker output
```

without:

* guessing
* fake evidence
* unsafe commands
* infinite retries
* silent fallback behavior
