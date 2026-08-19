
# Sohail Studio — Development Checkpoint

**Date:** 19-Aug-2026
**Current Status:** Phase 1 COMPLETE ✅
**Next Step:** Phase 2 — AI Control Plane / Read-Only Local Tools

---

## 1. Project

**Project:** Sohail Studio

**Purpose:**

Sohail Studio is being built as a **local-first AI engineering workspace** where I can interact with an AI mentor and eventually allow it to understand my actual project, inspect my environment, and give DevOps/engineering guidance.

**Local project path:**

```text
/Users/sohal/Downloads/testing-project/sohail-studio
```

Important development rules:

```text
Use the existing local project.

Do NOT clone another project.

Do NOT use GitHub repository URLs for Codex work.

Do NOT create another project.

Do NOT merge.

Do NOT push.

Do NOT run Git commands unless genuinely necessary.

Do NOT generate unnecessary reports.

Run commands only when genuinely necessary.

Build step-by-step.
```

---

# 2. Current UI

Sohail Studio currently has:

```text
Home
Workflows
Terminal
Sessions
Settings
```

Main workspace includes:

```text
Recent Tasks
AI Mentor / 3D Robot
Sohail Studio Chat
Knowledge Sphere
Execution Engine / Terminal
```

Chat controls:

```text
Chat
Terminal
Inspect
Workflow
```

The bottom-right panel represents the execution engine.

---

# 3. Current Terminal Architecture

### Terminal mode

Sohail Studio has a **real persistent local PTY**.

Flow:

```text
Sohail Studio
      ↓
Terminal WebSocket
      ↓
Local PTY
      ↓
Real shell
      ↓
Terminal output
      ↓
Dashboard
```

Commands such as:

```text
pwd
ls
whoami
```

work through the real local shell.

Terminal mode must remain unchanged while future AI features are added.

---

# 4. Current Chat Architecture

Chat was originally connected through an Ollama PTY.

We later improved this.

Current architecture:

```text
Sohail Studio
      ↓
backend
      ↓
OllamaProvider
      ↓
Ollama HTTP API
      ↓
/api/chat
      ↓
devops-qwen:latest
      ↓
streaming response
      ↓
Dashboard
```

Current model:

```text
devops-qwen:latest
```

Do NOT replace it yet.

---

# 5. Phase 1 — COMPLETE ✅

### Phase 1 goal

Stabilize Ollama and make Chat safe and clean.

Completed:

* Ollama HTTP `/api/chat` streaming
* Clean Chat response
* Removed raw PTY/ANSI garbage from central Chat
* Reduced unnecessary context/history
* Added Chat safety instructions
* Chat does NOT execute shell commands
* Chat does NOT falsely claim commands were executed
* Terminal remains real local PTY
* Chat and Terminal remain separate
* Ollama model remains `devops-qwen:latest`

---

# 6. Chat Safety

This was an important discovery.

Previously:

```text
User:
mkdir test-folder

AI:
The directory was created successfully.
```

That was WRONG because the model had not actually executed anything.

Now Chat should behave like:

```text
User:
mkdir test-folder

AI:
This command would create a directory named test-folder,
but Chat mode does not execute commands.
```

Likewise:

```text
rm -rf test-folder
```

must NOT delete anything.

And:

```text
docker compose up -d
```

must NOT start Docker.

Chat is:

```text
CONVERSATIONAL ONLY
```

Terminal is the place for actual commands.

---

# 7. Phase 1 Testing

Codex reported:

```text
9 tests passed
```

Also:

```text
Chat smoke test passed
Terminal smoke test passed
```

Latency measured by Codex:

```text
hello

First token:
~3.76 seconds

Total:
~4.05 seconds
```

Real dashboard experience after Phase 1:

```text
~7–8 seconds
```

This is much better than the earlier:

```text
30+ seconds
```

We decided **not to keep optimizing Phase 1 right now**.

The foundation is good enough to move forward.

---

# 8. Important Ollama Finding

Ollama does NOT automatically know live information.

Example:

```text
What is today's date?
```

Previously it correctly responded that it did not have live system time.

That is acceptable.

We do NOT want Ollama guessing.

Instead, future architecture will give it tools.

---

# 9. Important Project Knowledge Finding

When asked:

```text
What is Sohail Studio supposed to become?
```

Ollama did not know.

It asked for clarification.

This is expected because we haven't yet provided project knowledge.

We should NOT solve this by putting the entire project into the system prompt.

Instead, we will build a proper:

```text
Knowledge
```

layer later.

---

# 10. Future AI Control Plane Architecture

This is the architecture we agreed on:

```text
                    SOHAIL STUDIO
                         │
                         ▼
                  AI CONTROL PLANE
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
          Ollama      Read Tools   Knowledge
             │           │           │
             │       ┌───┼────┐      │
             │       │   │    │      │
             │      time files docker project
             │                       │
             └───────────┬───────────┘
                         ▼
                    Final Answer
```

This is the **main future architecture**.

---

# 11. Phase 2 — NEXT

Tomorrow we start:

## Phase 2 — Read-Only Local Tools

But we will NOT add everything at once.

