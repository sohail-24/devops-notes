# JARVIS 2.0 — MASTER PROJECT & DEVELOPMENT NOTES

**Project:** JARVIS 2.0 — Local macOS Personal AI Assistant  
**Developer:** Sohail  
**Development Machine:** MacBook Pro M3 Pro (Apple Silicon)  
**Current Development Environment:** macOS + Python 3.11  
**Current Stage:** AI Brain — Milestone 1 completed; first live AI response tested  
**Last Development Session:** November 23, 2026

---

# 1. PROJECT OVERVIEW

Jarvis 2.0 is a local-first personal AI assistant for macOS.

The goal is to upgrade the existing Jarvis application into a powerful personal AI assistant with:

- Multiple AI model providers.
- Natural language conversations.
- Voice interaction.
- Computer and system automation.
- Hand gesture recognition.
- Computer vision.
- Memory and contextual conversations.
- System monitoring and control.
- A modern visual interface.

**Important development decision:**

We are upgrading the existing Jarvis application, NOT deleting it and building a completely new application.

Existing functionality must be preserved.

We will develop and test each module independently before integrating it into the main application.

---

# 2. PROJECT LOCATION AND ENVIRONMENT

**Project directory:**

`~/Downloads/jarvis_ai_system`

**Main environment:**

- Operating System: macOS
- Hardware: MacBook Pro M3 Pro
- Python: 3.11.15
- Active virtual environment: `venv311`
- Node.js: Installed
- npm: Installed

Activate the Python environment:

```bash
cd ~/Downloads/jarvis_ai_system
source venv311/bin/activate
```

The terminal should show:

```text
(venv311)
```

Important installed Python packages include:

- requests
- python-dotenv
- SpeechRecognition
- pyttsx3
- OpenCV and computer-vision dependencies

Use the existing virtual environment rather than creating another one unnecessarily.

---

# 3. EXISTING JARVIS ARCHITECTURE

The existing project contains approximately 18,000 lines of Python code.

Important existing files:

| File | Responsibility |
|---|---|
| `main.py` | Main application entry point |
| `ai_chat_module.py` | Original rule-based AI placeholder |
| `voice_assistant.py` | Voice recognition and speech output |
| Hand tracking modules | Hand and gesture recognition |
| Cursor controller | Mouse movement and gesture-based control |
| System controller | System operations |
| Media controller | Media operations |
| HUD components | OpenCV-based visual interface |

### Existing functionality

**Voice assistant**
- Speech recognition using SpeechRecognition.
- Google speech recognition API.
- Text-to-speech using pyttsx3.

**Computer vision**
- OpenCV.
- Hand tracking.
- Gesture recognition.
- Cursor control.

**System and media**
- System controller.
- Media controller.
- Desktop interaction capabilities.

### Existing issues identified earlier

These are older audit findings, not necessarily currently fixed:

1. `cursor_controller.toggle_enabled()` was called from `main.py` but was missing.
2. A test block in hand tracking referenced `self` outside the class.
3. Duplicate microphone access was identified.
4. Shared TTS and command queue concerns were identified.
5. Debug print statements needed cleanup.

Do not fix unrelated legacy issues during AI Brain development unless necessary.

---

# 4. AI BRAIN — NEW ARCHITECTURE

We decided to introduce a dedicated AI Core module.

Architecture:

```text
             USER
              |
              v
       JARVIS APPLICATION
              |
              v
          AI BRAIN
              |
              v
       Python AI Client
              |
              v
          OMNIROUTE
              |
       +------+------+
       |      |      |
       v      v      v
     Gemini OpenAI Mistral
       |
       +------ FreeLLMAPI
       |
       +------ Other providers
              |
              v
       AI RESPONSE
              |
              v
          JARVIS
```

The purpose of OmniRoute is to provide one local API interface through which Jarvis can communicate with different AI providers.

We do not want to hardcode one AI provider into the entire application.

### AI Brain development principles

1. Keep the AI client independent.
2. Use environment variables for configuration.
3. Never hardcode API keys.
4. Keep existing Jarvis modules untouched during isolated testing.
5. Support model selection.
6. Handle API errors and timeouts.
7. Build conversation memory later.
8. Integrate voice only after the AI Core is reliable.

