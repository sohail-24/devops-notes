# JARVIS 2.0 — DEVELOPMENT HANDOVER NOTES
## Session: November 25, 2026

---

# 1. Project Overview

**Project:** JARVIS 2.0 — macOS Personal AI Assistant

**Local project directory:**
```bash
~/Downloads/jarvis_ai_system
```

**Environment:**
- MacBook Pro M3 Pro (Apple Silicon)
- macOS
- Python 3.11.15
- Node v24.13.0
- npm v11.6.2
- Virtual environment: `venv311`
- Claude Code installed and working
- Claude Code launched using `claude-free`

**Project startup:**
```bash
cd ~/Downloads/jarvis_ai_system
source venv311/bin/activate
python main.py
```

**Python syntax validation:**
```bash
python -m py_compile main.py voice_assistant.py utils.py ai_chat_module.py
```

## Project architecture

JARVIS currently contains:

- Voice recognition and text-to-speech.
- AI conversation using OmniRoute.
- Gemini model integration.
- Local knowledge base and command handlers.
- Chat Mode with session-only conversation history.
- Hand tracking.
- Gesture recognition.
- Cursor control.
- System control.
- OpenCV HUD.
- Holographic UI.
- JARVIS visual effects.

Important existing files:

| File | Responsibility |
|---|---|
| `main.py` | Main application, voice loop, command processing |
| `voice_assistant.py` | Speech recognition and speech output |
| `ai_chat_module.py` | AI conversation and local fallback |
| `ai_core/ai_client.py` | OmniRoute API client |
| `utils.py` | Configuration and utility functions |

The project has approximately 18,000 lines of Python code. Preserve existing functionality and avoid broad rewrites.

---

# 2. What We Previously Completed

## A. Hybrid AI Response Engine — Completed

Implemented Gemini AI through OmniRoute.

Architecture:
1. Existing local handlers execute first where applicable.
2. Unknown conversational questions are sent to the AI client.
3. Gemini response returns through the existing JARVIS response pipeline.
4. Local fallback handles AI service failures.

Default model:
```text
gemini/gemini-3-flash-preview
```

OmniRoute API:
```text
http://127.0.0.1:20128/v1
```

Dashboard:
```text
http://localhost:20128
```

The AI client is implemented in:
```text
ai_core/ai_client.py
```

## B. macOS FLAC issue — Solved

Original error:
```text
[Errno 86] Bad CPU type in executable
```

Installed native Apple Silicon FLAC:
```bash
brew install flac
```

Verified:
```bash
which flac
# /opt/homebrew/bin/flac
```

SpeechRecognition now uses the Homebrew FLAC executable.

## C. Microphone ownership — Improved

Previously, two threads attempted to access the same microphone.

This caused:
```text
Internal PortAudio error
This audio source is already inside a context manager
```

Fix:
- `_voice_loop()` is the microphone capture owner.
- The old duplicate STT thread is not started.
- Removed unsafe manual microphone context-manager exit.

**Important:** Do not reintroduce the duplicate microphone capture thread.

## D. Rishi voice — Configured

Selected macOS voice:
```text
Rishi (English (India))
```

Voice ID:
```text
com.apple.voice.compact.en-IN.Rishi
```

Configured rate:
```text
175 WPM
```

Volume:
```text
1.0
```

## E. TTS audible-output investigation — Improved

Earlier pyttsx3 implementation had unreliable subsequent speech calls.

Claude investigated and moved actual speech generation to native macOS `say` using subprocess.

Example:
```python
subprocess.run(
    ['say', '-v', 'Rishi', text],
    capture_output=True,
    text=True,
    timeout=30
)
```

The native macOS speech test reportedly produced audible output for three phrases.

However:
- The configured 175 WPM is not yet passed to macOS `say`.
- Claude reported a default speech rate around 200 WPM.
- The TTS implementation should remain unchanged until we deliberately investigate the rate.

Do not reintroduce duplicate pyttsx3 and macOS `say` speech execution.

## F. Chat Mode — Implemented

