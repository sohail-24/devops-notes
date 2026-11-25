# JARVIS 2.0 — DEVELOPMENT HANDOVER NOTES
## Date: 25 November 2026
## Milestone: PySide6 Dashboard Foundation & Hardware Integration
## Status: Dashboard launches; camera display and full subsystem integration remain incomplete.

---

# 1. PROJECT INFORMATION

Project: JARVIS 2.0 — Local AI Personal Assistant

Project location:
`/Users/sohal/Projects/jarvis_ai_system`

Device:
- MacBook Pro M3 Pro
- Apple Silicon
- macOS

Python environment:
- Python 3.11.15
- Virtual environment: `venv311_new`
- PySide6: 6.12.0
- OpenCV: 4.11.0
- MediaPipe: 0.10.21
- NumPy: 1.26.4

Activate the correct environment:

```bash
cd ~/Projects/jarvis_ai_system
source venv311_new/bin/activate
```

Verify:

```bash
python --version
which python
```

Expected Python:
`/Users/sohal/Projects/jarvis_ai_system/venv311_new/bin/python`

IMPORTANT:
Do not use the old `venv311`, `venv`, or `venv_new` environments.

---

# 2. WHAT WE WORKED ON TODAY

Our main objective was to upgrade the existing JARVIS 2.0 OpenCV visual interface into a professional PySide6 desktop dashboard.

We decided to preserve the existing:
- AI brain
- Ollama integration
- Voice assistant
- Native macOS TTS
- MediaPipe hand tracking
- Gesture recognition
- Cursor controller
- System controller

We chose PySide6 because we need a real desktop application with interactive controls, panels, conversation history and subsystem switches.

## Dashboard foundation

The following files exist:

```text
gui/
├── __init__.py
├── dashboard.py
├── styles.py
└── webcam_widget.py
```

### gui/styles.py
Contains:
- JARVIS dark theme.
- Cyan/blue color palette.
- QSS styles.
- Widget palette configuration.

### gui/webcam_widget.py
Contains:
- FrameBuffer.
- WebcamWidget.
- CameraManager.
- CameraThread.

### gui/dashboard.py
Contains:
- Dashboard QMainWindow.
- HUDOverlay.
- GestureIndicator.
- FrameIndicator.
- DashboardApp.
- Standalone `main()` function.

### gui/__init__.py
Package exports for dashboard components and styling.

---

# 3. PROBLEMS WE SOLVED

## Problem 1 — Python environment

Verified that the active environment works.

Results:

```text
Python 3.11.15
PySide6 6.12.0
Dashboard import successful
```

Commands:

```bash
python -c "import PySide6; print(PySide6.__version__)"
python -c "from gui.dashboard import Dashboard; print('Dashboard import successful')"
```

Both passed.

## Problem 2 — Dashboard startup error

First dashboard launch:

```bash
python -m gui.dashboard
```

Error:

```text
KeyError: 'cyan'
```

Cause:

`dashboard.py` referenced:

```python
JARVIS_COLORS['cyan']
```

But `styles.py` defined the cyan color under:

```python
JARVIS_COLORS['primary']
```

We identified all incorrect references.

Claude Code fixed the color-key mismatch and addressed the package import warning.

After this fix, the dashboard successfully opened.

## Problem 3 — Dashboard startup

Successfully launched the PySide6 window using:

```bash
python -m gui.dashboard
```

The dashboard now opens without the previous `KeyError`.

---

# 4. CURRENT DASHBOARD APPEARANCE

The current dashboard has:

- Large central webcam area.
- Gesture HUD panel.
- FPS and frame indicator.
- System Status panel.
- Notifications panel.
- Gesture Controls panel.
- Bottom dashboard controls.
- Subsystem Controls panel.

Latest screenshot:
`Screenshot 2026-11-25 at 11.52.12 PM.png`

The screenshot confirms the application window opens and the new subsystem controls are visible.

## Current subsystem switches shown

| Subsystem | Displayed state |
|---|---|
| Camera | ON |
| Voice | OFF |
| Hand Tracking | OFF |
| Gesture Recognition | OFF |
| Cursor Control | OFF |