---

# 5. OMNIROUTE SETUP

OmniRoute v3.8.54 is installed through npm.

**Local dashboard:**

`http://localhost:20128`

**OpenAI-compatible API base:**

`http://127.0.0.1:20128/v1`

**Chat completion endpoint:**

`http://127.0.0.1:20128/v1/chat/completions`

### API keys

Two keys were registered in OmniRoute:

- Claude-Code-Local
- Jarvis-Local

The Jarvis application uses the Jarvis-Local key.

Never share the complete API key in project notes, screenshots, GitHub, or chat.

### Configured providers

Previously configured providers include:

- Google AI Studio / Gemini
- OpenAI
- Mistral
- Groq
- FreeLLMAPI

Groq previously showed no free models available in the provider configuration.

Search providers configured in FreeLLMAPI include:

- Tavily
- Firecrawl
- Exa
- Outcrawl
- Parallel

These search providers are separate from normal chat model providers.

### Important distinction

Claude Code is a development tool.

OmniRoute is the AI routing layer used by Jarvis at runtime.

Jarvis must not depend on Claude Code to answer user messages.

---

# 6. AI BRAIN FILES CREATED

The following files were created:

```text
jarvis_ai_system/
│
├── ai_core/
│   ├── __init__.py
│   └── ai_client.py
│
├── test_omniroute.py
├── test_ai_chat.py
│
├── main.py
├── ai_chat_module.py
├── voice_assistant.py
│
├── .env
└── .gitignore
```

### ai_core/ai_client.py

This is the main Python client for OmniRoute.

It provides:

**AIChatClient**

- Initializes the API client.
- Loads configuration from environment variables.
- Uses Bearer token authentication.
- Creates a requests session.
- Supports connection timeouts.
- Lists available models.
- Sends chat completion requests.
- Handles API errors.
- Extracts assistant responses.

Important methods:

```python
AIChatClient()
```

```python
client.list_models()
```

```python
client.chat(messages, model=None)
```

```python
client.get_completion(message, system_prompt=None)
```

```python
client.test_connection()
```

```python
client.close()
```

The `chat()` method returns the complete API response as a dictionary.

The `get_completion()` method extracts the assistant's response text.

### test_omniroute.py

Used to test:

1. Environment credentials.
2. AI client initialization.
3. API authentication.
4. Model discovery.
5. Model selection.

### test_ai_chat.py

Used to test an actual conversation with an AI model through OmniRoute.

It is separate from the existing main Jarvis application.

---

# 7. ENVIRONMENT CONFIGURATION

The `.env` file contains:

```env
OMNIROUTE_BASE_URL=http://127.0.0.1:20128/v1

JARVIS_LOCAL_API_KEY=YOUR_ACTUAL_OMNIROUTE_KEY

JARVIS_MODEL=gemini/gemini-3-flash-preview
```

The actual API key must remain private.

The `.gitignore` already includes `.env`.

### Important lesson from today's debugging

We initially entered the wrong value for the API key.

The value included the label `jarvis key:` rather than only the actual secret.

Python verification initially showed:

```text
Prefix: jar
Contains label: True
Length: 47
```

We corrected the `.env` entry.

Final verification:

```text
Starts with sk-: True
Contains label: False
Length: 35
```

This fixed the authentication problem.

Do not repeat this mistake: copy only the complete API key into the environment variable.

---

# 8. WORK COMPLETED — NOVEMBER 23, 2026

## Milestone 1: Authentication and model discovery

### Problem 1 — Invalid API key

Initial test:

```text
Authentication failed:
Invalid API key
```

Root cause:

The `.env` value included additional label text.

Solution:

Corrected the `JARVIS_LOCAL_API_KEY` entry.

Result:

- Environment loading works.
- Authentication succeeds.
- Model discovery succeeds.

## Problem 2 — Model discovery test bug

The model catalogue was successfully retrieved, but Test 5 showed:

```text
No models available to select from
```

We inspected:

```python
def test_valid_model_for_chat(model_list):
```

The actual problem was in `main()`:

```python
valid_model = test_valid_model_for_chat([])
```