Activation phrases include:
- Jarvis, chat mode on.
- Start chat mode.
- Let's chat.
- Begin conversation.

Deactivation phrases include:
- Jarvis, chat mode off.
- Exit chat mode.
- Stop conversation.

Expected behavior:
- Wake word is not required while Chat Mode is active.
- Conversation history exists only in memory.
- History is cleared when Chat Mode is deactivated.
- No database or persistent memory is used.

Recent hardware testing confirmed Chat Mode activation and follow-up command recognition.

---

# 3. Issues Investigated in Today's Session

## Issue 1: JARVIS repeats the same answer

Example hardware test:

Question:
```text
What is cloud computing?
```

Response:
```text
Cloud computing delivers computing services over the internet.
```

Follow-up:
```text
Give me one example of cloud computing.
```

JARVIS returned substantially the same answer.

### Investigation findings

Claude identified two possible causes:

1. Gemini API rate limiting.
2. Local fallback returning generic or previously stored knowledge instead of clearly reporting an AI service failure.

The local knowledge base should remain available, but a failed AI request must not be presented as a successful Gemini answer.

## Issue 2: OmniRoute HTTP 429

Previous terminal error:
```text
API error (429):
All credentials for model gemini-3-flash-preview are cooling down
```

Reported retry time:
```text
2026-11-25T08:00:00.096Z
```

This is a provider-side cooldown.

Required behavior:
- Detect 429 explicitly.
- Return a clear rate-limit message.
- Do not silently return unrelated cached answers.
- Keep the AI client available for future retries.
- Do not expose internal API details or credentials.

Important: The cooldown does not prove that the AI integration is broken.

## Issue 3: Chat Mode history not reaching Gemini

Investigation found:
- `main.py` maintained `chat_mode_history`.
- `ai_chat_module.py` also maintained `conversation_history`.
- The previous implementation did not consistently pass the complete history into the AI API request.

This must be verified and corrected.

Expected message order:

```text
System prompt
Previous user question
Previous assistant response
Current user question
```

The next assistant response should then be appended exactly once.

## Issue 4: No internet search integration

Investigation confirmed:

- OmniRoute provides access to the AI model.
- There is no current live web-search integration in the project.
- Gemini conversation and live internet search are separate capabilities.

We have NOT implemented internet search.

---

# 4. Duplicate AI Request Investigation

We noticed this code in an earlier pasted Claude output:

```python
response = self.ai_chat.ask(ai_query)

history = self.chat_mode_history if self.chat_mode_active else []

response = self.ai_chat.process_query(ai_query, history=history)
```

The first response would be overwritten.

Claude then inspected the current project and reported that the current `main.py` uses `process_query()` directly.

### Claude's findings

- `process_query()` does not internally call `ask()`.
- It calls `self.ai_client.chat()`.
- It supports history.
- It falls back to local processing when appropriate.
- It should make one AI request per question.

Claude reported that tests passed with one AI response.

This duplicate-request concern is therefore provisionally resolved, subject to final code and test verification.

---

# 5. Latest Claude Code Work — Current Status

The latest Claude Code activity:

1. Referenced:
   - `test_response_pipeline.py`
   - `main.py`
   - `ai_chat_module.py`
2. Read the TTS memory notes.
3. Read `voice_assistant.py` (445 lines).
4. Inspected the current test file.
5. Identified that new tests had been added but the `run_tests()` function did not include the new test class.
6. Updated `test_response_pipeline.py` by adding one line to include the new test class.

**Important: The latest output does not yet provide the final test results.**

Do not assume this last change is fully verified.

Next time, ask Claude to:
- Show the exact changed test registration.
- Run the complete relevant test suite.
- Report the actual pass/fail counts.
- Check for duplicate or incorrectly registered tests.

---

# 6. Current Development Priorities

## Priority 1 — Finish AI fallback handling

File:
```text
ai_chat_module.py
```

And:
```text
ai_core/ai_client.py
```

