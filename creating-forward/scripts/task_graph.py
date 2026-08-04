CURRENT_GRAPH_VERSION = "0.4.0-dev"

TASK_STATUSES = {
    "pending",
    "ready",
    "in_progress",
    "blocked",
    "skipped",
    "executed_pending_verification",
    "verified",
    "completed",
    "failed",
    "cancelled",
}

REQUIRED_TASK_FIELDS = (
    "id",
    "title",
    "goal",
    "status",
    "dependencies",
    "completionCriteria",
    "verificationMethods",
    "allowedFiles",
    "forbiddenActions",
    "assignedRole",
    "reviewRole",
)

NON_EMPTY_STRING_FIELDS = (
    "id",
    "title",
    "goal",
    "assignedRole",
    "reviewRole",
)

STRING_LIST_FIELDS = (
    "dependencies",
    "completionCriteria",
    "verificationMethods",
    "allowedFiles",
    "forbiddenActions",
    "evidenceIds",
    "blockedBy",
)

OPTIONAL_TASK_FIELDS = (
    "attemptCount",
    "maxAttempts",
    "evidenceIds",
    "blockedBy",
    "nextAction",
)

ALLOWED_TASK_FIELDS = set(REQUIRED_TASK_FIELDS + OPTIONAL_TASK_FIELDS)


