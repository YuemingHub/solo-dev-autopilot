#!/usr/bin/env python3
"""三合一仓库的协议层资产校验（原 creating-forward validate_package.py 的合并版）。

校验范围：协议技能、统一目录下的 schema/模板/脚本/评估目录/适配器，
以及协议技能必须保持项目无关（不得混入项目专属术语）。
"""
import json
import re
from pathlib import Path

from cf_validate_evals import discover_catalog_paths, validate_catalogs


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    ".claude/skills/creating-forward/SKILL.md",
    "adapters/README.md",
    "configs/schemas/project-state.schema.json",
    "configs/schemas/task-graph.schema.json",
    "configs/schemas/task.schema.json",
    "scripts/cf_task_graph.py",
    "scripts/cf_validate_evals.py",
    "scripts/cf_validate_task_graph.py",
    "scripts/cf_init_workspace.py",
    "scripts/cf_validate_workspace.py",
    "templates/creating-forward/project-state.yaml",
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

    for schema in (root / "configs" / "schemas").glob("*.json"):
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"Invalid JSON schema {schema.name}: {error}")

    skill_path = root / ".claude" / "skills" / "creating-forward" / "SKILL.md"
    if skill_path.is_file():
        try:
            skill = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"Unable to read creating-forward skill: {error}")
        else:
            if not re.search(r"(?m)^name: creating-forward$", skill):
                errors.append("Skill must declare name: creating-forward")
            for term in FORBIDDEN_CORE_TERMS:
                if term in skill:
                    errors.append(f"Project-specific term in creating-forward skill: {term}")

    state_template_path = root / "templates" / "creating-forward" / "project-state.yaml"
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
