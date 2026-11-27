# JARVIS AI SYSTEM — DEVELOPMENT HANDOVER NOTES

**Date:** 27 November 2026  
**Project:** JARVIS AI System — Dashboard, AI Brain & Voice Integration  
**Status:** Ollama primary integration and dashboard chat/voice integration successfully tested  
**Next session:** Improve AI response behavior, verify OmniRoute fallback and refine voice interaction.

---

# 1. PROJECT OVERVIEW

We are developing JARVIS 2.0, a local-first personal AI assistant running on macOS.

The system includes:

- Live camera feed
- Face tracking and AI vision HUD
- Hand tracking
- Gesture recognition
- Cursor control
- Voice recognition (STT)
- Text-to-speech (TTS)
- AI chat interface
- Local Ollama AI brain
- OmniRoute as backup AI provider
- PySide6 dashboard

### Development environment

| Component | Details |
|---|---|
| Laptop | MacBook Pro M3 Pro |
| OS | macOS |
| Python | 3.11.15 |
| Virtual environment | venv311_jarvis |
| Ollama | 0.30.10 |
| Dashboard | PySide6 |
| Main coding IDE | Google Antigravity Standalone |
| Inspection/testing assistant | Claude Code |
| AI local provider | Ollama |
| Backup AI provider | OmniRoute |

# 2. PROJECT DIRECTORIES — IMPORTANT

We decided to restart from the original working project instead of continuing with the problematic old dashboard experiment.

### Original backup — DO NOT MODIFY

`/Users/sohal/Downloads/jarvis_ai_system`

### Old dashboard experiment

`/Users/sohal/Projects/jarvis_ai_system`

Do not delete this until the new project is fully verified and explicitly approved.

### Current working project — SOURCE FOR ALL NEW DEVELOPMENT

`/Users/sohal/jarvis/jarvis_ai_system`

### Python environment

`/Users/sohal/jarvis/jarvis_ai_system/venv311_jarvis`

Activate:

```bash
cd /Users/sohal/jarvis/jarvis_ai_system
source venv311_jarvis/bin/activate
```

Launch JARVIS:

```bash
python main.py --dashboard
```

Do not change the launch command without a technical reason.

# 3. TODAY'S COMPLETED WORK

## Stage 7 — Integrated AI Chat Interface

We implemented a modern AI chat panel in the existing dashboard.

New file:

`gui/chat_widget.py`

Updated files:

- `gui/dashboard.py`
- `gui/__init__.py`
- `main.py`

### Features implemented

- User messages aligned to the right.
- JARVIS responses aligned to the left.
- Message timestamps.
- Scrollable chat history.
- Automatic scrolling to the latest message.
- Send button.
- Enter to send.
- Shift + Enter for multiline messages.
- Empty messages ignored.
- Thinking/loading indicator.
- Background AI worker thread.
- Thread-safe response delivery.
- Error handling and clean shutdown.
- Typed chat works when Voice is OFF.
- Voice-originated questions and responses appear in chat.

### Important architecture

The chat interface reuses the existing AIChatModule rather than introducing another independent AI brain.

Both typed and voice questions use the existing AI pipeline.

## Stage 8 — Dashboard redesign

We improved the dashboard layout.

### Current dashboard structure

```text
+-----------------------------------------------------------------------+
|                         JARVIS AI DASHBOARD                           |
+----------------------+--------------------------+---------------------+
|                      |                          |                     |
|    JARVIS AI CHAT    |       LIVE CAMERA        |    SYSTEM STATUS    |
|                      |                          |                     |
|  Welcome Message     |      CAMERA FEED         |  Camera: LIVE       |
|                      |      FACE TRACKING       |  FPS: 30            |
|  Chat History        |      AI VISION HUD       |                     |
|                      |                          |  NOTIFICATIONS      |
|  User Messages       |                          |                     |
|  JARVIS Responses    +--------------------------+  CORE CONTROLS      |
|                      |                          |                     |
|                      |    JARVIS AI ASSISTANT   |  Camera             |
|                      |                          |  Voice              |
|                      |  [ Message Input ]       |  Hand Tracking      |
|                      |                  [SEND]  |                     |
|                      |  [Commands] [Voice]      |  Subsystem Status   |
|                      |  [Gesture] [Files]       |                     |
+----------------------+--------------------------+---------------------+
```

