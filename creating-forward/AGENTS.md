# Creating Forward Development Guide

## Project

Creating Forward（向未来去创造） is a platform-independent Agent working protocol. The repository contains a generic Core plus optional project adapters and validation assets.

## Read Order

1. `README.md`
2. `START_HERE.md`
3. `docs/PRODUCT_DECISION_BASELINE.md`
4. `SKILL.md`
5. The files directly relevant to the current task
6. An adapter only when the target project uses it

## Commands

```powershell
python scripts/validate_package.py
python scripts/validate_evals.py
python scripts/validate_task_graph.py <graph.json>
python -m unittest discover -s tests -v
python scripts/init_workspace.py <project-path> [adapter ...]
python scripts/validate_workspace.py <project-path>
```

## Architecture Boundaries

- Keep `SKILL.md`, `protocol/`, `schemas/`, and generic templates project-independent.
- Put project-specific governance, data, branch, and validation rules in `adapters/`.
- Keep project launch instructions in `bootstrap/` and real-world plans in `plans/`.
- Treat `sources/` as read-only history, never as current execution state.
- A project adapter may tighten Core rules but may not weaken safety, evidence, recovery, or authorization gates.

## Change Rules

- Add or change behavior through a failing test first.
- Keep Python tooling on the standard library unless a concrete requirement justifies a dependency.
- Treat task-graph error codes as a public interface; add rather than rename codes without migration notes.
- Evaluation catalog validation proves structure only, never claim it proves Agent behavior passed.
- Update version and migration documentation when observable state contracts change.
- Do not store credentials, tokens, production data, or conversation transcripts.
- Do not generate a root `MANIFEST.json` during development; generate manifests only for immutable release packages.
- Do not edit version snapshots under `D:\LifeOs\个人引擎室\08_迭代日志\creating-forward`.
- Do not publish, deploy, merge, or create commits without explicit user authorization.
