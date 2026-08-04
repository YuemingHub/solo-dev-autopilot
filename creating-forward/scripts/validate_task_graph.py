#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from task_graph import validate_task_graph


class ArgumentError(Exception):
    pass


class ResultArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentError(message)


def input_error(message):
    return {
        "valid": False,
        "errors": [{"code": "INPUT_ERROR", "message": message}],
        "topologicalOrder": [],
    }


def print_result(result, output_format):
    if output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return

    if result["valid"]:
        print("TASK GRAPH VALIDATION: PASSED")
        print("TOPOLOGICAL ORDER: " + ", ".join(result["topologicalOrder"]))
        return

    print("TASK GRAPH VALIDATION: FAILED")
    for graph_error in result["errors"]:
        print(f"- [{graph_error['code']}] {graph_error['message']}")


def main(argv=None):
    raw_arguments = list(argv) if argv is not None else None
    inspected_arguments = raw_arguments if raw_arguments is not None else __import__("sys").argv[1:]
    requested_format = "text"
    for index, argument in enumerate(inspected_arguments):
        if argument == "--format=json":
            requested_format = "json"
        elif (
            argument == "--format"
            and index + 1 < len(inspected_arguments)
            and inspected_arguments[index + 1] == "json"
        ):
            requested_format = "json"
    parser = ResultArgumentParser(description="Validate a Creating Forward task graph")
    parser.add_argument("graph", help="Path to a JSON task graph")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    try:
        arguments = parser.parse_args(raw_arguments)
    except ArgumentError as error:
        result = input_error(f"Invalid command arguments: {error}")
        print_result(result, requested_format)
        return 2

    graph_path = Path(arguments.graph)
    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        result = input_error(f"Unable to read task graph: {error}")
        print_result(result, arguments.format)
        return 2

    result = validate_task_graph(graph)
    print_result(result, arguments.format)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