These are the states displayed in the screenshot. Their complete physical integration has not yet been verified.

---

# 5. CURRENT CAMERA PROBLEM — HIGHEST PRIORITY

This is the main unresolved issue.

### What happened?

1. First dashboard startup: camera did not start.
2. I manually switched Camera OFF.
3. I switched Camera ON again.
4. Camera status changed to ON.
5. However, the webcam panel remained completely black.

Therefore:

**Camera status ON does not currently prove that the camera is delivering visible frames to the dashboard.**

We must investigate the complete camera pipeline.

Potential areas to investigate (not confirmed causes):

- Camera initialization and ownership.
- CameraThread startup.
- FrameBuffer updates.
- Qt signal delivery.
- Frame conversion from OpenCV BGR to Qt image format.
- WebcamWidget painting and image display.
- Whether the camera thread actually produces frames.
- Whether the dashboard subscribes to the correct frame source.

### Important architecture rule

The original JARVIS system already has a camera capture and processing pipeline.

Do not create a second `cv2.VideoCapture`.

Reuse the existing camera owner and processed frames.

Do not create duplicate MediaPipe tracking objects.

The dashboard should display the existing live camera output.

---

# 6. VOICE PROBLEM

Previously, when starting JARVIS using:

```bash
python main.py
```

The application initialized its voice system and spoke the startup greeting using the existing Rishi voice.

But launching:

```bash
python -m gui.dashboard
```

does not reproduce that startup greeting.

The dashboard currently shows Voice OFF.

### Desired behavior

When launching the integrated dashboard:

1. Initialize the existing Voice Assistant.
2. Use existing native macOS `say` TTS.
3. Use the configured Rishi voice:
   `com.apple.voice.compact.en-IN.Rishi`
4. Play the existing startup greeting exactly once.
5. Display real voice states:
   - OFF
   - INITIALIZING
   - LISTENING
   - THINKING
   - SPEAKING
6. Add a working Voice ON/OFF switch.
7. Turning Voice OFF must safely disable listening.
8. Turning Voice ON must resume the existing microphone/listening pipeline.

Do not introduce pyttsx3.

Do not create a second microphone capture owner.

Preserve existing voice interruption and TTS coordination.

---

# 7. HAND TRACKING AND GESTURE CONTROL

The dashboard displays gesture-related panels, but complete integration has not been physically verified.

Desired controls:

| Control | Expected behavior |
|---|---|
| Hand Tracking ON/OFF | Enable/disable existing MediaPipe tracking |
| Gesture Recognition ON/OFF | Enable/disable existing gesture detection |
| Cursor Control ON/OFF | Enable/disable existing cursor controller |

Important:
- Do not duplicate the camera.
- Do not initialize duplicate tracking objects.
- Cursor Control must remain OFF by default.
- Cursor movement must never activate unexpectedly.
- Show genuine tracking and gesture status.

---

# 8. EXISTING JARVIS ARCHITECTURE

Important project files:

```text
main.py
voice_assistant.py
speech_recognition_engine.py
ai_chat_module.py
ai_core/
    ai_client.py
hand_tracking.py
gesture_recognition.py
cursor_controller.py
system_controller.py
media_controller.py
jarvis_visuals.py
ui_holographic_overlay.py
gui/
    __init__.py
    dashboard.py
    styles.py
    webcam_widget.py
```

### AI brain

- Ollama is the preferred local AI provider.
- OmniRoute remains an optional fallback.
- Existing AI chat logic is in `ai_chat_module.py`.
- AI clients are in `ai_core/ai_client.py`.

### Voice

- Native macOS `say` is used for TTS.
- Preferred voice is Rishi.
- Existing microphone and barge-in architecture must be preserved.

### Vision

- OpenCV.
- MediaPipe.
- Hand tracking.
- Gesture recognition.
- Cursor controller.

Do not rewrite working components unnecessarily.

---

# 9. TESTING DONE

Claude previously reported:

- 19/19 voice barge-in tests passed.
- 61/61 tests passed across:
  - `test_voice_barge_in.py`
  - `test_response_pipeline.py`

We independently verified:

```bash
python --version
python -c "import PySide6; print(PySide6.__version__)"
python -c "from gui.dashboard import Dashboard; print('Dashboard import successful')"
```

All passed.

We also launched:

```bash
python -m gui.dashboard
```

The GUI opened successfully after the color-key fix.

IMPORTANT:
The tests do not prove that camera, microphone or physical voice integration works.

---

# 10. NEXT SESSION — EXACT DEVELOPMENT PLAN

## Phase 1 — Fix camera integration

FIRST PRIORITY.

Investigate:

1. Existing camera owner.
2. CameraManager.
3. CameraThread.
4. FrameBuffer.
5. WebcamWidget.
6. OpenCV-to-QImage conversion.
7. Qt frame update signals.
8. Dashboard camera toggle.

Test the frame pipeline independently before connecting other subsystems.

Expected result:
- Dashboard starts.
- Webcam initializes on the first launch.
- Live video is visible.
- Camera OFF works.
- Camera ON restores live video.
- FPS and frame count update.
- Clean camera shutdown.

Do not proceed to voice integration until the camera display is verified.

## Phase 2 — Voice integration

After camera works:

1. Connect existing VoiceAssistant.
2. Initialize the microphone safely.
3. Play startup greeting once.
4. Add working Voice ON/OFF switch.
5. Display actual listening/thinking/speaking states.
6. Verify voice recognition.
7. Verify native Rishi TTS.
8. Preserve barge-in behavior.

## Phase 3 — Hand tracking

1. Connect existing hand tracker.
2. Add Hand Tracking ON/OFF.
3. Show actual landmarks.
4. Connect gesture recognition.
5. Add Gesture Recognition ON/OFF.
6. Verify supported gestures.

## Phase 4 — Cursor controller

1. Connect existing cursor controller.
2. Add Cursor Control ON/OFF.
3. Keep it OFF by default.
4. Test only after explicit activation.

## Phase 5 — Full JARVIS dashboard

Verify:
- Camera.
- Voice.
- AI brain.
- Conversation panel.
- Hand tracking.
- Gesture recognition.
- Cursor control.
- System status.
- Notifications.
- Clean startup and shutdown.

---

# 11. NEXT SESSION — FIRST COMMANDS

Start with:

```bash
cd ~/Projects/jarvis_ai_system
source venv311_new/bin/activate
```

Then:

```bash
python --version
python -c "import PySide6; print(PySide6.__version__)"
```

Launch the current dashboard:

```bash
python -m gui.dashboard
```

Do not start `main.py` at the same time.

---

# 12. IMPORTANT DEVELOPMENT RULES

1. Work in small steps.
2. Inspect existing code before changing it.
3. Fix the camera first.
4. Do not rewrite the entire JARVIS project.
5. Preserve existing AI brain functionality.
6. Preserve native Rishi TTS.
7. Never create duplicate camera or microphone owners.
8. Never install another OpenCV distribution.
9. Do not weaken tests.
10. Do not claim physical hardware functionality without testing it.
11. Keep cursor control OFF by default.
12. Verify each subsystem before moving to the next.

---

# FINAL STATUS

| Component | Status |
|---|---|
| Python environment | Working |
| PySide6 installation | Working |
| Dashboard import | Working |
| Dashboard window | Opens |
| Dashboard color error | Fixed |
| Dashboard layout | Visible |
| Camera initialization | Needs investigation |
| Camera live display | Not working yet |
| Camera toggle | Present; incomplete verification |
| Voice startup greeting | Not integrated into standalone dashboard |
| Voice ON/OFF | Needs integration and testing |
| Hand tracking toggle | Present; integration unverified |
| Gesture recognition | Integration unverified |
| Cursor control | OFF by default |
| AI conversation integration | Not yet verified |
| Full dashboard integration | In progress |

**NEXT STARTING POINT: Fix the black webcam panel and verify the live frame pipeline. Do not begin unrelated upgrades until this works.**