This passed an empty list.

### Fix implemented

Inside `test_model_discovery()`:

Changed the successful return to:

```python
client.close()
return True, models
```

In `main()`:

Changed:

```python
models_passed, models_displayed = test_model_discovery()
```

To:

```python
models_passed, discovered_models = test_model_discovery()
```

Changed:

```python
if models_displayed:
    valid_model = test_valid_model_for_chat([])
```

To:

```python
if discovered_models:
    valid_model = test_valid_model_for_chat(discovered_models)
```

Result:

The test successfully selected:

```text
auto/best-coding
```

Test summary:

```text
Total tests passed: 6
Total tests failed: 0

All tests passed!
```

Note: `auto/best-coding` was the first available model selected by the fallback logic. It is not our final chosen default model.

## Problem 3 — First live AI request timed out

Initial output:

```text
Request to http://127.0.0.1:20128/v1/chat/completions
timed out after 30s
```

A later execution succeeded without changing the architecture.

This suggests the first timeout may have been temporary, but we still need to test reliability.

## Problem 4 — Incomplete first response

Initial output:

```text
Jarvis:
Hello! I am
```

We inspected `get_completion()`.

Its response extraction was:

```python
return choice['message'].get('content', '')
```

No obvious truncation bug was found there.

### Claude Code investigation

Claude Code inspected the files and identified the original:

```python
max_tokens=200
```

The raw API response reportedly showed:

```text
finish_reason: length
```

This indicates generation stopped at the token limit.

Claude then increased the diagnostic request limit to:

```python
max_tokens=1000
```

Claude reported:

```text
Response length: 513 characters
finish_reason: stop
```

This suggests the larger token limit resolved the incomplete response in that test.

Important: This was a reported Claude Code test result. The final syntax check was verified separately.

---

# 9. CURRENT TEST RESULTS

Final syntax validation command:

```bash
python -m py_compile test_ai_chat.py
```

Output:

```text
(venv311) sohal@Mohammeds-MacBook-Pro jarvis_ai_system %
```

No error was produced.

Therefore:

- `test_ai_chat.py` passes Python syntax compilation.
- The earlier authentication issue is fixed.
- Model discovery works.
- Model selection works.
- A real Gemini response has been received.
- Claude reported a complete response with a higher token limit.

### Current milestone status

| Component | Status |
|---|---|
| Python AI client | Implemented |
| Environment loading | Working |
| OmniRoute authentication | Working |
| Model discovery | Working |
| Model selection | Working |
| Gemini model configuration | Set |
| First live AI response | Received |
| Complete response test | Reported successful by Claude |
| Python syntax validation | Passed |
| Multi-provider runtime testing | Pending |
| Conversation memory | Pending |
| Voice integration | Pending |
| Main Jarvis integration | Pending |

**Milestone 1 — Authentication and model discovery: completed.**

**Basic AI chat connection: demonstrated.**

The AI Brain is not yet fully integrated into the main Jarvis application.

---

# 10. CURRENT DEVELOPMENT TOOLS

### Claude Code

Claude Code is installed and working.

Previously used version:

`2.1.329`

The existing launch workflow:

```bash
claude-free
```

Continue using the established OmniRoute / FreeLLMAPI development setup.

### ChatGPT mentor workflow

Use ChatGPT as the architecture and debugging mentor.

Use Claude Code for:

- Inspecting source files.
- Editing Python modules.
- Running tests.
- Fixing bugs.
- Reviewing changes.
- Generating technical reports.

Important working method:

1. Discuss the problem with the mentor.
2. Inspect the relevant code.
3. Give Claude a narrowly scoped task.
4. Review Claude's proposed changes.
5. Run tests.
6. Share results with the mentor.

Do not allow Claude to make unrelated architectural changes.

---

# 11. NEXT DEVELOPMENT PLAN

## Immediate next task — verify final AI chat test

We stopped after the Python syntax check.

First inspect the current test:

```bash
cat test_ai_chat.py
```

Then execute:

```bash
python test_ai_chat.py
```

Confirm:

- Complete response is displayed.
- `finish_reason` is `stop`.
- No API errors occur.
- No credentials are printed.

If successful, save the result.