def _is_whole_number(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value == int(value) and not (value != value)  # exclude NaN
    return False


def error(code, message, task_id=None, **details):
    value = {"code": code, "message": message}
    if task_id is not None:
        value["taskId"] = task_id
    value.update(details)
    return value


def find_cycle(task_ids, dependencies):
    state = {task_id: 0 for task_id in task_ids}
    for task_id in task_ids:
        if state[task_id] != 0:
            continue

        frames = [[task_id, 0]]
        path = []
        positions = {}
        while frames:
            current_id, dependency_index = frames[-1]
            if state[current_id] == 0:
                state[current_id] = 1
                positions[current_id] = len(path)
                path.append(current_id)

            current_dependencies = dependencies[current_id]
            if dependency_index < len(current_dependencies):
                dependency_id = current_dependencies[dependency_index]
                frames[-1][1] += 1
                if state[dependency_id] == 0:
                    frames.append([dependency_id, 0])
                elif state[dependency_id] == 1:
                    return path[positions[dependency_id] :].copy()
                continue

            frames.pop()
            state[current_id] = 2
            positions.pop(current_id)
            path.pop()
    return []


def topological_order(task_ids, dependencies):
    original_index = {task_id: index for index, task_id in enumerate(task_ids)}
    dependents = {task_id: [] for task_id in task_ids}
    indegree = {task_id: len(dependencies[task_id]) for task_id in task_ids}
    for task_id in task_ids:
        for dependency_id in dependencies[task_id]:
            dependents[dependency_id].append(task_id)

    layer = [task_id for task_id in task_ids if indegree[task_id] == 0]
    ordered = []
    while layer:
        ordered.extend(layer)
        next_layer_ids = set()
        for task_id in layer:
            for dependent_id in dependents[task_id]:
                indegree[dependent_id] -= 1
                if indegree[dependent_id] == 0:
                    next_layer_ids.add(dependent_id)
        layer = sorted(next_layer_ids, key=original_index.__getitem__)
    return ordered


def validate_task_graph(graph):
    errors = []
    if not isinstance(graph, dict) or not isinstance(graph.get("tasks"), list):
        return {
            "valid": False,
            "errors": [
                error(
                    "INVALID_GRAPH_SHAPE",
                    "Task graph must be an object with a tasks array",
                )
            ],
            "topologicalOrder": [],
        }

    if graph.get("version") != CURRENT_GRAPH_VERSION:
        errors.append(
            error(
                "UNSUPPORTED_GRAPH_VERSION",
                f"Unsupported task graph version: {graph.get('version')!r}",
            )
        )

    extra_graph_fields = [field for field in graph if field not in {"version", "tasks"}]
    for field in extra_graph_fields:
        errors.append(
            error(
                "INVALID_GRAPH_SHAPE",
                f"Unexpected task graph field: {field}",
                field=field,
            )
        )

    object_tasks = []
    for index, task in enumerate(graph["tasks"]):
        if not isinstance(task, dict):
            errors.append(
                error(
                    "INVALID_TASK_SHAPE",
                    f"Task at index {index} must be an object",
                    taskIndex=index,
                )
            )
            continue

        task_id = task.get("id") if isinstance(task.get("id"), str) else None
        object_tasks.append(task)
        for field in task:
            if field not in ALLOWED_TASK_FIELDS:
                errors.append(
                    error(
                        "INVALID_TASK_FIELD",
                        f"Unexpected task field: {field}",
                        task_id,
                        field=field,
                        taskIndex=index,
                    )
                )
        for field in REQUIRED_TASK_FIELDS:
            if field not in task:
                errors.append(
                    error(
                        "MISSING_TASK_FIELD",
                        f"Missing task field: {field}",
                        task_id,
                        field=field,
                        taskIndex=index,
                    )
                )

        for field in NON_EMPTY_STRING_FIELDS:
            if field in task and (
                not isinstance(task[field], str) or not task[field].strip()
            ):
                errors.append(
                    error(
                        "INVALID_TASK_FIELD",
                        f"Task field must be a non-empty string: {field}",
                        task_id,
                        field=field,
                        taskIndex=index,
                    )
                )

        if "status" in task and (
            not isinstance(task["status"], str) or task["status"] not in TASK_STATUSES
        ):
            errors.append(
                error(
                    "INVALID_TASK_FIELD",
                    f"Invalid task status: {task['status']!r}",
                    task_id,
                    field="status",
                    taskIndex=index,
                )
            )

        for field in STRING_LIST_FIELDS:
            if field in task and (
                not isinstance(task[field], list)
                or not all(isinstance(item, str) for item in task[field])
            ):
                errors.append(
                    error(
                        "INVALID_TASK_FIELD",
                        f"Task field must be a string array: {field}",
                        task_id,
                        field=field,
                        taskIndex=index,
                    )
                )

        if "attemptCount" in task and (
            not _is_whole_number(task["attemptCount"])
            or task["attemptCount"] < 0
        ):
            errors.append(
                error(
                    "INVALID_TASK_FIELD",
                    "attemptCount must be an integer greater than or equal to 0",
                    task_id,
                    field="attemptCount",
                    taskIndex=index,
                )
            )

        if "maxAttempts" in task and (
            not _is_whole_number(task["maxAttempts"])
            or task["maxAttempts"] < 1
        ):
            errors.append(
                error(
                    "INVALID_TASK_FIELD",
                    "maxAttempts must be an integer greater than or equal to 1",
                    task_id,
                    field="maxAttempts",
                    taskIndex=index,
                )
            )

        if "nextAction" in task and not isinstance(task["nextAction"], str):
            errors.append(
                error(
                    "INVALID_TASK_FIELD",
                    "nextAction must be a string",
                    task_id,
                    field="nextAction",
                    taskIndex=index,
                )
            )

    seen_ids = set()
    duplicate_ids = set()
    for task in object_tasks:
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id.strip():
            continue
        if task_id in seen_ids and task_id not in duplicate_ids:
            errors.append(
                error(
                    "DUPLICATE_TASK_ID",
                    f"Duplicate task id: {task_id}",
                    task_id,
                )
            )
            duplicate_ids.add(task_id)
        seen_ids.add(task_id)

    task_ids = []
    ordered_seen_ids = set()
    for task in object_tasks:
        task_id = task.get("id")
        if (
            isinstance(task_id, str)
            and task_id.strip()
            and task_id not in ordered_seen_ids
        ):
            task_ids.append(task_id)
            ordered_seen_ids.add(task_id)
    known_ids = set(task_ids)
    for task in object_tasks:
        task_id = task.get("id")
        dependencies = task.get("dependencies")
        if (
            not isinstance(task_id, str)
            or not task_id.strip()
            or not isinstance(dependencies, list)
            or not all(isinstance(item, str) for item in dependencies)
        ):
            continue

        seen_dependencies = set()
        for dependency_id in dependencies:
            if dependency_id == task_id:
                errors.append(
                    error(
                        "SELF_DEPENDENCY",
                        f"Task depends on itself: {task_id}",
                        task_id,
                        dependencyId=dependency_id,
                    )
                )
            elif dependency_id not in known_ids:
                errors.append(
                    error(
                        "UNKNOWN_DEPENDENCY",
                        f"Unknown dependency {dependency_id} for task {task_id}",
                        task_id,
                        dependencyId=dependency_id,
                    )
                )
            if dependency_id in seen_dependencies:
                errors.append(
                    error(
                        "DUPLICATE_DEPENDENCY",
                        f"Duplicate dependency {dependency_id} for task {task_id}",
                        task_id,
                        dependencyId=dependency_id,
                    )
                )
            seen_dependencies.add(dependency_id)

    tasks_by_id = {task["id"]: task for task in object_tasks if task.get("id") in known_ids}
    dependencies = {task_id: tasks_by_id[task_id]["dependencies"] for task_id in task_ids}
    # Only detect cycles on tasks with valid, known dependency references
    # Exclude self-dependencies since they are already reported as SELF_DEPENDENCY
    detectable_ids = []
    detectable_deps = {}
    for task_id in task_ids:
        deps = dependencies.get(task_id, [])
        if isinstance(deps, list):
            filtered_deps = [dep for dep in deps if dep != task_id and dep in known_ids]
            detectable_ids.append(task_id)
            detectable_deps[task_id] = filtered_deps
    cycle = find_cycle(detectable_ids, detectable_deps)
    if cycle:
        errors.append(
            error(
                "DEPENDENCY_CYCLE",
                "Dependency cycle detected: " + " -> ".join(cycle + [cycle[0]]),
                cycleTaskIds=cycle,
            )
        )

    if errors:
        return {"valid": False, "errors": errors, "topologicalOrder": []}

    return {
        "valid": True,
        "errors": [],
        "topologicalOrder": topological_order(task_ids, dependencies),
    }
