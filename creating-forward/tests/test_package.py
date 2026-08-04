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

from validate_package import validate_package


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
            for relative_path in (
                "AGENTS.md",
                "adapters/README.md",
                "README.md",
                "START_HERE.md",
                "SKILL.md",
                "schemas/project-state.schema.json",
                "schemas/task-graph.schema.json",
                "schemas/task.schema.json",
                "scripts/init_workspace.py",
                "scripts/migrate_workspace_v02_to_v03.py",
                "scripts/task_graph.py",
                "scripts/validate_evals.py",
                "scripts/validate_workspace.py",
                "scripts/validate_package.py",
                "scripts/validate_task_graph.py",
                "templates/project-state.yaml",
            ):
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}\n", encoding="utf-8")
            (root / "evals").mkdir()

            errors = validate_package(root)

        self.assertIn("No evaluation catalogs found", errors)

    def test_package_validation_does_not_require_mingos_catalog(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "package"
            shutil.copytree(
                ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
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

    def test_mutable_repository_has_no_stale_release_manifest(self):
        self.assertFalse((ROOT / "MANIFEST.json").exists())

    def test_project_specific_seed_is_not_a_core_entrypoint(self):
        self.assertFalse((ROOT / "KNOWN_FACTS_SEED.md").exists())
        self.assertTrue((ROOT / "bootstrap" / "MINGOS_KNOWN_FACTS_SEED.md").exists())

    def test_required_package_files_exist(self):
        required = [
            "AGENTS.md",
            "adapters/README.md",
            "README.md",
            "START_HERE.md",
            "SKILL.md",
            "schemas/project-state.schema.json",
            "schemas/task-graph.schema.json",
            "schemas/task.schema.json",
            "scripts/init_workspace.py",
            "scripts/migrate_workspace_v02_to_v03.py",
            "scripts/task_graph.py",
            "scripts/validate_evals.py",
            "scripts/validate_workspace.py",
            "scripts/validate_package.py",
            "scripts/validate_task_graph.py",
            "templates/project-state.yaml",
            "evals/core-scenarios.json",
            "evals/mingos-scenarios.json",
        ]

        missing = [path for path in required if not (ROOT / path).exists()]

        self.assertEqual([], missing)

    def test_json_schemas_are_valid_json(self):
        for schema in (ROOT / "schemas").glob("*.json"):
            with self.subTest(schema=schema.name):
                json.loads(schema.read_text(encoding="utf-8"))

    def test_project_state_schema_pins_current_contract_versions(self):
        schema = json.loads(
            (ROOT / "schemas" / "project-state.schema.json").read_text(
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
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: creating-forward\n", skill)
        for project_specific_term in (
            "MingOS",
            "Ming Foundation",
            "realFamilyDataAccess",
        ):
            self.assertNotIn(project_specific_term, skill)

    def test_default_state_is_project_agnostic(self):
        template = (ROOT / "templates" / "project-state.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn('projectId: ""', template)
        self.assertIn("adapters: []", template)
        self.assertIn("sensitiveDataAccess: false", template)
        self.assertNotIn("mingos", template.lower())
        self.assertNotIn("realFamilyDataAccess", template)

    def test_core_protocol_is_project_agnostic(self):
        protocol_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "protocol").glob("*.md")
        )

        for project_specific_term in (
            "MingOS",
            "Ming Foundation",
            "真实家庭",
        ):
            self.assertNotIn(project_specific_term, protocol_text)


class WorkspaceLifecycleTests(unittest.TestCase):
    def v02_state(
        self,
        project_id,
        adapter_version=None,
        adapters=None,
        legacy_access="false",
        new_access=None,
    ):
        lines = [
            'protocolVersion: "0.2.0"',
            f'projectId: "{project_id}"',
        ]
        if adapter_version:
            lines.append(f'adapterVersion: "{adapter_version}"')
        if adapters is not None:
            lines.append(f"adapters: {json.dumps(adapters)}")
        lines.extend(
            [
                'schemaVersion: "0.2.0"',
                'workspaceVersion: "0.2.0"',
                'conformanceSuiteVersion: "0.2.0"',
                'phase: "idle"',
                'presenceMode: "attended"',
                'delegationMode: "supervised"',
                'requirementsStatus: "draft"',
                "authorizationProfile:",
                "  workspaceWrite: true",
                "  commandExecution: true",
                "  networkAccess: true",
                "  externalMessaging: false",
                "  productionDeploy: false",
                "  paidActions: false",
                "  destructiveActions: false",
                f"  realFamilyDataAccess: {legacy_access}",
            ]
        )
        if new_access is not None:
            lines.append(f"  sensitiveDataAccess: {new_access}")
        return "\n".join(lines) + "\n"

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

            init = self.run_script("init_workspace.py", project)
            validate = self.run_script("validate_workspace.py", project)
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

            result = self.run_script("init_workspace.py", project)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("user-owned-state\n", state.read_text(encoding="utf-8"))

    def test_initialization_records_explicit_adapters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "adapted-project"
            project.mkdir()

            result = self.run_script("init_workspace.py", project, "mingos")
            state = (project / ".creating-forward" / "state.yaml").read_text(
                encoding="utf-8"
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('adapters: ["mingos"]', state)

    def test_v02_migration_preserves_identity_and_generalizes_authorization(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "existing-mingos-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            state.write_text(
                self.v02_state(
                    "existing-project", adapter_version="mingos-0.2.0"
                ),
                encoding="utf-8",
            )
            (workspace / "events.jsonl").write_text("", encoding="utf-8")

            result = self.run_script("migrate_workspace_v02_to_v03.py", project)
            migrated = state.read_text(encoding="utf-8")

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('protocolVersion: "0.4.0-dev"', migrated)
            self.assertIn('projectId: "existing-project"', migrated)
            self.assertIn('adapters: ["mingos"]', migrated)
            self.assertIn("sensitiveDataAccess: false", migrated)
            self.assertNotIn("adapterVersion", migrated)
            self.assertNotIn("realFamilyDataAccess", migrated)

    def test_v01_migration_updates_versions_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "v01-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            state.write_text(
                'protocolVersion: "0.1.0"\n'
                'projectId: "v01-project"\n'
                'schemaVersion: "0.1.0"\n'
                'workspaceVersion: "0.1.0"\n'
                'conformanceSuiteVersion: "0.1.0"\n',
                encoding="utf-8",
            )
            events = workspace / "events.jsonl"
            events.write_text("", encoding="utf-8")

            first = self.run_script("migrate_workspace_v01_to_v02.py", project)
            second = self.run_script("migrate_workspace_v01_to_v02.py", project)
            migrated = state.read_text(encoding="utf-8")
            event_lines = [line for line in events.read_text(encoding="utf-8").splitlines() if line]

            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertIn('protocolVersion: "0.2.0"', migrated)
            self.assertIn('schemaVersion: "0.2.0"', migrated)
            self.assertIn('workspaceVersion: "0.2.0"', migrated)
            self.assertIn('conformanceSuiteVersion: "0.2.0"', migrated)
            self.assertEqual(1, len(event_lines))
            for directory in ("observations", "protocol-candidates", "reviews", "metrics"):
                self.assertTrue((workspace / directory).is_dir())

    def test_v02_migration_merges_existing_adapters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "existing-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            state.write_text(
                self.v02_state(
                    "existing-project",
                    adapter_version="mingos-0.2.0",
                    adapters=["other"],
                ),
                encoding="utf-8",
            )
            (workspace / "events.jsonl").write_text("", encoding="utf-8")

            result = self.run_script("migrate_workspace_v02_to_v03.py", project)
            migrated = state.read_text(encoding="utf-8")

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('adapters: ["other", "mingos"]', migrated)

    def test_v02_migration_rejects_authorization_conflict_without_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "conflicted-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            original = self.v02_state(
                "conflicted-project", legacy_access="true", new_access="false"
            )
            state.write_text(original, encoding="utf-8")
            events = workspace / "events.jsonl"
            events.write_text("", encoding="utf-8")

            result = self.run_script("migrate_workspace_v02_to_v03.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Conflicting authorization fields", result.stderr)
            self.assertEqual(original, state.read_text(encoding="utf-8"))
            self.assertEqual("", events.read_text(encoding="utf-8"))

    def test_v02_migration_rejects_wrong_version_without_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "wrong-version-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            original = 'protocolVersion: "9.9.9"\nprojectId: "wrong-version"\n'
            state.write_text(original, encoding="utf-8")
            events = workspace / "events.jsonl"
            events.write_text("", encoding="utf-8")

            result = self.run_script("migrate_workspace_v02_to_v03.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Unsupported protocolVersion", result.stderr)
            self.assertEqual(original, state.read_text(encoding="utf-8"))
            self.assertEqual("", events.read_text(encoding="utf-8"))

    def test_v02_migration_creates_required_evolution_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "minimal-v02-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            (workspace / "state.yaml").write_text(
                self.v02_state("minimal-v02-project"),
                encoding="utf-8",
            )
            (workspace / "events.jsonl").write_text("", encoding="utf-8")

            result = self.run_script("migrate_workspace_v02_to_v03.py", project)

            self.assertEqual(0, result.returncode, result.stderr)
            for directory in ("observations", "protocol-candidates", "reviews", "metrics"):
                self.assertTrue((workspace / directory).is_dir())

    def test_v02_migration_rejects_incomplete_source_without_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "incomplete-v02-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            original = (
                'protocolVersion: "0.2.0"\n'
                'projectId: "incomplete-v02-project"\n'
                'authorizationProfile:\n'
                '  realFamilyDataAccess: false\n'
            )
            state.write_text(original, encoding="utf-8")
            events = workspace / "events.jsonl"
            events.write_text("", encoding="utf-8")

            result = self.run_script("migrate_workspace_v02_to_v03.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Incomplete v0.2 state", result.stderr)
            self.assertEqual(original, state.read_text(encoding="utf-8"))
            self.assertEqual("", events.read_text(encoding="utf-8"))

    def test_v02_migration_rejects_authorization_fields_outside_profile(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "wrong-auth-scope-v02-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            original = self.v02_state("wrong-auth-scope-v02-project").replace(
                "authorizationProfile:\n", "unrelated:\n"
            )
            state.write_text(original, encoding="utf-8")
            events = workspace / "events.jsonl"
            events.write_text("", encoding="utf-8")

            result = self.run_script("migrate_workspace_v02_to_v03.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Incomplete v0.2 state", result.stderr)
            self.assertEqual(original, state.read_text(encoding="utf-8"))
            self.assertEqual("", events.read_text(encoding="utf-8"))

    def test_workspace_validation_rejects_invalid_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "invalid-state-project"
            project.mkdir()
            self.run_script("init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            state.write_text('protocolVersion: "0.4.0-dev"\n', encoding="utf-8")

            result = self.run_script("validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Missing state field: projectId", result.stdout)

    def test_workspace_validation_rejects_wrong_path_type(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "invalid-path-project"
            project.mkdir()
            self.run_script("init_workspace.py", project)
            tasks = project / ".creating-forward" / "tasks"
            tasks.rmdir()
            tasks.write_text("not-a-directory\n", encoding="utf-8")

            result = self.run_script("validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Expected directory", result.stdout)

    def test_workspace_validation_rejects_unknown_version_and_empty_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "invalid-version-project"
            project.mkdir()
            self.run_script("init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            content = state.read_text(encoding="utf-8")
            content = content.replace(
                'protocolVersion: "0.4.0-dev"', 'protocolVersion: "9.9.9"'
            ).replace(
                'projectId: "invalid-version-project"', 'projectId: ""'
            )
            state.write_text(content, encoding="utf-8")

            result = self.run_script("validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Unsupported protocolVersion", result.stdout)
            self.assertIn("projectId must be a non-empty quoted string", result.stdout)

    def test_workspace_validation_rejects_unquoted_protocol_version(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "unquoted-version-project"
            project.mkdir()
            self.run_script("init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            content = state.read_text(encoding="utf-8").replace(
                'protocolVersion: "0.4.0-dev"', "protocolVersion: 9.9.9"
            )
            state.write_text(content, encoding="utf-8")

            result = self.run_script("validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("protocolVersion must be a quoted string", result.stdout)

    def test_workspace_validation_requires_authorization_profile_scope(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "wrong-scope-project"
            project.mkdir()
            self.run_script("init_workspace.py", project)
            state = project / ".creating-forward" / "state.yaml"
            content = state.read_text(encoding="utf-8")
            content = content.replace("authorizationProfile:\n", "unrelated:\n")
            state.write_text(content, encoding="utf-8")

            result = self.run_script("validate_workspace.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Missing state field: authorizationProfile", result.stdout)

    def test_v01_migration_rejects_invalid_events_without_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "invalid-events-project"
            workspace = project / ".creating-forward"
            workspace.mkdir(parents=True)
            state = workspace / "state.yaml"
            original = (
                'protocolVersion: "0.1.0"\n'
                'projectId: "invalid-events-project"\n'
                'schemaVersion: "0.1.0"\n'
                'workspaceVersion: "0.1.0"\n'
                'conformanceSuiteVersion: "0.1.0"\n'
            )
            state.write_text(original, encoding="utf-8")
            events = workspace / "events.jsonl"
            events.write_text("not-json\n", encoding="utf-8")

            result = self.run_script("migrate_workspace_v01_to_v02.py", project)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Invalid events.jsonl", result.stderr)
            self.assertEqual(original, state.read_text(encoding="utf-8"))
            self.assertFalse((workspace / "observations").exists())
            self.assertFalse((workspace / "protocol-candidates").exists())
            self.assertFalse((workspace / "reviews").exists())
            self.assertFalse((workspace / "metrics").exists())


if __name__ == "__main__":
    unittest.main()
