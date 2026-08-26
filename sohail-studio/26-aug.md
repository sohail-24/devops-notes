
## 1. Main Goal

We are building **Sohail Studio Dockerize** as a:

* evidence-bound
* deterministic-first
* project-aware
* multi-language
* local AI-assisted

Docker generation workflow.

The system must **inspect the actual project in real time**, understand what technology the project really uses, and generate Docker artifacts based on:

1. Real repository evidence
2. Deterministic derived evidence
3. Explicit approved platform policies
4. Bounded model assistance

### Critical principle

> **No guessing. No copying a generic Dockerfile. No stale inspection data.**

Dockerize must use the selected/current persisted inspection snapshot. It must not silently use old data or scan the repository again during Dockerize.

---

# 2. Architecture Direction

The intended architecture is:

```text
PROJECT INSPECTION
        │
        ▼
Repository Truth
────────────────────────
Languages
Runtime versions
Frameworks
Build system
Application type
Components
Ports
Commands
Artifacts
Dependencies
Deployment files
Existing Docker files
        │
        ▼
Deterministic Derivation
────────────────────────
Derived artifacts
Derived launch commands
Build facts
Component relationships
        │
        ▼
GENERIC TECHNOLOGY PROFILE
────────────────────────
technology_profile
├── languages
├── runtimes
├── frameworks
├── build_system
├── application_type
├── component_role
├── explicit evidence
├── derived evidence
└── inspection identity
        │
        ▼
DOCKER CONTEXT
        │
        ├─────────────── Repository / Derived Evidence
        │
        └─────────────── Approved Platform Policy
                         ├── Java/Spring Boot
                         ├── Node.js
                         ├── Python
                         ├── Nginx
                         ├── React/Vite
                         └── future technologies
        │
        ▼
VALIDATED CONTEXT
        │
        ▼
Bounded Ollama Decision
        │
        ▼
Deterministic Validation
        │
        ▼
Technology-Specific Rendering
        │
        ▼
Dockerfile / Compose / Docker Ignore
        │
        ▼
Artifact Validation
        │
        ▼
Dry Run Preview OR Explicit Write
```

The important improvement is:

> We are no longer designing Dockerize as a Java-only system.

It must support different technology families through **generic technology context + explicit policies + separate renderers**.

---

# 3. Completed Before Today

Previously, the Java/Spring Boot Dockerize workflow was completed successfully.

Real repository used:

```text
/Users/sohal/Downloads/projects/expenses-tracker_webapp
```

Detected real project facts included:

* Java 17
* Spring Boot
* Maven
* MySQL dependency
* application port `9090`
* exact deterministic JAR artifact
* exact deterministic launch command

Generated Dockerfile:

```dockerfile
FROM maven:3.9.16-eclipse-temurin-17 AS build

WORKDIR /app

COPY . .

RUN mvn package

FROM eclipse-temurin:17-jre-jammy

WORKDIR /app

COPY --from=build /app/target/ExpensesTracker-0.0.1-SNAPSHOT.jar /app/target/ExpensesTracker-0.0.1-SNAPSHOT.jar

EXPOSE 9090

CMD ["java", "-jar", "target/ExpensesTracker-0.0.1-SNAPSHOT.jar"]
```

Generated Compose was minimal:

```yaml
services:
  application:
    build: .
    ports:
      - "9090:9090"
```

This successfully proved:

* persisted inspection reuse
* zero repository rescans during Dockerize
* deterministic preflight
* bounded Ollama decision
* policy-based base image
* policy-based working directory
* evidence validation
* dry run
* normal execution
* selected artifact writing

---

# 4. Important Existing Authority Model

The Dockerize system now has this authority hierarchy:

```text
1. EXPLICIT_EVIDENCE
2. DERIVED_DETERMINISTIC
3. APPROVED_PLATFORM_POLICY
4. MODEL_PROPOSED
5. UNSUPPORTED
```

Meaning:

### Explicit repository evidence

Real facts found in the project.

Examples:

```text
Java 17
Port 9090
pom.xml
application.properties
```

### Deterministic derived evidence

Facts deterministically calculated from repository evidence.

Examples:

```text
Exact executable JAR
Exact production launch command
```

### Approved platform policy

Explicit platform decisions not found in the repository.

Examples:

```text
Approved Java runtime image
Approved WORKDIR
Approved build image
```

