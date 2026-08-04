#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALS_ROOT = ROOT / "evals"
CATALOG_VERSION = "0.4.0-dev"
ASSERTION_TYPES = {
    "interaction",
    "state",
    "authority",
    "evidence",
    "recovery",
    "boundary",
}
REQUIRED_SCENARIO_FIELDS = (
    "id",
    "title",
    "input",
    "initialState",
    "assertionType",
    "expectedBehavior",
    "prohibitedBehavior",
    "evidenceRequired",
)
EXECUTION_RESULT_FIELDS = {"passed", "status", "result", "actualBehavior", "evidence"}
CORE_SEMANTIC_FIELDS = (
    "title",
    "input",
    "expectedBehavior",
    "prohibitedBehavior",
    "evidenceRequired",
)


def discover_catalog_paths(root=EVALS_ROOT):
    return sorted(root.glob("*-scenarios.json"), key=lambda path: path.name)


def evaluation_error(code, message, scenario_id=None, **details):
    value = {"code": code, "message": message}
    if scenario_id is not None:
        value["scenarioId"] = scenario_id
    value.update(details)
    return value


def validate_catalogs(catalogs):
    errors = []
    scenario_count = 0
    seen_ids = set()
    reserved_terms = []

    for catalog in catalogs:
        if isinstance(catalog, dict) and catalog.get("layer") == "adapter":
            terms = catalog.get("reservedTerms")
            if isinstance(terms, list) and all(
                isinstance(term, str) and term.strip() for term in terms
            ):
                reserved_terms.extend(terms)

    for catalog_index, catalog in enumerate(catalogs):
        if not isinstance(catalog, dict) or not isinstance(catalog.get("scenarios"), list):
            errors.append(
                evaluation_error(
                    "INVALID_CATALOG_SHAPE",
                    f"Catalog at index {catalog_index} must contain a scenarios array",
                    catalogIndex=catalog_index,
                )
            )
            continue

        result_fields = sorted(EXECUTION_RESULT_FIELDS.intersection(catalog))
        for field in result_fields:
            errors.append(
                evaluation_error(
                    "EXECUTION_RESULT_IN_DEFINITION",
                    f"Execution result field is not allowed in a catalog definition: {field}",
                    catalogIndex=catalog_index,
                    field=field,
                )
            )

        if catalog.get("catalogVersion") != CATALOG_VERSION:
            errors.append(
                evaluation_error(
                    "UNSUPPORTED_CATALOG_VERSION",
                    f"Unsupported catalog version: {catalog.get('catalogVersion')!r}",
                    catalogIndex=catalog_index,
                )
            )

        layer = catalog.get("layer")
        adapters = catalog.get("requiredAdapters")
        if layer not in {"core", "adapter"} or not isinstance(adapters, list) or not all(
            isinstance(adapter, str) and adapter.strip() for adapter in adapters
        ):
            errors.append(
                evaluation_error(
                    "INVALID_CATALOG_SHAPE",
                    f"Catalog at index {catalog_index} has invalid layer or adapters",
                    catalogIndex=catalog_index,
                )
            )
            continue

        catalog_adapter = catalog.get("adapter")
        if layer == "core" and adapters:
            errors.append(
                evaluation_error(
                    "CORE_REQUIRES_ADAPTER",
                    "Core evaluation catalog must not require adapters",
                    catalogIndex=catalog_index,
                )
            )
        if layer == "adapter" and (
            not isinstance(catalog_adapter, str)
            or not catalog_adapter.strip()
            or catalog_adapter not in adapters
        ):
            errors.append(
                evaluation_error(
                    "ADAPTER_NOT_DECLARED",
                    "Adapter catalog must declare and require its adapter",
                    catalogIndex=catalog_index,
                )
            )

        if not catalog["scenarios"]:
            errors.append(
                evaluation_error(
                    "EMPTY_SCENARIO_CATALOG",
                    "Evaluation catalog must contain at least one scenario",
                    catalogIndex=catalog_index,
                )
            )

        for scenario_index, scenario in enumerate(catalog["scenarios"]):
            scenario_count += 1
            if not isinstance(scenario, dict):
                errors.append(
                    evaluation_error(
                        "INVALID_SCENARIO_SHAPE",
                        f"Scenario at index {scenario_index} must be an object",
                        catalogIndex=catalog_index,
                        scenarioIndex=scenario_index,
                    )
                )
                continue

            scenario_id = scenario.get("id") if isinstance(scenario.get("id"), str) else None
            for field in REQUIRED_SCENARIO_FIELDS:
                if field not in scenario:
                    errors.append(
                        evaluation_error(
                            "MISSING_SCENARIO_FIELD",
                            f"Missing scenario field: {field}",
                            scenario_id,
                            field=field,
                            catalogIndex=catalog_index,
                            scenarioIndex=scenario_index,
                        )
                    )

            for field in sorted(EXECUTION_RESULT_FIELDS.intersection(scenario)):
                errors.append(
                    evaluation_error(
                        "EXECUTION_RESULT_IN_DEFINITION",
                        f"Execution result field is not allowed in a scenario definition: {field}",
                        scenario_id,
                        field=field,
                    )
                )

            for field in ("id", "title", "input"):
                if field in scenario and (
                    not isinstance(scenario[field], str) or not scenario[field].strip()
                ):
                    errors.append(
                        evaluation_error(
                            "INVALID_SCENARIO_FIELD",
                            f"Scenario field must be a non-empty string: {field}",
                            scenario_id,
                            field=field,
                        )
                    )
            if "initialState" in scenario and not isinstance(
                scenario["initialState"], dict
            ):
                errors.append(
                    evaluation_error(
                        "INVALID_SCENARIO_FIELD",
                        "Scenario initialState must be an object",
                        scenario_id,
                        field="initialState",
                    )
                )

            if scenario_id:
                if scenario_id in seen_ids:
                    errors.append(
                        evaluation_error(
                            "DUPLICATE_SCENARIO_ID",
                            f"Duplicate scenario id: {scenario_id}",
                            scenario_id,
                        )
                    )
                seen_ids.add(scenario_id)

            if scenario.get("assertionType") not in ASSERTION_TYPES:
                errors.append(
                    evaluation_error(
                        "INVALID_ASSERTION_TYPE",
                        f"Invalid assertion type: {scenario.get('assertionType')!r}",
                        scenario_id,
                    )
                )

            for field in ("expectedBehavior", "prohibitedBehavior", "evidenceRequired"):
                if field in scenario and (
                    not isinstance(scenario[field], list)
                    or not scenario[field]
                    or not all(
                        isinstance(item, str) and item.strip() for item in scenario[field]
                    )
                ):
                    errors.append(
                        evaluation_error(
                            "INVALID_SCENARIO_FIELD",
                            f"Scenario field must be a non-empty string array: {field}",
                            scenario_id,
                            field=field,
                        )
                    )

            if layer == "adapter" and isinstance(scenario.get("initialState"), dict):
                enabled_adapters = scenario["initialState"].get("adapters")
                if not isinstance(enabled_adapters, list) or catalog_adapter not in enabled_adapters:
                    errors.append(
                        evaluation_error(
                            "SCENARIO_ADAPTER_NOT_ENABLED",
                            f"Scenario initialState must enable adapter: {catalog_adapter}",
                            scenario_id,
                        )
                    )

            if layer == "core":
                semantic_values = []
                for field in CORE_SEMANTIC_FIELDS:
                    value = scenario.get(field)
                    if isinstance(value, str):
                        semantic_values.append(value.lower())
                    elif isinstance(value, list):
                        semantic_values.extend(
                            str(item).lower() for item in value if isinstance(item, str)
                        )
                semantic_text = " ".join(semantic_values)
                for term in reserved_terms:
                    if re.search(r"\b" + re.escape(term.lower()) + r"\b", semantic_text):
                        errors.append(
                            evaluation_error(
                                "PROJECT_TERM_IN_CORE",
                                f"Adapter-reserved term in Core scenario: {term}",
                                scenario_id,
                                term=term,
                            )
                        )

    return {
        "valid": not errors,
        "errors": errors,
        "catalogCount": len(catalogs),
        "scenarioCount": scenario_count,
    }


def load_catalogs(root=EVALS_ROOT):
    paths = discover_catalog_paths(root)
    if not paths:
        raise OSError(f"No evaluation catalogs found in {root}")
    return [json.loads(path.read_text(encoding="utf-8")) for path in paths]


def main():
    try:
        catalogs = load_catalogs()
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print("EVALUATION VALIDATION: FAILED")
        print(f"- [INPUT_ERROR] Unable to read evaluation catalogs: {error}")
        return 2

    result = validate_catalogs(catalogs)
    if result["valid"]:
        print("EVALUATION VALIDATION: PASSED")
        print(f"CATALOGS: {result['catalogCount']}")
        print(f"SCENARIOS: {result['scenarioCount']}")
        return 0

    print("EVALUATION VALIDATION: FAILED")
    for error in result["errors"]:
        print(f"- [{error['code']}] {error['message']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
