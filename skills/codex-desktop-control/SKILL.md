---
name: codex-desktop-control
description: Control and automate OpenAI Codex Desktop on the local PC. Use this skill whenever the user wants to dispatch prompts, create or manage sessions, queue messages, generate images via Codex Desktop (ChatGPT subscription / GPT-Image-2), or retrieve generated assets from Codex.
---

# Codex Desktop Control Skill for Antigravity

This skill enables Antigravity to programmatically control the local OpenAI Codex Desktop app (`ChatGPT.exe` / `codex app`) using native IPC queues and SQLite state synchronization.

## Key Capabilities

1. **Queueing Messages into Desktop Sessions (`codex queue`)**:
   - Injects user instructions directly into active Codex Desktop threads.
   - Runs with the user's **ChatGPT Subscription (Plus/Pro)** and built-in tools (such as `GPT-Image-2`) without requiring separate API keys.

2. **Session Lifecycle Management**:
   - Create project-bound or projectless (`new-chat`) conversations.
   - Automatically sets thread visibility (`source = 'vscode'`) so new sessions immediately show up in the Codex Desktop sidebar.

3. **Generated Asset Retrieval**:
   - Monitors `$CODEX_HOME/generated_images/` and automatically pulls newly created image assets into the current project workspace.

---

## Python Bridge CLI (`scripts/codex_bridge.py`)

Run via `uv` or Python:

```bash
& "$HOME\.local\bin\uv.exe" run python "C:\Users\pos06\.gemini\config\skills\codex-desktop-control\scripts\codex_bridge.py" <command> [options]
```

### Subcommands

* **List Recent Threads**:
  ```bash
  uv run python codex_bridge.py list -n 5
  ```

* **Queue Message into Session**:
  ```bash
  uv run python codex_bridge.py queue --thread "<THREAD_UUID>" --message "<PROMPT>"
  ```

* **Create New Visible Session**:
  ```bash
  uv run python codex_bridge.py new --prompt "안녕하세요!"
  ```

* **Fetch Latest Generated Image**:
  ```bash
  uv run python codex_bridge.py fetch-image --dest "path/to/destination.png"
  ```