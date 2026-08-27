
## 5-Minute Interview Explanation — Sohail Studio

**“One of my main projects is called Sohail Studio. It is a local-first AI engineering workspace and DevOps AI Control Plane that I built to explore a very important problem: how can we use AI for engineering tasks without allowing the AI to blindly guess or directly control our system?”**

The main idea behind the project is that **AI should assist with engineering decisions, but it should not be the final authority**. The final authority should always be real project evidence and deterministic validation.

The architecture is divided into several separate components.

First, there is a **browser-based dashboard** with three main areas: AI Chat, the workspace, and a real terminal environment. The backend is built with **Python and FastAPI**, and communication uses both HTTP REST APIs and WebSockets.

The first major component is the **AI Chat**. The Chat uses a completely local model through **Ollama**. Currently, I use a DevOps-focused Qwen-based model called `devops-qwen`.

One important architectural decision is that the AI Chat does not have unrestricted access to the user's machine. Instead, I created an **AI Control Plane**.

The Control Plane acts as a security and capability boundary between the AI model and the local environment.

For example, if the user asks a normal question like, *“What is Docker?”*, the model can answer normally without accessing the system.

But if the user asks something like, *“What is my current directory?”* or *“Show my Git status,”* the request can go through the Control Plane. The Control Plane only allows explicitly approved **read-only operations**, such as checking the current directory, listing files, checking Git state, Docker status, or Kubernetes information.

Importantly, it does not give the AI arbitrary shell access. It cannot execute destructive commands such as deleting files, resetting Git, stopping containers, or applying Kubernetes resources.

The second major component is the **Raw PTY Terminal**.

This is intentionally separate from the AI Chat. The terminal connects through a WebSocket to a real local PTY, which then connects to the actual shell.

So the flow is basically:

**Browser Terminal → WebSocket → Local PTY → Shell → Real Terminal Output.**

The important architectural principle here is separation. The terminal can provide real unrestricted execution because the user is directly operating it, but the AI Chat cannot secretly use that terminal to execute commands.

The third major part is called **Sohail-Agent**. This is a separate guided DevOps CLI and workflow system. It is not simply another chat interface.

One of its main capabilities is **Project Inspection**.

The Deep Inspector recursively examines a real project repository and extracts deterministic engineering evidence. For example, it can identify project components, manifests, runtime information, commands, ports, infrastructure configuration, and other relevant engineering facts.

However, it has important privacy boundaries. It does not store raw source code contents, `.env` secrets, private keys, credentials, or tokens.

The output from inspection becomes something called **Project Intelligence**.

Project Intelligence is essentially a normalized and persisted representation of what the system actually knows about a project. This information is stored in **PostgreSQL hosted by Neon**, and downstream workflows use this persisted intelligence instead of repeatedly guessing or depending on changing filesystem state.

One of the most important workflows I built using this architecture is the **Dockerize workflow**.

The Dockerize workflow follows a strict pipeline:

**Real Filesystem → Deep Inspector → Evidence → Project Intelligence → PostgreSQL → Focused Context → Local LLM → Deterministic Validation → Artifact Generation.**

This is one of the core ideas of the project.

The LLM does not directly create a Dockerfile and write it to disk. Instead, the model receives only focused engineering evidence and proposes a structured Docker decision.

Then a deterministic validation layer checks that decision against the real evidence.

For example, if the model proposes using:

`node:20`

the system requires authoritative evidence that Node 20 is actually supported by the project. Evidence such as an `.nvmrc` file or explicit `package.json` engine metadata may support that decision.

But the system will not use the developer's local Node version, a dependency version, a README assumption, or simply use `latest`.

Similarly, ports and start commands must be supported by evidence.

If the model invents something, such as a port that was never found in the project, or chooses an unsupported development command for a production Docker container, the validator rejects it.

The workflow returns:

**`NEEDS_EVIDENCE`**

instead of guessing.

This principle is central to Sohail Studio:

> **No evidence means no assumption.**

Another important safety feature is **dry-run protection**.

When a workflow runs in dry-run mode, it performs zero filesystem writes. The system can inspect, build a plan, and validate what would happen, but it cannot actually create or modify artifacts.

Also, Dockerize relies on the previously persisted Project Intelligence rather than rescanning the repository during execution. This helps prevent the workflow from silently changing its understanding if the filesystem changes in the middle of the process.

Currently, the project has successfully implemented the main foundation: the local-first workspace, secure Chat, AI Control Plane, real PTY terminal, project inspection, persisted Project Intelligence, Neon storage, local Ollama decision-making, and deterministic Docker validation.

There is also an interesting current limitation. Sometimes the model may propose a development command such as `vite` when the evidence supports a production-style command such as `vite preview`.

But this actually demonstrates why the architecture is important: the deterministic validator catches the incorrect proposal and safely blocks artifact generation rather than creating an invalid Dockerfile.

For the future, I am expanding the project toward a more advanced **production infrastructure derivation engine**.

The next phases focus on understanding runtime dependencies, classifying evidence more deeply, deriving real service relationships, creating a canonical Docker Compose contract, and eventually generating production-ready Docker and Docker Compose configurations.

The key principle will remain the same:

**First inspect reality. Then classify the evidence. Then derive deterministic engineering rules. Use the model only in a bounded role. Validate everything. And only then generate or write artifacts.**

So overall, Sohail Studio is my attempt to build a more trustworthy AI engineering system where AI is powerful, but it is not blindly trusted. The architecture combines local AI, real system inspection, strict security boundaries, persisted project intelligence, and deterministic validation to make engineering automation safer and more reliable.”

---

## Strong closing line for an interviewer

**“The biggest thing I learned from building Sohail Studio is that the challenge is not simply making an AI generate engineering files. The real challenge is building the system around the AI so that it knows what it is allowed to know, what it is allowed to do, and when it must safely say: I don't have enough evidence.”**

This is a strong interview explanation because it demonstrates not just that you used **FastAPI, Ollama, PostgreSQL, WebSockets, PTY, Docker, and Kubernetes concepts**, but that you understand **system architecture, security boundaries, deterministic validation, AI safety, and engineering reliability**.