The existing camera, HUD, status and control systems were preserved.

## Stage 1 — Ollama Primary AI Integration

We decided on this architecture:

**JARVIS automatically uses Ollama first and switches to OmniRoute only when Ollama is unavailable.**

### AI provider architecture

```text
                 JARVIS
                    |
             AIChatModule
                    |
               AIChatClient
                    |
              Provider Router
                    |
             Try Ollama First
                    |
           +--------+--------+
           |                 |
        Available         Unavailable
           |                 |
      Ollama Local        OmniRoute
           |              Fallback
           |                 |
           +--------+--------+
                    |
              AI Response
                    |
          Dashboard / Voice
```

### Primary provider

Ollama:

- Endpoint: `http://localhost:11434`
- Default model: `qwen3.5:latest`

### Backup provider

OmniRoute:

- Uses existing OmniRoute configuration.
- Uses existing environment variables and API credentials.
- Activated when Ollama is unavailable under the configured fallback conditions.

### Files changed

- `ai_core/provider_router.py` — new
- `ai_core/ai_client.py`
- `ai_core/__init__.py`
- `ai_chat_module.py`
- `utils.py`
- `test_stage1_ollama_primary.py` — new

### Important behavior

- Ollama is the primary provider.
- OmniRoute is the fallback provider.
- When Ollama becomes available again, new requests should automatically use Ollama.
- Ollama credentials and OmniRoute credentials are kept separate.
- Existing conversation history is preserved.
- Both typed and voice AI requests use the same provider-routing architecture.

### Available local models

Output from `ollama list`:

| Model | Size |
|---|---:|
| devops-qwen:v1 | 2.5 GB |
| qwen3.5:latest | 6.6 GB |
| devops-qwen:latest | 2.5 GB |
| llama3.2:latest | 2.0 GB |
| llama3.2:1b | 1.3 GB |
| qwen3:4b | 2.5 GB |
| gemma3:4b | 3.3 GB |

**Decision:** Keep `qwen3.5:latest` as the default model. We liked its response quality and speed better than the DevOps model during our comparisons.

Do not change the primary model without testing the replacement first.

# 4. STAGE 9 — OLLAMA PERFORMANCE OPTIMIZATION

We investigated why Qwen 3.5 was generating long internal thinking output even for simple greetings.

Inspection confirmed that the model supports the `think` parameter.

The previous implementation did not explicitly disable thinking or set a default generation limit.

### Changes implemented

New configurable settings:

```python
ollama_think = False
ollama_num_predict = 512
```

Environment overrides:

```text
OLLAMA_THINK
OLLAMA_NUM_PREDICT
```

### Parameter explanation

| Parameter | Current setting | Purpose |
|---|---|---|
| think | False | Avoid unnecessary reasoning on ordinary requests |
| num_predict | 512 | Limit maximum generated tokens |
| stream | False | Keep the existing single-response interface |

Complex reasoning can be requested using:

```python
think=True
max_tokens=1024
```

The provider router also includes model capability detection through Ollama `/api/show`, a compatibility retry if a model rejects the `think` parameter, and inference telemetry.

### Performance telemetry

JARVIS now logs:

- Provider
- Model
- Thinking setting
- Token limit
- Total inference duration
- Evaluation duration
- Prompt token count
- Generated token count

### Files changed

- `utils.py`
- `ai_core/provider_router.py`
- `ai_core/ai_client.py`
- `ai_chat_module.py`
- `test_stage9_ollama_optimization.py` — new

# 5. AUTOMATED TEST RESULTS

### Stage 7 — AI Chat

- 65 tests passed.
- Covered chat layout, input handling, loading state, history, voice-to-chat integration and shutdown.

### Stage 1 — Ollama Primary

- 83 tests passed in the combined regression suite.
- Covered primary routing, fallback, credential isolation and conversation history.

### Stage 9 — Ollama Optimization

- 88 tests passed in the combined regression suite.
- Covered thinking control, token limits, telemetry and OmniRoute fallback.

