#!/usr/bin/env python3
import json
import re
from pathlib import Path

from validate_evals import discover_catalog_paths, validate_catalogs


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = [
    "AGENTS.md",
    "adapters/README.md",
    "README.md",
    "START_HERE.md",
    "SKILL.md",
    "schemas/project-state.schema.json",
    "schemas/task-graph.schema.json",
    "schemas/task.schema.json",
    "scripts/task_graph.py",
    "scripts/validate_evals.py",
    "scripts/validate_task_graph.py",
    "scripts/init_workspace.py",
    "scripts/migrate_workspace_v02_to_v03.py",
    "scripts/validate_workspace.py",
    "templates/project-state.yaml",
    "evals/core-scenarios.json",
]
FORBIDDEN_CORE_TERMS = (
    "MingOS",
    "Ming Foundation",
    "mingos",
    "真实家庭",
    "realFamilyDataAccess",
)


def validate_package(root=ROOT):
    errors = []

    for relative_path in REQUIRED_PATHS:
        if not (root / relative_path).exists():
            errors.append(f"Missing: {relative_path}")

    for schema in (root / "schemas").glob("*.json"):
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"Invalid JSON schema {schema.name}: {error}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        try:
            skill = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"Unable to read SKILL.md: {error}")
        else:
            if not re.search(r"(?m)^name: creating-forward$", skill):
                errors.append("SKILL.md must declare name: creating-forward")
            for term in FORBIDDEN_CORE_TERMS:
                if term in skill:
                    errors.append(f"Project-specific term in Core SKILL.md: {term}")

    protocol_root = root / "protocol"
    if protocol_root.is_dir():
        try:
            protocol_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in protocol_root.glob("*.md")
            )
        except (OSError, UnicodeError) as error:
            errors.append(f"Unable to read Core protocol: {error}")
        else:
            for term in FORBIDDEN_CORE_TERMS:
                if term in protocol_text:
                    errors.append(f"Project-specific term in Core protocol: {term}")

    state_template_path = root / "templates" / "project-state.yaml"
    if state_template_path.is_file():
        try:
            state_template = state_template_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"Unable to read default project state: {error}")
        else:
            if 'projectId: ""' not in state_template:
                errors.append("Default project state must leave projectId empty")
            if "adapters: []" not in state_template:
                errors.append("Default project state must declare an empty adapters list")
            if "sensitiveDataAccess: false" not in state_template:
                errors.append("Default project state must deny sensitive data access")

    catalog_paths = discover_catalog_paths(root / "evals")
    if not catalog_paths:
        errors.append("No evaluation catalogs found")
    catalogs = []
    for catalog_path in catalog_paths:
        try:
            catalogs.append(json.loads(catalog_path.read_text(encoding="utf-8")))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"Invalid evaluation catalog {catalog_path.name}: {error}")
    if catalog_paths and len(catalogs) == len(catalog_paths):
        evaluation_result = validate_catalogs(catalogs)
        for evaluation_error in evaluation_result["errors"]:
            errors.append(
                f"Evaluation catalog error [{evaluation_error['code']}]: "
                f"{evaluation_error['message']}"
            )

    return errors


if __name__ == "__main__":
    package_errors = validate_package()
    if package_errors:
        print("PACKAGE VALIDATION: FAILED")
        for package_error in package_errors:
            print("-", package_error)
        raise SystemExit(1)
    print("PACKAGE VALIDATION: PASSED")
