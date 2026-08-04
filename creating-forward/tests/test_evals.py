import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_evals import discover_catalog_paths, validate_catalogs


class EvaluationCatalogTests(unittest.TestCase):
    def load_catalogs(self):
        return [
            json.loads(
                (ROOT / "evals" / "core-scenarios.json").read_text(encoding="utf-8")
            ),
            json.loads(
                (ROOT / "evals" / "mingos-scenarios.json").read_text(
                    encoding="utf-8"
                )
            ),
        ]

    def error_codes(self, result):
        return [error["code"] for error in result["errors"]]

    def test_repository_catalogs_are_valid_and_not_marked_as_executed(self):
        result = validate_catalogs(self.load_catalogs())

        self.assertTrue(result["valid"])
        self.assertEqual([], result["errors"])
        self.assertEqual(2, result["catalogCount"])
        self.assertGreaterEqual(result["scenarioCount"], 8)
        for catalog in self.load_catalogs():
            self.assertNotIn("passed", catalog)
            for scenario in catalog["scenarios"]:
                self.assertNotIn("status", scenario)
                self.assertNotIn("result", scenario)

    def test_rejects_duplicate_scenario_ids_across_catalogs(self):
        catalogs = self.load_catalogs()
        catalogs[1]["scenarios"][0]["id"] = catalogs[0]["scenarios"][0]["id"]

        result = validate_catalogs(catalogs)

        self.assertIn("DUPLICATE_SCENARIO_ID", self.error_codes(result))

    def test_rejects_core_adapter_and_project_specific_terms(self):
        catalogs = self.load_catalogs()
        core = catalogs[0]
        core["requiredAdapters"] = ["mingos"]
        core["scenarios"][0]["title"] = "MingOS production boundary"

        result = validate_catalogs(catalogs)

        self.assertIn("CORE_REQUIRES_ADAPTER", self.error_codes(result))
        self.assertIn("PROJECT_TERM_IN_CORE", self.error_codes(result))

    def test_rejects_adapter_catalog_without_matching_adapter(self):
        catalogs = self.load_catalogs()
        catalogs[1]["adapter"] = "other"

        result = validate_catalogs(catalogs)

        self.assertIn("ADAPTER_NOT_DECLARED", self.error_codes(result))

    def test_adapter_catalog_is_not_hardcoded_to_mingos(self):
        catalogs = self.load_catalogs()
        adapter = catalogs[1]
        adapter["adapter"] = "example"
        adapter["requiredAdapters"] = ["example"]
        adapter["reservedTerms"] = ["Example Product"]
        for scenario in adapter["scenarios"]:
            scenario["initialState"]["adapters"] = ["example"]

        result = validate_catalogs(catalogs)

        self.assertTrue(result["valid"], result["errors"])

    def test_rejects_incomplete_scenario_and_unknown_assertion_type(self):
        catalogs = self.load_catalogs()
        scenario = catalogs[0]["scenarios"][0]
        del scenario["evidenceRequired"]
        scenario["assertionType"] = "magic"

        result = validate_catalogs(catalogs)

        self.assertIn("MISSING_SCENARIO_FIELD", self.error_codes(result))
        self.assertIn("INVALID_ASSERTION_TYPE", self.error_codes(result))

    def test_rejects_invalid_scenario_types_and_execution_results(self):
        catalogs = self.load_catalogs()
        scenario = catalogs[0]["scenarios"][0]
        scenario["id"] = 1
        scenario["title"] = ""
        scenario["input"] = None
        scenario["initialState"] = "invalid"
        scenario["status"] = "passed"
        catalogs[0]["passed"] = True

        result = validate_catalogs(catalogs)

        self.assertIn("INVALID_SCENARIO_FIELD", self.error_codes(result))
        self.assertIn("EXECUTION_RESULT_IN_DEFINITION", self.error_codes(result))

    def test_rejects_empty_catalog(self):
        catalogs = self.load_catalogs()
        catalogs[0]["scenarios"] = []

        result = validate_catalogs(catalogs)

        self.assertIn("EMPTY_SCENARIO_CATALOG", self.error_codes(result))

    def test_adapter_scenarios_must_enable_catalog_adapter(self):
        catalogs = self.load_catalogs()
        catalogs[1]["scenarios"][0]["initialState"]["adapters"] = []

        result = validate_catalogs(catalogs)

        self.assertIn("SCENARIO_ADAPTER_NOT_ENABLED", self.error_codes(result))

    def test_core_terms_are_derived_from_adapter_catalog_metadata(self):
        catalogs = self.load_catalogs()
        catalogs[1]["reservedTerms"].append("Project Codename")
        catalogs[0]["scenarios"][0]["input"] = "Use Project Codename rules"

        result = validate_catalogs(catalogs)

        self.assertIn("PROJECT_TERM_IN_CORE", self.error_codes(result))

    def test_reserved_terms_use_semantic_values_and_word_boundaries(self):
        catalogs = self.load_catalogs()
        catalogs[1]["reservedTerms"].extend(["title", "MingOS"])
        catalogs[0]["scenarios"][0]["title"] = "MingOSian workflow"

        result = validate_catalogs(catalogs)

        self.assertNotIn("PROJECT_TERM_IN_CORE", self.error_codes(result))

    def test_validator_does_not_mutate_catalogs(self):
        catalogs = self.load_catalogs()
        original = copy.deepcopy(catalogs)

        validate_catalogs(catalogs)

        self.assertEqual(original, catalogs)


class EvaluationCliTests(unittest.TestCase):
    def test_catalog_discovery_includes_every_scenario_json(self):
        paths = discover_catalog_paths(ROOT / "evals")

        self.assertEqual(
            ["core-scenarios.json", "mingos-scenarios.json"],
            [path.name for path in paths],
        )

    def test_repository_evaluation_command_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_evals.py")],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("EVALUATION VALIDATION: PASSED", result.stdout)
        self.assertIn("CATALOGS: 2", result.stdout)


if __name__ == "__main__":
    unittest.main()