These are separate cumulative test runs, not one combined total.

### Existing test issue

One pre-existing date-related test failed:

`test_date_returns_response`

It expected Wednesday, but the current date was Friday, 27 November 2026.

This was not caused by the Ollama integration.

# 6. LIVE LOCAL TEST RESULTS

## Test 1 — Simple greeting

Command:

```bash
python -c 'from ai_chat_module import AIChatModule; m = AIChatModule(); print(m.process_query("Hello Jarvis")); print(m.ai_client.router.last_metrics); m.cleanup()'
```

Result:

- Provider: Ollama
- Model: qwen3.5:latest
- Think: False
- Generated tokens: 31
- Total duration: 1.861 seconds

**PASS**

## Test 2 — Complex reasoning

We tested:

```python
think=True
max_tokens=1024
```

Result:

- Ollama request timed out after 30 seconds.
- Error was returned.
- OmniRoute did not automatically take over.

**NOT VERIFIED / NEEDS INVESTIGATION**

Do not assume complex reasoning mode is reliable yet.

## Test 3 — Dashboard typed chat

Launch:

```bash
python main.py --dashboard
```

We asked:

- Hello
- Explain Docker in exactly three simple lines.
- What is AWS?

Results:

| Prompt | Duration |
|---|---:|
| Hello | 2.797 seconds |
| Explain Docker | 3.439 seconds |
| What is AWS | 6.226 seconds |

Terminal confirmed Ollama was used for all three.

**PASS**

## Test 4 — Voice integration

Voice assistant initialized successfully.

TTS voice:

`Rishi (English (India))`

We tested:

- Hello Jarvis
- Explain Docker and what it is used for
- Explain Docker in simple words

### Results

- Microphone recognized voice commands.
- Questions reached AIChatModule.
- Provider router selected Ollama.
- Qwen 3.5 generated answers.
- Voice questions appeared in dashboard chat.
- JARVIS started speaking responses through TTS.
- Voice interruption behavior was observed.

Example terminal output:

```text
[AIClient] Provider selected: ollama
(model=qwen3.5:latest, think=False, num_predict=512)

[AIChat] AI context response received
[JARVIS] Speaking response:
```

One Docker explanation generated 512 tokens and took 24.712 seconds.

A later query took 23.613 seconds and generated 479 tokens. That second response was discarded because Voice was disabled while the AI request was still pending.

**PASS for basic voice-to-AI integration. Further voice testing required.**

# 7. CURRENT ISSUES AND OBSERVATIONS

These are improvements, not reasons to discard the working implementation.

### Issue A — Voice answers are too long

The 512-token limit is generous for spoken answers.

We need separate response behavior for:

- Voice: concise, conversational, easy to speak.
- Typed chat: detailed answers when requested.

Important: Do not blindly reduce the global token limit because typed chat may need longer answers.

### Issue B — Instruction-following

The Docker question requested exactly three simple lines, but the response exceeded that limit.

We should improve prompt handling and response formatting.

### Issue C — Complex reasoning timeout

The `think=True` test timed out after 30 seconds.

Investigate the timeout and model reasoning performance before using complex reasoning in normal JARVIS workflows.

### Issue D — Voice interruption

The system logs show that pending voice responses are discarded when Voice is disabled.

We need to verify that:

- The user can interrupt TTS.
- The microphone resumes correctly.
- Pending responses do not speak after Voice is disabled.
- A new voice query does not cause duplicate messages.
- Camera streaming remains smooth during AI inference.

### Issue E — OmniRoute fallback

Automated mocked tests passed, but live fallback has not yet been verified.

We must test it directly.

### Minor warnings observed

- Qt font warning for `-apple-system`.
- `osascript not available` warning from System Controller.
- MediaPipe initialization messages.

These have not been established as blockers. Do not modify unrelated subsystems just to remove harmless warnings.

# 8. NEXT SESSION — EXACT DEVELOPMENT PLAN

Follow this order. Do not jump into new features yet.

## Priority 1 — Improve AI response behavior

Goal:

