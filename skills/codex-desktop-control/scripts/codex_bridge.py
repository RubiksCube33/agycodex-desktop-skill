"""Codex Desktop Bridge Script for Antigravity.

Provides automated control over OpenAI Codex Desktop sessions, queue injection,
session lifecycle, multi-modal image input, and generated asset retrieval.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
STATE_DB = CODEX_HOME / "state_5.sqlite"
QUEUE_DB = CODEX_HOME / "queue_1.sqlite"
GENERATED_IMAGES_DIR = CODEX_HOME / "generated_images"


def get_db_connection(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        sys.exit(1)
    return sqlite3.connect(str(db_path))


def list_threads(limit: int = 10) -> List[Dict[str, Any]]:
    con = get_db_connection(STATE_DB)
    cur = con.cursor()
    query = """
        SELECT id, title, cwd, source, model, updated_at
        FROM threads
        ORDER BY updated_at DESC
        LIMIT ?
    """
    rows = cur.execute(query, (limit,)).fetchall()
    con.close()
    return [
        {
            "id": r[0],
            "title": r[1],
            "cwd": r[2],
            "source": r[3],
            "model": r[4],
            "updated_at": r[5],
        }
        for r in rows
    ]


def queue_message(thread_id: str, message: str, images: Optional[List[str]] = None) -> bool:
    cmd = ["codex", "queue", "--thread", thread_id, "--message", message]
    if images:
        for img in images:
            cmd.extend(["-i", str(Path(img).resolve())])

    res = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    if res.returncode == 0:
        print(res.stdout.strip())
        return True
    else:
        print(f"Failed to queue message: {res.stderr.strip()}", file=sys.stderr)
        return False


def create_new_session(
    prompt: str,
    cwd: Optional[str] = None,
    images: Optional[List[str]] = None,
    make_visible: bool = True,
) -> Optional[str]:
    target_dir = Path(cwd) if cwd else (Path.home() / "Documents" / "Codex" / time.strftime("%Y-%m-%d") / "new-chat")
    target_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "codex",
        "exec",
        "-C",
        str(target_dir),
        "--dangerously-bypass-approvals-and-sandbox",
    ]
    if images:
        for img in images:
            cmd.extend(["-i", str(Path(img).resolve())])

    # Pass prompt via stdin with automatic EOF
    res = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if res.returncode != 0:
        print(f"Error running codex exec: {res.stderr.strip()}", file=sys.stderr)
        return None

    con = get_db_connection(STATE_DB)
    row = con.execute("SELECT id FROM threads ORDER BY created_at DESC LIMIT 1").fetchone()
    if not row:
        con.close()
        return None
    thread_id = row[0]

    if make_visible:
        con.execute("UPDATE threads SET source='vscode' WHERE id=?", (thread_id,))
        con.commit()
    con.close()

    print(f"Session created: {thread_id} at {target_dir}")
    return thread_id


def get_latest_generated_image(dest: Optional[str] = None) -> Optional[str]:
    if not GENERATED_IMAGES_DIR.exists():
        print(f"Directory {GENERATED_IMAGES_DIR} does not exist.", file=sys.stderr)
        return None

    images = list(GENERATED_IMAGES_DIR.rglob("*.png")) + list(GENERATED_IMAGES_DIR.rglob("*.jpg"))
    if not images:
        print("No generated images found.", file=sys.stderr)
        return None

    latest_img = max(images, key=lambda p: p.stat().st_mtime)
    print(f"Latest image: {latest_img}")

    if dest:
        dest_path = Path(dest)
        if dest_path.is_dir():
            dest_path = dest_path / latest_img.name
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(latest_img, dest_path)
        print(f"Copied to {dest_path}")
        return str(dest_path)

    return str(latest_img)


def main():
    parser = argparse.ArgumentParser(description="Codex Desktop Automation Bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    list_p = subparsers.add_parser("list", help="List recent threads")
    list_p.add_argument("-n", "--limit", type=int, default=5, help="Number of threads")

    # queue
    queue_p = subparsers.add_parser("queue", help="Queue message to a session")
    queue_p.add_argument("--thread", required=True, help="Thread UUID")
    queue_p.add_argument("--message", required=True, help="Message text")
    queue_p.add_argument("-i", "--image", nargs="*", default=[], help="Image path(s) to attach")

    # new
    new_p = subparsers.add_parser("new", help="Create a new session")
    new_p.add_argument("--prompt", required=True, help="Initial prompt")
    new_p.add_argument("--cwd", help="Working directory (default: auto projectless scratch)")
    new_p.add_argument("-i", "--image", nargs="*", default=[], help="Image path(s) to attach")
    new_p.add_argument("--hidden", action="store_true", help="Keep hidden from desktop sidebar")

    # fetch-image
    fetch_p = subparsers.add_parser("fetch-image", help="Get latest generated image")
    fetch_p.add_argument("--dest", help="Destination file/folder to copy the image to")

    args = parser.parse_args()

    if args.command == "list":
        threads = list_threads(limit=args.limit)
        print(json.dumps(threads, indent=2, ensure_ascii=False))
    elif args.command == "queue":
        queue_message(args.thread, args.message, images=args.image)
    elif args.command == "new":
        create_new_session(args.prompt, cwd=args.cwd, images=args.image, make_visible=not args.hidden)
    elif args.command == "fetch-image":
        get_latest_generated_image(args.dest)


if __name__ == "__main__":
    main()