### Model proposed

Ollama can suggest within a bounded context but:

> Ollama cannot invent authoritative project facts.

It cannot override:

* runtime
* artifact
* port
* command
* selected component
* approved policy values
* artifact scope

---

# 5. Previous Java Platform Policy

Current policy:

```text
java-spring-boot-container-v1
version: 1
```

Applies when evidence proves:

```text
Java
Java 17
Spring Boot
deterministic executable JAR
java -jar launch strategy
```

Policy authorizes:

```text
Runtime image:
eclipse-temurin:17-jre-jammy

WORKDIR:
/app

Build image:
maven:3.9.16-eclipse-temurin-17
```

These are explicitly marked:

```text
APPROVED_PLATFORM_POLICY
```

They are **not repository evidence**.

---

# 6. Problem Identified Today

We looked at the original project's existing Docker artifacts on GitHub.

The original project Dockerfile was richer and included design decisions such as:

```dockerfile
# Stage 1 – Build the JAR
FROM maven:3.8-eclipse-temurin-17 AS build

WORKDIR /app

COPY . .

RUN mvn clean package -DskipTests

# Stage 2 – Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

ENV SERVER_PORT=9090

EXPOSE 9090

ENTRYPOINT ["java", "-jar", "app.jar", "--server.port=9090"]
```

Original Compose was also much richer:

* MySQL service
* application service
* healthcheck
* database dependency
* network
* ports
* container names

Example concepts:

```text
mysql
├── image
├── environment
├── ports
├── healthcheck
└── network

application
├── build
├── image
├── ports
├── depends_on
│   └── service_healthy
└── network
```

Our generated Compose currently has only approximately:

```yaml
services:
  application:
    build: .
    ports:
      - "9090:9090"
```

That is technically valid, but it is **too simplistic for the quality level we want**.

However:

> We must NOT simply copy the original project's Dockerfile or Compose.

The system must inspect and determine whether those things are actually supported by current evidence.

For example:

* MySQL dependency ≠ automatic permission to generate a MySQL container.
* A repository README mentioning MySQL ≠ enough to invent credentials.
* A database URL/environment configuration may provide stronger evidence.
* Existing Docker/Compose files are repository evidence but must be interpreted carefully.
* Dockerize must understand what is already present versus what the user asked to generate.

---

# 7. User Requirements Established Today

You explicitly requested:

### A. Multi-language Dockerize

Not Java-only.

Future technology support should include at minimum:

```text
Java / Spring Boot
Node.js
Python
React
Vite
Nginx
```

Potential future families:

```text
FastAPI
Flask
Django
Express
Next.js
Gradle
Go
Rust
static frontend
reverse proxy
```

But technology support must be added correctly.

No generic fallback like:

```text
everything → Node renderer
```

No hidden defaults like:

```text
unknown technology → /app
unknown runtime → latest
unknown port → 8080
```

Unknown remains:

```text
NEEDS_EVIDENCE
```

or another controlled unsupported state.

---

### B. Dry Run Must Show Generated Files Clearly

Current Dry Run logs are useful but the file previews need better structure.

Desired behavior:

```text
DRY RUN COMPLETED

Generated artifacts:

┌─────────────────────────────────────────────┐
│ Dockerfile                                  │
├─────────────────────────────────────────────┤
│ FROM ...                                    │
│ WORKDIR ...                                 │
│ ...                                         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ docker-compose.yml                          │
├─────────────────────────────────────────────┤
│ services:                                   │
│   ...                                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ .dockerignore                               │
├─────────────────────────────────────────────┤
│ ...                                         │
└─────────────────────────────────────────────┘
```

Requirements:

* print each selected/generated file separately
* clear filename/path
* clear boundary between files
* do not mix previews confusingly
* indicate:

  * CREATE
  * UPDATE
  * KEEP
  * SKIPPED
* dry run must still write zero files

---

### C. Docker Compose Needs More Intelligence

Compose must not always be:

```yaml
services:
  application:
    build: .
```

It should be designed based on actual inspected project facts.

Possible evidence-driven Compose concepts:

```text
Application service
Database service
Cache service
Message broker
Networks
Volumes
Health checks
depends_on
environment
ports
```

But each service must have authority.

Example:

```text
Repository evidence says PostgreSQL URL exists
        ↓
Database dependency is strongly established
        ↓
Can Dockerize construct a service?
        ↓
Only if exact version/config/credentials/default policy
are authorized
```