Required:
- Correct 429 handling.
- Clear API failure messages.
- Preserve useful local knowledge answers.
- Never return unrelated cached answers as if they were AI responses.
- Do not permanently disable the AI client for temporary rate limits.

## Priority 2 — Finish Chat Mode history

Files:
```text
main.py
ai_chat_module.py
```

Required:
- Use one authoritative history list where practical.
- Preserve correct user/assistant message ordering.
- Append each exchange exactly once.
- Do not append failed API responses as genuine assistant answers.
- Clear history on activation, deactivation, and shutdown.
- Never reuse Chat Mode history in normal mode.

## Priority 3 — Test AI response quality

After the implementation is verified, test:

1. What is cloud computing?
2. Give me one example.
3. Give me another example.
4. How is it different from Azure?

Expected:
- Each answer addresses the actual question.
- Follow-up questions use previous context.
- No repeated generic answer.
- Exactly one AI request per question.

Use mocked tests for reliable validation while the provider is rate-limited.

## Priority 4 — TTS rate adjustment

Only after AI functionality is stable:

- Pass the configured 175 WPM to macOS `say -r`.
- Verify actual voice output.
- Preserve Rishi voice.
- Do not reintroduce pyttsx3 duplication.

---

# 7. Future Features — Not Yet Implemented

These are future tasks, not current work:

- Live internet search integration.
- Phase 3A voice interruption: "Jarvis, stop", "Stop speaking", "Silence".
- Phase 3B voice performance and latency improvements.
- Further improvements to local offline knowledge.

Do not start these until the existing AI conversation pipeline is stable and tested.

---

# 8. Important Development Rules

1. Use Claude Code to inspect and modify the existing project.
2. Investigate before making changes.
3. Prefer minimal, targeted changes.
4. Preserve existing functionality.
5. Never rewrite entire modules without approval.
6. Do not modify `.env` or expose API keys.
7. Do not change microphone ownership.
8. Do not add persistent Chat Mode memory.
9. Do not add internet search until explicitly approved.
10. Run syntax checks and relevant tests after modifications.
11. Distinguish mocked tests from actual hardware tests.
12. Do not accept a claim of success without actual evidence.

---

# 9. Next Session — Exact Starting Point

Start here:

### Step 1
Open Terminal:

```bash
cd ~/Downloads/jarvis_ai_system
source venv311/bin/activate
```

### Step 2
Run syntax validation:

```bash
python -m py_compile main.py voice_assistant.py utils.py ai_chat_module.py
```

### Step 3
Open Claude Code:

```bash
claude-free
```

### Step 4
Give Claude this instruction:

"Continue from the JARVIS 2.0 November 25 handover notes. First inspect the latest changes in test_response_pipeline.py, main.py and ai_chat_module.py. We stopped after adding the new test class to run_tests(). Verify that registration, run the relevant test suites, and report exact results. Then inspect the AI fallback and Chat Mode history implementation. Do not make unrelated changes. Do not start Phase 3B or implement internet search."

### Step 5
Share Claude's output with Mentor before proceeding with more changes.

---

# 10. Final Project Status

| Component | Status |
|---|---|
| Project startup | Working |
| Python environment | Working |
| FLAC / microphone dependency | Solved |
| Microphone ownership | Improved |
| Rishi voice | Configured |
| Native macOS TTS | Implemented; hardware tests reported successful |
| Voice echo coordination | Improved; continue hardware verification |
| Hybrid AI engine | Implemented |
| OmniRoute connection | Configured |
| Gemini 429 handling | Needs final verification |
| Chat Mode activation | Working |
| Chat Mode history | Needs final verification |
| Duplicate AI request | Current implementation reported correct |
| Local knowledge fallback | Needs final verification |
| Internet search | Not implemented |
| Voice interruption | Not implemented |
| Phase 3B performance | Not started |

**Today's stopping point:** Claude updated test registration in `test_response_pipeline.py`. Final test results and verification are pending.

**Next objective:** Finish AI fallback and Chat Mode history validation before adding any new capabilities.

End of handover notes.
