---
name: codex-desktop-control
description: Control and automate OpenAI Codex Desktop on the local PC. Use this skill whenever the user wants to dispatch prompts, create or manage sessions, queue messages, generate images via Codex Desktop (ChatGPT subscription / GPT-Image-2), or retrieve generated assets from Codex.
---

# Codex Desktop Control Skill for Antigravity

This skill enables Antigravity to programmatically control the local OpenAI Codex Desktop app (`ChatGPT.exe` / `codex app`) using native IPC queues and SQLite state synchronization.

---

## ⚠️ Critical Execution Guardrail: Stdin Hanging Prevention

> [!CAUTION]
> **NEVER execute raw, unpiped `codex exec` commands directly in PowerShell.**
> In Windows PowerShell, running `codex exec <prompt>` without closing standard input causes `codex.exe` to hang indefinitely waiting for EOF on stdin (`Reading additional input from stdin...`), stalling the background process.

### Safe Execution Rules:
1. **Always Prefer `codex_bridge.py`**:
   The bridge script properly handles process subprocess pipes, timeout, and stdin isolation automatically.
   ```bash
   python "C:\Users\pos06\.gemini\config\skills\codex-desktop-control\scripts\codex_bridge.py" <subcommand> [options]
   ```
2. **For Active Desktop Sessions**:
   Use `codex queue` or `codex_bridge.py queue`. `codex queue` writes directly to SQLite and never blocks on stdin:
   ```bash
   codex queue --thread "<THREAD_UUID>" --message "<PROMPT>"
   ```
3. **If `codex exec` MUST be called directly**:
   You **MUST** pipe the prompt through `cmd.exe /c "echo ... | codex exec ..."` or `$null | codex exec ...` so stdin is explicitly closed:
   ```powershell
   cmd.exe /c "echo <PROMPT> | codex exec -C ""<DIR>"" --dangerously-bypass-approvals-and-sandbox"
   ```

---

## 🛠️ Python Bridge CLI (`scripts/codex_bridge.py`)

Run via `python` or `uv run python`:

### Subcommands

* **1. List Recent Threads**:
  ```bash
  python "C:\Users\pos06\.gemini\config\skills\codex-desktop-control\scripts\codex_bridge.py" list -n 5
  ```

* **2. Queue Message into Desktop Session** *(ChatGPT Subscription / GPT-Image-2)*:
  ```bash
  python "C:\Users\pos06\.gemini\config\skills\codex-desktop-control\scripts\codex_bridge.py" queue --thread "<THREAD_UUID>" --message "<PROMPT>"
  ```

* **3. Create New Visible Session** *(Appears in Desktop Sidebar)*:
  ```bash
  python "C:\Users\pos06\.gemini\config\skills\codex-desktop-control\scripts\codex_bridge.py" new --prompt "<INITIAL_PROMPT>"
  ```

* **4. Fetch Latest Generated Image**:
  ```bash
  python "C:\Users\pos06\.gemini\config\skills\codex-desktop-control\scripts\codex_bridge.py" fetch-image --dest "./output.png"
  ```

---

## 📋 Standard Workflow for Tasks

1. **For Image Generation Requests**:
   - Check active threads or create a new session via `codex_bridge.py new`.
   - Queue the prompt instructing Codex to use its built-in `GPT-Image-2` tool.
   - Once completed, run `codex_bridge.py fetch-image --dest "<TARGET_PATH>"` to copy the image to the workspace and present it to the user.

2. **For Subagent / Async Delegation**:
   - Queue the task into an active thread using `codex queue`.
   - The Desktop app will process it in the background using the user's ChatGPT subscription.