If exact values are unknown:

```text
NEEDS_EVIDENCE
```

Do not invent:

```text
postgres:16
username: postgres
password: password
```

unless explicitly authorized by evidence or policy.

---

### D. Docker Command Suggestions

You requested a new output box at the bottom of Dockerize results.

Example:

```text
┌──────────────── TERMINAL COMMANDS ────────────────┐

Build and start:
docker compose up --build

Run in background:
docker compose up -d --build

Stop services:
docker compose down

View running containers:
docker ps

View logs:
docker compose logs -f

Rebuild:
docker compose build --no-cache

└───────────────────────────────────────────────────┘
```

Important design rule:

> Commands must be relevant to the generated artifacts and actual project.

Do not blindly print:

```text
docker run -d --name webserver -p 8080:80 nginx:latest
```

for every project.

For example:

### Nginx project

Relevant commands could include:

```bash
docker build -t project-nginx .
docker run -d --name project-nginx -p 8080:80 project-nginx
```

### Compose project

Relevant commands:

```bash
docker compose up --build
docker compose up -d --build
docker compose down
docker compose logs -f
```

### Single Dockerfile project

Relevant commands:

```bash
docker build -t project-name .
docker run -p HOST_PORT:CONTAINER_PORT project-name
```

Commands must come from the actual generated plan and evidence.

---

# 8. Step 1 Completed Today

Codex completed Step 1.

Changed files:

```text
core/storage/project_intelligence.py
sohail_agent_cli/dockerize/context_builder.py
sohail_agent_cli/dockerize/platform_policy.py
sohail_agent_cli/dockerize/decision.py
tests/test_step1_technology_context.py
```

Step 1 added generic Docker technology context:

```text
technology_profile
├── languages
├── runtimes
├── frameworks
├── build system
├── application type
├── component role
├── explicit evidence
├── derived evidence
├── applicable policies
└── inspection run identity
```

Important fixes:

### Exact inspection identity

Dockerize can now load the exact requested inspection run using:

```text
load_run()
```

It should not silently fall back to:

```text
latest inspection
```

This is important because we explicitly require:

> Current requested inspection data only. No accidental old snapshot substitution.

### Unsupported technology safety

Unknown technologies:

* do not fall into Node renderer
* do not get implicit `/app`
* remain unresolved/controlled

### Step 1 tests

```text
Focused tests: 66 passed
Full suite: 311 passed
```

---

# 9. Current Git/Worktree Situation

Codex reported existing changes that were preserved:

```text
modified Dockerfile
modified docker-compose.yml
deleted Jenkinsfile
untracked .dockerignore
```

Important:

> Do not casually reset or clean the worktree tomorrow.

Preserve existing changes unless we intentionally inspect and decide otherwise.

---

# 10. Step 2 — NEXT TASK TOMORROW

We continue from **Step 2**.

The main objective should be:

## Build the reusable technology-aware Docker rendering architecture.

Likely direction:

```text
Generic Technology Context
        │
        ▼
Technology Detection / Classification
        │
        ▼
Applicable Policy Selection
        │
        ▼
Renderer Selection
        │
        ├── Java/Spring Boot
        ├── Node.js
        ├── Python
        ├── Static Frontend
        └── Nginx
        │
        ▼
Artifact Plan
        │
        ├── Dockerfile
        ├── docker-compose.yml
        └── .dockerignore
```

Step 2 should probably focus on the **technology-aware rendering/policy framework**, not trying to implement every possible language perfectly at once.

We need inspect current code first and determine:

* what renderer abstractions already exist
* how Node currently works
* whether Java and Node share enough architecture
* where technology-specific policy should live
* where rendering selection belongs
* how validation can remain deterministic

Potential Step 2 supported families:

```text
1. Java / Spring Boot
2. Node.js
3. Python web applications
4. Static React/Vite → Nginx runtime
5. Nginx projects
```

But implementation must follow real evidence.

For each family, determine required evidence.

Example:

### Python

Could require evidence such as:

```text
requirements.txt
pyproject.toml
Pipfile
framework dependency
entrypoint
port
```

Do not assume:

```text
CMD uvicorn main:app
```

without evidence.

---

### Node.js

Could inspect:

```text
package.json
package-lock.json
pnpm-lock.yaml
yarn.lock
scripts
framework dependencies
start script
build script
port
```