### First tool:

```text
TIME / DATE
```

Only.

Example:

```text
User:
What is today's date?

        ↓

AI Control Plane

        ↓

Local Time Tool

        ↓

Mac system time

        ↓

Ollama

        ↓

Final Answer
```

This solves the exact problem we already observed.

---

# 12. Phase 2 Development Strategy

We will build tools incrementally.

### Phase 2A

```text
Local Time
```

Test:

```text
What is today's date?
What time is it?
```

---

### Phase 2B

Read-only filesystem/project information.

Example:

```text
What files are in my project?
What is the project path?
What Python files exist?
```

No modifications.

---

### Phase 2C

Docker read-only.

Example:

```text
What Docker containers are running?
What Docker images exist?
```

The tool may execute safe read-only commands such as:

```text
docker ps
docker images
```

but must NOT execute:

```text
docker compose up
docker rm
docker system prune
```

---

### Phase 2D

Git read-only.

Example:

```text
What branch am I on?
What files are modified?
```

Possible read-only operations:

```text
git status
git branch
git log
```

Only when appropriate.

---

### Phase 2E

Kubernetes read-only.

Example:

```text
What pods are running?
What Kubernetes version is installed?
What namespaces exist?
```

Read-only commands only.

---

# 13. Project Knowledge / Inspect

After basic read tools work, we build the **Knowledge** layer.

The future Inspect flow:

```text
User
 ↓
Inspect Project
 ↓
Python Project Inspector
 ↓
Important project files
 ↓
Architecture/context extraction
 ↓
Knowledge
 ↓
Ollama
 ↓
Final Answer
```

The inspector should focus on important information rather than dumping thousands of lines.

Potential information:

```text
project structure
languages
frameworks
dependencies
important configuration
backend
frontend
tests
Docker
Kubernetes
CI/CD
architecture
README
ARCHITECTURE.md
DOCUMENTATION.md
```

---

# 14. Future Agent Architecture

After Project Knowledge is stable, we can build the agent flow originally discussed.

```text
Agent 1
Project Inspector
      ↓
collect important project information
      ↓
Agent 2
Ollama / Understanding
      ↓
understand architecture + problems
      ↓
Agent 3
Mentor / Answer
      ↓
explain project
recommend improvements
```

Example:

```text
Inspect Project

↓

Agent 1:
Find important files and architecture

↓

Agent 2:
Understand what the project actually does

↓

Agent 3:
Tell Sohail:

- what the project does
- current architecture
- problems
- missing components
- possible improvements
- DevOps recommendations
```

This is where **Sohail Studio becomes much more than a chatbot**.

---

# 15. Future Live Information

Later we can add controlled current-information tools.

Examples:

```text
latest Kubernetes version
latest Docker information
current AWS documentation
current technology information
```

Architecture:

```text
User question
     ↓
AI Control Plane
     ↓
Does this require live information?
     ↓
appropriate tool/source
     ↓
Ollama
     ↓
final answer
```

---

# 16. Neon Decision

We discussed using Neon PostgreSQL to host Ollama.

### Decision:

**NO.**

Ollama should remain the inference engine.

If we eventually need a database, it can store things such as:

```text
project knowledge
sessions
conversation history
metadata
tool results
embeddings
```

But Ollama itself should not be moved into Neon.

We will only introduce a database if the architecture actually needs persistent storage.

---

# 17. Ruflo / PicoClaw Decision

We discussed adding:

```text
Ruflo
PicoClaw
other AI agents
```

Decision:

**Not now.**

First build:

```text
Ollama
 ↓
AI Control Plane
 ↓
Read-only tools
 ↓
Project Knowledge
```

Only after that should we evaluate orchestration frameworks.

---

# 18. The Long-Term Vision

The final Sohail Studio should become:

```text
                    SOHAIL STUDIO
                         │
                         ▼
                 AI CONTROL PLANE
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
     Ollama          Local Tools       Knowledge
        │                │                 │
        │        ┌───────┼────────┐        │
        │        │       │        │        │
        │       Time   Files    Docker    Project
        │                │                 │
        │             Git/K8s              │
        │                                  │
        └────────────────┬─────────────────┘
                         ▼
                  Reasoning / Mentor
                         │
                         ▼
                  Final Answer
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
        Chat           Inspect       Workflow
```

The goal is:

> **Sohail Studio should understand my engineering environment and help me operate, troubleshoot, inspect, and improve projects safely — not simply chat with an LLM.**

---

# 19. Development Rule for Tomorrow

We continue **step-by-step**.

Tomorrow:

```text
Phase 2
   ↓
Local Time Tool
   ↓
Test
   ↓
Verify
   ↓
Only then next tool
```

We will **not** jump directly to:

```text
Agents
Ruflo
RAG
Neon
Web
Kubernetes
Docker
Knowledge
```

Everything gets built and tested individually.

---

# 🔖 TOMORROW'S STARTING POINT

When you come back, just tell me:

> **Mentor, continue Sohail Studio from Phase 2.**

We will start from:

```text
PHASE 2 — LOCAL READ-ONLY TIME TOOL
```

No need to explain the project again.
