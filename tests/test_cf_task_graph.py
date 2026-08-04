import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cf_task_graph import validate_task_graph


def task(task_id, dependencies=None, **overrides):
    value = {
        "id": task_id,
        "title": f"Task {task_id}",
        "goal": f"Complete {task_id}",
        "status": "pending",
        "dependencies": dependencies or [],
        "completionCriteria": ["Result exists"],
        "verificationMethods": ["Inspect result"],
        "allowedFiles": [],
        "forbiddenActions": [],
        "assignedRole": "builder",
        "reviewRole": "verifier",
    }
    value.update(overrides)
    return value


class TaskGraphValidationTests(unittest.TestCase):
    def graph(self, tasks):
        return {"version": "0.4.0-dev", "tasks": tasks}

    def error_codes(self, result):
        return [error["code"] for error in result["errors"]]

    def test_valid_graph_returns_stable_topological_order(self):
        graph = self.graph(
            [
                task("T-003", ["T-001"]),
                task("T-001"),
                task("T-002"),
                task("T-004", ["T-002"]),
            ]
        )

        result = validate_task_graph(graph)

        self.assertTrue(result["valid"])
        self.assertEqual([], result["errors"])
        self.assertEqual(
            ["T-001", "T-002", "T-003", "T-004"],
            result["topologicalOrder"],
        )

    def test_rejects_invalid_root_and_version(self):
        invalid_root = validate_task_graph([])
        invalid_version = validate_task_graph({"version": "9.9.9", "tasks": []})

        self.assertEqual(["INVALID_GRAPH_SHAPE"], self.error_codes(invalid_root))
        self.assertEqual(
            ["UNSUPPORTED_GRAPH_VERSION"], self.error_codes(invalid_version)
        )

    def test_reports_missing_and_invalid_task_fields(self):
        missing = task("T-001")
        del missing["goal"]
        invalid = task("T-002", title="", dependencies="T-001")

        result = validate_task_graph(self.graph([missing, invalid]))

        self.assertIn("MISSING_TASK_FIELD", self.error_codes(result))
        self.assertGreaterEqual(self.error_codes(result).count("INVALID_TASK_FIELD"), 2)
        self.assertFalse(result["valid"])
        self.assertEqual([], result["topologicalOrder"])

    def test_non_string_status_returns_structured_error(self):
        result = validate_task_graph(self.graph([task("T-001", status=[])]))

        self.assertFalse(result["valid"])
        self.assertIn("INVALID_TASK_FIELD", self.error_codes(result))

    def test_reports_duplicate_task_ids(self):
        result = validate_task_graph(self.graph([task("T-001"), task("T-001")]))

        self.assertEqual(["DUPLICATE_TASK_ID"], self.error_codes(result))
        self.assertEqual("T-001", result["errors"][0]["taskId"])

    def test_duplicate_ids_do_not_suppress_other_dependency_errors(self):
        incomplete_duplicate = task("T-001")
        del incomplete_duplicate["goal"]
        result = validate_task_graph(
            self.graph(
                [
                    task("T-001"),
                    incomplete_duplicate,
                    task("T-002", ["T-999"]),
                ]
            )
        )

        self.assertIn("MISSING_TASK_FIELD", self.error_codes(result))
        self.assertIn("DUPLICATE_TASK_ID", self.error_codes(result))
        self.assertIn("UNKNOWN_DEPENDENCY", self.error_codes(result))

    def test_reports_unknown_self_and_duplicate_dependencies(self):
        result = validate_task_graph(
            self.graph(
                [
                    task("T-001", ["T-001"]),
                    task("T-002", ["T-999"]),
                    task("T-003", ["T-001", "T-001"]),
                ]
            )
        )

        self.assertEqual(
            ["SELF_DEPENDENCY", "UNKNOWN_DEPENDENCY", "DUPLICATE_DEPENDENCY"],
            self.error_codes(result),
        )

    def test_reports_dependency_cycle_with_cycle_nodes(self):
        result = validate_task_graph(
            self.graph(
                [
                    task("T-001", ["T-003"]),
                    task("T-002", ["T-001"]),
                    task("T-003", ["T-002"]),
                    task("T-004", ["T-003"]),
                ]
            )
        )

        self.assertEqual(["DEPENDENCY_CYCLE"], self.error_codes(result))
        self.assertEqual(
            ["T-001", "T-003", "T-002"],
            result["errors"][0]["cycleTaskIds"],
        )
        self.assertNotIn("T-004", result["errors"][0]["cycleTaskIds"])

    def test_cycle_error_is_aggregated_with_independent_errors(self):
        result = validate_task_graph(
            self.graph(
                [
                    task("T-001", ["T-002"], unexpected=True),
                    task("T-002", ["T-001"]),
                    task("T-003", ["T-999"]),
                ]
            )
        )

        self.assertIn("INVALID_TASK_FIELD", self.error_codes(result))
        self.assertIn("UNKNOWN_DEPENDENCY", self.error_codes(result))
        self.assertIn("DEPENDENCY_CYCLE", self.error_codes(result))

    def test_deep_acyclic_graph_does_not_use_recursive_cycle_detection(self):
        tasks = []
        count = 1100
        for index in range(count):
            dependency = [] if index == count - 1 else [f"T-{index + 1:04d}"]
            tasks.append(task(f"T-{index:04d}", dependency))

        result = validate_task_graph(self.graph(tasks))

        self.assertTrue(result["valid"])
        self.assertEqual(count, len(result["topologicalOrder"]))

    def test_runtime_enforces_schema_root_and_attempt_constraints(self):
        graph = self.graph(
            [task("T-001", attemptCount=-1, maxAttempts=0, unexpected=True)]
        )
        graph["extra"] = True

        result = validate_task_graph(graph)

        self.assertGreaterEqual(self.error_codes(result).count("INVALID_GRAPH_SHAPE"), 1)
        self.assertGreaterEqual(self.error_codes(result).count("INVALID_TASK_FIELD"), 3)

    def test_json_mathematical_integers_match_schema_semantics(self):
        result = validate_task_graph(
            self.graph([task("T-001", attemptCount=1.0, maxAttempts=2.0)])
        )

        self.assertTrue(result["valid"], result["errors"])


class TaskGraphCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "cf_validate_task_graph.py"),
                *arguments,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def write_graph(self, directory, graph):
        path = Path(directory) / "graph.json"
        path.write_text(json.dumps(graph), encoding="utf-8")
        return path

    def test_text_output_reports_success_and_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            graph_path = self.write_graph(
                temp_dir,
                {
                    "version": "0.4.0-dev",
                    "tasks": [task("T-002", ["T-001"]), task("T-001")],
                },
            )

            result = self.run_cli(str(graph_path))

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("TASK GRAPH VALIDATION: PASSED", result.stdout)
            self.assertIn("TOPOLOGICAL ORDER: T-001, T-002", result.stdout)

    def test_json_output_uses_stable_result_shape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            graph_path = self.write_graph(
                temp_dir,
                {
                    "version": "0.4.0-dev",
                    "tasks": [task("T-001", ["T-999"])],
                },
            )

            result = self.run_cli(str(graph_path), "--format", "json")
            payload = json.loads(result.stdout)

            self.assertEqual(1, result.returncode)
            self.assertEqual(["valid", "errors", "topologicalOrder"], list(payload))
            self.assertEqual("UNKNOWN_DEPENDENCY", payload["errors"][0]["code"])

    def test_missing_file_is_an_input_error(self):
        result = self.run_cli("missing-graph.json", "--format", "json")
        payload = json.loads(result.stdout)

        self.assertEqual(2, result.returncode)
        self.assertFalse(payload["valid"])
        self.assertEqual("INPUT_ERROR", payload["errors"][0]["code"])

    def test_invalid_json_is_an_input_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid.json"
            path.write_text("not-json", encoding="utf-8")

            result = self.run_cli(str(path), "--format", "json")
            payload = json.loads(result.stdout)

            self.assertEqual(2, result.returncode)
            self.assertEqual("INPUT_ERROR", payload["errors"][0]["code"])

    def test_json_format_usage_error_uses_json_result_shape(self):
        result = self.run_cli("--format", "json")
        payload = json.loads(result.stdout)

        self.assertEqual(2, result.returncode)
        self.assertEqual("INPUT_ERROR", payload["errors"][0]["code"])
        self.assertEqual([], payload["topologicalOrder"])

    def test_equals_style_json_format_usage_error_uses_json_result_shape(self):
        result = self.run_cli("--format=json")
        payload = json.loads(result.stdout)

        self.assertEqual(2, result.returncode)
        self.assertEqual("INPUT_ERROR", payload["errors"][0]["code"])


if __name__ == "__main__":
    unittest.main()
