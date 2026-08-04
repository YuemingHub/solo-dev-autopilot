#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


if len(sys.argv) != 2:
    raise SystemExit("Usage: python validate_workspace.py <project-path>")

project = Path(sys.argv[1]).resolve()
workspace = project / ".creating-forward"
required_files = [
    workspace / "state.yaml",
    workspace / "events.jsonl",
    workspace / "requirements.md",
    workspace / "deliverables.md",
]
required_directories = [
    workspace / "decisions",
    workspace / "tasks",
    workspace / "evidence",
    workspace / "context-packs",
    workspace / "observations",
    workspace / "protocol-candidates",
    workspace / "reviews",
    workspace / "metrics",
]
errors = []

for path in required_files:
    if not path.exists():
        errors.append(f"Missing: {path}")
    elif not path.is_file():
        errors.append(f"Expected file: {path}")

for path in required_directories:
    if not path.exists():
        errors.append(f"Missing: {path}")
    elif not path.is_dir():
        errors.append(f"Expected directory: {path}")

state_path = workspace / "state.yaml"
if state_path.is_file():
    try:
        state = state_path.read_text(encoding="utf-8")
    except UnicodeError as error:
        errors.append(f"Invalid UTF-8 state.yaml: {error}")
    else:
        required_state_fields = [
            "protocolVersion",
            "projectId",
            "phase",
            "presenceMode",
            "delegationMode",
            "requirementsStatus",
            "authorizationProfile",
        ]
        for field in required_state_fields:
            if not re.search(rf"(?m)^{re.escape(field)}:", state):
                errors.append(f"Missing state field: {field}")

        protocol_match = re.search(
            r'(?m)^protocolVersion:\s*"([^"\n]+)"\s*$', state
        )
        if not protocol_match:
            errors.append("protocolVersion must be a quoted string")
        elif protocol_match.group(1) != "0.4.0-dev":
            errors.append(
                f"Unsupported protocolVersion: {protocol_match.group(1)}"
            )

        project_match = re.search(r'(?m)^projectId:\s*"([^"\n]*)"\s*$', state)
        if not project_match or not project_match.group(1).strip():
            errors.append("projectId must be a non-empty quoted string")

        for version_field in (
            "schemaVersion",
            "workspaceVersion",
            "conformanceSuiteVersion",
        ):
            match = re.search(
                rf'(?m)^{version_field}:\s*"([^"\n]+)"\s*$', state
            )
            if not match:
                errors.append(f"Missing state field: {version_field}")
            elif match.group(1) != "0.4.0-dev":
                errors.append(
                    f"Unsupported {version_field}: {match.group(1)}"
                )

        allowed_values = {
            "phase": {
                "idle", "understanding", "exploring", "confirming", "planning",
                "executing", "reviewing", "delivering", "complete", "blocked",
                "paused_for_human", "cancelled",
            },
            "presenceMode": {"attended", "away"},
            "delegationMode": {"advisory", "supervised", "delegated"},
            "requirementsStatus": {"draft", "confirmed", "changed", "rejected"},
        }
        for field, allowed in allowed_values.items():
            match = re.search(rf'(?m)^{field}:\s*"?([^"\n]+)"?\s*$', state)
            if match and match.group(1).strip() not in allowed:
                errors.append(f"Invalid state value for {field}: {match.group(1).strip()}")

        authorization_match = re.search(
            r"(?ms)^authorizationProfile:\s*\n((?:^  [^\n]+\n?)*)", state
        )
        authorization_block = authorization_match.group(1) if authorization_match else ""
        required_authorizations = [
            "workspaceWrite", "commandExecution", "networkAccess",
            "externalMessaging", "productionDeploy", "paidActions",
            "destructiveActions", "sensitiveDataAccess",
        ]
        for field in required_authorizations:
            match = re.search(
                rf"(?m)^  {field}:\s*(\S+)\s*$", authorization_block
            )
            if not match:
                errors.append(f"Missing authorization field: {field}")
            elif match.group(1) not in {"true", "false"}:
                errors.append(f"Authorization must be boolean: {field}")

events_path = workspace / "events.jsonl"
if events_path.is_file():
    try:
        event_lines = events_path.read_text(encoding="utf-8").splitlines()
    except UnicodeError as error:
        errors.append(f"Invalid UTF-8 events.jsonl: {error}")
    else:
        for line_number, line in enumerate(event_lines, 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"Invalid JSONL line {line_number}: {error}")

sensitive_names = {".env", "credentials.json", "secrets.json", "token.json"}
try:
    for path in workspace.rglob("*"):
        if path.name.lower() in sensitive_names:
            errors.append(f"Potential sensitive file in workspace: {path}")
except OSError as error:
    errors.append(f"Unable to inspect workspace files: {error}")

if errors:
    print("VALIDATION: FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("VALIDATION: PASSED")
