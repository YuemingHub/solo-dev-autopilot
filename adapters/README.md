# Adapter Catalog

Adapters add project or platform constraints to Creating Forward Core. They may tighten Core rules but may not weaken safety, evidence, recovery, or authorization gates.

## Available Adapters

- `mingos.md`: MingOS governance, data, branch, and validation boundaries.

Load Core first, inspect the applicable Adapter, then record its name during workspace initialization:

```powershell
python scripts/cf_init_workspace.py <project-path> <adapter-name>
```