No guessing whether:

```text
npm run start
```

or:

```text
npm run dev
```

or:

```text
node server.js
```

Production command must be evidence-backed.

---

### React/Vite

Need distinguish:

```text
development project
```

from:

```text
production static build
```

Likely evidence:

```text
package.json
build script
dist output
framework
vite config
```

If production static output is deterministically established:

```text
Build stage
→ Node
Runtime stage
→ Nginx
```

But Nginx configuration should not be invented unless default policy is explicitly allowed.

---

### Nginx

Need inspect:

```text
nginx.conf
conf.d
existing site configuration
static files
Docker artifacts
ports
```

No assumption that every Nginx project uses:

```text
80
```

unless evidence/policy authorizes it.

---

# 11. Step 3 — Planned After Step 2

Step 3 is the **output quality and Docker Compose intelligence stage**.

Main goals:

### 1. Improve Dry Run artifact display

Separate artifact boxes:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

Each must have:

```text
status
path
authority summary
content preview
```

---

### 2. Improve Docker Compose generation

Compose should become evidence-aware.

Concept:

```text
Technology profile
+
component graph
+
runtime dependencies
+
explicit configuration
+
authorized platform policy
        │
        ▼
Compose Service Plan
```

Potential service types:

```text
application
database
cache
proxy
worker
frontend
```

But:

> Never generate services merely because a dependency package exists.

There must be sufficient authority.

---

### 3. Add Docker command output box

At the bottom of successful output:

```text
NEXT STEPS / TERMINAL COMMANDS
```

Commands should be derived from:

* Dockerfile
* Compose
* service names
* ports
* image strategy

Example:

```text
docker compose up --build
docker compose up -d --build
docker compose logs -f
docker compose down
```

Or, for a Dockerfile-only project:

```text
docker build -t <project> .
docker run ...
docker ps
docker logs ...
docker stop ...
docker rm ...
```

No irrelevant generic commands.

---

### 4. Better artifact quality validation

Validate:

```text
Dockerfile structure
Compose syntax/structure
service relationships
ports
healthcheck references
depends_on references
environment references
generated command consistency
```

---

# 12. Important Rules for Tomorrow

When we continue, follow these rules strictly:

### Never guess

If not proven:

```text
NEEDS_EVIDENCE
```

is acceptable.

### Never copy a repository's existing Docker files blindly

Existing files are evidence, not automatically the new generated solution.

### Inspect actual current project

Do not use stale assumptions.

### No hidden defaults

Every value must come from:

```text
repository evidence
deterministic derivation
approved policy
```

### Keep Ollama bounded

Ollama is not the authority.

### No unnecessary redesign

We have limited Codex usage.

Each step should be:

```text
small
focused
testable
end-to-end
```

### Preserve architecture neutrality

The system itself must not become:

```text
Java-specific
Node-specific
Spring-specific
```

The architecture should be generic while policies/renderers are technology-specific.

---

# 13. Where We Resume Tomorrow

Start with:

> **Sohail Studio Dockerize — Step 2**

First inspect the current Step 1 implementation and existing Docker renderer architecture.

Then verify:

```text
technology_profile
```

actually flows correctly through:

```text
persisted inspection
→ DockerContext
→ policy applicability
→ decision
→ renderer selection
→ validation
```

Then implement the next minimal reusable technology-aware rendering layer.

**Do not jump directly into Step 3 output/UI improvements until Step 2 architecture is correct.**

---

# 14. Overall Roadmap

```text
STEP 1 ✅ COMPLETE
Generic technology context
Freshness/inspection identity
No unsupported fallback
311 tests passed

        ↓

STEP 2 ⏳ NEXT
Technology-aware policies/renderers
Java
Node
Python
Static frontend
Nginx
Evidence requirements
Renderer selection

        ↓

STEP 3 ⏳ AFTER STEP 2
Dry Run artifact boxes
Improved Compose intelligence
Evidence-bound service planning
Terminal command suggestions
Output/UX improvements

        ↓

FINAL VERIFICATION
Multiple real repositories
Different technologies
Dry Run
Normal execution
No stale inspection
No repository rescan
No guessing
No unauthorized services
No unrelated files modified
```

Tomorrow, just say **“mentor continue Sohail Studio Step 2”** and we can continue from this checkpoint.