- Short answers for voice.
- Detailed answers for typed chat.
- Respect requests such as "exactly three lines".
- Avoid unnecessary long responses.
- Preserve conversation history.
- Keep Qwen 3.5 as the default model.

Do not change the model yet.

## Priority 2 — Verify OmniRoute fallback

Test procedure:

1. Start JARVIS with Ollama running.
2. Confirm a normal query uses Ollama.
3. Stop Ollama temporarily.
4. Send a typed question.
5. Confirm logs show fallback to OmniRoute.
6. Restart Ollama.
7. Send another question.
8. Confirm routing returns to Ollama.

Do not modify routing code unless this live test identifies a real problem.

## Priority 3 — Improve voice experience

Test and refine:

- Voice recognition.
- TTS playback.
- Interruptions.
- Microphone listening after TTS.
- Voice ON/OFF behavior.
- Voice message synchronization with chat.
- Preventing stale responses after interruption.

## Priority 4 — Upgrade Ollama

Only after current behavior is stable.

Possible model roles:

| Role | Candidate |
|---|---|
| General assistant | qwen3.5:latest |
| DevOps specialist | devops-qwen:v1 |
| Lightweight backup | llama3.2:1b |
| Additional model evaluation | qwen3:4b, gemma3:4b |

Evaluate response quality, speed, memory usage and reliability before choosing any replacement.

## Priority 5 — Future JARVIS capabilities

After stabilization, consider:

- Better AI vision integration.
- More useful system control.
- DevOps assistant capabilities.
- Local file understanding.
- Better command execution and permission handling.

Do not add unnecessary features before stabilizing the existing system.

# 9. IMPORTANT DEVELOPMENT RULES

1. Preserve the original Downloads backup.
2. Work only in `/Users/sohal/jarvis/jarvis_ai_system`.
3. Do not replace the existing camera pipeline.
4. Do not rewrite `hand_tracking.py` without a demonstrated need.
5. Do not break working voice recognition or TTS.
6. Do not replace the existing AIChatModule with a second AI architecture.
7. Keep Ollama as primary and OmniRoute as fallback.
8. Test changes before moving to the next stage.
9. Avoid unnecessary refactoring.
10. Do not add new features unless they are important.
11. Use Google Antigravity for focused implementation.
12. Use Claude Code for code inspection, diagnostics and test reports.
13. Use ChatGPT as the architecture and development mentor.

**Important workflow preference:** Keep coding tasks short and focused. Avoid giant prompts that cause unrelated code changes.

# 10. NEXT SESSION STARTING POINT

Current project directory:

```bash
cd /Users/sohal/jarvis/jarvis_ai_system
source venv311_jarvis/bin/activate
```

Check Ollama:

```bash
ollama list
```

Check the local service:

```bash
curl http://localhost:11434/api/tags
```

Launch JARVIS:

```bash
python main.py --dashboard
```

### First task next time

Start with **Priority 1: Improve AI response behavior**.

Before modifying anything, inspect the current implementation of:

- `ai_chat_module.py`
- `ai_core/provider_router.py`
- `ai_core/ai_client.py`
- `gui/chat_widget.py`
- `main.py`

Focus on separating voice and typed response behavior without breaking conversation history or provider routing.

Then test the improvement locally.

---

# FINAL PROJECT STATUS

**Completed and live-tested:**

- Dashboard redesign
- Camera feed
- AI chat panel
- Ollama primary provider
- OmniRoute fallback architecture
- Qwen 3.5 inference optimization
- Typed AI chat
- Basic voice-to-AI integration
- Rishi TTS response playback

**Still pending:**

- Better voice answer length and formatting
- Live OmniRoute fallback verification
- Ollama automatic recovery verification
- Complex reasoning timeout investigation
- Further voice interruption testing
- Future Ollama model upgrades

**Current AI architecture decision:**

Ollama (`qwen3.5:latest`) = PRIMARY BRAIN

OmniRoute = BACKUP BRAIN

**Current launch command:**

`python main.py --dashboard`

**Next starting task:**

Improve AI response behavior while preserving everything that currently works.

---

END OF JARVIS DEVELOPMENT HANDOVER — 27 NOVEMBER 2026
