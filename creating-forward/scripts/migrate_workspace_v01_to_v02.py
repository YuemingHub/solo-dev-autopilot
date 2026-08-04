#!/usr/bin/env python3
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def atomic_write(path, content):
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


if len(sys.argv) != 2:
    raise SystemExit("Usage: python migrate_workspace_v01_to_v02.py <project-path>")

project = Path(sys.argv[1]).resolve()
workspace = project / ".creating-forward"
state_path = workspace / "state.yaml"
events_path = workspace / "events.jsonl"

if not state_path.is_file() or not events_path.is_file():
    raise SystemExit("No complete v0.1 workspace found. Run validation before migration.")

state = state_path.read_text(encoding="utf-8")
version_match = re.search(r'(?m)^protocolVersion:\s*"([^"\n]+)"\s*$', state)
version = version_match.group(1) if version_match else None
if version == "0.2.0":
    for directory in ("observations", "protocol-candidates", "reviews", "metrics"):
        (workspace / directory).mkdir(parents=True, exist_ok=True)
    print("Workspace already uses protocol 0.2.0.")
    raise SystemExit(0)
if version != "0.1.0":
    raise SystemExit(f"Unsupported protocolVersion: {version or 'missing'}")

migrated = re.sub(
    r'(?m)^(protocolVersion|schemaVersion|workspaceVersion|conformanceSuiteVersion):\s*"0\.1\.0"$',
    lambda match: f'{match.group(1)}: "0.2.0"',
    state,
)

events_text = events_path.read_text(encoding="utf-8")
parsed_events = []
for line_number, line in enumerate(events_text.splitlines(), 1):
    if not line.strip():
        continue
    try:
        parsed_events.append(json.loads(line))
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"Invalid events.jsonl line {line_number}: {error}"
        ) from error

already_recorded = any(
    event.get("type") == "workspace_migrated"
    and event.get("toVersion") == "0.2.0"
    for event in parsed_events
)
if not already_recorded:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "workspace_migrated",
        "fromVersion": "0.1.0",
        "toVersion": "0.2.0",
        "summary": "Added governed evolution directories without overwriting project history.",
    }
    events_text += json.dumps(event, ensure_ascii=False) + "\n"

atomic_write(events_path, events_text)
atomic_write(state_path, migrated)
for directory in ("observations", "protocol-candidates", "reviews", "metrics"):
    (workspace / directory).mkdir(parents=True, exist_ok=True)
print("Migration completed without overwriting existing project state.")
