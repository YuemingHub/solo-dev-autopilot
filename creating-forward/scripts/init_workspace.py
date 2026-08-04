#!/usr/bin/env python3
from pathlib import Path
import sys, shutil, json
from datetime import datetime, timezone

if len(sys.argv) < 2:
    raise SystemExit("Usage: python init_workspace.py <project-path> [adapter ...]")

repo = Path(sys.argv[1]).resolve()
adapters = list(dict.fromkeys(sys.argv[2:]))
if not repo.exists():
    raise SystemExit(f"Repository path does not exist: {repo}")

root = repo / ".creating-forward"
(root / "decisions").mkdir(parents=True, exist_ok=True)
(root / "tasks").mkdir(parents=True, exist_ok=True)
(root / "evidence").mkdir(parents=True, exist_ok=True)
(root / "context-packs").mkdir(parents=True, exist_ok=True)
for _name in ["observations", "protocol-candidates", "reviews", "metrics"]:
    (root / _name).mkdir(parents=True, exist_ok=True)

package_root = Path(__file__).resolve().parents[1]
templates = package_root / "templates"

def copy_if_missing(src_name, dst_name):
    src = templates / src_name
    dst = root / dst_name
    if not dst.exists():
        shutil.copyfile(src, dst)

state = root / "state.yaml"
if not state.exists():
    state_template = (templates / "project-state.yaml").read_text(encoding="utf-8")
    project_id = json.dumps(repo.name, ensure_ascii=False)
    adapter_list = json.dumps(adapters, ensure_ascii=False)
    state.write_text(
        state_template.replace('projectId: ""', f"projectId: {project_id}").replace(
            "adapters: []", f"adapters: {adapter_list}"
        ),
        encoding="utf-8",
    )
copy_if_missing("deliverables.md", "deliverables.md")

req = root / "requirements.md"
if not req.exists():
    req.write_text("""# Requirements

## Problem

## Target users

## Desired outcome

## Deliverables

## Constraints

## Success criteria

## Out of scope

## Unknowns

## Approval status

draft
""", encoding="utf-8")

events = root / "events.jsonl"
if not events.exists():
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "workspace_initialized",
        "actor": "creating-forward",
        "summary": "Initialized Creating Forward workspace",
    }
    events.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"Initialized: {root}")
