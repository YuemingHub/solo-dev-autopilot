#!/usr/bin/env python3
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


TARGET_VERSION = "0.4.0-dev"


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


def scalar_value(state, field):
    match = re.search(rf'(?m)^{re.escape(field)}:\s*"([^"\n]+)"\s*$', state)
    return match.group(1) if match else None


def authorization_block(state):
    matches = re.findall(
        r"(?ms)^authorizationProfile:\s*\n((?:^  [^\n]+\n?)*)", state
    )
    return matches[0] if len(matches) == 1 else ""


def authorization_value(block, field):
    match = re.search(
        rf"(?m)^  {re.escape(field)}:\s*(true|false)\s*$", block
    )
    return match.group(1) if match else None


if len(sys.argv) != 2:
    raise SystemExit("Usage: python migrate_workspace_v02_to_v03.py <project-path>")

project = Path(sys.argv[1]).resolve()
workspace = project / ".creating-forward"
state_path = workspace / "state.yaml"
events_path = workspace / "events.jsonl"

if not state_path.is_file():
    raise SystemExit("No v0.2 state.yaml found. Run init_workspace.py first.")
if not events_path.is_file():
    raise SystemExit("No events.jsonl found. Validate the v0.2 workspace first.")

state = state_path.read_text(encoding="utf-8")
authorization = authorization_block(state)
source_version = scalar_value(state, "protocolVersion")
legacy_fields_present = "adapterVersion:" in state or "realFamilyDataAccess:" in state
if source_version == TARGET_VERSION and not legacy_fields_present:
    print(f"Workspace already uses protocol {TARGET_VERSION}.")
    raise SystemExit(0)
if source_version not in {"0.2.0", TARGET_VERSION}:
    raise SystemExit(f"Unsupported protocolVersion: {source_version or 'missing'}")

if source_version == "0.2.0":
    required_scalar_fields = {
        "projectId": None,
        "schemaVersion": "0.2.0",
        "workspaceVersion": "0.2.0",
        "conformanceSuiteVersion": "0.2.0",
    }
    missing_or_invalid = []
    for field, expected in required_scalar_fields.items():
        value = scalar_value(state, field)
        if not value or (expected is not None and value != expected):
            missing_or_invalid.append(field)

    allowed_state_values = {
        "phase": {
            "idle", "understanding", "exploring", "confirming", "planning",
            "executing", "reviewing", "delivering", "complete", "blocked",
            "paused_for_human", "cancelled",
        },
        "presenceMode": {"attended", "away"},
        "delegationMode": {"advisory", "supervised", "delegated"},
        "requirementsStatus": {"draft", "confirmed", "changed", "rejected"},
    }
    for field, allowed in allowed_state_values.items():
        if scalar_value(state, field) not in allowed:
            missing_or_invalid.append(field)

    for field in (
        "workspaceWrite",
        "commandExecution",
        "networkAccess",
        "externalMessaging",
        "productionDeploy",
        "paidActions",
        "destructiveActions",
        "realFamilyDataAccess",
    ):
        if authorization_value(authorization, field) not in {"true", "false"}:
            missing_or_invalid.append(f"authorizationProfile.{field}")

    if missing_or_invalid:
        raise SystemExit(
            "Incomplete v0.2 state; migration made no changes: "
            + ", ".join(missing_or_invalid)
        )

old_access = authorization_value(authorization, "realFamilyDataAccess")
new_access = authorization_value(authorization, "sensitiveDataAccess")
if old_access and new_access and old_access != new_access:
    raise SystemExit("Conflicting authorization fields; migration made no changes.")

adapter_match = re.search(r'(?m)^adapterVersion:\s*"([^"\n]+)"\s*$', state)
legacy_adapter = adapter_match.group(1).split("-", 1)[0] if adapter_match else None
adapters_match = re.search(r"(?m)^adapters:\s*(\[[^\n]*\])\s*$", state)
if adapters_match:
    try:
        adapters = json.loads(adapters_match.group(1))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid adapters list: {error}") from error
    if not isinstance(adapters, list) or not all(
        isinstance(adapter, str) for adapter in adapters
    ):
        raise SystemExit("adapters must be an inline JSON string array")
else:
    adapters = []

if legacy_adapter and legacy_adapter not in adapters:
    adapters.append(legacy_adapter)

migrated = re.sub(
    r'(?m)^protocolVersion:\s*"(?:0\.2\.0|0\.3\.0-dev)"$',
    f'protocolVersion: "{TARGET_VERSION}"',
    state,
)
migrated = re.sub(
    r'(?m)^(schemaVersion|workspaceVersion|conformanceSuiteVersion):\s*"0\.2\.0"$',
    lambda match: f'{match.group(1)}: "{TARGET_VERSION}"',
    migrated,
)
migrated = re.sub(r'(?m)^adapterVersion:.*\n?', "", migrated)

adapter_line = f"adapters: {json.dumps(adapters, ensure_ascii=False)}"
if adapters_match:
    migrated = re.sub(r"(?m)^adapters:.*$", adapter_line, migrated)
else:
    project_id_match = re.search(r"(?m)^projectId:.*$", migrated)
    if not project_id_match:
        raise SystemExit("Missing projectId; migration made no changes.")
    migrated = (
        migrated[: project_id_match.end()]
        + f"\n{adapter_line}"
        + migrated[project_id_match.end() :]
    )

if old_access and not new_access:
    migrated = re.sub(
        r"(?m)^(\s{2})realFamilyDataAccess:(\s*(?:true|false)\s*)$",
        r"\1sensitiveDataAccess:\2",
        migrated,
    )
elif old_access and new_access:
    migrated = re.sub(
        r"(?m)^\s{2}realFamilyDataAccess:\s*(?:true|false)\s*\n?", "", migrated
    )

event = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "type": "workspace_migrated",
    "fromVersion": source_version,
    "toVersion": TARGET_VERSION,
    "summary": "Generalized project state while preserving project identity.",
}
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
    and event.get("toVersion") == TARGET_VERSION
    for event in parsed_events
)
if not already_recorded:
    events_text += json.dumps(event, ensure_ascii=False) + "\n"

# Write the migration journal first. A retry can safely finish state replacement
# without duplicating the event if the process stops between these two writes.
atomic_write(events_path, events_text)
atomic_write(state_path, migrated.lstrip("\n"))
for directory in ("observations", "protocol-candidates", "reviews", "metrics"):
    (workspace / directory).mkdir(parents=True, exist_ok=True)

print("Migration completed without overwriting project identity or history.")
