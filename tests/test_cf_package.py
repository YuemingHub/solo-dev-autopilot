import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cf_validate_package import validate_package


REQUIRED_FOR_GENERIC_PACKAGE = (
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
    "scripts/cf_validate_package.py",
    "templates/creating-forward/project-state.yaml",
)


class PackageStructureTests(unittest.TestCase):
    def test_package_validation_reports_missing_files_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            errors = validate_package(Path(temp_dir))

        self.assertTrue(errors)
        self.assertTrue(all(isinstance(error, str) for error in errors))
        self.assertTrue(any(error.startswith("Missing:") for error in errors))

    def test_package_validation_rejects_empty_evaluation_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative_path in REQUIRED_FOR_GENERIC_PACKAGE:
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}\n", encoding="utf-8")
            (root / "evals").mkdir()

            errors = validate_package(root)

        self.assertIn("No evaluation catalogs found", errors)

    def test_repository_package_validation_passes(self):
        self.assertEqual([], validate_package(ROOT))

    def test_package_validation_does_not_require_mingos_catalog(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "package"
            shutil.copytree(
                ROOT,
                root,
                ignore=shutil.ignore_patterns(
                    ".git", "__pycache__", "*.pyc", "references", ".github"
                ),
            )
            mingos_path = root / "evals" / "mingos-scenarios.json"
            adapter = json.loads(mingos_path.read_text(encoding="utf-8"))
            adapter["adapter"] = "example"
            adapter["requiredAdapters"] = ["example"]
            adapter["reservedTerms"] = ["Example Product"]
            for scenario in adapter["scenarios"]:
                scenario["initialState"]["adapters"] = ["example"]
            (root / "evals" / "example-scenarios.json").write_text(
                json.dumps(adapter, ensure_ascii=False), encoding="utf-8"
            )
            mingos_path.unlink()

            errors = validate_package(root)

        self.assertEqual([], errors)

    def test_required_package_files_exist(self):
        missing = [path for path in REQUIRED_FOR_GENERIC_PACKAGE if not (ROOT / path).exists()]

        self.assertEqual([], missing)

    def test_json_schemas_are_valid_json(self):
        for schema in (ROOT / "configs" / "schemas").glob("*.json"):
            with self.subTest(schema=schema.name):
                json.loads(schema.read_text(encoding="utf-8"))

    def test_project_state_schema_pins_current_contract_versions(self):
        schema = json.loads(
            (ROOT / "configs" / "schemas" / "project-state.schema.json").read_text(
                encoding="utf-8"
            )
        )

        for field in (
            "protocolVersion",
            "schemaVersion",
            "workspaceVersion",
            "conformanceSuiteVersion",
        ):
            self.assertEqual("0.4.0-dev", schema["properties"][field]["const"])

    def test_core_skill_is_project_agnostic(self):
        skill = (ROOT / ".claude" / "skills" / "creating-forward" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("name: creating-forward\n", skill)
        for project_specific_term in (
            "MingOS",
            "Ming Foundation",
            "realFamilyDataAccess",
        ):
            self.assertNotIn(project_specific_term, skill)

    def test_default_state_is_project_agnostic(self):
        template = (ROOT / "templates" / "creating-forward" / "project-state.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn('projectId: ""', template)
        self.assertIn("adapters: []", template)
        self.assertIn("sensitiveDataAccess: false", template)
        self.assertNotIn("mingos", template.lower())
        self.assertNotIn("realFamilyDataAccess", template)


class WorkspaceLifecycleTests(unittest.TestCase):
    def run_script(self, script_name, project_path, *extra_args):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / script_name),
                str(project_path),
                *extra_args,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_initialization_creates_valid_generic_workspace(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "sample-project"
            project.mkdir()

            init = self.run_script("cf_init_workspace.py", project)
            validate = self.run_script("cf_validate_workspace.py", project)
            state = (project / ".creating-forward" / "state.yaml").read_text(
                encoding="utf-8"
            )

            self.assertEqual(0, init.returncode, init.stderr)
            self.assertEqual(0, validate.returncode, validate.stdout + validate.stderr)
            self.assertIn('projectId: "sample-project"', state)
            self.assertNotIn("mingos", state.lower())

    def test_reinitialization_preserves_existing_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "existing-project"
            project.mkdir()
            workspace = project / ".creating-forward"
            workspace.mkdir()
            state = workspace / "state.yaml"
            state.write_text("user-owned-state\n", encoding="utf-8")

            result = self.run_script("cf_init_workspace.py", project)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("user-owned-state\n", state.read_text(encoding="utf-8"))

    def test_initialization_records_explicit_adapters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "adapted-project"
            project.mkdir()

            result = self.run_script("cf_init_workspace.py", project, "mingos")
            state = (project / ".creating-forward" / "state.yaml").read_text(
                encoding="utf-8"
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('adapters: ["mingos"]', state)

    def test_workspace_validation_rejects_invalid_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "invalid-state-project"
            project.mkdir()
            self.run_script("cf_init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            state.write_text('protocolVersion: "0.4.0-dev"\n', encoding="utf-8")

            result = self.run_script("cf_validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Missing state field: projectId", result.stdout)

    def test_workspace_validation_rejects_wrong_path_type(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "invalid-path-project"
            project.mkdir()
            self.run_script("cf_init_workspace.py", project)
            tasks = project / ".creating-forward" / "tasks"
            tasks.rmdir()
            tasks.write_text("not-a-directory\n", encoding="utf-8")

            result = self.run_script("cf_validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Expected directory", result.stdout)

    def test_workspace_validation_rejects_unknown_version_and_empty_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "invalid-version-project"
            project.mkdir()
            self.run_script("cf_init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            content = state.read_text(encoding="utf-8")
            content = content.replace(
                'protocolVersion: "0.4.0-dev"', 'protocolVersion: "9.9.9"'
            ).replace(
                'projectId: "invalid-version-project"', 'projectId: ""'
            )
            state.write_text(content, encoding="utf-8")

            result = self.run_script("cf_validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Unsupported protocolVersion", result.stdout)
            self.assertIn("projectId must be a non-empty quoted string", result.stdout)

    def test_workspace_validation_rejects_unquoted_protocol_version(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "unquoted-version-project"
            project.mkdir()
            self.run_script("cf_init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            content = state.read_text(encoding="utf-8").replace(
                'protocolVersion: "0.4.0-dev"', "protocolVersion: 9.9.9"
            )
            state.write_text(content, encoding="utf-8")

            result = self.run_script("cf_validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("protocolVersion must be a quoted string", result.stdout)

    def test_workspace_validation_requires_authorization_profile_scope(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "wrong-scope-project"
            project.mkdir()
            self.run_script("cf_init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            content = state.read_text(encoding="utf-8")
            content = content.replace("authorizationProfile:\n", "unrelated:\n")
            state.write_text(content, encoding="utf-8")

            result = self.run_script("cf_validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Missing state field: authorizationProfile", result.stdout)


if __name__ == "__main__":
    unittest.main()