## Milestone 2 — Reliable AI chat client

Tasks:

1. Test Gemini multiple times.
2. Test Mistral.
3. Test another available provider.
4. Verify error handling.
5. Test timeouts.
6. Test model switching.
7. Verify response extraction.
8. Ensure the client closes sessions properly.

Potential models to test:

```text
gemini/gemini-3-flash-preview
gemini/gemini-3.1-flash-lite
mistral/mistral-medium-3-5
mistral/codestral-latest
```

Availability must be verified at runtime; a listed model is not automatically guaranteed to respond successfully.

## Milestone 3 — AI Brain architecture

Develop:

- Central AI service.
- Provider/model configuration.
- Conversation manager.
- System prompt management.
- Error and retry handling.
- Context management.

The AI Brain should become the central entry point for all Jarvis AI interactions.

## Milestone 4 — Conversation memory

Plan persistent conversation memory.

Potential capabilities:

- Remember conversation history.
- Retrieve previous context.
- Store useful user preferences.
- Maintain conversation sessions.
- Control how much context is sent to the AI model.

Do not confuse conversation history with long-term memory. They should be designed separately.

## Milestone 5 — Voice integration

Integrate the AI Brain with the existing voice assistant.

Target architecture:

```text
Microphone
    |
    v
Speech Recognition
    |
    v
Jarvis AI Brain
    |
    v
OmniRoute
    |
    v
AI Response
    |
    v
Text-to-Speech
    |
    v
Speaker
```

Preserve the existing voice functionality.

Do not replace the voice assistant until the new integration is tested.

## Milestone 6 — Computer automation

Planned future features:

- Open applications.
- Search files.
- Execute approved commands.
- Control system functions.
- Browser automation.
- File management.
- Workflow automation.

Use appropriate permission checks for sensitive actions.

## Milestone 7 — Vision and gesture upgrades

Improve existing:

- Hand tracking.
- Gesture recognition.
- Cursor controller.
- Camera interaction.
- Visual HUD.

These features should remain independent modules connected to the central Jarvis application.

## Milestone 8 — Unified Jarvis experience

Final goal:

One assistant combining:

- AI intelligence.
- Voice.
- Memory.
- Vision.
- Gesture control.
- System automation.
- A modern desktop interface.

---

# 12. IMPORTANT DEVELOPMENT RULES

1. Never delete or rebuild the existing Jarvis application.
2. Preserve working features.
3. Avoid unnecessary changes to `main.py`.
4. Avoid changing `voice_assistant.py` until AI Core is reliable.
5. Never expose API keys.
6. Keep `.env` out of Git.
7. Use isolated test files.
8. Test every major change.
9. Avoid changing multiple unrelated modules in one task.
10. Keep the project cost-effective by using available provider options.
11. Verify actual model availability instead of assuming every listed model works.
12. Keep architecture modular so we can switch models and providers.

---

# 13. NEXT SESSION — EXACT STARTING INSTRUCTIONS

When continuing, start from:

```bash
cd ~/Downloads/jarvis_ai_system
source venv311/bin/activate
```

Confirm OmniRoute is running.

Then run:

```bash
python test_ai_chat.py
```

If the response is complete, proceed with Milestone 2.

If it fails, inspect the error before changing code.

### First discussion for the next session

Ask:

**"Mentor, let's continue Jarvis 2.0 from the November 23 master notes. First verify the final Gemini chat response, then start Milestone 2 — reliable multi-provider AI chat."**

The mentor should understand the project, architecture, current code state, completed work, and next development tasks from these notes.

---

# FINAL PROJECT STATUS

Jarvis 2.0 is an existing macOS desktop assistant being upgraded with a modular AI Brain.

The biggest achievement of this session was establishing a working connection between the Python AI client and OmniRoute, discovering available models, correcting the model-selection test, and receiving the first real Gemini response.

We have not yet integrated the new AI Brain into the main Jarvis application.

**Next objective: Make the AI Brain reliable, test multiple models, and then connect it to Jarvis's existing voice and desktop functionality.**

One milestone at a time. Preserve everything that already works.

**JARVIS 2.0 — BUILDING STEP BY STEP.**
